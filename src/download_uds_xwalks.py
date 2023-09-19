import pandas as pd
import requests
import logging
import hydra

LOGGER = logging.getLogger(__name__)

@hydra.main(config_path="../conf", config_name="config", version_base=None)
def main(cfg):
    """
    Download zip to zcta crosswalks from the UDS website and convert to csv.
    """

    # define http headers required so that the download is not rejected
    # headers = {
    #     "User-Agent": (
    #         "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
    #         " AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
    #     )
    # }
    headers = {
        "User-Agent": "curl/7.68.0"
    } 
    
    ## download the raw uds crosswalks which are xlsx files ----
    for year, xwalk_metadata in cfg.uds_raw_xwalks.years.items():

        LOGGER.info(f"Downloading {year} crosswalk")
        
        ## get url ----
        url = xwalk_metadata.url
        
        ## get file extension ----
        ext = url.split(".")[-1] # UDS files are xls or xlsx 

        ## set headers to avoid 403 error ----
        r = requests.get(url, headers=headers)

        # check if the request was successful
        if r.status_code != 200:
            msg = f"Failed to download {year} crosswalk from {url}"
            LOGGER.error(msg)
            raise Exception(msg)
        
        ## write file ----
        xwalk_xls_file = f"data/input/uds_raw_xwalks/uds_xwalk_{year}.{ext}"
        LOGGER.info(f"Writing {year} crosswalk to {xwalk_xls_file}")
        with open(xwalk_xls_file, "wb") as f:
            f.write(r.content)

        ## convert to csv ----
        LOGGER.info(f"Converting {year} crosswalk to csv")
        xwalk_csv_file = f"data/input/uds_raw_xwalks/uds_xwalk_{year}.csv"
        df = pd.read_excel(xwalk_xls_file)
        df.to_csv(xwalk_csv_file, index=False)

if __name__ == "__main__":
    main()
