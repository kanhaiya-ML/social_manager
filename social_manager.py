import customtkinter as ctk
import json
import os

from whatsapp_app import whatsapp_message, stop_whatsapp_bot
from dms_app import send_insta_message, stop_instagram_dms
from reels_app import send_insta_reels, stop_instagram_bot

# =========================
# Helpers
# =========================

def has_api_key():
    if not os.path.exists("config.json"):
        return False

    with open("config.json", "r") as f:
        data = json.load(f)

    return bool(data.get("groq_api_key", "").strip())


def has_credentials():
    """Check if username and password exist in config"""
    if not os.path.exists("config.json"):
        return False
    
    with open("config.json", "r") as f:
        data = json.load(f)
    
    return bool(data.get("username", "").strip() and data.get("password", "").strip())

def verify_credentials(username, password):
    """Verify credentials (you can add your own logic here)"""
    # For now, just check if fields are not empty
    # You can add database verification or hardcoded credentials here
    return bool(username.strip() and password.strip())


def load_settings():
    """Load settings from config file"""
    if os.path.exists("config.json"):
        with open("config.json", "r") as f:
            data = json.load(f)
        return data.get("headless", False)
    return False


def save_settings(headless_mode):
    """Save settings to config file"""
    config_data = {}
    if os.path.exists("config.json"):
        with open("config.json", "r") as f:
            config_data = json.load(f)
    
    config_data["headless"] = headless_mode
    
    with open("config.json", "w") as f:
        json.dump(config_data, f, indent=4)

#--------------------------------------------------------
#                                                       |
# def save_api():
#     headless = headless_var.get()
#     with open("config.json", "w") as f:
#         json.dump(
#             {"groq_api_key": api_entry.get()},
#             f,
#             indent=4
#         )
#     show_dashboard()

def save_api():
    # Load existing config
    config_data = {}
    if os.path.exists("config.json"):
        with open("config.json", "r") as f:
            config_data = json.load(f)
    
    # Update API key while preserving username/password
    config_data["groq_api_key"] = api_entry.get()
    
    # Save config
    with open("config.json", "w") as f:
        json.dump(config_data, f, indent=4)
    
    show_dashboard()

#-----------------------------------------------------------

def get_whatsapp_stats():
    with open("data/whatsapp_stats.json", "r") as f:
        return json.load(f)

def get_dm_stats():
    with open("data/dm_stats.json", "r") as f:
        return json.load(f)

def get_reels_stats():
    with open("data/reels_stats.json", "r") as f:
        return json.load(f)

# =========================
# App
# =========================

app = ctk.CTk()
app.title("Social Manager")
app.geometry("1000x600")

headless_var = ctk.BooleanVar(value=load_settings())

api_frame = ctk.CTkFrame(app)
dashboard_frame = ctk.CTkFrame(app)

login_frame = ctk.CTkFrame(app)

# =========================
# LOGIN PAGE
# =========================

ctk.CTkLabel(
    login_frame,
    text="Social Manager Login",
    font=("Arial", 28)
).pack(pady=30)

ctk.CTkLabel(
    login_frame,
    text="Please enter your credentials"
).pack(pady=10)

username_entry = ctk.CTkEntry(
    login_frame,
    width=300,
    placeholder_text="Username"
)
username_entry.pack(pady=10)

password_entry = ctk.CTkEntry(
    login_frame,
    width=300,
    placeholder_text="Password",
    show="*"  # Hide password characters
)
password_entry.pack(pady=10)

error_label = ctk.CTkLabel(
    login_frame,
    text="",
    text_color="red"
)
error_label.pack(pady=5)


def save_credentials():
    username = username_entry.get().strip()
    password = password_entry.get().strip()
    
    if verify_credentials(username, password):
        # Load existing config or create new one
        config_data = {}
        if os.path.exists("config.json"):
            with open("config.json", "r") as f:
                config_data = json.load(f)
        
        # Add credentials
        config_data["username"] = username
        config_data["password"] = password
        
        # Save config
        with open("config.json", "w") as f:
            json.dump(config_data, f, indent=4)
        
        # Show next page (API or Dashboard)
        if has_api_key():
            show_dashboard()
        else:
            show_api_page()
    else:
        error_label.configure(text="Invalid username or password")

