# config.py

DIVAR_URL = "https://api.divar.ir/v8/postlist/w/search"

HEADERS = {
    "accept": "application/json",
    "content-type": "application/json",
    "User-Agent": "Mozilla/5.0"
}

CITY_ID = "4"

# Page range
PAGE_START = 1
PAGE_END = 3   # exclusive → means pages 1 to 199

# Scan delay
SCAN_INTERVAL = 60   # seconds

# Discord
WEBHOOK_URL = ""

# Storage
SAVE_FILE = "data/posts.json"
LOG_FILE = "logs/notifications.json"

# Multithreading
THREAD_COUNT = 10

# Keyword filter (empty = match everything)
KEYWORDS = [
    "تلگرام",
    "ایدی تلگرام",
    "آیدی تلگرام",
]
