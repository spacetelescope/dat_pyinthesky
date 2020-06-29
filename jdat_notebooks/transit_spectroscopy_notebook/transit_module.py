"""
Helper module for transit marginalisation.
"""

import numpy as np
import astropy.units as u

def occultnl(rl, c1, c2, c3, c4, b0):
    """
    MANDEL & AGOL (2002) transit model.
    :param rl: float, transit depth (Rp/R*)
    :param c1: float, limb darkening parameter 1
    :param c2: float, limb darkening parameter 2
    :param c3: float, limb darkening parameter 3
    :param c4: float, limb darkening parameter 4
    :param b0: impact parameter in stellar radii
    :return: mulimb0: limb-darkened transit model, mulimbf: lightcurves for each component that you put in the model
    """
    mulimb0 = occultuniform(b0, rl)
    bt0 = b0
    fac = np.max(np.abs(mulimb0 - 1))
    if fac == 0:
        fac = 1e-6  # DKS edit

    omega = 4 * ((1 - c1 - c2 - c3 - c4) / 4 + c1 / 5 + c2 / 6 + c3 / 7 + c4 / 8)
    nb = len(b0)
    indx = np.where(mulimb0 != 1.0)[0]
    if len(indx) == 0:
        indx = -1
    mulimb = mulimb0[indx]
    mulimbf = np.zeros((5, nb))
    mulimbf[0, :] = mulimbf[0, :] + 1.
    mulimbf[1, :] = mulimbf[1, :] + 0.8
    mulimbf[2, :] = mulimbf[2, :] + 2 / 3
    mulimbf[3, :] = mulimbf[3, :] + 4 / 7
    mulimbf[4, :] = mulimbf[4, :] + 0.5
    nr = np.int64(2)
    dmumax = 1.0

    while (dmumax > fac * 1.e-3) and (nr <= 131072):
        #print(nr)
        mulimbp = mulimb
        nr = nr * 2
        dt = 0.5 * np.pi / nr
        t = dt * np.arange(nr + 1)
        th = t + 0.5 * dt
        r = np.sin(t)
        sig = np.sqrt(np.cos(th[nr - 1]))
        mulimbhalf = sig ** 3 * mulimb0[indx] / (1 - r[nr - 1])
        mulimb1 = sig ** 4 * mulimb0[indx] / (1 - r[nr - 1])
        mulimb3half = sig ** 5 * mulimb0[indx] / (1 - r[nr - 1])
        mulimb2 = sig ** 6 * mulimb0[indx] / (1 - r[nr - 1])
        for i in range(1, nr):
            mu = occultuniform(b0[indx] / r[i], rl / r[i])
            sig1 = np.sqrt(np.cos(th[i - 1]))
            sig2 = np.sqrt(np.cos(th[i]))
            mulimbhalf = mulimbhalf + r[i] ** 2 * mu * (sig1 ** 3 / (r[i] - r[i - 1]) - sig2 ** 3 / (r[i + 1] - r[i]))
            mulimb1 = mulimb1 + r[i] ** 2 * mu * (sig1 ** 4 / (r[i] - r[i - 1]) - sig2 ** 4 / (r[i + 1] - r[i]))
            mulimb3half = mulimb3half + r[i] ** 2 * mu * (sig1 ** 5 / (r[i] - r[i - 1]) - sig2 ** 5 / (r[i + 1] - r[i]))
            mulimb2 = mulimb2 + r[i] ** 2 * mu * (sig1 ** 6 / (r[i] - r[i - 1]) - sig2 ** 6 / (r[i + 1] - r[i]))

        mulimb = ((1 - c1 - c2 - c3 - c4) * mulimb0[
            indx] + c1 * mulimbhalf * dt + c2 * mulimb1 * dt + c3 * mulimb3half * dt + c4 * mulimb2 * dt) / omega
        ix1 = np.where(mulimb + mulimbp != 0.)[0]
        if len(ix1) == 0:
            ix1 = -1

        #print(ix1)
        # python cannot index on single values so you need to use atlest_1d for the below to work when mulimb is a single value
        dmumax = np.max(np.abs(np.atleast_1d(mulimb)[ix1] - np.atleast_1d(mulimbp)[ix1]) / (
                np.atleast_1d(mulimb)[ix1] + np.atleast_1d(mulimbp)[ix1]))

    mulimbf[0, indx] = np.atleast_1d(mulimb0)[indx]
    mulimbf[1, indx] = mulimbhalf * dt
    mulimbf[2, indx] = mulimb1 * dt
    mulimbf[3, indx] = mulimb3half * dt
    mulimbf[4, indx] = mulimb2 * dt
    np.atleast_1d(mulimb0)[indx] = mulimb
    b0 = bt0

    return mulimb0, mulimbf


def occultuniform(b0, w):
    """
    Compute the lightcurve for occultation of a uniform source without microlensing (Mandel & Agol 2002).

    :param b0: array; impact parameter in units of stellar radii
    :param w: array; occulting star size in units of stellar radius
    :return: muo1: float; fraction of flux at each b0 for a uniform source
    """

    if np.abs(w - 0.5) < 1.0e-3:
        w = 0.5

    nb = len(np.atleast_1d(b0))
    muo1 = np.zeros(nb)


    for i in range(nb):
        # substitute z=b0(i) to shorten expressions
        z = np.atleast_1d(b0)[i]
        #z = z.value    # stripping it of astropy units
        if z >= 1+w:
            muo1[i] = 1.0
            continue

        if w >= 1 and z <= w-1:
            muo1[i] = 0.0
            continue

        if z >= np.abs(1-w) and z <= 1+w:
            kap1 = np.arccos(np.min(np.append((1 - w ** 2 + z ** 2) / 2 / z, 1.)))
            kap0 = np.arccos(np.min(np.append((w ** 2 + z ** 2 - 1) / 2 / w / z, 1.)))
            lambdae = w ** 2 * kap0 + kap1
            lambdae = (lambdae - 0.5 * np.sqrt(np.max(np.append(4. * z ** 2 - (1 + z ** 2 - w ** 2) ** 2, 0.)))) / np.pi
            muo1[i] = 1 - lambdae

        if z <= 1-w:
            muo1[i] = 1 - w ** 2
            continue

    return muo1



