import requests
from PIL import Image
from io import BytesIO
from fuzzywuzzy import process

# Optional: Enable voice
ENABLE_VOICE = True
if ENABLE_VOICE:
    import speech_recognition as sr

# Fields user can ask about
ALLOWED_FIELDS = {
    "title": "Title",
    "year": "Year",
    "released": "Released",
    "director": "Director",
    "actors": "Actors",
    "plot": "Plot",
    "genre": "Genre",
    "language": "Language",
    "country": "Country",
    "awards": "Awards",
    "imdb rating": "imdbRating",
    "runtime": "Runtime",
    "poster": "Poster"
}

def get_user_input():
    if ENABLE_VOICE:
        recognizer = sr.Recognizer()
        with sr.Microphone() as source:
            print("🎙️ Speak now...")
            audio = recognizer.listen(source)
            try:
                text = recognizer.recognize_google(audio)
                print(f"You said: {text}")
                return text
            except Exception as e:
                print("Voice recognition failed. Falling back to text.")
    return input("Ask about any movie (or type 'exit' to quit): ")

def extract_movie_and_fields(query):
    query = query.lower()
    
    # Use fuzzy match to find relevant fields
    found_fields = []
    for word in query.split():
        match, score = process.extractOne(word, ALLOWED_FIELDS.keys())
        if score > 80 and match not in found_fields:
            found_fields.append(match)

    # Attempt to extract movie name heuristically
    for sep in ["of", "about", "on"]:
        if sep in query:
            movie = query.split(sep)[-1].strip().title()
            return found_fields, movie

    return found_fields, None

def fetch_movie_data(movie_title):
    baseurl = "http://www.omdbapi.com/"
    params = {
        "t": movie_title,
        "apikey": "b8e811a1"
    }
    response = requests.get(baseurl, params=params)
    return response.json()

def show_poster(url):
    try:
        img_response = requests.get(url)
        img = Image.open(BytesIO(img_response.content))
        img.show()
    except:
        print("Could not display poster.")

def respond_to_query(query):
    fields, movie = extract_movie_and_fields(query)

    if not movie:
        print("Could not detect the movie name. Try rephrasing your question.")
        return

    data = fetch_movie_data(movie)

    if data.get("Response") != "True":
        print(f"❌ Movie '{movie}' not found.")
        return

    print(f"\n🎬 Movie: {data['Title']}")
    for field in fields:
        api_key = ALLOWED_FIELDS[field]
        value = data.get(api_key, "Not available")
        if field == "poster" and value != "N/A":
            print("🖼️ Displaying Poster...")
            show_poster(value)
        else:
            print(f"{field.title()}: {value}")

# ----- Chat Loop -----
while True:
    user_input = get_user_input()
    if user_input.lower() in ["exit", "quit"]:
        break
    respond_to_query(user_input)
