# Motivation

**zcta** 

* In theory, zctas change every 10 years and there are currently three editions: zcta500, zcta510 and zcta520
* In practice, there are yearly zcta shp file realeases. For the same editions there might be small differences between the releases.

**zipcode**

* In theory, zipcodes change yearly. There are several providers of shapefiles for zipcodes, there is not an official USPS realease.
* ESRI provides yearly releases of zipcode shapefiles which exclude poboxes.

**xwalks**

* Zipcodes are "smaller" than zctas. Zipcode to zcta crosswalks have a single entry per zipcode. There might be zctas that point to multiple zipcodes. 
* There is no official zip2zcta xwalk.
* USD provides xwalks 2009 onwards. The yearly releases are not harmonized: there are changes in column names and other file format changes.
* Within a single zcta edition, there are small differences in the zip to zcta mapping across years.

**Questions**

* Is it worth using yearwise crosswalks?

For the most part, the crosswalk entries will have the same mapping every year. Also, years prior to 2009 do not have a uds crosswalk. In consequence, merging year-zip to year-zcta, requires a different logic to be applied years prior to 2009.

Another complication is identifying retired zipcodes that are not cleaned in other data sources. 

**Conclusion**
It make sense to have a single master zip2zcta crosswalk that harmonizes all zcta editions and **incorporates all retired zipcodes and retired zctas**.

