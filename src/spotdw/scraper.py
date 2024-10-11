import os
import shutil
import pandas as pd
import geopandas as gpd
from shapely.geometry import shape
import json
import requests


def list_available_data(base_url, cookie, years=[2021]):
    all_data = []
    for year in years:
        year = str(year)
        for source in ["MS", "PAN"]:
            url = base_url.replace("YEAR", year).replace("SOURCE", source)
            r = json.loads(requests.get(url, cookies={"session": cookie}).content)
            for elt in r["features"]:
                filename = elt["properties"]["f_quicklook"]
                filename = "IMG_" + "_".join(filename.split("_")[1:]).replace(".JPG", "_R1C1.TIF")
                df = {
                    "filename": filename,
                    "date": pd.to_datetime(filename.split("_")[2][:8]),
                    "geometry": shape(elt["geometry"]),
                    "source": source,
                }
                all_data.append(df)

    all_data = gpd.GeoDataFrame(all_data)
    return all_data


def download_image(filename, year, source, save_dir, cookie, api_url):
    folder_path = os.path.join(save_dir, "spot_" + str(year) + "_" + source.lower())
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)

    if os.path.exists(os.path.join(folder_path, filename)):
        print(f"File {filename} already exists")
        return None

    with requests.get(os.path.join(api_url, filename), cookies={"session": cookie}, stream=True) as r:
        print(f" filename : {os.path.join(folder_path, filename)}, response : {r}")

        with open(os.path.join(folder_path, filename), "wb") as f:
            shutil.copyfileobj(r.raw, f)
