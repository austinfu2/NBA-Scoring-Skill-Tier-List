import os
import random
import sqlite3
from flask import Flask, request, render_template, url_for
from bs4 import BeautifulSoup
import csv
import re

app = Flask(__name__, template_folder='templates')

# get a list of all player image filenames in the player_faces folder
player_images = os.listdir("static/player_faces")
# shuffle the list of player image filenames
random.shuffle(player_images)

def get_player_name(player_id):
    with open('static/names.csv', encoding="utf-8") as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            if row[0] == player_id:
                player_name = row[1]
                player_name_fixed = re.sub('[^a-zA-Z0-9 \n\.]', '', player_name)
                return player_name_fixed
    return None

with open("templates/index.html", encoding="utf-8") as file:
    soup = BeautifulSoup(file, 'html.parser')

@app.route('/')
def index():
    # find all the image tags and update their src attributes with the random filenames
    for i, img in enumerate(soup.find_all('img', class_='player-image')):
        img['src'] = f"{{{{ url_for('static', filename='player_faces/{player_images[i]}') }}}}"
        img.parent['data-image'] = player_images[i][:-4]
        img.parent['data-player-name'] = get_player_name(img.parent['data-image'])

    # save the updated HTML back to the file
    with open("templates/index.html", "w", encoding="utf-8") as output_file:
        output_file.write(str(soup))

    return render_template('index.html')

@app.route('/results', methods=['POST'])
def results():
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

    # Calculate the average dropzone ranking for the 8 players
    player_averages = {}
    for record in data:
        player_id = record['data_image']
        c.execute("SELECT AVG(CAST(SUBSTR(dropzone_id, 10) AS INTEGER)) FROM player_real WHERE data_image = ?",
                  (player_id,))
        avg_ranking = c.fetchone()[0]
        player_averages[player_id] = avg_ranking

    # Commit the changes and close the connection
    conn.commit()
    conn.close()

    # Return a success response
    return render_template("results.html", player_averages=player_averages)

if __name__ == "__main__":
    app.run(debug=True)
