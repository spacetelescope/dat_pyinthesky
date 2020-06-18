This describes a transition plan to move `spectral-cube` functionality to `specutils`.

# Top-level plan

1. Expand the "needs implementation" items into concrete issues in `specutils`.  In general new functionality that's cube-specific should be a function/class in a relevant space like `specutils.analysis.cube`.
2. Write unit tests for all the exsting analysis/manipulation functions in `SpectrumCollection` and `Spectrum1D` with cube shape/wcs.
3. Add a label "spectral-cube feature" for all those needed for feature parity.
4. Create parallel Jira tickets to track and prioritize internal STScI work.
5. Declare victory when the label is empty, and at that point suggest deprecation of `spectral-cube` to Adam Ginsburg.


# Needs Implementation in specutils

* `NDCube` compatibility (although a proof-of-concept is here: https://github.com/astrofrog/nddata-experiments) - note this has the *highest* uncertainty.
* indexing via world coordinates.  This is already supported in `NDCube`, so re-using this functionality would be useful if possible.
* `spectral_slab` - note however that this is another word for the existing spectral region machinery in `specutils.manipulation.extract_region`, just with slightly different syntax. So `spectral_slab` might just be an alternate name that would be adopted in a `RadioSpectrum1D` or similar.
* Moment maps: Not this is already possible in `specutils`, particularly for first- (np.mean) and second- (line width) maps, but exposing a generic "nth moment" function is a good idea.
* `minimal_subcube` (see spectral-cube docs), although this would need a different name in a `Spectrum1D` context (since it would also potentially mask off the spectral "edges"?)
* Spectral extraction (based on astropy regions/photutils?)
* `with_mask` convenience method (not mandatory, but spectral-cube demonstrates it's use as syntactic sugar?)
* Lazy masking (may not be a requirement?)
* Automatic (?) parallel processing of analysis functions across multiple spaxels.  If possible should depend on dask or similar wider ecosystem tools.
* Automatic (?) parallel processing of fitting across multiple spaxels.  (May or may not be best implemented via Dask as the above, but less clear because models are sometimes inherently 3d.)


# Problems/incompatibilities and solutions

## Problem: the name `Spectrum1D`/`SpectralCollection`

A user may not naturally think "cube" when they see "1d" or even "collection".

### Solution

1. Documentation/explanation that yes, a cube can be "1D" in the sense that it's rectified.  Caveat: people don't read documentation!
2. Set up some aliases or subclasses with specific conventions.  E.g. `specutils.RectifiedSpectralCube` could be a subclass of `Spectrum1D` but just with an initializer that checks that the wcs has a spatial and spectral component.
3. Point users to `NDCube` as a way to see explicit cube language, but have them use the NDCube<->Spectrum1D compatibility layer as the way to still use `specutils` functionality

## Problem: large cubes/those that don't fit in memory

`SpectralCube` takes some care to not copy cubes when possible.  It also provides hints on how to use memory mapping (from fits files) to handle cubes that are too big to fit in memory.  It is not clear if `specutils` is as careful about this or not.

### Solution

Run side-by-side tests of `spectral-cube` operations and the equivalent `specutils` operations and see if the later uses more memory.  Where this occurs, identify where the copying occurs and fix it.  Note this is a potentially unbounded amount of work, so some careful prioritization may be needed.

## Incompatibility: masking convention

The `spectral-cube` masking convention is the opposite of that used in specutils (which is the one used in numpy), and instead matches "indexing" convention.  This means code written for `spectral-cube` is subtly different. Relatedly: JWST cubes by default also have a different on-disk dimensionality convention (although that may not present an *API* concern if the loader auto-transposes appropriately).

### Solution

1. Don't fix.  Just accept that there's not direct-API compatibility
2. Add a spectral-cube-like compatibility layer that auto inverts the masks - this isn't too hard because masking in `spectral-cube` is done via a `with_mask` method instead of direct indexing.  But it might make for more confusion because then there's two ways to do the same thing.


# Won't-implement (as part of this plan)

This plan explicitly is aimed at only `spectral-cube` features that are relevant for jwst, and does *not* include some of the `spectral-cube` feature that are radio-specific.  This does *not* mean these cannot be done in specutils, just that the jdat effort at STScI does not plan to do them.

* CASA file read/write: this is a radio-specific format not important for JWST or other space telescopes.  (But probably the `spectral-cube` code can be ported over to specutils without a tremendous amount of difficulty?)
* Extracting subcube from ds9/crtf region: not clear this is needed given viztool interfaces.  If desirable this could be done via `astropy-regions` later on.

* Spectral Extraction