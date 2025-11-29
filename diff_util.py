# diff_util.py
from deepdiff import DeepDiff

TIME_KEYWORDS = ["لحظاتی پیش", "دقایقی پیش", "ساعت"]

def is_time_change(old, new):
    if not isinstance(old, str) or not isinstance(new, str):
        return False
    return any(k in old for k in TIME_KEYWORDS) and any(k in new for k in TIME_KEYWORDS)

def filter_deepdiff(diff):
    """Filter DeepDiff result to remove timestamp-only changes."""
    filtered = {}
    for change_type, items in diff.items():
        keep = {}
        for k, v in items.items():
            if isinstance(v, dict) and "old_value" in v and "new_value" in v:
                if not is_time_change(v.get("old_value"), v.get("new_value")):
                    keep[k] = v
            else:
                keep[k] = v
        if keep:
            filtered[change_type] = keep
    return filtered

def compute_diff(old, new):
    d = DeepDiff(old, new, ignore_order=True)
    return filter_deepdiff(d)
