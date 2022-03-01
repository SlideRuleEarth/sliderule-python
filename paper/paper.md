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

## ATL06-SR
ATL06 algorithm and products [@smith2019land]
Modifications to the standard SlideRule
Key parameters:
* segment length
* ... 

### Photon classification 
ATL08 classification [@neuenschwander2019atl08]

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
