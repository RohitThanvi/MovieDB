import tkinter as tk
import requests
from PIL import Image, ImageTk
from io import BytesIO

def fetch_movie_data(movie):
    baseurl = "http://www.omdbapi.com/"
    params = {
        "t": movie,
        "apikey": "b8e811a1"
    }
    try:
        response = requests.get(baseurl, params=params)
        data = response.json()
        if data.get("Response") == "True":
            label3.config(text=f"Actors: {data['Actors']}\nPlot: {data['Plot']}")
            
            poster_url = data.get("Poster")
            if poster_url and poster_url != "N/A":
                img_response = requests.get(poster_url)
                img = Image.open(BytesIO(img_response.content))
                img = img.resize((80, 150))  # Resize image for display
                poster_img = ImageTk.PhotoImage(img)
                
                label_img.config(image=poster_img)
                label_img.image = poster_img  # Keep reference
            else:
                label_img.config(image="", text="No Poster Available")
        else:
            label3.config(text="Movie not found!")
            label_img.config(image="")
    except Exception as e:
        label3.config(text=f"Error: {e}")

def butclik():
    search = tb.get().strip()
    if not search:
        label3.config(text="Please enter a movie name.")
        return
    label2.config(text=f"You asked: {search}")
    label2.place_configure(relx=0.0, rely=0.0, anchor="nw")
    label3.config(text=f"Searching for: {search}...")
    tb.delete(0, tk.END)
    fetch_movie_data(search)

window = tk.Tk()
window.title("Movie Bot")
window.geometry("600x600")
window.configure(bg="black")

label = tk.Label(window, text="Movie Bot", font=("Comic Sans Ms", 16), bg="green", fg="white")
label.pack(pady=20)

frame1 = tk.Frame(window, bg="blue", width=500, height=500)
frame1.pack(pady=20)
frame1.pack_propagate(False)

frame2 = tk.Frame(frame1, bg="red", width=400, height=280)
frame2.place(relx=0.5, rely=0.4, anchor="center")
frame2.pack_propagate(False)

frame3 = tk.Frame(frame1, bg="green", width=400, height=100)
frame3.place(relx=0.5, rely=0.85, anchor="center")
frame3.pack_propagate(False)

label2 = tk.Label(frame2, text="Enter your movie-related question:", font=("Arial", 14), bg="red", fg="white")
label2.place(relx=0.5, rely=0.1, anchor="center")

label3 = tk.Label(frame2, text="", font=("Arial", 12), bg="red", fg="white", wraplength=380, justify="left")
label3.place(relx=0.05, rely=0.1, anchor="nw")

label_img = tk.Label(frame2, bg="red")
label_img.place(relx=0.5, rely=1, anchor="s")

tb = tk.Entry(frame3, font=("Arial", 14), width=20, bg="white", fg="black")
tb.place(relx=0.3, rely=0.5, anchor="center")
tb.focus()

b1 = tk.Button(frame3, text="Search", font=("Arial", 12), command=butclik, width=10, bg="orange", fg="white")
b1.place(relx=0.9, rely=0.5, anchor="e")

window.mainloop()
