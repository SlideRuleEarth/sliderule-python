---
title: 'ICESat-2 SlideRule: Enabling Rapid, Scaleable, Open Science'
tags:
  - Python
  - NASA
  - ICESat-2
  - Glacier
  - Earth observation
authors:
  - name: J.P. Swinski #^[co-first author] # note this makes a footnote saying 'co-first author'
    orcid: 0000-0000-0000-0000
    affiliation: 1 
  - name: David Shean 
    orcid: 0000-0003-3840-3860
    affiliation: "2, 5" 
  - name: Ben Smith 
    affiliation: 4 
  - name: Tyler Sutterley 
    affiliation: 4 
  - name: Scott Henderson 
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

SlideRule is a server-side framework for on-demand processing of science data. This enables researchers and other data systems to have low-latency access to custom-generated, high-level, analysis-ready data products using processing parameters supplied at the time of the request. The Sliderule project has the goal of demonstrating a new paradigm for providing science data products to researchers.

While SlideRule can be accessed by any http client (e.g., curl) by making GET and POST requests, the sliderule-python client provides an API and functionality to enable easy interaction with the SlideRule service, returning community-standard Python data types. 

The ICESat-2 SlideRule plug-in for the python client supports science applications for the NASA Ice Cloud and land Elevation Satellite-2 (ICESat-2) mission. The ICESat-2 plug-in includes a simplified, cloud-optimized version of the ATL06 algorithm to process the lower-level ATL03 photon data products hosted on AWS by the NSIDC DAAC [@atl03_nsidc]. The user can specify several key algorithm parameters, and select subsets of classified photons to process. Custom data products are returned in seconds to minutes, enabling rapid parameter iteration, and subsequent scientific analysis, visualization, and output of archive-ready files for reproducible science.

# Statement of need
The Ice, Cloud, and Land Elevation Satellite – 2 (ICESat-2) launched in September 2018 to continue as the follow on mission to the original ICESat mission (2003-2010) which pioneered the use of a space-based laser altimeter to measure the height of the Earth.  As the names imply, these missions are optimized to measure elevation changes in the cryosphere, including ice sheets and sea ice.  The ICESat-2 mission [@markus2017ice] leveraged the lessons and achievements of ICESat and provides a substantial improvement in spatial and temporal coverage.

ICESat-2 carries the Advanced Topographic Laser Altimeter System (ATLAS), which generates six laser footprints on the Earth’s surface, and records the time the laser light leaves ATLAS, and the time reflected photons of laser light return to ATLAS [@neumann2019ice].  Combining the time of flight with the pointing vectors for the beams with the position of the observatory in space allows the ground processing to establish a precise latitude, longitude, and height for each photon.  These data allow scientists to study the height of our planet, and by aggregating these data in space and time, study the changes in the height of Earth.

The ICESat-2 Level 2A Geolocated Photon Data Product (ATL03) [@neumann2019atbd] provides unique latitude, longitude, height and timing of ICESat-2 photons, and is the lowest level data product most scientists will use.  ATL03 provides an initial photon classification, identifying them as likely signal photons reflected off Earth, or as likely background photons due to sunlight or instrument noise. The product, however, also contains a wide range of additional parameters that may not be of use to most users, and the product format is somewhat complex. The complexity and large data volume (~2 GB / granule) of ATL03 likely present a barrier to the use of these data for the development and verification of new algorithms, and for data exploration by new users.

The ICESat-2 project generates a range of higher-level products [@nsidc_url] that reduce the data volume and complexity and provides user with a more accurate determination of the height of Earth, posted at lower along-track resolution than the ATL03 product. In particular, the ATL06 product [@smith2019ice] provides high-precision estimates of surface height at 40-meter resolution, using parameters appropriate to flat, highly reflective polar snow surfaces. Similar to ATL03, ATL06 contains a large number of parameters describing each height measurement that may not be useful to all users, and is provided in ~100 MB granules that are often too large for convenient data exploration, and are generally only produced over glaciers and ice sheets. Further, the 40-meter resolution of ATL06 may be too coarse for some users, and the algorithm used to segregate photons returned from the surface may not be optimal for complex land surfaces or for vegetated surfaces. SlideRule provides users with the ability to generate products using the ATL06 algorithm, but with parameters and photon classification strategies tailored to the characteristics of their areas of study.


