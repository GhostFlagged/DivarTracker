# DivarThreadHunting

A Python monitoring tool that continuously scans Divar (Iranian classified ads platform) for posts matching specific keywords and sends real-time Discord notifications when new posts are found or existing posts are updated.

## Features

- 🔍 **Automated Monitoring**: Continuously scans Divar posts across multiple pages
- 🔑 **Keyword Filtering**: Filters posts based on customizable keywords (default: Telegram-related terms)
- 📢 **Discord Notifications**: Sends rich embed notifications via Discord webhooks
- 🔄 **Change Detection**: Detects and reports updates to existing posts (title, price, location changes)
- 🚀 **Multithreaded**: Uses concurrent fetching for efficient page scanning
- 💾 **Local Storage**: Persists post data and notification logs locally
- 🎯 **Smart Diffing**: Computes meaningful differences, ignoring time-only changes

## Requirements

- Python 3.6+
- Internet connection
- Discord webhook URL

## Installation

1. Clone or download this repository:
```bash
git clone <repository-url>
cd DivarThreadHunting
```

2. Install required dependencies:
```bash
pip install requests deepdiff
```

Or create a `requirements.txt` file:
```
requests
deepdiff
```

Then install:
```bash
pip install -r requirements.txt
```

## Configuration

Edit `config.py` to customize the monitoring behavior:

```python
# Page range to scan
PAGE_START = 1
PAGE_END = 3   # exclusive (scans pages 1 to 2)

# Scan interval in seconds
SCAN_INTERVAL = 60

# Discord webhook URL
WEBHOOK_URL = "https://discord.com/api/webhooks/YOUR_WEBHOOK_URL"

# City ID (4 = Tehran, adjust as needed)
CITY_ID = "4"

# Keywords to filter posts (empty list = match everything)
KEYWORDS = [
    "تلگرام",
    "ایدی تلگرام",
    "آیدی تلگرام",
]

# Number of threads for concurrent fetching
THREAD_COUNT = 10
```

### Getting a Discord Webhook URL

1. Go to your Discord server settings
2. Navigate to **Integrations** → **Webhooks**
3. Click **New Webhook**
4. Copy the webhook URL and paste it into `config.py`

## Usage

Run the monitoring script:

```bash
python main.py
```

The script will:
1. Load previously stored posts (if any)
2. Scan the configured page range
3. Compare with stored posts to find new/updated posts
4. Send Discord notifications for matching posts
5. Save the current state
6. Wait for the configured interval and repeat

### First Run

On the first run, the script will scan and store all posts but won't send notifications (to avoid spamming). Subsequent runs will only notify about new posts or updates.

## Project Structure

```
DivarThreadHunting/
├── main.py           # Main monitoring loop
├── config.py         # Configuration settings
├── fetcher.py        # API fetching logic
├── post_parser.py    # Post extraction and parsing
├── notifier.py       # Discord notification sender
├── storage.py        # Local JSON storage
├── diff_util.py      # Change detection utilities
├── data/
│   └── posts.json    # Stored post data
└── logs/
    └── notifications.json  # Notification history
```

## How It Works

1. **Fetching**: Uses multithreaded requests to fetch multiple pages from Divar's API simultaneously
2. **Parsing**: Extracts post data (title, price, location, image) from API responses
3. **Filtering**: Matches posts against configured keywords (searches in post descriptions)
4. **Comparison**: Compares current posts with stored posts to detect:
   - New posts (not in stored data)
   - Updated posts (changed title, price, or location)
5. **Notification**: Sends Discord embeds with:
   - Post title and link
   - Post description (fetched from post detail page)
   - Image preview
   - Change details (for updates)
6. **Storage**: Saves current state and logs all notifications

## Notification Format

Notifications are sent as Discord embeds containing:
- **Title**: Post title with emoji indicator (🆕 for new, ✏️ for updated)
- **Description**: Full post description from Divar
- **Image**: Post thumbnail
- **Changes**: Field-by-field changes for updated posts
- **Link**: Direct link to the Divar post

## Logging

All notifications are logged to `logs/notifications.json` for audit purposes, including:
- Post title and token
- Timestamp
- Change details
- Success/failure status

## Customization

### Adding More Keywords

Edit the `KEYWORDS` list in `config.py`:

```python
KEYWORDS = [
    "keyword1",
    "keyword2",
    # Add more keywords here
]
```

### Adjusting Scan Range

Modify `PAGE_START` and `PAGE_END` in `config.py` to scan more or fewer pages. Note: scanning too many pages may be rate-limited by Divar.

### Changing Scan Frequency

Adjust `SCAN_INTERVAL` in `config.py` (in seconds). Lower values mean more frequent scans but higher API usage.

## Troubleshooting

- **No notifications**: Check that keywords match posts, webhook URL is valid, and posts are being found
- **Rate limiting**: Increase `SCAN_INTERVAL` or reduce `PAGE_END`
- **Missing descriptions**: Descriptions are fetched separately; network issues may cause empty descriptions

## Notes

- The script skips notifications on the first run to avoid spam
- Only meaningful changes are reported (time-only changes are filtered out)
- Post data is stored locally in JSON format
- The script runs indefinitely until stopped (Ctrl+C)

## License

This project is provided as-is for educational and personal use.

