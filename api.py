from flask import Flask, render_template, request , send_file
from utils.youtube import youtube_watch, youtube_reels
from utils.instagram import fetch_instagram_post_data
from utils.flipkart import flipkart_search
from utils.database import add_data , check_query_exists , get_query , database
import requests
from io import BytesIO

app = Flask(__name__)

@app.route('/')
def home():
    data = database()
    return render_template('search.html', data=data)


@app.route('/scrape', methods=['POST'])
def scrape():
    url = request.form['url']
    platform_type = ""
    data = None
    
    try:
        # youtube
        if "youtube" in url:
            # check in db
            if check_query_exists(url):
                data = get_query(url)
                platform_type = "youtube"
            elif url.startswith("https://www.youtube.com/watch?v="):
                data = youtube_watch(url)
                platform_type = "youtube"
                add_data(url, data)
            elif url.startswith("https://www.youtube.com/shorts/"):
                data = youtube_reels(url)
                platform_type = "youtube"
                add_data(url, data)
        # instagram
        elif "instagram" in url:
            InstagramPostID = None
            if "/p/" in url:
                platform_type = "instagram_post"
                InstagramPostID = url.split("/p/")[1].replace("/", "")
            elif "reel" in url:
                platform_type = "instagram_reel"
                InstagramPostID = url.split("/reel/")[1].replace("/", "")
             
            if InstagramPostID is None:
                return "Not a valid URL", 400
            
            # checking in db
            if check_query_exists(url):
                data = get_query(url)
            else: 
                data = fetch_instagram_post_data(InstagramPostID)
                add_data(url,data)
        elif not url.startswith("http"):
            if check_query_exists(url):
                data = get_query(url)
                platform_type = "flipkart"
            else:
                data = flipkart_search(url)
                if data is not None:
                    platform_type = "flipkart"
                    add_data(url, data)
                
             

        # data is none
        if data is None:
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
