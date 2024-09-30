import pandas as pd
import duckdb
import logging

# configure logger to print at info level
logging.basicConfig(level=logging.INFO)
LOGGER = logging.getLogger(__name__)

def main():
    conn = duckdb.connect()

    LOGGER.info("""
        ## Extract unique zcta from uds crosswalks per year----
        """)
    
    CE = dict()
    
    CE['2000'] = 'ZCTA5CE00'
    CE['2010'] = 'ZCTA5CE10'
    CE['2020'] = 'ZCTA5CE20'

    df = conn.execute(
        """
        SELECT 
            DISTINCT 
                zcta, 
                year, 
                year - (year % 10) AS census_edition
        FROM
            'data/intermediate/uds_clean_xwalk/uds_clean_xwalk.csv'
        ORDER BY
            zcta, year
        """).fetchdf()

    LOGGER.info(f"Head: {df.head()}")
    LOGGER.info(f"Shape: {df.shape}")
    LOGGER.info(f"Number of unique zcta per year: {df.groupby('year').zcta.nunique()}")

    LOGGER.info("""
        ## Extract unique zcta per census edition ----
    """)

    df = df[['zcta', 'census_edition']].drop_duplicates(subset=['zcta', 'census_edition'], keep='first')
    df.rename(columns={'census_edition': 'year'}, inplace=True)
    df['census_edition'] = df['year'].astype(str)
    df['census_edition'] = df.census_edition.apply(lambda x: CE[x]) 
    LOGGER.info(f"Head: {df.head()}")
    LOGGER.info(f"Shape: {df.shape}")
    LOGGER.info(f"Number of unique zcta per census edition: {df.groupby('census_edition').zcta.nunique()}")

    LOGGER.info("""
        ## Expand all years in a census edition ----
    """)
    query = """
        WITH expanded_years AS (
            SELECT zcta, 
                UNNEST(generate_series(2000, 2009)) AS year, 
                'ZCTA5CE00' AS census_edition
            FROM df WHERE census_edition = 'ZCTA5CE00'
            UNION ALL
            SELECT zcta, 
                UNNEST(generate_series(2010, 2019)) AS year, 
                'ZCTA5CE10' AS census_edition
            FROM df WHERE census_edition = 'ZCTA5CE10'
            UNION ALL
            SELECT zcta, 
                UNNEST(generate_series(2020, 2029)) AS year, 
                'ZCTA5CE20' AS census_edition
            FROM df WHERE census_edition = 'ZCTA5CE20'
        )
        SELECT * FROM expanded_years
        ORDER BY zcta, year
    """
    df = conn.execute(query).fetchdf()
    LOGGER.info(f"Head: {df.head()}")
    LOGGER.info(f"Shape: {df.shape}")
    LOGGER.info(f"Number of unique zcta per year: {df.groupby('year').zcta.nunique()}")
    
    LOGGER.info("""
    ## Saving ----
    """)
    df.to_csv("data/output/zip2zcta_master_xwalk/unique_zcta.csv", index=False)
    df.to_parquet("data/output/zip2zcta_master_xwalk/unique_zcta.parquet", index=False, engine='pyarrow')
 
if __name__ == "__main__":
    main()
