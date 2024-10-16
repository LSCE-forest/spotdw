import os
from spotdw.scraper_utils import list_available_data, download_file_with_check
import hydra
from omegaconf import DictConfig, OmegaConf
from tqdm import tqdm


@hydra.main(version_base=None, config_path="config", config_name="download_config")
def main(cfg: DictConfig) -> None:
    print(OmegaConf.to_yaml(cfg))

    # save the config next to the data
    OmegaConf.save(cfg, os.path.join(cfg.save_dir, "download_config.yaml"))

    gdf = list_available_data(cfg.base_url, cfg.cookie, year=cfg.year)
    os.makedirs("data", exist_ok=True)

    list_of_failures = []

    for _, row in tqdm(gdf.iterrows(), desc="Download images"):
        try:
            # check if a file is already present on the server
            _ = download_file_with_check(
                row["filename"], row["date"].year, row["source"], cfg.save_dir, cfg.cookie, cfg.api_url
            )
        except Exception as e:
            print(e)
            list_of_failures.append(row["filename"])
            continue

    print(
        f"List of files for which download failed : {list_of_failures}. Relaunch this script if the list is not empty."
    )


if __name__ == "__main__":
    main()
