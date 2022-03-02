See example: https://joss.readthedocs.io/en/latest/submitting.html#example-paper-and-bibliography

Can generate pdf preview here: https://whedon.theoj.org/
* repo: https://github.com/ICESat2-SlideRule/sliderule-python
* branch: paper

SlideRule docs: https://github.com/ICESat2-SlideRule/sliderule-project/tree/main/rtd

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

SlideRule is a server-side framework for on-demand processing of science data. This enables researchers and other data systems to have low-latency access to custom-generated, high-level, analysis-ready data products using processing parameters supplied at the time of the request. The sliderule-python client enables easy interaction with SlideRule. The Sliderule project has the goal of demonstrating a new paradigm for providing science data products to researchers.

The ICESat-2 SlideRule software is plug-in for the SlideRule framework to support science applications for the NASA Ice Cloud and land Elevation Satellite-2 (ICESat-2) mission. We implemented a simplified, cloud-optimized version of the ATL06 algorithm to process the official lower-level ATL03 photon data products hosted by NASA NSIDC on AWS. The user can specify several key algorithm parameters, and select subsets of classified photons to process. Custom data products are returned in seconds to minutes, enabling rapid parameter iteration, and subsequent scientific analysis, visualization, and output of archive-ready files for reproducible science.  

# Statement of need

Need to fill this in...

ATL03 products [@neumann2019ice]

# SlideRule Framework
Implemented in C++/Lua
REST API

# Algorithm Description
The ICESat-2-slideRule API provides two main types of services.  The first provides access to existing ICESat-2 products stored as cloud assets, the second provides a customized level-2 (ATL06-SR) product generated on demand from ATL03 and ATL08 cloud assets.

### Classified photons

The ATL03 (photon height) product provides all of the information needed to calculate the height, location, and timing of ICESat-2 photons, and provides a set of classification variables that estimate the likelihood that each photon results from a reflection from the surface, or that it results from instrumental noise or from solar background.  The product, however, also contains a wide range of additional parameters that may not be of use to most users, and the product format is somewhat complex.  slideRule provides services that allow users to access ATL03 photon-height and classification data from cloud assets without the need to download entire granules, returning the subset of ATL03 parameters that are needed to interpret surface heights from the photon-height distribution.  

For vegetated surfaces, a more advanced photon classification scheme has been made available as part of the ATL08 Land and Vegetation Height product.  This classification allows better segregation between photons returned from vegetation, photons that reflected from land surfaces, and noise than does the classification in the ATL03 product [@neuenschwander2019atl08].  Users wishing to apply this classification to ATL03 data would ordinarily need to download both an ATL03 granule and the corresponding ATL08 granule, and apply the classification from ATL08 to ATL03.  The ICESat-2 slideRule API includes an option to retrieve the photon classifications from ATL08 cloud assests, and apply them directly to ATL03 photons.


## ATL06-SR

The ATL06 (land-ice height) product provided by NASA's ICESat-2  [@smith2019land] (hereafter ATL06-legacy) provides estimates of surface height derived from ATL03 photon height using an algorithm adapted to the flat surfaces and high reflectivities common over polar ice sheets.  Briefly, the algorithm uses photons identified as likely surface returns by the ATL03 photon classification, or by a backup algorithm where the ATL03 classification fails, to estimate the height and slope of 40-meter-long line segments for data from each of ICESat-2's ground tracks. It uses an iterative algorithm to improve the initial photon classification, and calculates a set of corrections based on the residuals between the segment heights and the selected photon heights to correct for sub-centimeter biases in the resulting height estimates.

ATL06-SR implements much of the ATL06-legacy algorithm in a framework that allows customization of the initial photon classification, the resolution and posting of the product, and the filtering strategy used to identify valid segments.  For the sake of simplicity and speed of calculation, ATL06-SR omits some of the corrections required for sub-centimeter accuracy over polar surfaces, including the first-photon bias and pulse-shape corrections ([@smith2019land]).  Over non-polar surfaces, omitting these biases should result in sub-centimeter vertical errors in ATL06-SR product.  

One important difference between the ATL06-legacy and ATL06-SR algorithms is in the iterative photon-selection strategy.  Both algorithms begin with photons selected based on the input photon classification.  The selection is then refined to reject photons that have large residual values (i.e. larger than three times a robust estimate of the standard deviation of the previously selected residuals) and the fit is recalculated.  This process continues until a specified number of iterations has occurred, or until subsequent iterations leave the photon selection unchanged.  In ATL06-legacy, at each iteration the photons are selected from the complete set of input photons, regardless of how they were initially flagged or selected, while in ATL06-SR, each iteration selects photons exclusively from those selected in the previous iteration.  This means that in ATL06-legacy, the number of photons can increase from one iteration to the next, while in ATL06-SR it can only remain constant or decrease.  This choice lets ATL06-SR more faithfully reflect the height distribution of the initial selection, at the expense of sometimes missing photons close to the surface that might add more information t 
 

### Input classification source
ATL06-SR allows the user to select from three sources of classification information: 
  * ATL03 photon confidence values based on algorithm-specific classification types for land, ocean, sea-ice, land-ice, or inland water
  * ATL08 photon classification
  * Experimental YAPC (Yet Another Photon Classification) photon-density-based classification

Users can further select the classification values to be included in the initial photon selection: For example, a user might request ATL06-SR product based only on photons with ATL03 photon classification values indicating medium or better confidence, or might request a product based only on photons flagged in ATL08 as coming from 'ground.'



ATL06 algorithm and products 
Modifications to the standard SlideRule
Key parameters:
* segment length
* ... 


Single dollars ($) are required for inline mathematics e.g. $f(x) = e^{\pi/x}$

Double dollars make self-standing equations:

$$\Theta(x) = \left\{\begin{array}{l}
0\textrm{ if } x < 0\cr
1\textrm{ else}
\end{array}\right.$$

You can also use plain \LaTeX for equations
\begin{equation}\label{eq:fourier}
\hat f(\omega) = \int_{-\infty}^{\infty} f(x) e^{i\omega x} dx
\end{equation}
and refer to \autoref{eq:fourier} from text.

# Citations

Citations to entries in paper.bib should be in
[rMarkdown](http://rmarkdown.rstudio.com/authoring_bibliographies_and_citations.html)
format.

If you want to cite a software repository URL (e.g. something on GitHub without a preferred
citation) then you can do it with the example BibTeX entry below for @fidgit.

For a quick reference, the following citation commands can be used:
- `@author:2001`  ->  "Author et al. (2001)"
- `[@author:2001]` -> "(Author et al., 2001)"
- `[@author1:2001; @author2:2001]` -> "(Author1 et al., 2001; Author2 et al., 2002)"

# Figures

Figures can be included like this:
![Caption for example figure.\label{fig:example}](figure.png)
and referenced from text using \autoref{fig:example}.

Figure sizes can be customized by adding an optional second parameter:
![Caption for example figure.](figure.png){ width=20% }

# Acknowledgements

We acknowledge support from the NASA ICESat-2 project...

# References