## State of the Field
__Do the authors describe how this software compares to other commonly-used packages?__

#### Granule download

The current paradigm for using data from the ICESat-2 mission involves downloading large volumes of standard data products from the NASA DAAC. The National Snow and Ice Data Center offers subsetting services allowing users to download geographic subsets of products, and to select the specific variables to be included in the subsets.  These services are sufficient for many science applications, but not all, and users may experience substantial latency that reduces these services' utility for data exploration. 

#### On-demand Data Processing

Several other projects are exploring on-demand, cloud-based processing for satellite and/or point cloud data. 
The Alaska Satellite Facility's Hybrid Pluggable Processing Pipeline (ASF HyP3) enables custom processing of satellite SAR images from multiple missions. 
The OpenTopography project offers "Web service-based data access, processing, and analysis capabilities that are scalable, extensible, and innovative" with emphasis on "high-resolution (meter to sub-meter scale), Earth science-oriented, topography data acquired with lidar and other technologies." The current processing options and data products are focused on airborne LiDAR point clouds, with no plans to support ICESat-2 data.

#### ICESat-2 packages

`icepyx` [@scheick2019ipx] is a python library for querying the NASA Common Metadata Repository (CMR) and allowing for programmatic access to ICESat-2 data through NSIDC services. `icepyx` allows for queries based on spatial and temporal parameters, as well as ICESat-2 orbital cycle and Reference Ground Track (RGT). Accessing NSIDC API services through icepyx allows users to spatiotemporally subset ICESat-2 data and convert data to other file formats. At present, `icepyx` allows users to read and visualize data available from NSIDC, but it is not a data processing service.

The `OpenAltimetry` platform [@khalsa2020openaltimetry], which is closely related to the OpenTopography project, offers discovery, access, and visualization of data from NASA’s ICESat and ICESat-2 missions.  This service includes an API that can provide access to either photon-level data or height variables from the along-track products, but does not offer processing from photons to higher-level products.

`phoREAL` (Photon Research and Engineering Analysis Library) from the University of Texas is an open-source application allowing for subsetting and conversion of ICESat-2 ATL03 Global Geolocated Photon Height and ATL08 Land and Vegetation Height data products. `phoREAL` allows users to spatially subset locally available data and subset based on Ground Track. `phoREAL` allows users to visualize data from both ATL03 and ATL08 and perform some statistics on heights based on time or geospatial location. 

`captoolkit` (Cryosphere Altimetry Processing Toolkit) is a software library from the NASA Jet Propulsion Library (JPL). `captoolkit` allows users to estimate elevation change using altimetry data from multiple airborne and satellite missions.`captoolkit` has functions to apply geophysical corrections, calculate elevation change, and interpolate into gridded fields. `captoolkit` is built for processing on High Performance Computing (HPC) clusters by subsetting datasets into smaller granules and using parallelized functions. 

Ute processor? [not open source.  only available through email to her as far as I know](/HJQfPXSdQo2pmcKzhkAe0w)

# SlideRule Framework

Implemented in C++/Lua
SlideRule is a C++/Lua framework for on-demand data processing \autoref{fig:architecture}. It is a science data processing service that runs in the cloud and responds to REST API calls to process and return science results.

![SlideRule architecture.\label{fig:architecture}](./sliderule_architecture.png)

# Algorithm Description
The ICESat-2-slideRule API provides two main types of services.  The first provides access to existing ICESat-2 products stored as cloud assets, the second provides a customized level-2 product (ATL06-SR) generated on demand from ATL03 and ATL08 cloud assets.

### ATL03 photon-data access

