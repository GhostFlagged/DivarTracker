# main.py
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from config import PAGE_START, PAGE_END, SCAN_INTERVAL, KEYWORDS, THREAD_COUNT
from fetcher import fetch_pages
from post_parser import extract_posts_from_page
from storage import load_posts, save_posts
from diff_util import compute_diff
from notifier import send_notification

def post_matches_keywords(post, keywords):
    if not keywords:
        return True
    # Use the description instead of title
    text = post.get('description', '')  # assuming your post dict has a 'description' key
    text = text.lower()
    for kw in keywords:
        if kw.lower() in text:
            return True
    return False


def scan_once():
    pages = list(range(PAGE_START, PAGE_END))
    responses = fetch_pages(pages)

    current = {}
    for page_json in responses.values():
        posts = extract_posts_from_page(page_json)
        current.update(posts)
    return current

def main():
    print("Divar Monitor started")

    first_run = True
    stored = load_posts()

    while True:
        print("\n--- Scanning pages... ---")
        current = scan_once()

        added = set(current.keys()) - set(stored.keys())
        common = set(current.keys()) & set(stored.keys())

        sent_count = 0

        # Handle added
        for token in sorted(added):
            post = current[token]
            if not post_matches_keywords(post, KEYWORDS):
                continue
            if not first_run:
                ok = send_notification(f"🆕 New: {post.get('title','No Title')}", token,
                                       diff=None, image_url=post.get("image"),
                                       fetch_description=True)
                if ok:
                    sent_count += 1

        # Handle updated (compute meaningful diffs)
        for token in sorted(common):
            old = stored[token]
            new = current[token]
            # compare selected fields (title, price, location, status)
            old_comp = {
                "title": old.get("title"),
                "price": old.get("price"),
                "location": old.get("location")
            }
            new_comp = {
                "title": new.get("title"),
                "price": new.get("price"),
                "location": new.get("location")
            }
            diff = compute_diff(old_comp, new_comp)
            if diff:
                if not post_matches_keywords(new, KEYWORDS):
                    continue
                if not first_run:
                    ok = send_notification(f"✏️ Updated: {new.get('title','No Title')}", token,
                                           diff=diff, image_url=new.get("image"),
                                           fetch_description=True)
                    if ok:
                        sent_count += 1

        # Save current state (overwrite)
        save_posts(current)
        stored = current
        first_run = False

        print(f"Sent {sent_count} notifications this scan.")
        print(f"Sleeping for {SCAN_INTERVAL} seconds...")
        time.sleep(SCAN_INTERVAL)

if __name__ == "__main__":
    main()
