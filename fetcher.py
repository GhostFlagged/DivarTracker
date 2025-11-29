# fetcher.py
import requests
from concurrent.futures import ThreadPoolExecutor, as_completed
from config import DIVAR_URL, HEADERS, CITY_ID, THREAD_COUNT

API_SEARCH = DIVAR_URL
API_POST = "https://api.divar.ir/v8/posts-v2/web/"


def fetch_page(page):
    body = {
        "city_ids": [CITY_ID],
        "source_view": "CATEGORY",
        "pagination_data": {
            "@type": "type.googleapis.com/post_list.PaginationData",
            "page": page,
            "layer_page": 1
        },
        "disable_recommendation": False,
        "search_data": {
            "form_data": {
                "data": {
                    "category": {
                        "str": {"value": ""}
                    }
                }
            }
        },
        "server_payload": {"@type": "type.googleapis.com/widgets.SearchData.ServerPayload"}
    }

    try:
        r = requests.post(API_SEARCH, headers=HEADERS, json=body, timeout=15)
        if r.status_code != 200:
            return page, None

        return page, r.json()

    except Exception:
        return page, None


def fetch_pages(page_numbers):
    results = {}

    with ThreadPoolExecutor(max_workers=THREAD_COUNT) as executor:
        futures = {executor.submit(fetch_page, p): p for p in page_numbers}

        for future in as_completed(futures):
            page = futures[future]
            try:
                pg, data = future.result()
                results[page] = data or {}
            except Exception:
                results[page] = {}

    return results


def fetch_post_description(token):
    """Fetch Divar post details and extract all DESCRIPTION_ROW text."""
    try:
        r = requests.get(API_POST + token, headers=HEADERS, timeout=12)
        if r.status_code != 200:
            return ""
        data = r.json()
        descriptions = []
        for section in data.get("sections", []):
            if section.get("section_name") != "DESCRIPTION":
                continue
            for w in section.get("widgets", []):
                if w.get("widget_type") == "DESCRIPTION_ROW":
                    text = w.get("data", {}).get("text", "").strip()
                    if text:
                        descriptions.append(text)
        return "\n\n".join(descriptions).strip()
    except Exception:
        return ""
