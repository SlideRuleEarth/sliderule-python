# sliderule-python

[![DOI](https://zenodo.org/badge/311384982.svg)](https://zenodo.org/badge/latestdoi/311384982)

Example notebooks that use SlideRule's Python client for processing Earth science data.

## Overview
Detailed [documentation](https://slideruleearth.io/rtd/) on installing and using the SlideRule Python client can be found at [slideruleearth.io](https://slideruleearth.io/).

> NOTE: As of 3/10/2023 the source code for SlideRule's Python client has moved to the [sliderule](https://github.com/SlideRuleEarth/sliderule) repository. This [sliderule-python](https://github.com/SlideRuleEarth/sliderule-python) repository continues to function as a collection of example notebooks that use the SlideRule Python client and demonstrate common workflows.

## Getting Started

The easiest way to install the Sliderule Python client and run the example notebooks in this repository is to create a conda environment from the provided `environment.yml` file:
```bash
conda env create -f environment.yml
conda activate sliderule_env
```

If you have your own conda environment that you want to install the SlideRule Python client into, then:
```bash
conda activate my_env
conda install -c conda-forge sliderule
```

If you already have the SlideRule Python client installed in a conda environment and want to update to the latest version, then:
```bash
conda activate sliderule_env
conda update -c conda-forge sliderule
```

For alternate methods to install SlideRule, including options for developers, please see the [installation instructions](https://slideruleearth.io/rtd/getting_started/Install.html).

## Documentation

Please see our [documentation](https://slideruleearth.io/rtd/) page for reference and user's guide material.
