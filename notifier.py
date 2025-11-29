# notifier.py
import requests
from storage import log_notification
from fetcher import fetch_post_description
from config import WEBHOOK_URL

def post_url(token):
    return f"https://divar.ir/v/{token}"

def build_embed(title, token, diff=None, image_url=None, description=None):
    embed = {
        "title": title,
        "url": post_url(token),
        "color": 0x00ff00,
    }
    if description:
        # Discord description length limit ~ 4096
        embed["description"] = description[:4000]
    if diff:
        text = ""
        for t, items in diff.items():
            for k, v in items.items():
                # present old/new in readable format when possible
                if isinstance(v, dict) and "old_value" in v and "new_value" in v:
                    text += f"**{k}**: `{v['old_value']}` → `{v['new_value']}`\n"
                else:
                    text += f"**{k}**: `{v}`\n"
        if text:
            embed.setdefault("fields", []).append({"name": "Changes", "value": text[:1024]})
    if image_url:
        embed["image"] = {"url": image_url}
    return embed

def send_notification(title, token, diff=None, image_url=None, fetch_description=False):
    description = None
    if fetch_description:
        description = fetch_post_description(token)

    embed = build_embed(title, token, diff=diff, image_url=image_url, description=description)
    payload = {"embeds": [embed]}

    try:
        r = requests.post(WEBHOOK_URL, json=payload, timeout=10)
        ok = r.status_code in (200, 204)
    except Exception:
        ok = False

    # log regardless of success for audit
    log_notification({
        "title": title,
        "token": token,
        "diff": diff,
        "image": image_url,
        "sent": ok
    })
    return ok
