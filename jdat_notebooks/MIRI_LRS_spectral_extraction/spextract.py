# useful function that should work for boxcar, boxcar scalled with wavelength
# and [TBD] psf-weighted extractions
import numpy as np
from gwcs.wcstools import grid_from_bounding_box


def get_boxcar_weights(center, hwidth, npix):
    """
    Compute the weights given an aperture center, half widths, and number of pixels
    """
    weights = np.zeros((npix))
    # pixels with full weight
    fullpixels = [max(0, int(center - hwidth + 1)), min(int(center + hwidth), npix)]
    weights[fullpixels[0] : fullpixels[1]] = 1.0

    # pixels at the edges of the boxcar with partial weight
    if fullpixels[0] > 0:
        weights[fullpixels[0] - 1] = hwidth - (center - fullpixels[0])
    if fullpixels[1] < npix:
        weights[fullpixels[1]] = hwidth - (fullpixels[1] - center)

    return weights


def ap_weight_images(
    center, width, bkg_offset, bkg_width, image_size, waves, wavescale=None
):
    """
    Create a weight image that defines the desired extraction aperture
    and the weight image for the requested background regions

    Parameters
    ----------
    center : float
        center of aperture in pixels
    width : float
        width of apeture in pixels
    bkg_offset : float
        offset from the extaction edge for the background
        never scaled for wavelength
    bkg_width : float
        width of background region
        never scaled with wavelength
    image_size : tuple with 2 elements
        size of image
    waves : array
        wavelegth values
    wavescale : float
        scale the width with wavelength (default=None)
        wavescale gives the reference wavelenth for the width value

    Returns
    -------
    wimage, bkg_wimage : (2D image, 2D image)
        wimage is the weight image defining the aperature
        bkg_image is the weight image defining the background regions
    """
    wimage = np.zeros(image_size)
    bkg_wimage = np.zeros(image_size)
    hwidth = 0.5 * width
    # loop in dispersion direction and compute weights
    for i in range(image_size[1]):
        if wavescale is not None:
            hwidth = 0.5 * width * (waves[i] / wavescale)

        wimage[:, i] = get_boxcar_weights(center, hwidth, image_size[0])

        # bkg regions
        if (bkg_width is not None) & (bkg_offset is not None):
            bkg_wimage[:, i] = get_boxcar_weights(
                center - hwidth - bkg_offset, bkg_width, image_size[0]
            )
            bkg_wimage[:, i] += get_boxcar_weights(
                center + hwidth + bkg_offset, bkg_width, image_size[0]
            )
        else:
            bkg_wimage = None

    return (wimage, bkg_wimage)


def extract_1dspec(jdatamodel, center, width, bkg_offset, bkg_width, wavescale=None):
    """
    Extract the 1D spectrum using the boxcar method.
    Does a background subtraction as part of the extraction.

    Parameters
    ----------
    jdatamodel : jwst.DataModel
        jwst datamodel with the 2d spectral image
    center : float
        center of aperture in pixels
    width : float
        width of apeture in pixels
    bkg_offset : float
        offset from the extaction edge for the background
        never scaled for wavelength
    bkg_width : float
        width of background region
        never scaled with wavelength
    wavescale : float
        scale the width with wavelength (default=None)
        wavescale gives the reference wavelenth for the width value

    Returns
    -------
    waves, ext1d : (ndarray, ndarray)
        2D `float` array with wavelengths
        1D `float` array with extracted 1d spectrum in Jy
    """
    # should be determined from the gWCS in cal.fits
    image = np.transpose(jdatamodel.data)
    grid = grid_from_bounding_box(jdatamodel.meta.wcs.bounding_box)
    ra, dec, lam = jdatamodel.meta.wcs(*grid)
    lam_image = np.transpose(lam)

    # compute a "rough" wavelength scale to allow for aperture to scale with wavelength
    rough_waves = np.average(lam_image, axis=0)

    # images to use for extraction
    wimage, bkg_wimage = ap_weight_images(
        center,
        width,
        bkg_width,
        bkg_offset,
        image.shape,
        rough_waves,
        wavescale=wavescale,
    )

    # extract the spectrum using the weight image
    if bkg_wimage is not None:
        ext1d_boxcar_bkg = np.average(image, weights=bkg_wimage, axis=0)
        data_bkgsub = image - np.tile(ext1d_boxcar_bkg, (image.shape[0], 1))
    else:
        data_bkgsub = image

    ext1d = np.sum(data_bkgsub * wimage, axis=0)
    # convert from MJy/sr to Jy
    ext1d *= 1e6 * jdatamodel.meta.photometry.pixelarea_steradians

    # compute the average wavelength for each column using the weight image
    # this should correspond directly with the extracted spectrum
    #   wavelengths account for any tiled spectra this way
    waves = np.average(lam_image, weights=wimage, axis=0)

    return (waves, ext1d, data_bkgsub)
