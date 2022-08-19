---
title: 'SlideRule: Enabling rapid, scalable, open science for the NASA ICESat-2 mission and beyond'
tags:
  - Python
  - NASA
  - ICESat-2
  - Glacier
  - Earth observation
authors:
  - name: J.P. Swinski #^[co-first author] # note this makes a footnote saying 'co-first author'
    affiliation: 1
  - name: David Shean
    orcid: 0000-0003-3840-3860
    affiliation: "2, 5"
  - name: Ben Smith
    affiliation: 4
  - name: Tyler Sutterley
    affiliation: 4
  - name: Scott Henderson
    orcid: 0000-0003-0624-4965
    affiliation: "3, 5"
  - name: Carlos Ugarte
    affiliation: 1
  - name: Thomas Neumann
    affiliation: 1
affiliations:
 - name: NASA Goddard Space Flight Center
   index: 1
 - name: University of Washington, Department of Civil and Environmental Engineering
   index: 2
 - name: University of Washington, Department of Earth and Space Sciences
   index: 3
 - name: University of Washington, Applied Physics Laboratory
   index: 4
 - name: University of Washington, eScience Institute
   index: 5

date: 1 March 2022
bibliography: paper.bib
---

# Summary
`SlideRule` is an open source server-side framework for on-demand processing of science data in the cloud. The `SlideRule` project offers a new paradigm for NASA archival data management: Rapid delivery of customizable on-demand data products, rather than hosting large volumes of standard derivative products which do not meet the needs of all scientists. Scalable server-side components of `SlideRule` run in Amazon Web Services and are optimized to read HDF formatted data hosted by NASA in S3 object storage.

While `SlideRule` can be accessed by any HTTP client (e.g., curl) through GET and POST requests, the `sliderule-python` client provides a user-friendly API for easy interaction with the `SlideRule` service. The client library converts results into standard Python data containers (i.e., Pandas DataFrame) and facilitates serialization with provenance metadata for reproducible science.

`SlideRule` uses a plugin framework to work with different NASA archival datasets. For example, the Ice Cloud and land Elevation Satellite-2 (ICESat-2) mission operates a laser altimeter that measures elevation at precisely located points. The ICESat-2 `SlideRule` plugin includes custom algorithms for generating continuous surface extractions from point clouds in seconds to minutes, enabling rapid interpretation and scientific algorithm development.

# Statement of need
ICESat-2 launched in September 2018 to continue as the follow on mission to the original ICESat mission (2003-2010) which pioneered the use of a space-based laser altimeter to measure the height of the Earth [@markus2017ice]. These missions are optimized to measure elevation changes in the cryosphere, including ice sheets and sea ice, allowing us to quantify changes in response to Earth's warming climate.

ICESat-2 carries the Advanced Topographic Laser Altimeter System (ATLAS) which records the two-way travel time of transmitted photons [@neumann2019ice]. The ICESat-2 Level 2A Geolocated Photon Data Product (ATL03) provides unique latitude, longitude, height and timing of photons, and is the lowest level data product most scientists use [@neumann2019atbd]. ATL03 provides an initial photon classification, identifying them as reflected off Earth, or background photons due to sunlight or instrument noise. The complexity and large data volume of the ATL03 granules (stored as ~2 Gigabyte HDF formatted files) impede new users and slow the speed of algorithm development.

