import shutil
import argparse

def main(args):
    # Copy the metadata.yml file to the output folder ----
    shutil.copy(args.metadata_yaml, args.output_path)
    
if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--metadata_yaml',
        default='./data/metadata/metadata.yml'),
    parser.add_argument(
        '--output_path',
        type=str,
        default='./data/output/zip2zcta_master_xwalk')
    args = parser.parse_args()
    main(args)
