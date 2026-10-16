"""One-time Telegram setup: find your chat_id and save it to <workspace>/job_scan/telegram_config.json.

1. In Telegram, message @BotFather -> /newbot -> copy the token it gives you.
2. Create job_scan/telegram_config.json containing: {"bot_token": "<token>", "chat_id": ""}
3. Open your new bot in Telegram and send it any message.
4. Run: python get_chat_id.py --workspace <ws>
Keep the token private; if it leaks, send /revoke to @BotFather.
"""
import argparse, json, os, urllib.request

ap = argparse.ArgumentParser()
ap.add_argument("--workspace", required=True)
CFG = os.path.join(ap.parse_args().workspace, "job_scan", "telegram_config.json")
cfg = json.load(open(CFG, encoding="utf-8"))
with urllib.request.urlopen(f"https://api.telegram.org/bot{cfg['bot_token']}/getUpdates", timeout=30) as r:
    updates = json.load(r).get("result", [])
chats = {u["message"]["chat"]["id"]: u["message"]["chat"].get("first_name", "") for u in updates if "message" in u}
if not chats:
    print("No messages found. Send your bot a message in Telegram first, then run this again.")
else:
    chat_id, name = list(chats.items())[-1]
    cfg["chat_id"] = str(chat_id)
    json.dump(cfg, open(CFG, "w", encoding="utf-8"), indent=1)
    print(f"Saved chat_id for '{name}'. Test with: python send_telegram.py --workspace <ws>")