The ICESat-2 project generates a range of [higher-level products](https://nsidc.org/data/icesat-2/products) that reduce the ATL03 data using established processing algorithms. For example, the ATL06 product [@smith2019land] provides high-precision estimates of surface height at 40-meter resolution, using parameters appropriate to flat, highly reflective polar snow surfaces. Similar to ATL03, the ATL06 products contain a large number of parameters describing each height measurement that may not be relevant to all users. Furthermore, standard ATL06 products are only produced over glaciers and ice sheets and the algorithm parameters (such as 40-meter binning) are not optimal for complex land surfaces or for vegetated surfaces. `SlideRule` offers a solution to these issues by providing on-demand products using the vetted ATL06 algorithm, but with adjustable parameters and photon classification strategies tailored to the characteristics of their application and study sites.

## State of the field

The current paradigm for using data from the ICESat-2 mission involves downloading large volumes of standard data products from a NASA Distributed Active Archive Center (DAAC). The National Snow and Ice Data Center (NSIDC) offers limited subsetting services allowing users to download geographic subsets of products, and to select the specific variables to be included in the subsets [@atl03_nsidc]. However, these services do not permit custom on-the-fly data transformation.

### On-demand data processing
Several other projects are exploring on-demand, cloud-based processing for satellite and/or point cloud data. The Alaska Satellite Facility's Hybrid Pluggable Processing Pipeline (ASF HyP3) enables custom processing of satellite SAR images from multiple missions [@hogenson_kirk_2020_6917373].

The [OpenTopography project](https://opentopography.org/) offers "Web service-based data access, processing, and analysis capabilities that are scalable, extensible, and innovative" with emphasis on "high-resolution (meter to sub-meter scale), Earth science-oriented, topography data acquired with LiDAR and other technologies." The current processing options and data products are focused on airborne LiDAR point clouds, with no plans to support ICESat-2 data.

### ICESat-2 packages
[`icepyx`](https://icepyx.readthedocs.io) is a python library for querying the NASA Common Metadata Repository (CMR) and allowing for programmatic access to ICESat-2 data through NSIDC services [@icepyx]. `icepyx` allows for queries based on spatial and temporal parameters, as well as ICESat-2 orbital cycle and Reference Ground Track (RGT). Accessing NSIDC API services through `icepyx` allows users to spatiotemporally subset ICESat-2 data and convert data to other file formats. At present, `icepyx` facilitates reading and visualizing data available from NSIDC, but it is not a data processing service.

[`OpenAltimetry`](https://openaltimetry.org) offers discovery, access, and visualization of data from NASA’s ICESat and ICESat-2 missions. This service includes an API that can provide access to either photon-level data or height variables from the along-track products, but does not offer processing from photons to higher-level products [@khalsa2020openaltimetry].

[`phoREAL`](https://github.com/icesat-2UT/PhoREAL) (Photon Research and Engineering Analysis Library) from the University of Texas is an open source application allowing for subsetting and conversion of ICESat-2 ATL03 Global Geolocated Photon Height and ATL08 Land and Vegetation Height data products. `phoREAL` allows users to spatially subset locally-stored data based on Ground Track. `phoREAL` allows users to visualize data from both ATL03 and ATL08 and perform some statistics on heights based on time or geospatial location.

[`captoolkit`](https://github.com/nasa-jpl/captoolkit) (Cryosphere Altimetry Processing Toolkit) is a software library from the NASA Jet Propulsion Library [@fernando_paolo_2020_3665785]. `captoolkit` allows users to estimate elevation change using altimetry data from multiple airborne and satellite missions.`captoolkit` has functions to apply geophysical corrections, calculate elevation change, and interpolate into gridded fields. `captoolkit` is built for processing on High Performance Computing (HPC) clusters by using parallelized function that operate on local granule files.

# SlideRule framework
`SlideRule` is a C++/Lua framework for on-demand data processing (\autoref{fig:architecture}). It is a science data processing service that runs in the cloud and responds to REST API calls to process and return science results.

![SlideRule architecture schematic.\label{fig:architecture}](./sliderule_architecture.png)

## ICESat-2 SlideRule plugin
The ICESat-2 SlideRule plugin provides two main types of services. The first provides access to existing ICESat-2 products stored as cloud assets, the second provides a customized level-2 product (ATL06-SR) generated on demand from the ATL03 cloud assets.

### ATL03 data access
`SlideRule` provides services that allow users to access ATL03 photon-height and classification data from cloud assets without the need to download entire granules, returning the subset of ATL03 parameters that are needed to interpret surface heights from the photon-height distribution.

For vegetated surfaces, a more advanced photon classification scheme has been made available as part of the ATL08 Land and Vegetation Height product [@neuenschwander2019atl08]. This classification approach allows improved segregation between photons returned from vegetation, photons that reflected from land surfaces, and noise. Users wishing to apply this classification to ATL03 data would ordinarily need to download both an ATL03 granule and the corresponding ATL08 granule, and apply the classification from ATL08 to ATL03. The ICESat-2 SlideRule API includes an option to retrieve the photon classifications from ATL08 cloud assets, and apply them directly to ATL03 photons for subsequent processing.

### ATL06-SR algorithm
The ATL06 (land-ice height) product provided by NASA's ICESat-2 [@smith2019land] (hereafter "ATL06-legacy") provides estimates of surface height and slope derived from ATL03 photon height using an algorithm adapted to the flat surfaces and high reflectivities common over polar ice sheets. ATL06 uses an iterative algorithm to improve the initial photon classification, and calculates a set of corrections based on the residuals between the segment heights and the selected photon heights to correct for sub-centimeter biases in the resulting height estimates.

ATL06-SR implements much of the ATL06-legacy algorithm in a framework that allows customization of the initial photon classification, the resolution and posting of the product, and the filtering strategy used to identify valid segments. For the sake of simplicity and speed of calculation, ATL06-SR omits some of the corrections required for sub-centimeter accuracy over polar surfaces, including the first-photon bias and pulse-shape corrections [@smith2019land]. Over non-polar surfaces, omitting these biases should result in sub-centimeter vertical errors in ATL06-SR heights.

One important difference between the ATL06-legacy and ATL06-SR algorithms is in the iterative photon-selection strategy. Both algorithms begin with photons selected based on the input photon classification. The selection is then refined to reject photons that have large residual values (i.e., larger than three times a robust estimate of the standard deviation of the previously selected residuals) and the fit is recalculated. This process continues until a specified number of iterations has occurred, or until subsequent iterations leave the photon selection unchanged. In ATL06-legacy, at each iteration the photons are selected from the complete set of input photons, regardless of how they were initially flagged or selected, while in ATL06-SR, each iteration selects photons exclusively from those selected in the previous iteration. This means that in ATL06-legacy, the number of photons can increase from one iteration to the next, while in ATL06-SR it can only remain constant or decrease. This choice lets ATL06-SR more faithfully reflect the height distribution of the initial selection, at the expense of sometimes missing photons close to the surface that might add more information to the fitting algorithm, possibly improving the accuracy of the fit. Under most circumstances, the two algorithms produce very similar results.

#### Photon classification
The ATL06-SR algorithm supports three sources of photon classification data (\autoref{fig:classification}): 1) ATL03 photon confidence values, based on algorithm-specific classification types for land, ocean, sea-ice, land-ice, or inland water [@neumann2019ice], 2) ATL08 photon classification [@neuenschwander2019atl08], and 3) YAPC (Yet Another Photon Classification) photon-density-based classification [@tyler_sutterley_2022_6717591].

![Example SlideRule output of classified ATL03 photons and corresponding ATL06-SR points.\label{fig:classification}](./sliderule_classification.png)

Users can select the classification values to be included in the initial photon selection for the ATL06-SR fitting. For example, a user might wish to generate ATL06-SR products based only on photons with ATL03 photon classification values indicating medium or better confidence, or photons flagged as ground returns in ATL08 to remove photons from canopy returns.

The rapid processing offered by the `SlideRule` service allows for interactive testing and evaluation of various combinations of ATL06-SR parameter and classification schemes for application-specific needs.

# Acknowledgements

The `SlideRule` project is funded by the NASA ICESat-2 project and NASA award 80NSSC20K0995.

# References
