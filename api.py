from flask import Flask, render_template, request
from utils.youtube import youtube_watch, youtube_reels
from utils.instagram import fetch_instagram_post_data

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/scrape', methods=['POST'])
def scrape():
    url = request.form['url']
    data = {}
    
    try:
        if "youtube" in url:
            if url.startswith("https://www.youtube.com/watch?v="):
                data = youtube_watch(url)
            elif url.startswith("https://www.youtube.com/shorts/"):
                data = youtube_reels(url)

        elif "instagram" in url:
            if "/p/" in url:
                postcode = url.split("/p/")[1].replace("/", "")
                data = fetch_instagram_post_data(postcode)
            elif "reel" in url:
                reelcode = url.split("/reel/")[1].replace("/", "")
                data = fetch_instagram_post_data(reelcode)
        if not data:
            return "Not a valid URL", 400

        return render_template('results.html', data=data)

    except Exception as e:
        return f"Error: {str(e)}", 500

if __name__ == "__main__":
    app.run(debug=True)
