# sliderule-python

Example notebooks that use SlideRule's Python client for processing Earth science data.

[![Read the Docs](https://readthedocs.org/projects/sliderule-python/badge/?version=latest)](https://slideruleearth.io/rtd/)
[![Binder](https://mybinder.org/badge_logo.svg)](https://gke.mybinder.org/v2/gh/ICESat2-SlideRule/sliderule-python/main?urlpath=lab)
[![badge](https://img.shields.io/static/v1.svg?logo=Jupyter&label=PangeoBinderAWS&message=us-west-2&color=orange)](https://aws-uswest2-binder.pangeo.io/v2/gh/ICESat2-SlideRule/sliderule-python/main?urlpath=lab)
[![DOI](https://zenodo.org/badge/311384982.svg)](https://zenodo.org/badge/latestdoi/311384982)

Detailed [documentation](https://slideruleearth.io/rtd/) on installing and using the SlideRule Python client can be found at [slideruleearth.io](https://slideruleearth.io/).

NOTE: As of 3/10/2023 the source code for SlideRule's Python client has moved to the [sliderule](https://github.com/ICESat2-SlideRule/sliderule) repository. This [sliderule-python](https://github.com/ICESat2-SlideRule/sliderule-python) repository continues to function as a collection of example notebooks that use the SlideRule Python client and demonstrate common workflows.

### Installing the SlideRule Python Client

The easiest way to install the Sliderule Python client and run the example notebooks in this repository is to create a conda environment from the provided `environment.yml` file:
```bash
conda env create -f environment.yml
```

If you have your own conda environment that you want to install the SlideRule Python client into, then:
```bash
conda activate <myenv>
conda install -c conda-forge sliderule
```

For alternate methods to install SlideRule, including options for developers, please see the [installation instructions](https://slideruleearth.io/rtd/getting_started/Install.html).

### Reference and User's Guide

Please see our [documentation](https://slideruleearth.io/rtd/) page for reference and user's guide material.
