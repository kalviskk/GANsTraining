import requests
import random
import os
from PIL import Image
import io
import math
import numpy as np

'''
Šī programma nestrādās, jo esmu noņēmis savu API token
'''

# Your Mapbox access 
access_token = "token" # savu nelikšu jo tā jau nejauši pārtērēju limitu un esmu viņiem parādā

# custom roadmap stils bez liekās informācijas
street_id = 'kkalvis/cloott2z200hu01pr0pghdnnr'

locations = np.load('prevLocs2.npy')
zoom_level = 16
width = 256
height = 256
# Separate folders for roadmap and satellite images
roadmap_dir = r'mapbox_images2\roadmap'
satellite_dir = r'mapbox_images2\satellite'
download_log_file = 'download_log2.txt'
np.random.seed(13)
np.random.shuffle(locations)
#%%

num_random_locations = 10000  

# Pick the first 'num_random_locations' after shuffling
selected_locations = locations[:num_random_locations]
# Load the download log
if os.path.exists(download_log_file):
    with open(download_log_file, 'r') as file:
        downloaded = set(file.read().splitlines())
else:
    downloaded = set()

def fetch_and_save_image(url, folder, filename):
    if filename in downloaded:
        print(f"Already downloaded {filename}")
        return  # skip
    response = requests.get(url)
    if response.status_code == 200:
        image = Image.open(io.BytesIO(response.content))
        if image.mode in ('RGBA', 'LA', 'P'):
            image = image.convert('RGB')
        image_path = os.path.join(folder, f"{filename}.jpg")
        image.save(image_path, 'JPEG')
        with open(download_log_file, 'a') as file:
            file.write(filename + '\n')
        
    else:
        print(f"Failed to retrieve image. Status code: {response.status_code}")

def generate_image_urls(location, zoom_level, width, height, access_token, street_id):
    location_formatted = location.replace(',', '_').replace('.', '_')
    roadmap_url = f'https://api.mapbox.com/styles/v1/{street_id}/static/{location},{zoom_level},0/{width}x{height}@2x?access_token={access_token}'
    satellite_url = f'https://api.mapbox.com/styles/v1/mapbox/satellite-v9/static/{location},{zoom_level},0/{width}x{height}@2x?access_token={access_token}'

    return roadmap_url, satellite_url, location_formatted

# Fetchojam un saglabājam attēlus
n = 0
for loc in locations:
    n+=1
    if n >= num_random_locations:
        break
    
    lat, lon = loc
    location = f"{lon},{lat}"
    roadmap_url, satellite_url, location_formatted = generate_image_urls(location, zoom_level, width, height, access_token, street_id)
    fetch_and_save_image(roadmap_url, roadmap_dir, f'roadmap_{location_formatted}')
    fetch_and_save_image(satellite_url, satellite_dir, f'satellite_{location_formatted}')