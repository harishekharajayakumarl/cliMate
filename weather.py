import tkinter as tk
import requests
from tkinter import messagebox
from PIL import Image, ImageTk
import ttkbootstrap

def get_weather(city):
    api_key = "ca5aab6c3d45a8f256b2b9b20c9e1c32"
    url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}"
    res = requests.get(url)

    if res.status_code == 404:
        messagebox.showerror("Error! City not found...")
        return None

    weather = res.json()
    icon_id = weather['weather'][0]['icon']
    temperature = weather['main']['temp'] - 273.15
    description = weather['weather'][0]['description']
    city_name = weather['name']
    country = weather['sys']['country']

    icon_url = f"https://openweathermap.org/img/wn/{icon_id}@2x.png"
    return {'icon_url': icon_url, 'temperature': temperature, 'description': description, 'city': city_name, 'country': country}

def search():
    city = city_entry.get()
    result = get_weather(city)
    if result is None:
        return

    location_label.configure(text=f"{result['city']}, {result['country']}")
    image = Image.open(requests.get(result['icon_url'], stream=True).raw)
    icon = ImageTk.PhotoImage(image)
    icon_label.configure(image=icon)
    icon_label.image = icon

    temperature_label.configure(text=f"Temperature: {result['temperature']:.2f}°C")
    description_label.configure(text=f"Description: {result['description']}")

root = ttkbootstrap.Window(themename="morph")
root.title("cli-MATE")
root.geometry("500x500")  # Increase the size of the window

city_entry = ttkbootstrap.Entry(root, font="Helvetica,18")
city_entry.pack(pady=10)

search_button = ttkbootstrap.Button(root, text="Search", command=search, bootstyle="warning")
search_button.pack(pady=10)

location_label = tk.Label(root, font="Helvetica, 25")
location_label.pack(pady=20)

icon_label = tk.Label(root)
icon_label.pack()

temperature_label = tk.Label(root, font="Helvetica, 20")
temperature_label.pack()

description_label = tk.Label(root, font="Helvetica, 20")
description_label.pack()

root.mainloop()
