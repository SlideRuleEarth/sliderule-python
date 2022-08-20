---
title: 'SlideRule: Enabling rapid, scalable, open science for the NASA ICESat-2 mission and beyond'
tags:
  - Python
  - NASA
  - ICESat-2
  - Glacier
  - Earth observation
authors:
  - name: David Shean ^[co-first author] 
    orcid: 0000-0003-3840-3860
    affiliation: "1, 5"
  - name: J.P. Swinski ^[co-first author] # note this makes a footnote saying 'co-first author'
    affiliation: 2
  - name: Ben Smith
    affiliation: 4
  - name: Tyler Sutterley
    affiliation: 4
  - name: Scott Henderson
    orcid: 0000-0003-0624-4965
    affiliation: "3, 5"
  - name: Carlos Ugarte
    affiliation: 2
  - name: Thomas Neumann
    affiliation: 2
affiliations:
 - name: University of Washington, Department of Civil and Environmental Engineering
   index: 1
 - name: NASA Goddard Space Flight Center
   index: 2
 - name: University of Washington, Department of Earth and Space Sciences
   index: 3
 - name: University of Washington, Applied Physics Laboratory
   index: 4
 - name: University of Washington, eScience Institute
   index: 5

date: 19 August 2022
bibliography: paper.bib
---

# Summary
`SlideRule` is an open source server-side framework for on-demand processing of science data in the cloud. The `SlideRule` project offers a new paradigm for NASA archival data management – rapid delivery of customizable on-demand data products, rather than hosting large volumes of standard derivative products, which will inevitably be insufficient for some science applications. The scalable server-side components of `SlideRule` run in the AWS cloud with optimized functions to read HDF5 data hosted by NASA in S3 cloud object storage.

While `SlideRule` can be accessed by any HTTP client (e.g., curl) through GET and POST requests, the `sliderule-python` client provides a user-friendly API for easy interaction with the `SlideRule` service. The client library converts results into standard Python data containers (i.e., Pandas DataFrame) and facilitates serialization with provenance metadata for reproducible science.

`SlideRule` uses a plugin framework to support different NASA datasets. The ICESat-2 `SlideRule` plugin offers customizable algorithms to process the archive of low-level data products from the NASA Ice Cloud and land Elevation Satellite-2 (ICESat-2) laser altimetry mission. The user simply defines a geographic area of interest and key processing parameters, and SlideRule returns high-level surface elevation point cloud products in seconds to minutes, enabling rapid algorithm developent, visualization and scientific interpretation. 

# Statement of need
ICESat-2 launched in September 2018 as the follow-on mission for the original ICESat mission (2003-2010), which pioneered the application of space-based laser altimetry to precisely measure the height of the Earth's changing surface [@markus2017ice]. These missions are optimized to measure elevation change of the cryosphere, including ice sheets and sea ice, allowing scientists to quantify and understand changes in response to a warming climate.

ICESat-2 carries the Advanced Topographic Laser Altimeter System (ATLAS) which records the two-way travel time of transmitted photons from six laser beams [@neumann2019ice]. The Level 2A Geolocated Photon Data Product (ATL03) provides unique latitude, longitude, height and timing of each photon, along with many other attributes, including basic classification as a return from the Earth's surface vs. background photons from sunlight or instrument noise.

