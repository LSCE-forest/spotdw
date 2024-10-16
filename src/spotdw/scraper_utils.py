import os
import shutil
import pandas as pd
import geopandas as gpd
from shapely.geometry import shape
import json
import requests
from retry import retry


def list_available_data(base_url, cookie, year=2021):
    all_data = []
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


class DownloadError(Exception):
    pass


@retry(exceptions=DownloadError, delay=1, tries=10)
def download_file_with_check(filename, year, source, save_dir, cookie, api_url):
    try:
        dest_folder_path = os.path.join(save_dir, "spot_" + str(year) + "_" + source.lower())
        if not os.path.exists(dest_folder_path):
            os.makedirs(dest_folder_path)
        dest_path = os.path.join(dest_folder_path, filename)

        # Check if the file has already been downloaded by checking
        # if it is already present with the same size
        url = os.path.join(api_url, filename)

        # Get remote file size
        remote_size = get_file_size(url, cookie=cookie)["bytes"]

        if remote_size is None:
            print("Cannot determine remote file size. Proceeding with download.")
            need_download = True
        else:
            if os.path.exists(dest_path):
                # Get local file size
                local_size = os.path.getsize(dest_path)
                print(f"Local file size: {local_size} bytes")
                print(f"Remote file size: {remote_size} bytes")

                if local_size == remote_size:
                    print("File already exists and sizes match. Skipping download.")
                    need_download = False
                else:
                    print("File exists but sizes differ. Re-downloading.")
                    need_download = True
            else:
                print("File does not exist locally. Downloading.")
                need_download = True

        # Download the file if needed
        if need_download:
            with requests.get(url, cookies={"session": cookie}, stream=True) as r:
                print(f" filename : {dest_path}, response : {r}")

                with open(dest_path, "wb") as f:
                    shutil.copyfileobj(r.raw, f)

            # Check download succeeded:
            if os.path.getsize(dest_path) != remote_size:
                raise RuntimeError(f"Could not properly download {filename}")
    except Exception as e:
        raise DownloadError(e)


def get_file_size(url, cookie=None):
    try:
        # Send a HEAD request to get headers
        response = requests.head(url, allow_redirects=True, cookies={"session": cookie})

        # Check if the request was successful
        if response.status_code == 200:
            # Extract the 'Content-Length' header
            content_length = response.headers.get("Content-Length")

            if content_length is None:
                print("Content-Length header is not provided by the server.")
                return None

            # Convert to integer (bytes)
            size_in_bytes = int(content_length)

            # Optionally, convert to more readable formats
            size_mb = size_in_bytes / (1024 * 1024)
            size_gb = size_in_bytes / (1024 * 1024 * 1024)

            return {"bytes": size_in_bytes, "megabytes": size_mb, "gigabytes": size_gb}
        else:
            print(f"HEAD request failed with status code: {response.status_code}")
            return None
    except requests.RequestException as e:
        print(f"An error occurred: {e}")
        return None
