import requests
from PIL import Image
from io import BytesIO

# Step 1: User input
movie = input("Enter Movie Name: ")

# Step 2: API setup
baseurl = "http://www.omdbapi.com/"
params = {
    "t": movie,
    "apikey": "b8e811a1"
}

# Step 3: Send request
response = requests.get(url=baseurl, params=params)
data = response.json()

# Step 4: Check response and display info
if data.get("Response") == "True":
    print("\nTitle:", data["Title"])
    print("Plot:", data["Plot"])

    # Step 5: Display poster
    poster_url = data.get("Poster")
    if poster_url and poster_url != "N/A":
        print("Loading poster...")

        # Get image content
        img_response = requests.get(poster_url)
        img = Image.open(BytesIO(img_response.content))
        img.show()  # This will open the image using your default image viewer
    else:
        print("Poster not available.")
else:
    print("\nMovie not found. Please check the name and try again.")