ctk.CTkButton(
    login_frame,
    text="Login",
    command=save_credentials
).pack(pady=20)


# =========================
# API PAGE
# =========================

ctk.CTkLabel(
    api_frame,
    text="Social Manager",
    font=("Arial", 28)
).pack(pady=30)

api_entry = ctk.CTkEntry(
    api_frame,
    width=400,
    placeholder_text="Enter GROQ API Key"
)

api_entry.pack(pady=20)

ctk.CTkButton(
    api_frame,
    text="Save API",
    command=save_api
).pack(pady=10)


# Headless mode checkbox on API page
headless_checkbox_api = ctk.CTkCheckBox(
    api_frame,
    text="Headless Mode (Browser runs in background)",
    variable=headless_var,
    onvalue=True,
    offvalue=False
)
headless_checkbox_api.pack(pady=10)

# =========================
# DASHBOARD LAYOUT
# =========================

sidebar = ctk.CTkFrame(
    dashboard_frame,
    width=180
)

sidebar.pack(
    side="left",
    fill="y"
)

content_frame = ctk.CTkFrame(
    dashboard_frame
)

content_frame.pack(
    side="right",
    fill="both",
    expand=True
)


# =========================
# STATUS
# =========================

whatsapp_running = False
dm_running = False
reels_running = False
current_page = "whatsapp"


# =========================
# HEADLESS TOGGLE FUNCTION
# =========================

def toggle_headless():
    """Toggle headless mode and save to config"""
    current_value = headless_var.get()
    save_settings(current_value)
    # Show a temporary label to confirm the change
    show_headless_status(current_value)

def show_headless_status(value):
    """Show current headless mode status"""
    status = "ON (Hidden)" if value else "OFF (Visible)"
    try:
        headless_status_label.configure(text=f"Headless Mode: {status}")
    except:
        pass

# =========================
# WHATSAPP PAGE
# =========================

def start_whatsapp():
    global whatsapp_running
    headless = headless_var.get()
    whatsapp_message(headless=headless)
    whatsapp_running = True
    show_whatsapp_page()


def stop_whatsapp():
    global whatsapp_running
    stop_whatsapp_bot()
    whatsapp_running = False
    show_whatsapp_page()


def show_whatsapp_page():
    global current_page, headless_status_label
    current_page = "whatsapp"

    for widget in content_frame.winfo_children():
        widget.destroy()

    whatsapp_stats = get_whatsapp_stats()
    dm_stats = get_dm_stats()
    reels_stats = get_reels_stats()


    status = "Running" if whatsapp_running else "Stopped"
    headless_status = "ON (Hidden)" if headless_var.get() else "OFF (Visible)"

    ctk.CTkLabel(
        content_frame,
        text="WhatsApp Dashboard",
        font=("Arial", 24)
    ).pack(pady=20)

    status_frame = ctk.CTkFrame(content_frame)
    status_frame.pack(pady=10)

    ctk.CTkLabel(
        status_frame,
        text=f"Bot Status: {status}",
        font=("Arial", 16),
        text_color="green" if whatsapp_running else "red"
    ).pack(side="left", padx=10)

    ctk.CTkLabel(
        status_frame,
        text="|",
        font=("Arial", 16)
    ).pack(side="left", padx=5)

    ctk.CTkLabel(
        status_frame,
        text=f"Headless: {headless_status}",
        font=("Arial", 16),
        text_color="blue" if headless_var.get() else "orange"
    ).pack(side="left", padx=10)

    # Headless mode toggle
    headless_frame = ctk.CTkFrame(content_frame)
    headless_frame.pack(pady=10)
    
    headless_checkbox = ctk.CTkCheckBox(
        headless_frame,
        text="Headless Mode (Browser hidden)",
        variable=headless_var,
        onvalue=True,
        offvalue=False,
        command=toggle_headless
    )
    headless_checkbox.pack(side="left", padx=5)
    
    # Control buttons
    button_frame = ctk.CTkFrame(content_frame)
    button_frame.pack(pady=10)


    ctk.CTkButton(
        button_frame,
        text="Start WhatsApp",
        command=start_whatsapp,
        fg_color="green",
        hover_color="dark green"
    ).pack(side="left",padx=5)

    ctk.CTkButton(
        button_frame,
        text="Stop WhatsApp",
        command=stop_whatsapp,
        fg_color="red",
        hover_color="dark red"
    ).pack(side="left",padx=5)

    ctk.CTkLabel(
        content_frame,
        text=f"Messages Sent: {whatsapp_stats['messages_sent']}",
        font=("Arial", 18)
    ).pack(pady=15)

    textbox = ctk.CTkTextbox(
        content_frame,
        width=600,
        height=250
    )
    

    textbox.pack(pady=10)

    for msg in whatsapp_stats["recent_messages"]:

        textbox.insert(
            "end",
            f"Chat: {msg['chat']}\n"
        )

        textbox.insert(
            "end",
            f"Message: {msg['message']}\n"
        )

        textbox.insert(
            "end",
            "-" * 50 + "\n\n"
        )

    textbox.configure(state="disabled")


