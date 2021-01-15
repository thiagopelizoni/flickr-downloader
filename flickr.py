import sys
import shutil
import requests
import re
import time

def download(url):
    url = url.replace("\n", "").strip()
    img_url = get_image_url(url).decode("utf-8").replace("\\", "")
    img_url = f"https://{img_url}"

    response = requests.get(img_url, stream=True)

    if response.status_code != 200:
        sys.exit(f"Error when accessing {response.url} - status code: {response.status_code}")

    timestamp = int(time.time())
    file_name = f"{timestamp}.jpg"

    with open(file_name, 'wb') as image:
        shutil.copyfileobj(response.raw, image)

    if shutil.os.path.exists(file_name):
        print(f"{img_url} downloaded as {file_name}")

"""
Return a link to download an image even when its original is not available for it

When original is not available
* Given URL: https://www.flickr.com/photos/vid_pogacnik/48451363657
* Returned image URL: live.staticflickr.com\\/65535\\/48451363657_6f16fda6f1_b.jpg

When original is able to be downloaded
* Given URL: https://www.flickr.com/photos/lonesomecrow/50288624778/
* Returned image URL: live.staticflickr.com\\/65535\\/50288624778_74e906e739_o.jpg
"""
def get_image_url(url):
    url = url.replace("\n", "").strip()
    response = requests.get(url)

    if response.status_code != 200:
        sys.exit(f"Error when accessing {response.url} - status code: {response.status_code}")

    img_urls = re.findall(b'live\.staticflickr\.com\\\\\/.+?\.[a-z]{3}', response.content)
    for img in img_urls:
        has_original = re.findall(b'.*?_o\.[a-z]{3}', img)
        if has_original:
            return has_original[0]
    # In case of original download is not available return best image size
    return img_urls[-1]

"""
How to use
==========

Command line
=============

If you wanna call if in a command line, just run:

python3 flickr.py "https://www.flickr.com/photos/lonesomecrow/50288624778/"

Python script
============
import flickr
flickr.download("https://www.flickr.com/photos/lonesomecrow/50288624778/")
"""
def main():
    url = sys.argv[1]
    if not url:
        sys.exit("Enter a valid Flickr URL!")
    download(url)

if __name__ == "__main__":
    main()
