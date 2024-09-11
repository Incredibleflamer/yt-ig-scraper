from flask import Flask, render_template, request , send_file
from utils.youtube import youtube_watch, youtube_reels
from utils.instagram import fetch_instagram_post_data
import requests
from io import BytesIO

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/scrape', methods=['POST'])
def scrape():
    url = request.form['url']
    platform_type = ""
    data = {}
    
    try:
        if "youtube" in url:
            if url.startswith("https://www.youtube.com/watch?v="):
                data = youtube_watch(url)
                platform_type = "youtube"
            elif url.startswith("https://www.youtube.com/shorts/"):
                data = youtube_reels(url)
                platform_type = "youtube"

        elif "instagram" in url:
            if "/p/" in url:
                postcode = url.split("/p/")[1].replace("/", "")
                data = fetch_instagram_post_data(postcode)
                platform_type = "instagram_post"
            elif "reel" in url:
                reelcode = url.split("/reel/")[1].replace("/", "")
                data = fetch_instagram_post_data(reelcode)
                platform_type = "instagram_reel"
        if not data:
            return "Not a valid URL", 400

        return render_template('results.html', platform_type=platform_type , data=data)

    except Exception as e:
        return f"Error: {str(e)}", 500

@app.route('/proxy-image')
def proxy_image():
    image_url = request.args.get('url')
    response = requests.get(image_url)
    return send_file(BytesIO(response.content), mimetype='image/jpeg')


if __name__ == "__main__":
    app.run(debug=True)