# =========================
# INSTA DM PAGE
# =========================

def start_dm():
    global dm_running
    headless = headless_var.get()
    send_insta_message(headless=headless)
    dm_running = True
    show_dm_page()

def stop_dm():
    global dm_running
    stop_instagram_dms()
    dm_running = False
    show_dm_page() 


def show_dm_page():
    global current_page
    current_page = "dm"

    for widget in content_frame.winfo_children():
        widget.destroy()

    status = "Running" if dm_running else "Stopped"
    headless_status = "ON (Hidden)" if headless_var.get() else "OFF (Visible)"


    ctk.CTkLabel(
        content_frame,
        text="Instagram DM Dashboard",
        font=("Arial", 24)
    ).pack(pady=20)


    # Status indicators
    status_frame = ctk.CTkFrame(content_frame)
    status_frame.pack(pady=10)

    ctk.CTkLabel(
        status_frame,
        text=f"Bot Status: {status}",
        font=("Arial", 16),
        text_color="green" if dm_running else "red"
    ).pack(side="left", padx=10)

    ctk.CTkLabel(
        status_frame,
        text="|",
        font=("Arial", 16)
    ).pack(side="left", padx=5)

    ctk.CTkLabel(
        status_frame,
        text=f"Headless: {headless_status}",
        font=("Arial", 16),
        text_color="blue" if headless_var.get() else "orange"
    ).pack(side="left", padx=10)


    # Headless mode toggle
    headless_frame = ctk.CTkFrame(content_frame)
    headless_frame.pack(pady=10)
    
    headless_checkbox = ctk.CTkCheckBox(
        headless_frame,
        text="Headless Mode (Browser hidden)",
        variable=headless_var,
        onvalue=True,
        offvalue=False,
        command=toggle_headless
    )
    headless_checkbox.pack(side="left", padx=5)

    # Control buttons
    button_frame = ctk.CTkFrame(content_frame)
    button_frame.pack(pady=10)


    ctk.CTkButton(
        button_frame,
        text="Start DM Bot",
        command=start_dm,
        fg_color="green",
        hover_color="dark green"
    ).pack(side="left",padx=5)

    ctk.CTkButton(
        button_frame,
        text="Stop DM Bot",
        command=stop_dm,
        fg_color="red",
        hover_color="dark red"
    ).pack(side="left", padx=5)


# =========================
# REELS PAGE
# =========================

def start_reels():
    global reels_running
    contacts = [
        u.strip()
        for u in username_entry.get().split(",")
        if u.strip()
    ]
    if contacts:
        headless = headless_var.get()
        send_insta_reels(contacts, headless=headless)  # Pass headless parameter
        reels_running = True
        show_reels_page()

def stop_reels():
    global reels_running
    stop_instagram_bot()
    reels_running = False
    show_reels_page()


