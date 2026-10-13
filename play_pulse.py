#!/usr/bin/env python3
"""Weekly Play Store pulse for an Android app.

Usage:
    pip install google-play-scraper
    python play_pulse.py --app com.moveinsync.ets --snapdir pulse_snapshots

Notes:
    Public review data is enough for rating, written-review volume, recent
    1-star share, app-version spikes and text themes. Crash-free users still
    needs Play Console, so pass it with --crashfree when available.
"""
import argparse
import csv
import json
import statistics
import sys
from collections import Counter
from datetime import datetime, timedelta
from pathlib import Path


THEMES = {
    "No-show / cancel penalty": ["no show", "no-show", "noshow", "cancel", "penalt", "marked absent"],
    "Tracking / GPS / ETA": ["gps", "location", "track", "eta", "live", "wrong time"],
    "OTP / login": ["otp", "login", "log in", "sign in", "verification"],
    "Update / redesign": ["update", "upgrade", "new version", "redesign", "interface", "confusing", " ui"],
    "Crash / performance": ["crash", "not opening", "white screen", "freez", "hang", "slow", "lag"],
    "Notifications": ["notification", "push", "reminder"],
    "Booking / scheduling": ["book", "schedule", "shuttle", "roster", "date"],
    "Support / ops": ["driver", "support", "late", "pickup point", "no response", "helpline"],
}


def themes_of(text):
    t = " " + (text or "").lower()
    return [name for name, keys in THEMES.items() if any(k in t for k in keys)] or ["Other"]


def load_public(app_id, days=90, cap=3000):
    from google_play_scraper import Sort, app, reviews

    meta = app(app_id, lang="en", country="in")
    rows, token, cutoff = [], None, datetime.now() - timedelta(days=days)
    while len(rows) < cap:
        batch, token = reviews(
            app_id,
            lang="en",
            country="in",
            sort=Sort.NEWEST,
            count=200,
            continuation_token=token,
        )
        if not batch:
            break
        rows += [
            {
                "at": r["at"],
                "score": r["score"],
                "content": r["content"],
                "version": r.get("reviewCreatedVersion") or "unknown",
                "reply_at": r.get("repliedAt"),
            }
            for r in batch
        ]
        if batch[-1]["at"] < cutoff or token is None:
            break
    return meta, [r for r in rows if r["at"] >= cutoff]


def load_csv(path):
    with open(path, newline="", encoding="utf-8") as f:
        return None, [
            {
                "at": datetime.fromisoformat(r["at"]),
                "score": int(r["score"]),
                "content": r["content"],
                "version": r.get("version") or "unknown",
                "reply_at": datetime.fromisoformat(r["reply_at"]) if r.get("reply_at") else None,
            }
            for r in csv.DictReader(f)
        ]


def pulse(meta, rows, crashfree, now):
    last = [r for r in rows if r["at"] >= now - timedelta(days=30)]
    prev = [r for r in rows if now - timedelta(days=60) <= r["at"] < now - timedelta(days=30)]
    avg = lambda rs: round(statistics.mean(r["score"] for r in rs), 2) if rs else None
    one_share = lambda rs: round(100 * sum(r["score"] == 1 for r in rs) / len(rs), 1) if rs else None
    bad = lambda rs: [r for r in rs if r["score"] <= 2]
    cnt = lambda rs: Counter(t for r in bad(rs) for t in themes_of(r["content"]))
    c_now, c_prev = cnt(last), cnt(prev)
    by_ver = Counter(r["version"] for r in last if r["score"] == 1)
    replied = [r for r in bad(last) if r["reply_at"]]
    raw_hours = [(r["reply_at"] - r["at"]).total_seconds() / 3600 for r in replied]
    valid_hours = [h for h in raw_hours if h >= 0]
    return {
        "date": now.date().isoformat(),
        "n_last30": len(last),
        "n_prev30": len(prev),
        "score": meta["score"] if meta else None,
        "ratings": meta["ratings"] if meta else None,
        "avg_last30": avg(last),
        "avg_prev30": avg(prev),
        "one_star_share_last30": one_share(last),
        "one_star_share_prev30": one_share(prev),
        "one_star_by_version": by_ver.most_common(3),
        "themes_last30": c_now.most_common(3),
        "themes_prev30": dict(c_prev),
        "reply_rate": round(100 * len(replied) / len(bad(last)), 1) if bad(last) else None,
        "median_reply_hours": round(statistics.median(valid_hours), 1) if valid_hours else None,
        "reply_time_anomalies": len(raw_hours) - len(valid_hours),
        "crashfree": crashfree,
    }


def show(p, prior):
    d = lambda a, b: "" if a is None or b is None else f" ({a - b:+.1f} vs prior 30 days)"
    print(f"MOVEINSYNC PLAY PULSE, {p['date']}  (written reviews: {p['n_last30']} in last 30 days)")
    print(f"1. Play score {p['score']} from {p['ratings']} ratings" if p["score"] else "1. Play score: not available offline")
    print(f"2. Average stars of written reviews, last 30 days: {p['avg_last30']}{d(p['avg_last30'], p['avg_prev30'])}")
    print(
        f"3. 1-star share, last 30 days: {p['one_star_share_last30']}%{d(p['one_star_share_last30'], p['one_star_share_prev30'])}; "
        f"top versions: {', '.join(f'{v} ({n})' for v, n in p['one_star_by_version']) or 'none'}"
    )
    th = "; ".join(f"{t} {n} ({n - p['themes_prev30'].get(t, 0):+d})" for t, n in p["themes_last30"]) or "none"
    print(f"4. Top themes in 1 and 2-star reviews (change vs prior 30 days): {th}")
    print(
        f"5. Reply rate on 1 and 2-star reviews: {p['reply_rate']}%, "
        f"median {p['median_reply_hours'] if p['median_reply_hours'] is not None else 'n/a'} hours to reply; "
        f"{p['reply_time_anomalies']} public timestamp anomalies ignored"
    )
    print(f"6. Crash-free users (Play Console): {p['crashfree'] if p['crashfree'] is not None else 'enter with --crashfree'}")
    if prior:
        print(f"   Since last snapshot ({prior['date']}): 1-star share {prior['one_star_share_last30']}% -> {p['one_star_share_last30']}%")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--app", default="com.moveinsync.ets")
    ap.add_argument("--csv")
    ap.add_argument("--crashfree", type=float)
    ap.add_argument("--now", help="override today's date, YYYY-MM-DD")
    ap.add_argument("--snapdir", default="pulse_snapshots")
    a = ap.parse_args()
    meta, rows = load_csv(a.csv) if a.csv else load_public(a.app)
    if not rows:
        sys.exit("No reviews returned. If Google blocks your network, rerun from your laptop.")
    now = datetime.fromisoformat(a.now) if a.now else datetime.now()
    p = pulse(meta, rows, a.crashfree, now)
    snaps = Path(a.snapdir)
    snaps.mkdir(exist_ok=True)
    older = sorted(f for f in snaps.glob("*.json") if f.stem < p["date"])
    prior = json.loads(older[-1].read_text()) if older else None
    show(p, prior)
    (snaps / f"{p['date']}.json").write_text(json.dumps(p, indent=2, default=str))


if __name__ == "__main__":
    main()
