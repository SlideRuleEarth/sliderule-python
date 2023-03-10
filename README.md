# sliderule-python
[![Read the Docs](https://readthedocs.org/projects/sliderule-python/badge/?version=latest)](https://slideruleearth.io/rtd/)
[![Binder](https://mybinder.org/badge_logo.svg)](https://gke.mybinder.org/v2/gh/ICESat2-SlideRule/sliderule-python/main?urlpath=lab)
[![badge](https://img.shields.io/static/v1.svg?logo=Jupyter&label=PangeoBinderAWS&message=us-west-2&color=orange)](https://aws-uswest2-binder.pangeo.io/v2/gh/ICESat2-SlideRule/sliderule-python/main?urlpath=lab)
[![DOI](https://zenodo.org/badge/311384982.svg)](https://zenodo.org/badge/latestdoi/311384982)

Example notebooks that use SlideRule's Python client for processing Earth science data.

Detailed [documentation](https://slideruleearth.io/rtd/) on installing and using this client can be found at [slideruleearth.io](https://slideruleearth.io/).

### Installing the SlideRule Python Client

The easiest way to install the Sliderule Python client and run the example notebooks is to create a conda environment from the provided `environment.yml` file:
```bash
conda env create -f environment.yml
```

If you have your own conda environment that you want to install the SlideRule Python client into, then:
```bash
conda activate <myenv>
conda install -c conda-forge sliderule
```

For alternate methods to install SlideRule, including options for developers, please see the [installation instructions](https://slideruleearth.io/rtd/getting_started/Install.html).

### Dependencies

Basic functionality of sliderule-python depends on `requests` and `numpy`.  But if you intend on running the example notebooks, please refer to the package requirements listed in `environment.yml` for a full list of recommended python libraries.

### Reference and User's Guide

Please see our [documentation](https://slideruleearth.io/rtd/) page for reference and user's guide material.
