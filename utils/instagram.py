import requests

def fetch_instagram_post_data(post_code):
    url = "https://www.instagram.com/graphql/query"
    
    headers = {
        "accept": "*/*",
        "accept-language": "en-US,en;q=0.9",
        "content-type": "application/x-www-form-urlencoded",
        "priority": "u=1, i",
        "sec-ch-prefers-color-scheme": "dark",
        "sec-ch-ua": '"Not)A;Brand";v="99", "Google Chrome";v="127", "Chromium";v="127"',
        "sec-ch-ua-full-version-list": '"Not)A;Brand";v="99.0.0.0", "Google Chrome";v="127.0.6533.73", "Chromium";v="127.0.6533.73"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-model": '""',
        "sec-ch-ua-platform": '"Windows"',
        "sec-ch-ua-platform-version": '"10.0.0"',
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-origin",
        "x-asbd-id": "129477",
        "x-bloks-version-id": "165b590a165c34e5a3bc20fc9f898b42f79ec60dd01e449dbee3ed8558d41987",
        "x-csrftoken": "sNfrgwZ3sCbPgG-IiBC4nv",
        "x-fb-friendly-name": "PolarisPostActionLoadPostQueryQuery",
        "x-fb-lsd": "AVqzLxmyVdo",
        "x-ig-app-id": "936619743392459",
        "cookie": "csrftoken=sNfrgwZ3sCbPgG-IiBC4nv; dpr=1.25; mid=ZqYyRAALAAGhaxvJntaEymJYdKcW; ig_did=F7083790-056D-4DC3-9C34-855D7645328B; ig_nrcb=1; datr=QzKmZs8stmyMi05_jYXsAwQ6; wd=982x695",
        "Referer": f"https://www.instagram.com/p/{post_code}",
        "Referrer-Policy": "strict-origin-when-cross-origin"
    }
    
    body = (
        f"av=0&__d=www&__user=0&__a=1&__req=3&__hs=19932.HYP%3Ainstagram_web_pkg.2.1..0.0"
        f"&dpr=1&__ccg=UNKNOWN&__rev=1015209738&__s=pt63fp%3A5g5vx1%3Awiezka"
        f"&__hsi=7396654748830316011&__dyn=7xeUjG1mxu1syUbFp41twpUnwgU7SbzEdF8aUco2qwJw5ux609vCwjE1xoswaq0yE6ucw5Mx62G5UswoEcE7O2l0Fwqo31w9O1TwQzXwae4UaEW2G0AEco5G0zK5o4q3y1Sx-0iS2Sq2-azo7u3C2u2J0bS1LwTwKG1pg2fwxyo6O1FwlEcUed6goK2O4UrAwCAxW6Uf9EO2e2e1ew"
        f"&__csr=h42ezsheh6ibGihnhnVAXGD_niApaBihahpAUXJ3rhoy9KvhpUCurXFacx2HAzbzqGh6yUSt4AS-9BBjKcizay_Vcxby8hG9V8K5V9uhCByGmq4ayKlx24qK64hxSdByuu49oKmuV8018AHjwYwAzk0OQ0eIwkC1tyo6Gq5yGq1-g1uo0ab6bU7a1aIAMdo755CgBF05LwnZC55gDc0gq3258aiGfiaFwC5-1xzUzCwaKOo66dg0grxe16g4y4U0axE05B2"
        f"&__comet_req=7&lsd=AVqzLxmyVdo&jazoest=21109&__spin_r=1015209738&__spin_b=trunk&__spin_t=1722167886"
        f"&fb_api_caller_class=RelayModern&fb_api_req_friendly_name=PolarisPostActionLoadPostQueryQuery"
        f"&variables=%7B%22shortcode%22%3A%22{post_code}%22%2C%22fetch_comment_count%22%3A40%2C%22parent_comment_count%22%3A24%2C%22child_comment_count%22%3A3%2C%22fetch_like_count%22%3A10%2C%22fetch_tagged_user_count%22%3Anull%2C%22fetch_preview_comment_count%22%3A2%2C%22has_threaded_comments%22%3Atrue%2C%22hoisted_comment_id%22%3Anull%2C%22hoisted_reply_id%22%3Anull%7D"
        f"&server_timestamps=true&doc_id=25531498899829322"
    )
    
    response = requests.post(url, headers=headers, data=body)
    data = response.json()
    
    rawdata = data.get("data", {}).get("xdt_shortcode_media", "Not Found")
    
    if rawdata == "Not Found":
        return None
     
    # post data
    caption = rawdata.get("edge_media_to_caption", {}).get("edges", {})[0].get("node", {}).get("text", "Not Found")
    likes = rawdata.get("edge_media_preview_like", {}).get("count", "Not Found")
    comment_count = rawdata.get("edge_media_to_parent_comment", {}).get("count", "Not Found")
    
    # extracting comments
    comments = []
    rawcomments = rawdata.get("edge_media_to_parent_comment", {}).get("edges", {})
    
    for link in rawcomments:
        comment = link.get("node", {})
        
        if not comment:
            continue
        
        comments.append(
        f"Text: {comment.get('text', "Not Found")}\n"
        f"User PFP: {comment.get("owner", {}).get('profile_pic_url', "Not Found")}\n"
        f"Username: {comment.get("owner", {}).get("username", "Not Found")}\n"
        f"Likes: {comment.get("edge_liked_by", {}).get("count", 0)}"
    )
        
    # owner info
    ownername = rawdata.get("owner", {}).get("username" , "Not Found")
    ownerfullname = rawdata.get("owner", {}).get("full_name", "Not Found")
    ownerpfp = rawdata.get("owner", {}).get("profile_pic_url", "Not Found")
    ownerposts = rawdata.get("owner", {}).get("edge_owner_to_timeline_media", {}).get("count", 0)
    ownerfollowers = rawdata.get("owner", {}).get("edge_followed_by", {}).get("count", 0)
    
    # video or image?
    is_video = rawdata.get("is_video", "Not Found")
    if is_video:
        video_url = rawdata.get("video_url", "Not Found")
        display_url = rawdata.get("display_url", "Not Found")
        video_play_count = rawdata.get("video_play_count", "Not Found")
        return {
            "caption": caption,
            "likes": likes,
            "video_play_count": video_play_count,
            "video_url": video_url,
            "display_url": display_url,
            "ownername": ownername,
            "ownerfullname": ownerfullname,
            "ownerpfp": ownerpfp,
            "ownerposts": ownerposts,
            "ownerfollowers": ownerfollowers,
            "comment_count": comment_count,
            "comments": comments
            }
    else:
        Raw_Images = rawdata.get("display_resources", {})
        image_links = []
        for link in Raw_Images:
            image_links.append(link["src"])
        
        return {
            "caption": caption,
            "likes": likes,
            "image_links": image_links,
            "ownername": ownername,
            "ownerfullname": ownerfullname,
            "ownerpfp": ownerpfp,
            "ownerposts": ownerposts,
            "ownerfollowers": ownerfollowers,
            "comment_count": comment_count,
            "comments": comments
            }
