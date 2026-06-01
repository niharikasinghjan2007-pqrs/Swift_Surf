import tkinter as tk
from tkinter import messagebox
import webbrowser
import datetime
import speech_recognition as sr

# ================= Window Setup =================
root = tk.Tk()
root.title("SwiftSurf Browser")
root.geometry("1000x620")
root.configure(bg="#f4f4f4")

dark_mode = False
history_list = []
bookmarks = []

# ================= Functions =================
def open_site(url):
    webbrowser.open_new_tab(url)
    save_history(url)

def search():
    query = search_box.get()
    if query:
        url = f"https://www.google.com/search?q={query}"
        webbrowser.open_new_tab(url)
        save_history(url)
    else:
        messagebox.showwarning("Empty Search", "Please enter something to search!")

def voice_search():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        messagebox.showinfo("Voice Search", "Listening... Speak now.")
        audio = recognizer.listen(source)
    try:
        text = recognizer.recognize_google(audio)
        search_box.delete(0, tk.END)
        search_box.insert(0, text)
        search()
    except sr.UnknownValueError:
        messagebox.showerror("Error", "Sorry, I couldn't understand.")
    except sr.RequestError:
        messagebox.showerror("Error", "Voice search not available.")

def toggle_mode():
    global dark_mode
    dark_mode = not dark_mode
    bg = "#1e1e1e" if dark_mode else "#f4f4f4"
    fg = "white" if dark_mode else "black"
    side_color = "#2d2d2d" if dark_mode else "#e0e0e0"
    root.configure(bg=bg)
    side_frame.configure(bg=side_color)
    main_frame.configure(bg=bg)
    label_title.configure(bg=bg, fg=fg)
    search_box.configure(bg="white" if not dark_mode else "#333", fg=fg, insertbackground=fg)
    bottom_frame.configure(bg=side_color)
    weather_button.configure(bg="#0078d7" if not dark_mode else "#444", fg="white")
    time_label.configure(bg=side_color, fg="black" if not dark_mode else "white")

def save_history(url):
    history_list.append((datetime.datetime.now().strftime("%H:%M:%S"), url))

def view_history():
    history_win = tk.Toplevel(root)
    history_win.title("Browsing History")
    history_win.geometry("400x300")
    history_box = tk.Listbox(history_win, font=("Arial", 11))
    history_box.pack(fill="both", expand=True)
    for time, site in history_list:
        history_box.insert(tk.END, f"{time}  -  {site}")

def add_bookmark():
    url = search_box.get()
    if url:
        bookmarks.append(url)
        messagebox.showinfo("Bookmark", f"Bookmarked: {url}")
    else:
        messagebox.showwarning("No URL", "Enter or search something to bookmark!")

def view_bookmarks():
    bookmark_win = tk.Toplevel(root)
    bookmark_win.title("Bookmarks")
    bookmark_win.geometry("400x300")
    bookmark_box = tk.Listbox(bookmark_win, font=("Arial", 11))
    bookmark_box.pack(fill="both", expand=True)
    for b in bookmarks:
        bookmark_box.insert(tk.END, b)

# ================= Top Navigation Bar =================
top_frame = tk.Frame(root, bg="#101010", height=50)
top_frame.pack(side="top", fill="x")

btn_home = tk.Button(top_frame, text="🏠 Home", bg="#101010", fg="white", bd=0, font=("Arial", 11),
                     command=lambda: open_site("https://www.google.com"))
btn_home.pack(side="left", padx=15)

btn_toggle = tk.Button(top_frame, text="🌗 Mode", bg="#101010", fg="white", bd=0, font=("Arial", 11),
                       command=toggle_mode)
btn_toggle.pack(side="left", padx=15)

btn_bookmark = tk.Button(top_frame, text="⭐ Add Bookmark", bg="#101010", fg="white", bd=0, font=("Arial", 11),
                         command=add_bookmark)
btn_bookmark.pack(side="left", padx=15)

btn_view_bookmarks = tk.Button(top_frame, text="📂 View Bookmarks", bg="#101010", fg="white", bd=0,
                               font=("Arial", 11), command=view_bookmarks)
