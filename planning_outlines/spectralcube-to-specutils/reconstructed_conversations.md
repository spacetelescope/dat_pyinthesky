* From https://innerspace.stsci.edu/pages/viewpage.action?pageId=186182883
  Upshot: "I think most of the 1D equivalent functionality is already in specutils and just needs to be enhanced to be ND"

* https://innerspace.stsci.edu/display/DATB/2019-09-05+Discussion+on+SpectralCube%2C+NDCube%2C+NDData+and+Specutils
  Upshot: `spectral_cube` can be deprecated in favor of `specutils` once there is approximate feature-parity

* Discussions from [specreduce sprint](https://docs.google.com/document/d/1s2yjhy9raDGtU58WNFjFDbgcIEnSEQ9kRYb6htPiXsI/edit?usp=sharing) are primarily in [Breakout on cubes and NDData/NDCube](https://docs.google.com/document/d/1s2yjhy9raDGtU58WNFjFDbgcIEnSEQ9kRYb6htPiXsI/edit#bookmark=id.3gz8e0d9lzr1)

* Discussions from [Astropy coordination meeting 2019](https://docs.google.com/document/d/1pO0giLKGEle5rJeyxhc33rIARY_e_naLiYprScROP84/edit?usp=sharing) - see "Spectroscopy Notes" section
  Not much recorded in notes, but upshot is that it is desirable to build machinery that allows NDData types to "look like" other data types using the `__from_nddata__` construct.  A test implementation is here: https://github.com/astrofrog/nddata-experiments