from flask import Flask, render_template, request
from flask_pymongo import PyMongo
import random
app = Flask(__name__)
app.config["MONGO_URI"] = "mongodb+srv://vaivai:1RJJ1JifgOc8VCos@cluster0.ualrt.mongodb.net/Music-Player"
app.config["SECRET_KEY"] = "safe^&*hdgahksdg"
mongo = PyMongo(app)
@app.route("/", methods = ["GET", "POST"])
def index():
    music_files = list(mongo.db.Music_Files.find())
    if request.args.get("Path"):
        selected_song = request.args.get("Path")
        return render_template("index.html", music_files=music_files, selected_song=selected_song[1:-1], selected_song_name=request.args.get("Name"))
    return render_template("index.html", music_files=music_files, selected_song=None, selected_song_name=None)

@app.route("/previous", methods=["GET"])
def previous():
    music_files = list(mongo.db.Music_Files.find())
    selected_song = request.args.get("Path")
    if selected_song and selected_song.strip():
        current_index = -1
        for i, song in enumerate(music_files):
            if song["Path"] == selected_song:
                current_index = i
                break
        if current_index != -1:
            previous_index = (current_index - 1) % len(music_files)
            return render_template("index.html", music_files=music_files, selected_song=music_files[previous_index]["Path"][1:-1], selected_song_name=music_files[previous_index]["Name"])
    return render_template("index.html", music_files=music_files, selected_song=None)

@app.route("/next", methods=["GET"])
def next():
    music_files = list(mongo.db.Music_Files.find())
    selected_song = request.args.get("Path")
    if selected_song and selected_song.strip():
        current_index = -1
        for i, song in enumerate(music_files):
            if song["Path"] == selected_song:
                current_index = i
                break
        if current_index != -1:
            next_index = (current_index + 1) % len(music_files)
            return render_template("index.html", music_files=music_files, selected_song=music_files[next_index]["Path"][1:-1], selected_song_name=music_files[next_index]["Name"])
    return render_template("index.html", music_files=music_files, selected_song=music_files[0]["Path"], selected_song_name=music_files[0]["Name"])

@app.route("/shuffle", methods = ["GET"])
def shuffle():
    music_files = list(mongo.db.Music_Files.find())
    random_song = random.choice(music_files)
    return render_template("index.html", music_files=music_files, selected_song=random_song["Path"][1:-1], selected_song_name=random_song["Name"])

@app.route("/repeat", methods = ["GET"])
def repeat():
    music_files = list(mongo.db.Music_Files.find())
    selected_song = request.args.get("Path")
    if selected_song:
        return render_template("index.html", music_files=music_files, selected_song=selected_song[1:-1], selected_song_name=next((song["Name"] for song in music_files if song["Path"] == selected_song), ""))
    return render_template("index.html", music_files=music_files, selected_song=None, selected_song_name=None)

if __name__ == "__main__":
    app.run(debug = True)