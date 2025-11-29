from fetcher import fetch_post_description

def extract_posts(data):
    posts = {}
    widgets = data.get("list_widgets", [])
    for w in widgets:
        if w.get("widget_type") == "POST_ROW":
            token = w["data"].get("token")
            if token:
                posts[token] = w["data"]
    return posts

def extract_important_fields(p):
    return {
        "title": p.get("title"),
        "price": p.get("middle_description_text"),
        "location": p.get("bottom_description_text"),
        "status": p.get("red_text"),
        "image_url": p.get("image_url")
    }

# post_parser.py
def extract_posts_from_page(api_search_response):
    """
    Convert a search response JSON into dict[token] -> post_data (minimal fields)
    """
    posts = {}
    if not api_search_response:
        return posts

    # Different possible shapes; prefer 'widget_list' / 'list_widgets' etc.
    # The search v8 endpoint often returns 'widget_list' or 'list_widgets' or 'post_list'
    # We'll attempt multiple keys that Divar uses.
    # 1) try list_widgets (POST_ROW)
    lw = api_search_response.get("list_widgets") or api_search_response.get("widget_list")
    if isinstance(lw, list):
        for widget in lw:
            if widget.get("widget_type") == "POST_ROW":
                data = widget.get("data", {})
                token = data.get("token") or data.get("post_token")
                if not token:
                    continue
                posts[token] = {
                    "token": token,
                    "title": data.get("title") or "",
                    "image": data.get("image_url") or data.get("image") and data["image"].get("url"),
                    "price": data.get("middle_description_text"),
                    "location": data.get("bottom_description_text"),
                    "raw": data
                }
        return posts

    # 2) fallback: 'post_list' with list of posts
    pl = api_search_response.get("post_list") or api_search_response.get("posts")
    if isinstance(pl, list):
        for p in pl:
            token = p.get("token")
            if not token:
                continue
            posts[token] = {
                "token": token,
                "title": p.get("title") or "",
                "image": (p.get("image") or {}).get("url") if isinstance(p.get("image"), dict) else p.get("image"),
                "price": p.get("middle_description_text"),
                "location": p.get("bottom_description_text"),
                "raw": p
            }
    return posts

def extract_posts_from_page(page_json):
    posts = {}
    for widget in page_json.get("list_widgets", []):
        if widget.get("widget_type") == "POST_ROW":
            data = widget.get("data", {})
            token = data.get("token")
            if token:
                posts[token] = {
                    "title": data.get("title", ""),
                    "price": data.get("middle_description_text", ""),
                    "location": data.get("bottom_description_text", ""),
                    "image": data.get("image_url", ""),
                    # Fetch description for storage
                    "description": fetch_post_description(token)
                }
    return posts