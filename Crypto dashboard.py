import requests
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime
import plotly.graph_objs as go
from plotly.offline import plot


api_key = "CG-usNERbcuAaA32z4B4vubasdP"
base_url = "https://api.coingecko.com/api/v3"
last_prices = []  # To store the last fetched prices

def fetch_prices():
    global last_prices
    token = token_entry.get().strip().lower()
    currency = currency_entry.get().strip().lower()
    days = interval_entry.get().strip()
    if not token or not currency or not days:
        messagebox.showerror("Input Error", "Please fill in all fields.")
        return

    endpoint = f"/coins/{token}/market_chart"
    params = {
        "vs_currency": currency,
        "days": days,
        "x_cg_demo_api_key": api_key
    }
    try:
        response = requests.get(f"{base_url}{endpoint}", params=params)
        response.raise_for_status()
        data = response.json()
        prices = data.get("prices", [])
        last_prices = prices  # Store for plotting
        if not prices:
            result_text.delete(1.0, tk.END)
            result_text.insert(tk.END, "No price data found.")
            return
        # Show the first 5 price points as a sample
        result_text.delete(1.0, tk.END)
        result_text.insert(tk.END, f"Showing {min(5, len(prices))} of {len(prices)} price points:\n")
        for i, (timestamp, price) in enumerate(prices[:5]):
            # Convert milliseconds to seconds, then to datetime
            dt = datetime.fromtimestamp(timestamp / 1000)
            time_str = dt.strftime('%H:%M:%S')
            result_text.insert(tk.END, f"{i+1}. Time: {time_str}, Price: {price} {currency.upper()}\n")
    except requests.exceptions.RequestException as e:
        result_text.delete(1.0, tk.END)
        result_text.insert(tk.END, f"Error making API call: {e}\n")
        if 'response' in locals():
            result_text.insert(tk.END, f"Response status code: {response.status_code}\n")
            result_text.insert(tk.END, f"Response body: {response.text}\n")

def show_line_graph():
    if not last_prices:
        messagebox.showinfo("No Data", "Please fetch prices first.")
        return
    times = [datetime.fromtimestamp(ts / 1000) for ts, _ in last_prices]
    values = [price for _, price in last_prices]
    trace = go.Scatter(x=times, y=values, mode='lines+markers', name='Price')
    layout = go.Layout(title='Crypto Price Over Time', xaxis=dict(title='Time'), yaxis=dict(title='Price'))
    fig = go.Figure(data=[trace], layout=layout)
    plot(fig, auto_open=True)

def export_csv():
    if not last_prices:
        messagebox.showinfo("No Data", "Please fetch prices first.")
        return
    # Prepare data for DataFrame
    dates = [datetime.fromtimestamp(ts / 1000).strftime('%Y-%m-%d') for ts, _ in last_prices]
    times = [datetime.fromtimestamp(ts / 1000).strftime('%H:%M:%S') for ts, _ in last_prices]
    values = [price for _, price in last_prices]
    df = pd.DataFrame({"Date": dates, "Timestamp": times, "Price": values})
    # Ask user where to save
    file_path = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV files", "*.csv")])
    if file_path:
        df.to_csv(file_path, index=False)
        messagebox.showinfo("Export Successful", f"Data exported to {file_path}")

root = tk.Tk()
root.title("Crypto Price Dashboard")

mainframe = ttk.Frame(root, padding="10")
mainframe.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

ttk.Label(mainframe, text="Token Ticker (e.g. tether, bitcoin):").grid(row=0, column=0, sticky=tk.W)
token_entry = ttk.Entry(mainframe, width=20)
token_entry.insert(0, "tether")
token_entry.grid(row=0, column=1, sticky=tk.W)

ttk.Label(mainframe, text="Currency (e.g. usd, cny):").grid(row=1, column=0, sticky=tk.W)
currency_entry = ttk.Entry(mainframe, width=20)
currency_entry.insert(0, "cny")
currency_entry.grid(row=1, column=1, sticky=tk.W)

ttk.Label(mainframe, text="Time Interval (days, e.g. 1, 7, 30, 90, max):").grid(row=2, column=0, sticky=tk.W)
interval_entry = ttk.Entry(mainframe, width=20)
interval_entry.insert(0, "90")
interval_entry.grid(row=2, column=1, sticky=tk.W)

fetch_button = ttk.Button(mainframe, text="Fetch Prices", command=fetch_prices)
fetch_button.grid(row=3, column=0, columnspan=2, pady=10)

# Add a button to show the line graph
show_graph_button = ttk.Button(mainframe, text="Show Line Graph", command=show_line_graph)
show_graph_button.grid(row=5, column=0, columnspan=2, pady=5)

# Add a button to export as CSV
export_csv_button = ttk.Button(mainframe, text="Export as CSV", command=export_csv)
export_csv_button.grid(row=6, column=0, columnspan=2, pady=5)

result_text = tk.Text(mainframe, width=60, height=10)
result_text.grid(row=4, column=0, columnspan=2, pady=5)

root.mainloop()
