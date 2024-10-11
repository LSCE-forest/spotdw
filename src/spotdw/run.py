import geopandas as gpd
import os
from shapely.ops import unary_union
from spotdw.scraper import list_available_data, download_image
import hydra
from omegaconf import DictConfig, OmegaConf
from tqdm import tqdm


@hydra.main(version_base=None, config_path="config", config_name="config")
def main(cfg: DictConfig) -> None:
    print(OmegaConf.to_yaml(cfg))

    # save the config next to the data
    OmegaConf.save(cfg, os.path.join(cfg.save_dir, "config.yaml"))

    gdf = list_available_data(cfg.base_url, cfg.cookie, years=cfg.years)
    os.makedirs("data", exist_ok=True)

    for _, row in tqdm(gdf.iterrows(), desc="Download images"):
        try:
            download_image(
                row["filename"], row["date"].year, row["source"], cfg.save_dir, cfg.cookie, cfg.api_url
            )
        except Exception as e:
            print(e)
            # raise ValueError("Cannot download image.")
            continue


# TODO add checks

if __name__ == "__main__":
    main()
