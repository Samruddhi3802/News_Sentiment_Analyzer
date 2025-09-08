import requests
import tkinter as tk
from tkinter import ttk, messagebox
import matplotlib.pyplot as plt
from textblob import TextBlob

# Replace with your NewsAPI key
API_KEY = "10b312e3c7b34b61b8ce7545d238b638"

def fetch_news(country_name):
    try:
        url = f"https://newsapi.org/v2/everything"
        params = {
            'q': country_name,     # search country as keyword
            'language': 'en',
            'sortBy': 'relevancy',
            'pageSize': 10,
            'apiKey': API_KEY
        }
        response = requests.get(url, params=params)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        messagebox.showerror("Error", f"Failed to fetch news: {e}")
        return None

def analyze_sentiment(text):
    analysis = TextBlob(text)
    if analysis.sentiment.polarity > 0:
        return "Positive"
    elif analysis.sentiment.polarity < 0:
        return "Negative"
    else:
        return "Neutral"

def show_news():
    for row in tree.get_children():
        tree.delete(row)

    country_name = entry.get().strip()
    if not country_name:
        messagebox.showwarning("Input Error", "Please enter a country name (e.g., India, UK, Japan)")
        return

    data = fetch_news(country_name)
    if not data or "articles" not in data:
        return

    sentiments = {"Positive": 0, "Negative": 0, "Neutral": 0}

    for article in data["articles"]:
        title = article["title"]
        sentiment = analyze_sentiment(title)
        tree.insert("", tk.END, values=(title, sentiment))
        sentiments[sentiment] += 1

    # Plot Bar Chart
    plt.figure(figsize=(6, 4))
    plt.bar(sentiments.keys(), sentiments.values(), color=["green", "red", "gray"])
    plt.title(f"News Sentiment Distribution ({country_name})")
    plt.xlabel("Sentiment")
    plt.ylabel("Count")
    plt.show()

# Tkinter GUI
root = tk.Tk()
root.title("News Sentiment Analyzer")
root.geometry("800x500")

label = tk.Label(root, text="Enter Country Name (e.g., India, UK, Japan):", font=("Arial", 12))
label.pack(pady=5)

entry = tk.Entry(root, font=("Arial", 12))
entry.pack(pady=5)

button = tk.Button(root, text="Fetch News", command=show_news, bg="lightblue", font=("Arial", 12))
button.pack(pady=10)

columns = ("Headline", "Sentiment")
tree = ttk.Treeview(root, columns=columns, show="headings", height=15)
tree.heading("Headline", text="Headline")
tree.heading("Sentiment", text="Sentiment")
tree.pack(fill=tk.BOTH, expand=True, pady=10)

root.mainloop()
