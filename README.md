# zip_zcta_master_xwalks

The code cleans crosswalks offered by the UDS mapper at https://udsmapper.org/zip-code-to-zcta-crosswalk/. The purpose is to have a single master zip2zcta crosswalk that can be used across years.

## Zip vs ZCTA

A ZIP Code is a postal code used by the United States Postal Service (USPS). Introduced in 1963, the term "ZIP" is an acronym for "Zone Improvement Plan," and it was implemented to improve the accuracy and efficiency of the delivery of mail within the United States.

A ZCTA, or ZIP Code Tabulation Area, is a statistical entity developed by the United States Census Bureau for tabulating summary statistics. These areas are roughly equivalent to the ZIP Codes used by the United States Postal Service, but there are some differences.

ZIP Codes don't always correspond neatly to municipal or other administrative boundaries, and sometimes ZIP Codes can encompass businesses or large facilities without any residential population.

ZCTAs were created to address these irregularities and better align statistical data with recognizable geographic areas. ZCTAs are constructed by aggregating the Census blocks that have addresses in the same ZIP Code.

The correspondence between ZIP Codes and ZCTAs isn't perfect, and there may be differences in the exact boundaries. However, ZCTAs are useful for demographic and geographic analysis and allow researchers to study areas that roughly correspond to the way people think about locations in terms of postal addresses.

## ZCTA Editions

ZIP Codes change to adapt to shifts in population, infrastructure, administrative boundaries, business needs, and the logistical requirements of mail delivery. These changes help ensure that the postal system remains efficient and responsive to the needs of both senders and recipients.

ZIP Code Tabulation Areas (ZCTAs) have been defined in different editions corresponding to different decennial census data. The term "ZCTA5CE00" is used by the by the United States Census Bureau, and can be broken down as follows:

* **ZCTA**: ZIP Code Tabulation Area
* **5**: Refers to the five-digit ZIP Code
* **CE00**: Refers to the Census Edition for the year 2000. Editions are labeled as CE00, CE10, and CE20, which correspond to the census data from the years 2000, 2010, and 2020, respectively.

These different editions allow for consistent analysis over time while accommodating changes in the underlying ZIP Code system and geographic boundaries. It helps ensure that researchers and policymakers are working with data that accurately reflects the geographic realities of the time period they are studying.

## ZIP2ZCTA crosswalks

A ZIP2ZCTA crosswalk is essentially a mapping between these two systems. It allows users to translate between ZIP Codes and ZCTAs, and it can be essential for researchers, policymakers, and others who need to correlate postal information with demographic or economic data collected by the Census Bureau.

> The UDSmapper offers yearly crosswalks from 2009 onwards. Yearly releases are not harmonized. In this repository, we offer a zip2zcta master xwalk that can be used across years. The master xwalk keeps all zipcodes that are retired at some point and resolves disambiguities when they exist.

## References

Grubesic TH, Matisziw TC. On the use of ZIP codes and ZIP code tabulation areas (ZCTAs) for the spatial analysis of epidemiological data. Int J Health Geogr. 2006 Dec 13;5:58. doi: 10.1186/1476-072X-5-58. PMID: 17166283; PMCID: PMC1762013.
https://www.ncbi.nlm.nih.gov/pmc/articles/PMC1762013/

Krieger N, Waterman P, Chen JT, Soobader MJ, Subramanian SV, Carson R. Zip code caveat: bias due to spatiotemporal mismatches between zip codes and US census-defined geographic areas--the Public Health Disparities Geocoding Project. Am J Public Health. 2002 Jul;92(7):1100-2. doi: 10.2105/ajph.92.7.1100. PMID: 12084688; PMCID: PMC1447194.
https://pubmed.ncbi.nlm.nih.gov/12084688/