btn_view_bookmarks.pack(side="left", padx=15)

btn_history = tk.Button(top_frame, text="🕓 History", bg="#101010", fg="white", bd=0, font=("Arial", 11),
                        command=view_history)
btn_history.pack(side="left", padx=15)

# ================= Left Sidebar =================
side_frame = tk.Frame(root, bg="#e0e0e0", width=140)
side_frame.pack(side="left", fill="y")

tk.Label(side_frame, text="Quick Access", bg="#e0e0e0", fg="black",
         font=("Arial", 11, "bold")).pack(pady=10)

# --- Common Social/Utility Sites ---
quick_sites = {
    "YouTube": "https://www.youtube.com",
    "Facebook": "https://www.facebook.com",
    "Instagram": "https://www.instagram.com",
    "Twitter": "https://www.twitter.com",
    "LinkedIn": "https://www.linkedin.com",
    "Wikipedia": "https://www.wikipedia.org",
    "Gmail": "https://mail.google.com",
    "Amazon": "https://www.amazon.in",
    "Reddit": "https://www.reddit.com",
    "Pinterest": "https://www.pinterest.com",
    "Spotify": "https://open.spotify.com/",
}

for name, url in quick_sites.items():
    btn = tk.Button(side_frame, text=name, bg="white", fg="black",
                    relief="groove", font=("Arial", 10, "bold"), width=15,
                    command=lambda url=url: open_site(url))
    btn.pack(pady=4)

# --- News Section ---
tk.Label(side_frame, text="News Portals", bg="#e0e0e0", fg="black",
         font=("Arial", 11, "bold")).pack(pady=(20, 5))

news_sites = {
    "BBC": "https://www.bbc.com/news",
    "CNN": "https://www.cnn.com",
    "NDTV": "https://www.ndtv.com",
    "TOI": "https://timesofindia.indiatimes.com",
    "The Guardian": "https://www.theguardian.com/international",
    "Al Jazeera": "https://www.aljazeera.com"
}

for name, url in news_sites.items():
    btn = tk.Button(side_frame, text=name, bg="#fafafa", fg="black",
                    relief="groove", font=("Arial", 10), width=15,
                    command=lambda url=url: open_site(url))
    btn.pack(pady=2)

# ================= Main Content Area =================
main_frame = tk.Frame(root, bg="#f4f4f4")
main_frame.pack(fill="both", expand=True)

label_title = tk.Label(main_frame, text="Welcome to SwiftSurf 🌐",
                       font=("Arial", 22, "bold"), bg="#f4f4f4", fg="black")
label_title.pack(pady=50)

search_box = tk.Entry(main_frame, font=("Arial", 15), width=45,
                      bd=2, relief="solid", bg="white")
search_box.pack(pady=10)

search_button = tk.Button(main_frame, text="Search 🔍",
                          font=("Arial", 12, "bold"), bg="#28a745", fg="white",
                          width=18, command=search)
search_button.pack(pady=5)

voice_button = tk.Button(main_frame, text="🎤 Voice Search",
                         font=("Arial", 12, "bold"), bg="#0078d7", fg="white",
                         width=18, command=voice_search)
voice_button.pack(pady=5)

# ================= Bottom Bar (Weather + Time) =================
bottom_frame = tk.Frame(root, bg="#e0e0e0", height=30)
bottom_frame.pack(side="bottom", fill="x")

def open_weather():
    webbrowser.open_new_tab("https://weather.com/en-IN/")

weather_button = tk.Button(bottom_frame, text="🌦 Weather", bg="#0078d7", fg="white",
                           font=("Arial", 10, "bold"), bd=0, width=10, command=open_weather)
weather_button.pack(side="left", padx=15, pady=3)

time_label = tk.Label(bottom_frame, text="", bg="#e0e0e0", fg="black",
                      font=("Arial", 10, "bold"))
time_label.pack(side="right", padx=15)

def update_time():
    now = datetime.datetime.now()
    formatted = now.strftime("%A, %d %B %Y | %I:%M:%S %p")
    time_label.config(text=formatted)
    root.after(1000, update_time)

update_time()

# ================= Run App =================
root.mainloop()




