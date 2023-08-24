import pandas as pd
import logging
import hydra

LOGGER = logging.getLogger(__name__)

@hydra.main(config_path="../conf", config_name="config", version_base=None)
def main(cfg):
    """
    Create a clean crosswalk from the raw crosswalks. 
    Disparate column names across years are harmonized.
    Duplicate rows are removed.
    """

    df_list = []
    for year, xwalk_metadata in cfg.uds_raw_xwalks.years.items():
        LOGGER.info(f"## Processing {year} crosswalk ----")
            
        # read crosswalk
        LOGGER.info(f"Read crosswalk")
        df = pd.read_csv(f"data/input/uds_raw_xwalks/uds_xwalk_{year}.csv")
        LOGGER.info(f"Crosswalk data types: \n{df.dtypes}")
            
        # assign xwalk_metadata values to variables
        zip_col = xwalk_metadata.zip_col
        zcta_col = xwalk_metadata.zcta_col
        area_zip_val = xwalk_metadata.area_zip_val
        post_office_zip_val = xwalk_metadata.post_office_zip_val
        state_col = xwalk_metadata.state_col
        #name_cols = xwalk_metadata.name_cols
        zip_type_col = xwalk_metadata.zip_type_col

        # log unique values of the zip type col
        vals = df[zip_type_col].value_counts()
        LOGGER.info(f"Unique of zip type: {vals}")

        # log fraction of zips that don't map to a zcta
        # remove unmapped zips coerce string type in zip and zcta as 05d
        no_zcta_val = getattr(xwalk_metadata, "no_zcta", "")
        unmapped = df[zcta_col].isna() | (df[zcta_col] == no_zcta_val)
        frac_unmapped = unmapped.sum() / len(unmapped)
        df = df[~unmapped]
        df[zip_col] = [f"{int(x):05d}" for x in df[zip_col]]
        df[zcta_col] = [f"{int(x):05d}" for x in df[zcta_col]]
        LOGGER.info(f"Frac of unmapped area zips: {100*frac_unmapped: 0.4f}%")

        # log subset of area zips and post office zips
        is_area = df[zip_type_col] == area_zip_val
        if is_area.sum() == 0:
            msg = f"No area zips found for {year} crosswalk"
            LOGGER.error(msg)
            raise Exception(msg)
        is_post_office = df[zip_type_col] == post_office_zip_val
        frac_area = is_area.sum() / len(is_area)
        frac_post_office = is_post_office.sum() / len(is_post_office)
        LOGGER.info(f"Frac of area zips: {100*frac_area: 0.2f}%")
        LOGGER.info(f"Frac of post office zips: {100*frac_post_office: 0.4f}%")

        # log fraction of zips mapping to themselves
        self_mapped = df[zip_col] == df[zcta_col]
        frac_self_mapped = self_mapped[is_area].sum() / is_area.sum()
        LOGGER.info(f"Frac of self-mapped area zips: {100*frac_self_mapped: 0.4f}%")

        # # make zipcode name by pasting the name vars in the config
        # col = df[name_cols[0]].copy()
        # for name_var in name_cols[1:]:
        #     col = col + ", " + df[name_var]

        # additional info
        if hasattr(xwalk_metadata, "info_col"):
            info = df[xwalk_metadata.info_col]
        else:
            info = ["" for _ in range(len(df))] #list of empty strings

        # store the df in a list
        df_ = pd.DataFrame(
            {
                "zip": df[zip_col],
                "zcta": df[zcta_col],
                "year": year,
                "state": df[state_col],
                #"name": col,
                "is_area": is_area,
                "is_self_mapped": self_mapped,
                "is_post_office": is_post_office,
                "info": info,
            }
        )
        LOGGER.info(f"Processed {year} crosswalk head: \n{df_.head()}")
        df_list.append(df_)

    # combine all years
    outdf = pd.concat(df_list)

    # remove duplicates
    LOGGER.info("## Removing duplicates ----")
    LOGGER.info(f"Shape before removing duplicates: {outdf.shape}")
    outdf.drop_duplicates(inplace=True)
    LOGGER.info(f"Shape after removing duplicates: {outdf.shape}")

    # save the parquet file
    LOGGER.info("## Saving cross-year clean crosswalk ----")
    outdf.to_csv("data/intermediate/uds_clean_xwalk/uds_clean_xwalk.csv", index=False)

if __name__ == "__main__":
    main()
