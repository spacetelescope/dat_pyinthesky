
.. image:: images/jda_notebooks_logo_wbg.png

|
|

##############################################
JWST Data Analysis Tool Notebooks (pyinthesky)
##############################################

JDAT and Jdaviz
***************

The James Webb Space Telescope Data Analysis Tool (JDAT) team at the Space Telescope Science Institute (STScI) is
developing analysis and visualization tools for the upcoming James Webb Space Telescope (JWST). JDAT is involved
with the development of `astropy <https://www.astropy.org>`_ core and its affiliated analysis tools (such as
`specutils <https://specutils.readthedocs.io/en/stable/>`_ and `photutils <https://photutils.readthedocs.io/en/stable/>`_).
JDAT is also responsible for the development of the JWST Data Analysis Visualization tools (`Jdaviz`).
`Jdaviz` is a package of astronomical data analysis and visualization tools based on the Jupyter platform.
The `Jdaviz` package includes the following visualization applications:

=============== ===============
**Application** **Description**
--------------- ---------------
`Specviz`       Visualization and quick-look analysis for 1D astronomical spectra.
`Cubeviz`       Visualization and analysis tool for data cubes from integral field units (IFUs).
`MOSviz`        Visualization and quick-look analysis tool for multi-object spectroscopy (MOS).
=============== ===============

.. seealso::

    - For more information on JDAT please see the `Data Analysis Tools JDox Page <https://jwst-docs.stsci.edu/jwst-post-pipeline-data-analysis>`_.
    - For more information on `Jdaviz`, please visit the `Jdaviz documentation <https://jdaviz.readthedocs.io/en/latest/>`_.

JDAT Notebooks
**************

The JDAT team is seeking help from the scientific community to develop example notebooks that outline scientific
workflows utilizing the analysis and visualization tools developed by the team. These notebooks will be
made available to the public to serve as teaching resources and a form of interactive documentation of the analysis tools.

The submitted notebooks should satisfy the following goals:

    1. Reduce and analyze JWST data (we currently use simulated or similar data).
    2. Showcase analysis and visualization tools.
    3. Drive development by identifying missing functionalities in the tools and libraries.

.. note::

    Completed notebooks are rendered and made available to the public in the
    `jdat_notebooks <https://github.com/spacetelescope/jdat_notebooks>`_ repository.
    Development of new notebooks is facilitated through the
    `dat_pyinthesky <https://github.com/spacetelescope/dat_pyinthesky>`_ repository.


JDAT Development Sprints
************************

The JDAT team at STScI develops the `Jdaviz` applications during two week sprints through out the year. During this time
developers are available to assist with the development of notebooks. Notebook leads are strongly encouraged to participate
in the JDAT sprints while composing their notebooks because it offers an opportunity to work with the developers and gain
exposure to the latest tools. During a Sprint, we expect notebook leads to learn how to contribute their science expertise
towards the development of tools via GitHub issues, JIRA tickets, Jupyter Notebook coding, communication with developers,
and all the machinery in between. The JDAT team also has staff members dedicated to helping notebook leads with `GitHub`
and `Box` related workflows. If you are interested in joining these sprints, please contact one of the maintainers of
the `dat_pyinthesky <https://github.com/spacetelescope/dat_pyinthesky>`_  repository or file a ticket in the
`STScI help desk <https://stsci.service-now.com/hst>`_. STScI and affilated staff should refer to the
:ref:`STScI Notebook Leads` section for instructions.

#################
Table of Contents
#################

.. toctree::
    :maxdepth: 3

    development_procedure
    data_files
    notebooks
    requirements
    submitting_notebooks
    useful_links
    developers_and_staff

