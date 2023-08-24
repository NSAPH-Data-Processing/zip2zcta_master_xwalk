import pandas as pd
import duckdb
import logging

# configure logger to print at info level
logging.basicConfig(level=logging.INFO)
LOGGER = logging.getLogger(__name__)

def main():
    conn = duckdb.connect()

    CE = dict()
    CE['2000'] = 'ZCTA5CE00'
    CE['2010'] = 'ZCTA5CE10'
    CE['2020'] = 'ZCTA5CE20'


    LOGGER.info("""
        ## Assigning each zip the zcta that corresponds to the most recent crosswalk ----
        """)
    df = conn.execute(
        """
            WITH zi AS (
                SELECT 
                    zip, 
                    MAX(year) AS year,
                FROM 
                    'data/intermediate/uds_clean_xwalk/uds_clean_xwalk.csv'
                GROUP BY
                    zip
            )
            SELECT 
                zi.zip,
                zc.zcta,
                zi.year,
                zc.year - (zc.year % 10) AS census_edition, 
                state, is_area, is_self_mapped, is_post_office, info
            FROM
                zi
            LEFT JOIN 
                'data/intermediate/uds_clean_xwalk/uds_clean_xwalk.csv' AS zc
            ON
                zi.zip = zc.zip AND zi.year = zc.year
            ORDER BY
                zi.zip
        """).fetchdf()
    df.rename(columns={'year': 'year_match'}, inplace=True)
    df['census_edition'] = df['census_edition'].astype(str)
    df['census_edition'] = df.census_edition.apply(lambda x: CE[x])
    LOGGER.info(f"Number of unique zipcodes {len(df.zip)}")
    LOGGER.info(f"Processed zcta assignment head: \n{df.head()}")

    LOGGER.info("""
        ## Identifying zip to zcta year matches ----
        """)
    df_zip = conn.execute(
        """
            SELECT 
                zip,
                MIN(year) AS min_match,
                MAX(year) AS max_match,
                COUNT(year) AS year_matches
            FROM 
                'data/intermediate/uds_clean_xwalk/uds_clean_xwalk.csv'
            GROUP BY
                zip
        """).fetchdf()
    LOGGER.info(f"Number of unique zipcodes {len(df_zip.zip)}")
    LOGGER.info(f"Processed year matches head: \n{df_zip.head()}")
    
    LOGGER.info("""
        ## Identifying zip to zcta matches ----
        """)
    df_zcta = conn.execute(
        """
            WITH z AS(
                SELECT DISTINCT zip, zcta
                FROM
                'data/intermediate/uds_clean_xwalk/uds_clean_xwalk.csv'
            )
            SELECT
                zip,
                COUNT(zcta) AS zcta_matches
            FROM z
            GROUP BY
                zip
        """).fetchdf()
    LOGGER.info(f"Number of unique zipcodes {len(df_zcta.zip)}")
    LOGGER.info(f"Processed zcta matches head: \n{df_zcta.head()}")
    
    LOGGER.info("""
        ## Merging ----
        """)
    df = pd.merge(df, df_zip, on='zip', how='left')
    df = pd.merge(df, df_zcta, on='zip', how='left')
    LOGGER.info(f"Number of unique zipcodes {len(df.zip)}")
    LOGGER.info(f"Processed merge head: \n{df.head()}")

    LOGGER.info("""
        ## Saving ----
        """)
    df.to_csv("data/output/zip2zcta_master_xwalk/zip2zcta_master_xwalk.csv", index=False)

if __name__ == "__main__":
    main()
