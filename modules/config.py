"""
Persistent configuration store.

Named configurations are saved as single JSON files in ``config/saved/``.
Each file contains all presets, timeline, and pump settings.
"""

import os
import json
import logging
from datetime import datetime

from modules._api import expose

log = logging.getLogger(__name__)

CONFIG_DIR = os.path.join(
    os.path.normpath(os.path.join(os.path.dirname(__file__), "..")),
    "config",
)
os.makedirs(CONFIG_DIR, exist_ok=True)

SAVED_DIR = os.path.join(CONFIG_DIR, "saved")
os.makedirs(SAVED_DIR, exist_ok=True)


def _safe_name(name: str) -> str:
    return "".join(c if c.isalnum() or c in "-_ " else "_" for c in name)


def load(key: str):
    """Read a config key from disk (used by obsbot for waypoints/crops)."""
    p = os.path.join(CONFIG_DIR, f"{key}.json")
    if not os.path.exists(p):
        return None
    with open(p, "r", encoding="utf-8") as f:
        return json.load(f)


def save(key: str, data):
    """Write a config key to disk (used by obsbot for waypoints/crops)."""
    with open(os.path.join(CONFIG_DIR, f"{key}.json"), "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)


# ── Named configurations ─────────────────────────────────────────────────────

@expose
def config_save_named(name, payload):
    """Save a complete named configuration (all presets + timeline + cavro)."""
    if not name or not name.strip():
        return {"error": "Configuration name is required"}
    safe = _safe_name(name.strip())
    path = os.path.join(SAVED_DIR, f"{safe}.json")
    try:
        data = {
            "name": name.strip(),
            "saved": datetime.now().isoformat(),
            "payload": payload,
        }
        with open(path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)
        return {"ok": True, "path": path}
    except Exception as e:
        log.error("config_save_named(%s) failed: %s", name, e)
        return {"error": str(e)}


@expose
def config_load_named(name):
    """Load a named configuration."""
    safe = _safe_name(name)
    path = os.path.join(SAVED_DIR, f"{safe}.json")
    if not os.path.exists(path):
        return {"error": f"Configuration '{name}' not found"}
    try:
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
        return {"ok": True, "data": data}
    except Exception as e:
        log.error("config_load_named(%s) failed: %s", name, e)
        return {"error": str(e)}


@expose
def config_list_named():
    """List all saved named configurations."""
    if not os.path.isdir(SAVED_DIR):
        return {"configs": []}
    configs = []
    for f in sorted(os.listdir(SAVED_DIR)):
        if not f.endswith(".json"):
            continue
        path = os.path.join(SAVED_DIR, f)
        try:
            with open(path, "r", encoding="utf-8") as fh:
                data = json.load(fh)
            configs.append({
                "name": data.get("name", f[:-5]),
                "saved": data.get("saved", ""),
            })
        except Exception:
            configs.append({"name": f[:-5], "saved": ""})
    return {"configs": configs}


@expose
def config_delete_named(name):
    """Delete a named configuration."""
    safe = _safe_name(name)
    path = os.path.join(SAVED_DIR, f"{safe}.json")
    if os.path.exists(path):
        os.remove(path)
        return {"ok": True}
    return {"error": "Not found"}
