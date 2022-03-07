---
title: 'ICESat-2 SlideRule: Enabling Rapid, Scaleable, Open Science'
tags:
  - Python
  - NASA
  - ICESat-2
  - Satellite
  - Snow
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
**what problems the software is designed to solve and who the target audience is?**

The ATL03 (photon height) product [@neumann2019ice] provides all of the information needed to calculate the height, location, and timing of ICESat-2 photons, and provides a set of classification variables that estimate the likelihood that each photon results from a reflection from the surface, or that it results from instrumental noise or from solar background. The ATL03 product, however, also contains a wide range of additional parameters that may not be of use to most users, and the product format is somewhat complex. The complexity and the large volume of the ATL03 product likely present a barrier to the use of these data for the development and verification of new algorithms, and for data exploration by new users.

The ICEsat-2 project has made available a range of higher-level products that reduce the volume and complexity of the ATL03 product, and provide estimates of surface height, a step beyond the photon locations provided by ATL03. In particular, the ATL06 product provides high-precision estimates of surface height at 40-meter resolution, using parameters appropriate to flat, highly reflective polar snow and ice surfaces. Similar to ATL03, ATL06 contains a large number of parameters describing each height measurement that may not be useful to all users, and is provided in large [CHECK SIZE] granules that are often too large for convenient data exploration or for studies of small geophysical targets. Further, the standard 40-meter resolution of ATL06 may be too coarse for some applications, and the algorithm used to segregate photons returned from the surface may not be optimal for complex land surfaces or for vegetated surfaces. ICESat-2 SlideRule provides users with the ability to generate products analagous to ATL06, but with parameters and photon classification strategies tailored to the characteristics of their areas of study.

## State of the Field
**Do the authors describe how this software compares to other commonly-used packages?**

Analogous services for other missions:

openTopography

ASF

Other serivces for ICESat-2:

icepyx

OpenAltimetry

phoreal


# SlideRule Framework
Implemented in C++/Lua
SlideRule is a C++/Lua framework for on-demand data processing \autoref{fig:architecture}. It is a science data processing service that runs in the cloud and responds to REST API calls to process and return science results.

![SlideRule architecture.\label{fig:architecture}](./sliderule_architecture.png)

# Algorithm Description
The ICESat-2 SlideRule API provides two main types of services. The first provides access to existing ICESat-2 products stored as cloud assets, the second provides a customized level-2 product (ATL06-SR) generated on demand from ATL03 and ATL08 cloud assets.

## ATL06-SR

The ATL06 (land-ice height) product provided by ICESat-2 [@smith2019land] (hereafter ATL06-legacy) provides estimates of surface height derived from ATL03 photon height using an algorithm adapted to the flat surfaces and high reflectivities common over polar ice sheets. Briefly, the algorithm uses photons identified as likely surface returns by the ATL03 photon classification, or by a backup algorithm where the ATL03 classification fails, to estimate the height and slope of 40-meter-long line segments for data from each of ICESat-2's ground tracks. It uses an iterative algorithm to improve the initial photon classification, and calculates a set of corrections based on the residuals between the segment heights and the selected photon heights to correct for sub-centimeter biases in the resulting height estimates.

The ATL06-SlideRule algorithm (ATL06-SR) implements much of the ATL06-legacy algorithm in a framework that allows customization of the initial photon classification, the resolution and posting of the product, and the filtering strategy used to identify valid segments. For the sake of simplicity and speed of calculation, ATL06-SR omits some of the corrections required for sub-centimeter accuracy over polar surfaces, including the first-photon bias and pulse-shape corrections ([@smith2019land]). Over non-polar surfaces, omitting these biases should result in sub-centimeter vertical errors in ATL06-SR heights.

One important difference between the ATL06-legacy and ATL06-SR algorithms is in the iterative photon-selection strategy. Both algorithms begin with photons selected based on the input photon classification. The selection is then refined to reject photons that have large residual values (i.e. larger than three times a robust estimate of the standard deviation of the previously selected residuals) and the fit is recalculated. This process continues until a specified number of iterations has occurred, or until subsequent iterations leave the photon selection unchanged. In ATL06-legacy, at each iteration the photons are selected from the complete set of input photons, regardless of how they were initially flagged or selected, while in ATL06-SR, each iteration selects photons exclusively from those selected in the previous iteration. This means that in ATL06-legacy, the number of photons can increase from one iteration to the next, while in ATL06-SR it can only remain constant or decrease. This choice lets ATL06-SR more faithfully reflect the height distribution of the initial selection, at the expense of sometimes missing photons close to the surface that might add more information to the fitting algorithm, possibly improving the accuracy of the fit. Under most circumstances, the two algorithms produce very similar results.
 

## Classified photons

SlideRule provides services that allow users to access ATL03 photon-height and classification data from cloud assets without the need to download entire granules, returning the subset of ATL03 parameters that are needed to interpret surface heights from the photon-height distribution.

ATL06-SR allows the user to select from three sources of classification information: 
  * ATL03 photon confidence values, based on algorithm-specific classification types for land, ocean, sea-ice, land-ice, or inland water
  * ATL08 photon classification
  * Experimental YAPC (Yet Another Photon Classification) photon-density-based classification

For vegetated surfaces, a more advanced photon classification scheme has been made available as part of the ATL08 Land and Vegetation Height product. This classification allows better segregation between photons returned from vegetation, photons that reflected from land surfaces, and noise than does the classification in the ATL03 product [@neuenschwander2019atl08]. Users wishing to apply this classification to ATL03 data would ordinarily need to download both an ATL03 granule and the corresponding ATL08 granule, and apply the classification from ATL08 to ATL03. The ICESat-2 SlideRule API includes an option to retrieve the photon classifications from ATL08 cloud assests, and apply them directly to ATL03 photons.

Users can further select the classification values to be included in the initial photon selection: For example, a user might request ATL06-SR product based only on photons with ATL03 photon classification values indicating medium or better confidence, or might request a product based only on photons flagged in ATL08 as coming from 'ground.'

## Key ATL06-SR parameters:

**For a new user - here are the key things to control output**

Filtering parameters
Algorithm parameters


- `srt`: surface type for ATL03 confidence level
- `cnf`: ATL03 confidence level for photon selection
    * `-2`: Possible instrumental artifact
    * `-1`: Events not associated with surface type
    *  `0`: Noise
    *  `1`: Buffer but algorithm classifies as background
    *  `2`: Low
    *  `3`: Medium
    *  `4`: High
- `atl08_class`: ATL08 land surface classifications [@neuenschwander2019]
    * `"atl08_noise"`
    * `"atl08_ground"`
    * `"atl08_canopy"`
    * `"atl08_top_of_canopy"`
    * `"atl08_unclassified"`
- ``quality_ph``: quality classification for photon selection
    * `0`: Nominal
    * `1`: Possible Afterpulse
    * `2`: Possible Impulse Response
    * `3`: Possible TEP 
- `ats` minimum along track spread
- `cnt`: minimum photon count in segment
- `len`: length of ATL06 segment in meters
- `res`: step distance for successive ATL06 segments in meters
- `maxi`: maximum iterations, not including initial least-squares-fit selection
- `H_min_win`: minimum height of photon window in meters 
- `sigma_r_max`: maximum robust dispersion in meters [@smith2017]


ATL03-SR return payload (?)

ATL06-SR products 

Modifications to the standard SlideRule

# Acknowledgements

The SlideRule project is supported by the NASA ICESat-2 project.

# References
