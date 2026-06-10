import json

STATS_FILE = "data/whatsapp_stats.json"


def add_whatsapp_message(chat_name, message):
    with open(STATS_FILE, "r") as f:
        data = json.load(f)
    data["messages_sent"] += 1
    data["recent_messages"].insert(
        0,
        {
            "chat": chat_name,
            "message": message
        }
    )

    data["recent_messages"] = data["recent_messages"][:10]

    with open(STATS_FILE, "w") as f:
        json.dump(data, f, indent=4)


def update_dm_stats(chat_name, message):
    with open("data/dm_stats.json", "r") as f:
        data = json.load(f)
    data["messages_sent"] += 1
    data["recent_messages"].insert(
        0,
        {
            "chat": chat_name,
            "message": message
        }
    )
    data["recent_messages"] = data["recent_messages"][:10]

    with open("data/dm_stats.json", "w") as f:
        json.dump(data, f, indent=4)


def update_reels_stats(contact_name):
    with open("data/reels_stats.json", "r") as f:
        data = json.load(f)
    data["reels_sent"] += 1
    data["recent_contacts"].insert(
        0,
        contact_name
    )
    data["recent_contacts"] = data["recent_contacts"][:10]
    with open("data/reels_stats.json", "w") as f:
        json.dump(data, f, indent=4)