The complexity and large data volume of the ATL03 granules, stored as ~2 GB HDF5-format files containing ~100 million records, impedes new users and slows the speed of algorithm development. The ICESat-2 project generates a range of [higher-level products](https://nsidc.org/data/icesat-2/products) that reduce the ATL03 data using established processing algorithms. For example, the ATL06 product [@smith2019land] provides high-precision estimates of surface height at 40-meter resolution, using parameters appropriate for flat, highly reflective polar snow surfaces. Similar to ATL03, the ATL06 products contain a large number of parameters describing each height measurement that may not be relevant to all users. Furthermore, standard ATL06 products are only produced over glaciers and ice sheets, and the default algorithm parameters (such as 40-meter spacing) are not optimal for complex land surfaces or vegetation. `SlideRule` offers a solution to these issues by providing on-demand products using the vetted ATL06 algorithm, but with adjustable parameters and photon classification strategies tailored to the characteristics of their application and study sites.

## State of the field
The current paradigm for ICESat-2 data access involves downloading large volumes of standard data products from a NASA Distributed Active Archive Center (DAAC), then writing custom routines to prepare those products for analysis. The National Snow and Ice Data Center (NSIDC) offers limited subsetting services, allowing users to request and download products for a user-specified geographic area, and to select the a subset of variables to be returned [@atl03_nsidc]. Even with these subsetting services, requesting, staging, and downloading hundreds of products can take several minutes to hours, especially for larger areas, and these services do not support custom server-side data processing.

### On-demand data processing
Several other projects are exploring on-demand, cloud-based processing for satellite and/or point cloud data. For example, the Alaska Satellite Facility's Hybrid Pluggable Processing Pipeline (ASF HyP3) enables custom processing of satellite SAR images from multiple missions [@hogenson_kirk_2020_6917373]. The [OpenTopography project](https://opentopography.org/) offers "Web service-based data access, processing, and analysis capabilities that are scalable, extensible, and innovative" with emphasis on "high-resolution (meter to sub-meter scale), Earth science-oriented, topography data acquired with LiDAR and other technologies." The current processing options and data products are focused on airborne LiDAR point clouds, with no plans to support ICESat-2 data.

### ICESat-2 packages
[`icepyx`](https://icepyx.readthedocs.io) is a python library for querying the NASA Common Metadata Repository (CMR) and allowing for programmatic access to ICESat-2 data through NSIDC services [@icepyx]. `icepyx` allows for queries based on spatial and temporal parameters, as well as ICESat-2 orbital cycle and Reference Ground Track (RGT). Accessing NSIDC API services through `icepyx` allows users to spatiotemporally subset ICESat-2 data and convert data to other file formats. At present, `icepyx` facilitates reading and visualizing data available from NSIDC, but it is not a data processing service.

[`OpenAltimetry`](https://openaltimetry.org) offers discovery, access, and visualization of data from NASA’s ICESat and ICESat-2 missions. This service includes an API that can provide access to either photon-level data or height variables from the along-track products, but does not offer processing from photons to higher-level products [@khalsa2020openaltimetry].

[`phoREAL`](https://github.com/icesat-2UT/PhoREAL) (Photon Research and Engineering Analysis Library) from the University of Texas is an open source application allowing for subsetting and conversion of ICESat-2 ATL03 Global Geolocated Photon Height and ATL08 Land and Vegetation Height data products. `phoREAL` allows users to spatially subset locally-stored data based on Ground Track. `phoREAL` allows users to visualize data from both ATL03 and ATL08 and perform some statistics on heights based on time or geospatial location.

[`captoolkit`](https://github.com/nasa-jpl/captoolkit) (Cryosphere Altimetry Processing Toolkit) from the NASA Jet Propulsion Library [@fernando_paolo_2020_3665785] allows users to estimate elevation change using altimetry data from multiple airborne and satellite missions. `captoolkit` has functions to apply geophysical corrections, calculate elevation change, and interpolate into gridded fields. `captoolkit` uses parallelized functions that operate on local granule files, with optimization for High Performance Computing (HPC) clusters. 

# SlideRule framework
`SlideRule` is a C++/Lua framework for on-demand data processing (\autoref{fig:architecture}). It is a science data processing service that runs in the cloud and responds to REST API calls to process and return science results.

![SlideRule architecture schematic.\label{fig:architecture}](./sliderule_architecture.png)

## ICESat-2 SlideRule plugin
The ICESat-2 SlideRule plugin provides two main types of services: 1) efficient access to archived ICESat-2 products, and 2) customized level-2 products (ATL06-SR) generated on demand from the ATL03 cloud assets.

### ATL03 data access
`SlideRule` provides services that allow users to access ATL03 photon-height and classification data from cloud assets without the need to download entire granules, returning the subset of ATL03 parameters that are needed to interpret surface heights from the photon-height distribution.

A more advanced photon classification scheme is available for vegetated surfaces as part of the ATL08 Land and Vegetation Height product [@neuenschwander2019atl08]. This classification approach allows improved segregation between photons returned from the canopy, ground surfaces, and noise. Users wishing to apply the ATL08 classification to the ATL03 photons must download and read both an ATL03 granule and the corresponding ATL08 granule, establish linked indices, and apply the ATL08 classification to the ATL03 photons. The ICESat-2 SlideRule API includes an option to retrieve the photon classifications from ATL08 cloud assets, and efficiently apply to the desired subset of ATL03 photons for subsequent processing.

### ATL06-SR algorithm
The standard ATL06 (land-ice height) product [@smith2019land] (hereafter "ATL06-legacy") provides estimates of surface height and slope with along-track spacing of 20 m, derived from 40-m segments of ATL03 photons classified as likely surface returns. The algorithm iteratively improves the initial photon classification, and calculates a set of corrections based on the residuals between the segment heights and the selected photon heights to correct for sub-centimeter biases in the resulting height estimates.

ATL06-SR implements much of the ATL06-legacy algorithm in a framework that allows for customization of the initial photon classification, the segment length and spacing, and the filtering strategy used to identify valid segmentsin the product. For the sake of simplicity and speed, ATL06-SR omits some of the corrections required for sub-centimeter accuracy over polar surfaces, including the first-photon bias and pulse-shape corrections [@smith2019land]. Over non-polar surfaces, omitting these biases should result in sub-centimeter vertical errors in ATL06-SR heights.

One important difference between the ATL06-legacy and ATL06-SR algorithms is in the iterative photon-selection strategy. Both algorithms begin with photons selected based on the input photon classification. The selection is then refined to reject photons that have large residual values (i.e., larger than three times a robust estimate of the standard deviation of the previously selected residuals) and the fit is recalculated. This process continues until a specified number of iterations has occurred, or until subsequent iterations leave the photon selection unchanged. In ATL06-legacy, at each iteration the photons are selected from the complete set of input photons, regardless of how they were initially flagged or selected, while in ATL06-SR, each iteration selects photons exclusively from those selected in the previous iteration. This means that in ATL06-legacy, the number of photons can increase from one iteration to the next, while in ATL06-SR it can only remain constant or decrease. This choice lets ATL06-SR more faithfully reflect the height distribution of the initial selection, at the expense of sometimes missing photons close to the surface that might add more information to the fitting algorithm, possibly improving the accuracy of the fit. Under most circumstances, the two algorithms produce very similar results.

#### Photon classification
The ATL06-SR algorithm supports three sources of photon classification data (\autoref{fig:classification}): 1) ATL03 photon confidence values (from respective classification algorithms for land, ocean, sea-ice, land-ice, or inland water) [@neumann2019ice], 2) ATL08 photon classification [@neuenschwander2019atl08], and 3) YAPC (Yet Another Photon Classification) photon-density-based classification [@tyler_sutterley_2022_6717591].

![Example SlideRule output of classified ATL03 photons and corresponding ATL06-SR points.\label{fig:classification}](./sliderule_classification.png)

Users can select the classification values to be included in the initial photon selection for the ATL06-SR algorithm. For example, a user might wish to generate ATL06-SR products based only on photons with ATL03 photon classification values indicating medium or better confidence, or photons flagged as ground returns in ATL08 to remove photons from canopy returns. This powerful approach enables precise surface elevation measurement with the ATL06 algorithm over all land surfaces, not just the polar ice sheets and glaciers.

The rapid processing offered by the `SlideRule` service allows for interactive testing and evaluation of various combinations of ATL06-SR parameter and classification schemes for a broad range of scientific and engineering applications.

# Acknowledgements

The `SlideRule` project is funded by the NASA ICESat-2 project and NASA award 80NSSC20K0995.

# References
