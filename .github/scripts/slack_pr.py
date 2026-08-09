#!/usr/bin/env python3
"""
Slack PR notifications for Nooz Optics — 2 modes:

- open    : post a 1-line notification to #tech when a PR opens; save the
            Slack message ts in a hidden marker comment on the PR.
- verdict : post the AI code review + autofix verdict as a reply in the
            thread of the open notification (looked up via the marker).

Falls back to a standalone canal message if no thread ts is found (e.g. PR
opened before this feature was deployed).
"""
import json
import os
import re
import subprocess
import sys
import urllib.request

SLACK_CHANNEL = "C0BNYCFV93Q"   # #agents-journal (décision Antoine 09.08.2026)
LEGACY_CHANNEL = "CT6NVGAMA"    # #tech — canal historique, et repli tant que
                                # @mcp_slack n'est pas /invite dans le journal
THREAD_TS_MARKER = "<!-- slack-thread-ts:"
REPO_EMOJI = {
    "nooz-pos": "🛒",
    "nooz-web": "🌐",
    "nooz-tv": "📺",
    "nooz-agents-explorer": "🧭",
    "nooz-studio": "🎨",
    "cloudflare": "☁️",
    "shopify-custom-app": "🛍️",
    "nooz-bridge": "🌉",
    "nooz-design-system": "📐",
}


def slack(method: str, payload: dict, strict: bool = True) -> dict:
    token = os.environ["SLACK_BOT_TOKEN"]
    req = urllib.request.Request(
        f"https://slack.com/api/{method}",
        data=json.dumps(payload).encode("utf-8"),
        headers={
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json; charset=utf-8",
        },
    )
    with urllib.request.urlopen(req) as resp:
        result = json.loads(resp.read().decode("utf-8"))
    if not result.get("ok") and strict:
        print(f"Slack API error: {result}", file=sys.stderr)
        sys.exit(1)
    return result


def post_message(payload: dict) -> dict:
    """Poste dans SLACK_CHANNEL, replie sur LEGACY_CHANNEL si le bot n'y est pas.

    Filet de transition : tant que le bot n'a pas été /invite dans
    #agents-journal, on continue de poster dans #tech plutôt que de faire
    échouer le job CI. Le canal réellement utilisé est renvoyé dans
    result["_channel"] — il est mémorisé dans le marqueur pour que les
    réponses de fil partent dans le bon canal."""
    result = slack("chat.postMessage", {**payload, "channel": SLACK_CHANNEL}, strict=False)
    if result.get("ok"):
        result["_channel"] = SLACK_CHANNEL
        return result
    if result.get("error") == "not_in_channel":
        print("⚠️ bot non invité dans #agents-journal — repli #tech", file=sys.stderr)
        result = slack("chat.postMessage", {**payload, "channel": LEGACY_CHANNEL})
        result["_channel"] = LEGACY_CHANNEL
        return result
    print(f"Slack API error: {result}", file=sys.stderr)
    sys.exit(1)


def gh(args: list[str]) -> str:
    r = subprocess.run(["gh"] + args, capture_output=True, text=True)
    if r.returncode != 0:
        print(f"gh failed: {r.stderr}", file=sys.stderr)
    return r.stdout.strip()


def find_thread_ts(repo: str, pr: str) -> tuple:
    """Renvoie (ts, channel). Les marqueurs d'avant la bascule du 09.08.2026
    ne portent pas de canal : leur fil vit dans #tech (LEGACY_CHANNEL)."""
    raw = gh(["pr", "view", pr, "--repo", repo, "--json", "comments"])
    if not raw:
        return None, None
    data = json.loads(raw)
    for c in data.get("comments", []):
        body = c.get("body", "")
        m = re.search(re.escape(THREAD_TS_MARKER) + r"\s*([\d.]+)(?:\s+(C[A-Z0-9]+))?\s*-->", body)
        if m:
            return m.group(1), (m.group(2) or LEGACY_CHANNEL)
    return None, None


def save_thread_ts(repo: str, pr: str, ts: str, channel: str) -> None:
    body = f"{THREAD_TS_MARKER} {ts} {channel} -->"
    gh(["pr", "comment", pr, "--repo", repo, "--body", body])


def open_mode() -> None:
    repo = os.environ["GITHUB_REPOSITORY"]
    pr = os.environ["PR_NUMBER"]
    title = os.environ["PR_TITLE"]
    url = os.environ["PR_URL"]
    author = os.environ["PR_AUTHOR"]

    repo_short = repo.split("/")[-1]
    emoji = REPO_EMOJI.get(repo_short, "📦")
    text = f"{emoji} <{url}|#{pr}> · {title} · _{author}_"

    result = post_message({
        "text": text,
        "unfurl_links": False,
        "unfurl_media": False,
    })
    ts = result["ts"]
    save_thread_ts(repo, pr, ts, result["_channel"])
    print(f"✅ PR open notification posted (ts={ts})")


def verdict_mode() -> None:
    repo = os.environ["GITHUB_REPOSITORY"]
    pr = os.environ["PR_NUMBER"]
    pr_url = os.environ.get("PR_URL", f"https://github.com/{repo}/pull/{pr}")
    has_criticals = os.environ.get("HAS_CRITICALS") == "true"
    has_warnings = os.environ.get("HAS_WARNINGS") == "true"
    n_critical = os.environ.get("N_CRITICAL", "0")
    n_warning = os.environ.get("N_WARNING", "0")
    autofix_result = os.environ.get("AUTOFIX_RESULT", "skipped")
    autofix_commit = os.environ.get("AUTOFIX_COMMIT", "")

    if has_criticals:
        emoji = "🔴"
        review_line = f"review · {n_critical} critical · {n_warning} warning"
    elif has_warnings:
        emoji = "🟡"
        review_line = f"review · {n_warning} warning"
    else:
        emoji = "🟢"
        review_line = "review · LGTM"

    parts = [f"{emoji} {review_line}"]

    if autofix_result == "success" and autofix_commit:
        parts.append(f"⚙️ autofix · ✅ `{autofix_commit[:7]}`")
    elif autofix_result == "success":
        parts.append("⚙️ autofix · ✅ rien à corriger")
    elif autofix_result == "failure":
        parts.append("⚙️ autofix · ❌ échec — voir Actions")

    text = "  ·  ".join(parts)

    ts, thread_channel = find_thread_ts(repo, pr)
    if ts:
        # Répondre dans le fil, LÀ où vit le message d'ouverture (le ts d'un
        # message #tech est invalide dans #agents-journal, et inversement).
        slack("chat.postMessage", {
            "channel": thread_channel,
            "text": text,
            "thread_ts": ts,
            "unfurl_links": False,
            "unfurl_media": False,
        })
    else:
        post_message({
            "text": f"<{pr_url}|#{pr}> · {text}",
            "unfurl_links": False,
            "unfurl_media": False,
        })
    print(f"✅ Verdict posted ({'thread ' + ts if ts else 'standalone'})")


def main() -> None:
    mode = sys.argv[1] if len(sys.argv) > 1 else ""
    if mode == "open":
        open_mode()
    elif mode == "verdict":
        verdict_mode()
    else:
        print("Usage: slack_pr.py {open|verdict}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
