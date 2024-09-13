# yt-ig-scraper

A Python script for scraping public data from YouTube and Instagram, including likes, comments, and more.

## Features

- Scrapes YouTube video/short metadata such as likes, comments, views, and more.
- Scrapes Instagram posts and reels, including user profiles, captions, likes, comments, and featured comments.

## Installation

1. Clone the repository:
```bash
   git clone https://github.com/your-username/yt-ig-scraper.git
   cd yt-ig-scraper
```

2. Install the required dependencies from requirements.txt
```bash
pip install -r requirements.txt
```

# Usage
## CLI Version
To use the command-line interface (CLI) version of the scraper, run the following command:
```bash
python main.py
```
This will start the CLI version of the scraper, allowing you to scrape data by entering the appropriate URLs for YouTube and Instagram.

## Browser Version
To use the browser-based version, run the following command:
```bash
python api.py
```
This will start a Flask server at http://127.0.0.1:5000/. You can visit this URL in your browser and enter the link to a YouTube video, YouTube short, Instagram post, or Instagram reel. The scraper will then retrieve and display information.

# Notes
This tool scrapes only public data from YouTube and Instagram. It does not access any private or restricted data.
