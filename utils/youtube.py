import json , re , requests
from bs4 import BeautifulSoup as bs

headers = {'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.135 Safari/537.36 Edge/12.246"}

def youtube_watch(url):
    response = requests.get(url, headers=headers)    
    soup = bs(response.content, 'lxml')
    
    script_tags = soup.find_all('script')
    
    VideoDetails = None
    VideoDetails2 = None
    
    for script in script_tags:
        if script.string is not None:
            if 'ytInitialPlayerResponse' in script.string:
                match = re.search(r'ytInitialPlayerResponse\s*=\s*({.*?});', script.string)
                if match:
                    json_str = match.group(1)
                    try:
                        VideoDetails = json.loads(json_str)["videoDetails"]
                    except KeyError as e:
                        print(e)
                        raise Exception("Video Not Found")
            
            if 'ytInitialData' in script.string:
                match = re.search(r'ytInitialData\s*=\s*({.*?});', script.string)
                if match:
                    json_str = match.group(1)
                    try:
                        VideoDetails2 = json.loads(json_str)["contents"]["twoColumnWatchNextResults"]["results"]["results"]["contents"]
                    except KeyError as e:
                        print(e)
                        raise Exception("Video Not Found")
            
            if VideoDetails is not None and VideoDetails2 is not None:
                break
            
    if VideoDetails is None or VideoDetails2 is None:
        raise Exception("Video Not Found")
    
    
    # thumbnails
    thumbnails = VideoDetails.get('thumbnail', {}).get("thumbnails", [{}])
    hqthumbnails = thumbnails[len(thumbnails) - 1].get("url", 'Not available')
    
    # Title
    title = VideoDetails.get('title', 'Not available')
    
    #Likes
    likes = VideoDetails2[0].get("videoPrimaryInfoRenderer", {}).get("videoActions", {}).get("menuRenderer", {}).get("topLevelButtons", {})[0].get("segmentedLikeDislikeButtonViewModel", {}).get("likeButtonViewModel", {}).get("likeButtonViewModel", {}).get("toggleButtonViewModel", {}).get("toggleButtonViewModel", {}).get("defaultButtonViewModel", {}).get("buttonViewModel", {}).get("title", "Not available")
    
    # Views
    Views = VideoDetails.get('viewCount', 'Not available')
    
    # channel name
    channel_name = VideoDetails.get('author', 'Not available')
    
    # subs
    Subs = VideoDetails2[1].get('videoSecondaryInfoRenderer', {}).get('owner', {}).get('videoOwnerRenderer', {}).get('subscriberCountText', {}).get('accessibility', {}).get('accessibilityData', {}).get('label', 'Not available')
    
    # keywords
    keywords =  VideoDetails.get('keywords', 'Not available')
    
    # upload date
    upload_date = VideoDetails2[0].get('videoPrimaryInfoRenderer', {}).get('dateText', {}).get('simpleText', 'Not available')
    
    # description 
    description = VideoDetails.get('shortDescription', 'Not available')
    
    
    video_details = {  
            "Thumbnail": hqthumbnails,
            "Title": title,
            "Likes": likes,
            "Views": Views,
            "Channel Name": channel_name,
            "Subscribers": Subs,
            "Keywords": keywords,
            "Date Uploaded": upload_date,
            "Description": description,
        }

    return video_details
        
def youtube_reels(url):
    response = requests.get(url, headers=headers)  
    soup = bs(response.content, 'lxml')
    script_tags = soup.find_all('script')
    VideoDetails = None
    VideoDetails2 = None
    for script in script_tags:
        if script.string is not None:
            if 'ytInitialPlayerResponse' in script.string:
                match = re.search(r'ytInitialPlayerResponse\s*=\s*({.*?});', script.string)
                if match:
                    json_str = match.group(1)
                    try:
                        VideoDetails = json.loads(json_str)["videoDetails"]
                    except KeyError as e:
                        raise Exception("Video Not Found")
            
            if 'ytInitialData' in script.string:
                match = re.search(r'ytInitialData\s*=\s*({.*?});', script.string)
                if match:
                    json_str = match.group(1)
                    try:
                        VideoDetails2 = json.loads(json_str)["engagementPanels"][1]["engagementPanelSectionListRenderer"]["content"]["structuredDescriptionContentRenderer"]["items"][0]["videoDescriptionHeaderRenderer"]
                        
                    except KeyError as e:
                        raise Exception("Video Not Found")
            
            if VideoDetails is not None and VideoDetails2 is not None:
                break
            
    if VideoDetails is None and VideoDetails2 is None:
        raise Exception("Video Not Found")
    
    # Thumbnail
    Thumbnails = VideoDetails.get('thumbnail', {}).get("thumbnails", [{}])
    Thumbnail = Thumbnails[len(Thumbnails) - 1].get("url", 'Not available')
    
    # Title
    Title = VideoDetails.get('title', 'Not available')
    
    # Likes
    Likes = VideoDetails2.get("factoid", {})[0].get("factoidRenderer", {}).get("accessibilityText", "Not available")
    
    # Views
    Views = VideoDetails2.get('views', {}).get('simpleText', 'Not available')
    
    # Channel Name
    Channel_Name = VideoDetails.get('author', 'Not available')
    
    # upload date
    upload_date = VideoDetails2.get('publishDate', {}).get('simpleText', 'Not available')
    
    # Description
    description = VideoDetails.get('shortDescription', 'Not available')
    
    
    video_details = {
            "Thumbnail": Thumbnail,
            "Title": Title,
            "Likes": Likes,
            "Views": Views,
            "Channel Name": Channel_Name,
            "Date Uploaded": upload_date,
            "Description": description,
        }
    return video_details
        