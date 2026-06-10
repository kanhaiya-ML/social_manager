import customtkinter as ctk
from reels_app import send_insta_reels
from dms_app import send_insta_message
from whatsapp_app import whatsapp_message
from whatsapp_app import stop_whatsapp_bot
from reels_app import stop_instagram_bot
from dms_app import stop_instagram_dms
import json
import os

def has_api_key():
    if not os.path.exists("config.json"):
        return False

    with open("config.json", "r") as f:
        data = json.load(f)

    return bool(data.get("groq_api_key", "").strip())


def get_whatsapp_stats():
    with open("data/whatsapp_stats.json", "r") as f:
        return json.load(f)
    
def refresh_whatsapp_stats():
    stats = get_whatsapp_stats()

    whatsapp_count_label.configure(
        text=f"Messages Sent: {stats['messages_sent']}"
    )


app = ctk.CTk()
app.geometry("600x550")

api_frame = ctk.CTkFrame(app)
dashboard_frame = ctk.CTkFrame(app)

app.title("Social Manager")

ctk.CTkLabel(
    api_frame,
    text="Social Manager",
    font=("Arial", 25)
).pack(pady=20)

# api Box
api_entry = ctk.CTkEntry(
    api_frame,
    width=300,
    placeholder_text="Enter GROQ API Key"
)

api_entry.pack(pady=20)


# save button
import json

def save_api():
    with open("config.json", "w") as f:
        json.dump(
            {"groq_api_key": api_entry.get()},
            f
        )

    show_dashboard()

def start_whatsapp():
    whatsapp_message()
    whatsapp_status.configure(text="WhatsApp: Running")

def stop_whatsapp():
    stop_whatsapp_bot()
    whatsapp_status.configure(text="WhatsApp: Stopped")


def start_reels():
    send_insta_reels()
    reels_status.configure(text="Reels: Running")

def stop_reels():
    stop_instagram_bot()
    reels_status.configure(text="Reels: stopped")

def start_DM():
    send_insta_message()
    DM_status.configure(text="DM: Running")

def stop_DM():
    stop_instagram_dms()
    DM_status.configure(text="DM: stopped")


save_btn = ctk.CTkButton(
    api_frame,
    text="Save API",
    command=save_api
)

save_btn.pack()

# Bot launcher Button

whatsapp_status = ctk.CTkLabel(
    dashboard_frame,
    text="WhatsApp: Stopped"
)

whatsapp_status.pack()

ctk.CTkButton(
    dashboard_frame,
    text="Start WhatsApp",
    command=start_whatsapp
).pack(pady=10)

whatsapp_count_label = ctk.CTkLabel(
    app,
    text="Messages Sent: 0"
)

whatsapp_count_label.pack()

ctk.CTkButton(
    dashboard_frame,
    text="Stop WhatsApp",
    command=stop_whatsapp
).pack(pady=10)

reels_status = ctk.CTkLabel(
    dashboard_frame,
    text="Reels: Stopped"
)

reels_status.pack()

ctk.CTkButton(
    dashboard_frame,
    text="Start Reels",
    command=start_reels
).pack(pady=10)


ctk.CTkButton(
    dashboard_frame,
    text="Stop Reels",
    command=stop_reels
).pack(pady=10)

DM_status = ctk.CTkLabel(
    dashboard_frame,
    text="DM: Stopped"
)

DM_status.pack()

ctk.CTkButton(
    dashboard_frame,
    text="Start Instagram DM",
    command=start_DM
).pack(pady=10)


ctk.CTkButton(
    dashboard_frame,
    text="Stop DM",
    command=stop_DM
).pack(pady=10)

def show_dashboard():
    api_frame.pack_forget()
    dashboard_frame.pack(fill="both", expand=True)

if has_api_key():
    dashboard_frame.pack(fill="both", expand=True)
else:
    api_frame.pack(fill="both", expand=True)
    

refresh_whatsapp_stats()
app.mainloop()