def show_reels_page():
    global username_entry,current_page
    current_page = "reels"

    for widget in content_frame.winfo_children():
        widget.destroy()

    status = "Running" if reels_running else "Stopped"
    headless_status = "ON (Hidden)" if headless_var.get() else "OFF (Visible)"


    ctk.CTkLabel(
        content_frame,
        text="Instagram Reels Dashboard",
        font=("Arial", 24)
    ).pack(pady=20)


    # Status indicators
    status_frame = ctk.CTkFrame(content_frame)
    status_frame.pack(pady=10)


    ctk.CTkLabel(
        status_frame,
        text=f"Bot Status: {status}",
        font=("Arial", 16),
        text_color="green" if reels_running else "red"
    ).pack(side="left", padx=10)

    ctk.CTkLabel(
        status_frame,
        text="|",
        font=("Arial", 16)
    ).pack(side="left", padx=5)

    ctk.CTkLabel(
        status_frame,
        text=f"Headless: {headless_status}",
        font=("Arial", 16),
        text_color="blue" if headless_var.get() else "orange"
    ).pack(side="left", padx=10)

    # Headless mode toggle
    headless_frame = ctk.CTkFrame(content_frame)
    headless_frame.pack(pady=10)
    
    headless_checkbox = ctk.CTkCheckBox(
        headless_frame,
        text="Headless Mode (Browser hidden)",
        variable=headless_var,
        onvalue=True,
        offvalue=False,
        command=toggle_headless
    )
    headless_checkbox.pack(side="left", padx=5)


    #user input
    ctk.CTkLabel(
        content_frame,
        text="Target Users (comma separated)"
    ).pack(pady=(10, 5))

    username_entry = ctk.CTkEntry(
        content_frame,
        width=300,
        placeholder_text="name1, name2, name3 ...."
    )
    username_entry.pack(pady=5)


    # Control buttons
    button_frame = ctk.CTkFrame(content_frame)
    button_frame.pack(pady=10)

    ctk.CTkButton(
        button_frame,
        text="Start Reels",
        command=start_reels,
        fg_color="green",
        hover_color="dark green"
    ).pack(side="left", padx=5)

    ctk.CTkButton(
        button_frame,
        text="Stop Reels",
        command=stop_reels,
        fg_color="red",
        hover_color="dark red"
    ).pack(side="left", padx=5)


# =========================
# GEMINI PAGE
# =========================

def show_gemini_page():
    global current_page
    current_page = "gemini"
    
    for widget in content_frame.winfo_children():
        widget.destroy()

    headless_status = "ON (Hidden)" if headless_var.get() else "OFF (Visible)"

    ctk.CTkLabel(
        content_frame,
        text="Ask Gemini",
        font=("Arial", 24)
    ).pack(pady=20)

    # Show headless status
    headless_frame = ctk.CTkFrame(content_frame)
    headless_frame.pack(pady=10)
    
    headless_checkbox = ctk.CTkCheckBox(
        headless_frame,
        text="Headless Mode (Browser hidden)",
        variable=headless_var,
        onvalue=True,
        offvalue=False,
        command=toggle_headless
    )
    headless_checkbox.pack(side="left", padx=5)

    ctk.CTkLabel(
        content_frame,
        text="Coming Soon"
    ).pack(pady=10)


