import os
import random
import sqlite3
from flask import Flask, request, render_template, url_for
from bs4 import BeautifulSoup
import csv
import re

app = Flask(__name__)

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
def home():
    # find all the image tags and update their src attributes with the random filenames
    for i, img in enumerate(soup.find_all('img', class_='player-image')):
        img['src'] = f"{{{{ url_for('static', filename='player_faces/{player_images[i]}') }}}}"
        img.parent['data-image'] = player_images[i][:-4]
        img.parent['data-player-name'] = get_player_name(img.parent['data-image'])

    # save the updated HTML back to the file
    with open("templates/index.html", "w", encoding="utf-8") as output_file:
        output_file.write(str(soup))

    # Get the current page HTML
    with open('templates/index.html', 'r') as f:
        current_page_html = f.read()

    return render_template('index.html', current_page_html=current_page_html)

@app.route('/insert', methods=['POST'])
def insert():
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
    # Commit the changes and close the connection
    conn.commit()
    conn.close()

    # Return a success response
    return render_template("results.html")

@app.route('/submit', methods=["GET", "POST"])
def submit():
    return render_template("results.html")

# define the route for the results page
@app.route('/results')
def results():
    return render_template("results.html")

# add a context processor to make the player_images list available to all templates
#@app.context_processor
#def inject_player_images():
#    return dict(player_images=player_images)

if __name__ == "__main__":
    app.run(debug=True)
