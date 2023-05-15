import os
import random
import sqlite3
from flask import Flask, request, render_template, url_for, redirect, render_template_string, jsonify
from bs4 import BeautifulSoup
import csv
import re

app = Flask(__name__, template_folder='templates')

# get a list of all player image filenames in the player_faces folder
player_images = os.listdir("static/player_faces")
# shuffle the list of player image filenames
random.shuffle(player_images)

def get_player_name(player_id):
    with open('static/Stats.csv', encoding="utf-8") as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            if row[0] == player_id:
                player_name = row[1]
                player_name_fixed = re.sub('[^a-zA-Z0-9 \n\.]', '', player_name)
                return player_name_fixed
    return None

def get_player_age(player_id):
    with open('static/Stats.csv', encoding="utf-8") as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            if row[0] == player_id:
                player_age = row[2]
                return player_age
    return None

def get_player_ppg(player_id):
    with open('static/Stats.csv', encoding="utf-8") as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            if row[0] == player_id:
                player_ppg = row[4]
                return player_ppg
    return None

with open("templates/index.html", encoding="utf-8") as file:
    soup = BeautifulSoup(file, 'html.parser')

@app.route('/', methods=['POST', 'GET'])
def index():
    # Connect to the database
    conn = sqlite3.connect('mydatabase.db')
    c = conn.cursor()

    players = []

    # find all the image tags and update their src attributes with the random filenames
    for i, img in enumerate(soup.find_all('img', class_='player-image')):
        #APPENDING TO HTML
        img['src'] = f"{{{{ url_for('static', filename='player_faces/{player_images[i]}') }}}}"
        img.parent['data-image'] = player_images[i][:-4]
        img.parent['data-player-name'] = get_player_name(img.parent['data-image'])
        img.parent['data-player-age'] = get_player_age(img.parent['data-image'])
        img.parent['data-player-ppg'] = get_player_ppg(img.parent['data-image'])

        #PREPPING DICTIONARY
        player_id = img.parent['data-image']
        player_name = img.parent['data-player-name']
        player_age = img.parent['data-player-age']
        player_ppg = img.parent['data-player-ppg']
        player_img = f'static/player_faces/{player_images[i]}'

        c.execute("SELECT AVG(CAST(SUBSTR(dropzone_id, 10) AS INTEGER)) FROM player_real WHERE data_image = ?",
                  (player_id,))
        avg_ranking = c.fetchone()[0]

        players.append({
                'id': player_id,
                'name': player_name,
                'age': player_age,
                'ppg': player_ppg,
                'avg_ranking': avg_ranking,
                'image': player_img
            })
    # save the updated HTML back to the file
    with open("templates/index.html", "w", encoding="utf-8") as output_file:
        output_file.write(str(soup))

    return render_template('index.html', players=players)

@app.route('/submit', methods=['POST', 'GET'])
def submit():
    # Get the data from the AJAX request
    data = request.get_json()

    # Connect to the database
    conn = sqlite3.connect('mydatabase.db')
    c = conn.cursor()

    # Loop over the data and insert each record into the database
    for record in data:
        dropzone_id = record['dropzone_id']
        data_image = record['data_image']
        data_player_name = record['data_player_name']
        c.execute("INSERT INTO player_real (dropzone_id, data_image, data_player_name) VALUES (?, ?, ?)", (dropzone_id, data_image, data_player_name))

    conn.commit()
    conn.close()
    return "submitted"

if __name__ == "__main__":
    app.run(debug=True)
