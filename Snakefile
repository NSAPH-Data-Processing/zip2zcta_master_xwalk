rule all:
    input:
        "data/output/zip2zcta_master_xwalk/zip2zcta_master_xwalk.csv",
        "data/output/zip2zcta_master_xwalk/zip2zcta_master_xwalk.parquet", 
        "data/output/zip2zcta_master_xwalk/unique_zcta.csv",
        "data/output/zip2zcta_master_xwalk/unique_zcta.parquet"

rule download_uds_xwalks:
    output:
        expand("data/input/uds_raw_xwalks/uds_xwalk_{year}.csv", year=range(2009, 2022))
    shell:
        """
        python src/download_uds_xwalks.py
        """

rule create_clean_uds:
    input:
        expand("data/input/uds_raw_xwalks/uds_xwalk_{year}.csv", year=range(2009, 2022))
    output:
        "data/intermediate/uds_clean_xwalk/uds_clean_xwalk.csv"
    shell:
        "python src/create_clean_uds.py"

rule master_xwalk:
    input:
        "data/intermediate/uds_clean_xwalk/uds_clean_xwalk.csv"
    output:
        "data/output/zip2zcta_master_xwalk/zip2zcta_master_xwalk.csv", 
        "data/output/zip2zcta_master_xwalk/zip2zcta_master_xwalk.parquet"
    shell:
        "python src/master_xwalk.py"

rule unique_zcta:
    input:
        "data/intermediate/uds_clean_xwalk/uds_clean_xwalk.csv"
    output:
        "data/output/zip2zcta_master_xwalk/unique_zcta.csv",
        "data/output/zip2zcta_master_xwalk/unique_zcta.parquet"
    shell:
        "python src/unique_zcta.py"
