# zip2zcta_master_xwalks
[![](<https://img.shields.io/badge/Dataverse-10.7910/DVN/SYNPBS-orange>)](https://doi.org/10.7910/DVN/HYNJSZ)

The code cleans crosswalks offered by the UDS mapper at https://udsmapper.org/ (status:out-of-service, date noted: Dec 2024). The purpose is to have a single master zip2zcta crosswalk that can be used across years.

> The UDSmapper offers yearly crosswalks from 2009 onwards. Yearly releases are not harmonized. In this repository, we offer a zip2zcta master xwalk that can be used across years. The master xwalk keeps all zipcodes that are retired at some point and resolves disambiguities when they exist.

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

## References

Grubesic TH, Matisziw TC. On the use of ZIP codes and ZIP code tabulation areas (ZCTAs) for the spatial analysis of epidemiological data. Int J Health Geogr. 2006 Dec 13;5:58. doi: 10.1186/1476-072X-5-58. PMID: 17166283; PMCID: PMC1762013.
https://www.ncbi.nlm.nih.gov/pmc/articles/PMC1762013/

Krieger N, Waterman P, Chen JT, Soobader MJ, Subramanian SV, Carson R. Zip code caveat: bias due to spatiotemporal mismatches between zip codes and US census-defined geographic areas--the Public Health Disparities Geocoding Project. Am J Public Health. 2002 Jul;92(7):1100-2. doi: 10.2105/ajph.92.7.1100. PMID: 12084688; PMCID: PMC1447194.
https://pubmed.ncbi.nlm.nih.gov/12084688/

## Data Description

* **Time coverage** NA
* **State coverage** All US states
* **Population coverage** NA
* **Unit** zipcode, zcta

## Codebook

Zip types as described in the UDS mapper site:

* ZIP Code Area - ZIP Code Areas are typical ZIP Codes without any special designation.
* Post Office or large volume customer - Post Offices or large volume customers typically occupy a very small geography and have few residential addresses located within them.

| Variable Name | Description |
|---|---|
| zip | (character): 5-digit ZIP code. A postal code used by the United States Postal Service. |
| zcta | (character): 5-digit ZIP Code Tabulation Area (ZCTA) code. Codes used by the U.S. Census Bureau for tabulating summary statistics. In this dataset, it represents which ZCTA the ZIP code matches with.|
| year_match | (int): Year of zip and zcta match. Represents the year when the mapping between the ZIP code and ZCTA is recorded in the raw uds xwalsk. |
|census_edition | (character): edition or version of the census data source from which the ZCTA information was derived. "ZCTA5CE20" indicates a 2020 Census ZCTA 5-digit edition. |
|state | (character): state. Represents the U.S. state or territory where the ZIP code is located. |
|is_area | (boolean): A boolean flag (True/False) indicating if the ZIP code type is a ZIP Code Area. |
|is_self_mapped | (boolean): A boolean flag (True/False) indicating if the ZIP code directly maps to the ZCTA (i.e., they are the same). This can be useful in identifying ZIP codes that don't need additional conversion for census-based studies. |
|is_post_office | (boolean): A boolean flag (True/False) indicating if the ZIP code type is a post office or large volume customer (pobox). That is, a postal delivery point rather than a general area. |
|info | (character): Provides additional context or information on the relation between the ZIP and ZCTA. For instance, "Spatial join to ZCTA" indicates that the ZIP was mapped to a ZCTA using spatial data, while "Zip matches ZCTA" indicates a direct match without any spatial consideration. |
|min_match | (int): Minimum year match. Represents the first year a particular ZIP-ZCTA relationship was recorded in the raw uds crosswalks. |
|max_match | (int): Maximum year match. Represents the the most recent year a particular ZIP-ZCTA relationship was recorded in the raw uds crosswalks. |
|year_matches | (int): Number of year matches. Number of year entries exist for each zip code in the original uds crosswalks. This can be an indication of how frequently or consistently the relationship has been noted over time. |
|zcta_matches | (int): Number of zcta matches. This counts the number of distinct zcta values associated with each distinct zip code in the original uds crosswalks. This can be used to determine if a ZIP code has multiple corresponding ZCTAs over different years or editions of the census data.|

## Content

**src**
* [src/create_dir_paths.py](src/create_dir_paths.py) Creates data subfolders and symbolic links if indicated in the [datapaths](conf/datapath) config file.
* [src/download_uds_xwalks.py](src/download_uds_xwalks.py) Downloads uds xwalks from source url's.
* [src/create_clean_uds.py](src/create_clean_uds.py) creates a single clean crosswalk from the raw crosswalks.
* [src/master_xwalk.py](src/master_xwalk.py) applies processing decisions to obtain a single row for each zipcode.
* [src/unique_zcta.py](src/unique_zcta.py) Extracts unique ZCTAs from uds xwalks, maps them to census editions and expands them across years.

**data**
* Input, intermediate and output data placeholders
* [data/metadata.yml](data/metadata.yml) summarizes key description elements for the output dataset. 

**conf**
* Configuration files containing the input arguments utilized in the scripts that make up the pipeline.

**notes**
* [notes/motivation.md](notes/motivation.md) motivation behind creatin a master zip2zcta crosswalk file.
* [notes/eda_clean_uds.ipynb](notes/eda_clean_uds.ipynb) notebook containing examples of discrepancies found in uds raw data.

**utils**
* [utils/](utils/) additional documentation modules.

## Data lineage

Inputs:

1. The input data is downloaded using this script [src/download_uds_xwalk.py](src/download_uds_xwalks.py).
2. No other inputs are required.

## Processing rules 

* **Processing steps executed in [src/create_clean_uds.py](src/create_clean_uds.py)**

1. Utilize the information provided in the configuration file [conf/uds_raw_xwalks/uds_raw_xwalks.yaml](conf/uds_raw_xwalks/uds_raw_xwalks.yaml) to harmonize the uds datasets.
2. Drop duplicates.

* **Processing steps executed in [src/master_xwalk.py](src/master_xwalk.py)**
1. Assign to each zip the zcta that corresponds to the most recent crosswalk.
2. Identify summary characteristics of zip to zcta cross-year matches such as the first year the zipcode is included in a uds crosswalk.

## Open datasets

Output crosswalks can be found on the Harvard Dataverse [https://doi.org/10.7910/DVN/HYNJSZ](https://doi.org/10.7910/DVN/HYNJSZ). To cite with Bibtex use:
```
@data{DVN/HYNJSZ_2024,
author = {Audirac, Michelle},
publisher = {Harvard Dataverse},
title = {{Zip2zcta master xwalk}},
UNF = {UNF:6:pZqmbScz/osTypCKIXPFNQ==},
year = {2024},
version = {V1},
doi = {10.7910/DVN/HYNJSZ},
url = {https://doi.org/10.7910/DVN/HYNJSZ}
}
```

## Run

### Conda Environment

**Clone the repository** Clone the repository and create a conda environment.

```bash
git clone <https://github.com/<user>/repo>
cd <repo>

conda env create -f requirements.yml
conda activate <env_name> #environment name as found in requirements.yml
```

It is also possible to use `mamba`.

```bash
mamba env create -f requirements.yml
mamba activate <env_name>
```

**Link entrypoints to data placeholders** Add symlinks to input, intermediate and output folders inside the corresponding `/data` subfolders.

Run:

```bash
python src/create_dir_paths.py
```

Additional instructions are found in [data/README.md](data/README.md).

**Run scripts** Run the main scripts:

```bash
python src/download_uds_xwalks.py
python src/create_clean_uds.py
python src/master_xwalk.py
python src/unique_zcta.py
```

or **run the pipeline**:

* Modify the configuration inputs on [conf/config.yaml] as necessary

```bash
snakemake --cores 1
```

`cores` determine number of processes that can be executed in parallel. In this pipeline only 1 is needed.

## Dockerized Pipeline

Create the folder where you would like to store the output dataset.

```bash 
mkdir <path>/zip2zcta_master_xwalk/
```

### Pull and Run:

```bash
docker pull nsaph/zip2zcta_master_xwalk
docker run -v <path>/zip2zcta_master_xwalk/:/app/data/output/zip2zcta_master_xwalk nsaph/zip2zcta_master_xwalk
```

If you are interested in storing the input raw and intermediate data run

```bash
docker run -v ./data:/app/data/ nsaph/zip2zcta_master_xwalk
```


**Building the image**

To create your own docker image
```bash
docker build -t <image_name> .
```

For a multiarch built do
```bash
docker buildx build --platform linux/amd64,linux/arm64 -t <image_name> . --push
```