slideRule provides services that allow users to access ATL03 photon-height and classification data from cloud assets without the need to download entire granules, returning the subset of ATL03 parameters that are needed to interpret surface heights from the photon-height distribution.

For vegetated surfaces, a more advanced photon classification scheme has been made available as part of the ATL08 Land and Vegetation Height product.  This classification allows better segregation between photons returned from vegetation, photons that reflected from land surfaces, and noise than does the classification in the ATL03 product [@neuenschwander2019atl08].  Users wishing to apply this classification to ATL03 data would ordinarily need to download both an ATL03 granule and the corresponding ATL08 granule, and apply the classification from ATL08 to ATL03.  The ICESat-2 slideRule API includes an option to retrieve the photon classifications from ATL08 cloud assests, and apply them directly to ATL03 photons.

## ATL06-SR

The ATL06 (land-ice height) product provided by NASA's ICESat-2  [@smith2019land] (hereafter ATL06-legacy) provides estimates of surface height derived from ATL03 photon height using an algorithm adapted to the flat surfaces and high reflectivities common over polar ice sheets.  Briefly, the algorithm uses photons identified as likely surface returns by the ATL03 photon classification, or by a backup algorithm where the ATL03 classification fails, to estimate the height and slope of 40-meter-long line segments for data from each of ICESat-2's ground tracks. It uses an iterative algorithm to improve the initial photon classification, and calculates a set of corrections based on the residuals between the segment heights and the selected photon heights to correct for sub-centimeter biases in the resulting height estimates.

ATL06-SR implements much of the ATL06-legacy algorithm in a framework that allows customization of the initial photon classification, the resolution and posting of the product, and the filtering strategy used to identify valid segments.  For the sake of simplicity and speed of calculation, ATL06-SR omits some of the corrections required for sub-centimeter accuracy over polar surfaces, including the first-photon bias and pulse-shape corrections ([@smith2019land]).  Over non-polar surfaces, omitting these biases should result in sub-centimeter vertical errors in ATL06-SR heights.

One important difference between the ATL06-legacy and ATL06-SR algorithms is in the iterative photon-selection strategy.  Both algorithms begin with photons selected based on the input photon classification.  The selection is then refined to reject photons that have large residual values (i.e. larger than three times a robust estimate of the standard deviation of the previously selected residuals) and the fit is recalculated.  This process continues until a specified number of iterations has occurred, or until subsequent iterations leave the photon selection unchanged.  In ATL06-legacy, at each iteration the photons are selected from the complete set of input photons, regardless of how they were initially flagged or selected, while in ATL06-SR, each iteration selects photons exclusively from those selected in the previous iteration.  This means that in ATL06-legacy, the number of photons can increase from one iteration to the next, while in ATL06-SR it can only remain constant or decrease.  This choice lets ATL06-SR more faithfully reflect the height distribution of the initial selection, at the expense of sometimes missing photons close to the surface that might add more information to the fitting algorithm, possibly improving the accuracy of the fit. Under most circumstances, the two algorithms produce very similar results.
 

### Input classification source
ATL06-SR allows the user to select from three sources of classification information: 
  * ATL03 photon confidence values, based on algorithm-specific classification types for land, ocean, sea-ice, land-ice, or inland water
  * ATL08 photon classification
  * Experimental YAPC (Yet Another Photon Classification) photon-density-based classification

Users can further select the classification values to be included in the initial photon selection: For example, a user might request ATL06-SR product based only on photons with ATL03 photon classification values indicating medium or better confidence, or might request a product based only on photons flagged in ATL08 as coming from 'ground.'

## Examples
Give example, explain the key parameters, general categories, what they do, sensitivity, then reference doc for more info

### Exposed surface
### Isolating ground and/or canopy
General ATL06 request
Green trees request (classification)

## Key ATL06-SR parameters:

For a new user - here are the key things to control output

Filtering parameters
Algorithm parameters




# Acknowledgements

The SlideRule project is funded by the NASA ICESat-2 project.

# References
