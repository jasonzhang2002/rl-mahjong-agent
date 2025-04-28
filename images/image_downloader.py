import os
import requests

# Folder to save downloaded images
DOWNLOAD_DIR = "mahjong_tiles_png"
os.makedirs(DOWNLOAD_DIR, exist_ok=True)

# Wikimedia API endpoint
API_URL = "https://commons.wikimedia.org/w/api.php"

# Parameters to list files in the category
params = {
    "action": "query",
    "format": "json",
    "list": "categorymembers",
    "cmtitle": "Category:PNG_3D_Mahjong_tiles",
    "cmtype": "file",
    "cmlimit": "500",  # Max limit
}

session = requests.Session()
response = session.get(API_URL, params=params)
data = response.json()

# Go through each file
for file in data["query"]["categorymembers"]:
    title = file["title"]  # Example: 'File:Mahjong_1_of_characters.png'
    if not title.lower().endswith('.png'):
        continue  # Only download PNG files

    # Now get the image URL
    image_info_params = {
        "action": "query",
        "format": "json",
        "titles": title,
        "prop": "imageinfo",
        "iiprop": "url",
    }
    image_info_response = session.get(API_URL, params=image_info_params)
    image_info_data = image_info_response.json()

    pages = image_info_data["query"]["pages"]
    for page_id, page_data in pages.items():
        image_url = page_data["imageinfo"][0]["url"]
        filename = title.replace("File:", "")

        # Download the image
        img_data = session.get(image_url).content
        with open(os.path.join(DOWNLOAD_DIR, filename), 'wb') as handler:
            handler.write(img_data)

        print(f"Downloaded: {filename}")

print("All PNG Mahjong tiles downloaded!")
