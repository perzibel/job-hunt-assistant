"""Send a text summary (and optionally a report file) to the candidate's Telegram via their own bot.

Reads <workspace>/job_scan/telegram_config.json: {"bot_token": "...", "chat_id": "..."}
Usage:
  python send_telegram.py --workspace <ws> job_scan/summary.txt
  python send_telegram.py --workspace <ws> job_scan/summary.txt --file "Weekly Reports/2026-10-18.md"
Setup: see get_chat_id.py. Keep the bot token private.
"""
import argparse, json, os, uuid, urllib.request


def api(token, method, data=None, files=None):
    url = f"https://api.telegram.org/bot{token}/{method}"
    if files:
        boundary = uuid.uuid4().hex
        body = b""
        for k, v in (data or {}).items():
            body += f'--{boundary}\r\nContent-Disposition: form-data; name="{k}"\r\n\r\n{v}\r\n'.encode()
        for k, path in files.items():
            body += (f'--{boundary}\r\nContent-Disposition: form-data; name="{k}"; filename="{os.path.basename(path)}"\r\n'
                     f"Content-Type: application/octet-stream\r\n\r\n").encode() + open(path, "rb").read() + b"\r\n"
        body += f"--{boundary}--\r\n".encode()
        req = urllib.request.Request(url, body, {"Content-Type": f"multipart/form-data; boundary={boundary}"})
    else:
        req = urllib.request.Request(url, json.dumps(data or {}).encode(), {"Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=30) as r:
        return json.load(r)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--workspace", required=True)
    ap.add_argument("summary", nargs="?")
    ap.add_argument("--file")
    a = ap.parse_args()
    cfg_path = os.path.join(a.workspace, "job_scan", "telegram_config.json")
    if not os.path.exists(cfg_path):
        print("telegram_config.json not found - skipping Telegram.")
        return
    cfg = json.load(open(cfg_path, encoding="utf-8"))
    token, chat = cfg.get("bot_token", ""), str(cfg.get("chat_id", ""))
    if not token or not chat or "PASTE" in token:
        print("telegram_config.json is not filled in - skipping Telegram.")
        return
    resolve = lambda p: p if os.path.isabs(p) else os.path.join(a.workspace, p)
    text = open(resolve(a.summary), encoding="utf-8").read() if a.summary else "Weekly job review finished."
    for i in range(0, len(text), 3900):  # Telegram limit is 4096 chars per message
        api(token, "sendMessage", {"chat_id": chat, "text": text[i:i + 3900], "disable_web_page_preview": True})
    if a.file:
        api(token, "sendDocument", {"chat_id": chat}, {"document": resolve(a.file)})
    print("Sent to Telegram.")


if __name__ == "__main__":
    main()
