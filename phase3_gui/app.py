import tkinter as tk 
from tkinter import messagebox
import requests

def search_ad():
    ad_id = entry_id.get()
    if not ad_id.isdigit():
        messagebox.showerror("Error", "Please enter a valid ID(numbers only")
        return
    
    url = f"http://127.0.0.1:8000/ads/{ad_id}"
    response = requests.get(url)
    
    if response.status_code == 200:
        ad_data = response.json()
        display_ad(ad_data)
    else:
        messagebox.showerror("Error"f"failed to fetch ad. Status code: {response.status_code}")
        Message: {response.text}
def display_ad(ad_data):
    for widget in frame_details.winfo_children():
        widget.destroy()
        
    tk.Label(frame_details, text=f"عنوان:{ad_data.get('title', 'N/A')}", font=("Arial",12)).pack(pady=5)
    tk.Label(frame_details, text=f"قیمت: {ad_data.get('price', 'N/A')}", font=("Arial", 12)).pack(pady=5)
    tk.Label(frame_details, text=f"منطقه: {ad_data.get('region', 'N/A')}", font=("Arial", 12)).pack(pady=5)
    tk.Label(frame_details, text=f"متراژ: {ad_data.get('area', 'N/A')} sqm", font=("Arial", 12)).pack(pady=5)
    
#Main Window
root = tk.Tk()
root.title("Divar Ad Search")
root.geometry("400x300")
root.configure(bg="#f0f0f0")

#Input Frame 
frame_input = tk.Frame(root, bg="#f0f0f0")
frame_input.pack(pady=20)

tk.Label(frame_input, text="Enter AD ID:", font=("Arial", 12), bg="#f0f0f0").pack(side=tk.LEFT, padx=5)
entry_id = tk.Entry(frame_input, font=("Arial",12), width=10)
entry_id.pack(side=tk.LEFT,padx=5)
tk.Button(frame_input, text="Search", font=("Arial", 12), bg="#4CAF50", fg="white",command=search_ad).pack(side=tk.LEFT, padx=5)

#Detail
frame_details = tk.Frame(root, bg="#f0f0f0")
frame_details.pack(pady=20)
frame_input.place(relx=0.5,rely=0.3,anchor=tk.CENTER)
frame_details.place(relx=0.5,rely=0.6, anchor=tk.CENTER)

root.mainloop()