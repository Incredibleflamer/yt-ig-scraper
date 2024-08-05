from utils.youtube import youtube_watch, youtube_reels
from utils.instagram import fetch_instagram_post_data
import sys

# talking input
print("""\033[38;5;32m
┌───────────────────────────────────────┐
│                                       │
│        Instagram (Post & Reel)        │
│        \033[38;5;196mYouTube (Shorts & Video)       │
│              Scraper                  │
│                                       │
└───────────────────────────────────────┘
""")

url = input("\033[38;5;159mEnter Link To Scrape : ")

print("\033[0m")

def print_data(data):
    for key, value in data.items():
        if isinstance(value, list):
            print(f"{key} :")
            for item in value:
                print(f"\n{item}")
        else:
            print(f"{key} : {value}\n")
    sys.exit(0)
        


# youtube
if "youtube" in url:
# video?
  if url.startswith("https://www.youtube.com/watch?v="):
    try:
      results = youtube_watch(url)
      print_data(results)
    except Exception as e:
      print(e)
# shorts
  elif url.startswith("https://www.youtube.com/shorts/"):
    try:
      results = youtube_reels(url)
      print_data(results)
    except Exception as e:
      print(e)

# instagram
elif "instagram" in url:
# post?
  if "/p/" in url:
    postcode = url.split("/p/")[1].replace("/", "")
    if len(postcode) != 0:
      data = fetch_instagram_post_data(postcode)
      print_data(data)
# reel?
  elif "reel" in url:
    reelcode = url.split("/reel/")[1].replace("/", "")
    if len(reelcode) != 0:
      data = fetch_instagram_post_data(reelcode)
      print_data(data)

print("Not A Valid Url")