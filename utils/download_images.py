import pandas as pd
import requests
import os
from PIL import Image
from io import BytesIO
from tqdm import tqdm
from concurrent.futures import ThreadPoolExecutor, as_completed

def download_and_process(row, idx, output_dir, target_size):
    """Download a single image and save it optimized"""
    filename = f"{(idx+1):04d}.jpg"
    output_path = os.path.join(output_dir, filename)

    try:
        response = requests.get(row['photo_image_url'], timeout=10, stream=True)
        if response.status_code == 200:
            img = Image.open(BytesIO(response.content))
            if img.mode in ('RGBA', 'P'):
                img = img.convert('RGB')
            img.thumbnail(target_size, Image.Resampling.LANCZOS)
            img.save(output_path, 'JPEG', quality=85, optimize=True)
            return True
    except Exception:
        return False
    return False

def download_images(num_images=None, output_dir="images", target_size=(800, 800), max_workers=16):
    """
    Download and optimize images from photos.csv in parallel
    """
    os.makedirs(output_dir, exist_ok=True)
    df = pd.read_csv("photos_url.csv")

    if num_images:
        df = df.head(num_images)

    print(f"Downloading {len(df)} images to {output_dir} using {max_workers} workers...")

    results = []
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = {
            executor.submit(download_and_process, row, idx, output_dir, target_size): idx
            for idx, row in df.iterrows()
        }
        for future in tqdm(as_completed(futures), total=len(futures)):
            results.append(future.result())

    print(f"Finished! {sum(results)} images downloaded successfully, {len(df)-sum(results)} failed.")

if __name__ == "__main__":
    download_images(num_images=None, max_workers=16)
