import os
import hydra

@hydra.main(config_path="conf", config_name="config", version_base=None)
def main(cfg):
    """Create data subfolders and symbolic links if indicated in config file."""
    
    for datapath, subfolder_dict in cfg.datapaths.items():
        for subfolder_name, subfolder_link in subfolder_dict.items():
            
            subfolder_path = f"data/{datapath}/{subfolder_name}"

            if subfolder_link is not None:
                os.symlink(subfolder_link, subfolder_path)
            
            else:
                os.makedirs(subfolder_path, exist_ok=True)

if __name__ == "__main__":
    main()