def show_home_page():
    global current_page
    current_page = "home"
    
    for widget in content_frame.winfo_children():
        widget.destroy()

    whatsapp_stats = get_whatsapp_stats()
    dm_stats = get_dm_stats()
    reels_stats = get_reels_stats()
    headless_status = "ON (Hidden)" if headless_var.get() else "OFF (Visible)"

    ctk.CTkLabel(
        content_frame,
        text="Home Dashboard",
        font=("Arial", 24)
    ).pack(pady=20)

    # Settings section
    settings_frame = ctk.CTkFrame(content_frame)
    settings_frame.pack(pady=10, fill="x", padx=20)

    ctk.CTkLabel(
        settings_frame,
        text="Settings",
        font=("Arial", 18, "bold")
    ).pack(pady=10)

    headless_checkbox = ctk.CTkCheckBox(
        settings_frame,
        text=f"Headless Mode: {headless_status}",
        variable=headless_var,
        onvalue=True,
        offvalue=False,
        command=toggle_headless
    )
    headless_checkbox.pack(pady=10)

    # Stats section
    stats_frame = ctk.CTkFrame(content_frame)
    stats_frame.pack(pady=10, fill="x", padx=20)

    ctk.CTkLabel(
        stats_frame,
        text="Statistics",
        font=("Arial", 18, "bold")
    ).pack(pady=10)

    ctk.CTkLabel(
        stats_frame,
        text=f"WhatsApp Messages: {whatsapp_stats['messages_sent']}",
        font=("Arial", 16)
    ).pack(pady=5)

    ctk.CTkLabel(
        stats_frame,
        text=f"Instagram Replies: {dm_stats['messages_sent']}",
        font=("Arial", 16)
    ).pack(pady=5)

    ctk.CTkLabel(
        stats_frame,
        text=f"Reels Sent: {reels_stats['reels_sent']}",
        font=("Arial", 16)
    ).pack(pady=5)


# Add logout function
def logout():
    # Remove credentials from config
    if os.path.exists("config.json"):
        with open("config.json", "r") as f:
            config_data = json.load(f)
        
        # Remove credentials but keep API key
        config_data.pop("username", None)
        config_data.pop("password", None)
        
        with open("config.json", "w") as f:
            json.dump(config_data, f, indent=4)
    
    show_login_page()
    
# =========================
# SIDEBAR
# =========================

ctk.CTkLabel(
    sidebar,
    text="Features",
    font=("Arial", 20)
).pack(pady=20)

ctk.CTkButton(
    sidebar,
    text="Home",
    command=show_home_page
).pack(fill="x", padx=10, pady=5)

ctk.CTkButton(
    sidebar,
    text="WhatsApp",
    command=show_whatsapp_page
).pack(fill="x", padx=10, pady=5)

ctk.CTkButton(
    sidebar,
    text="Instagram DM",
    command=show_dm_page
).pack(fill="x", padx=10, pady=5)

ctk.CTkButton(
    sidebar,
    text="Instagram Reels",
    command=show_reels_page
).pack(fill="x", padx=10, pady=5)

ctk.CTkButton(
    sidebar,
    text="Ask Gemini",
    command=show_gemini_page
).pack(fill="x", padx=10, pady=5)

# Add this at the bottom of sidebar buttons
ctk.CTkButton(
    sidebar,
    text="Logout",
    command=logout,
    fg_color="red",
    hover_color="dark red"
).pack(fill="x", padx=10, pady=5)



# =========================
# SHOW DASHBOARD
# =========================

def show_dashboard():
    api_frame.pack_forget()
    dashboard_frame.pack(
        fill="both",
        expand=True
    )
    show_whatsapp_page()


def show_login_page():
    dashboard_frame.pack_forget()
    api_frame.pack_forget()
    login_frame.pack(fill="both", expand=True)

def show_api_page():
    login_frame.pack_forget()
    dashboard_frame.pack_forget()
    api_frame.pack(fill="both", expand=True)

def show_dashboard():
    login_frame.pack_forget()
    api_frame.pack_forget()
    dashboard_frame.pack(fill="both", expand=True)
    show_whatsapp_page()


def auto_refresh():
    if dashboard_frame.winfo_ismapped():
        try:
            # Refresh the current page instead of always showing WhatsApp
            if current_page == "whatsapp":
                show_whatsapp_page()
            elif current_page == "dm":
                show_dm_page()
            elif current_page == "reels":
                show_reels_page()
            elif current_page == "gemini":
                show_gemini_page()
            elif current_page == "home":
                show_home_page()
        except:
            pass

    app.after(
        30000,
        auto_refresh
    )


# =========================
# STARTUP
# =========================

if not has_credentials():
    # No credentials - show login page
    login_frame.pack(fill="both", expand=True)
elif has_api_key():
    # Has credentials and API - show dashboard
    dashboard_frame.pack(fill="both", expand=True)
    show_whatsapp_page()
else:
    # Has credentials but no API - show API page
    api_frame.pack(fill="both", expand=True)


auto_refresh()
app.mainloop()