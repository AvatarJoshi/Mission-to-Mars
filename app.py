# Import dependencies
from flask import Flask, render_template, redirect, url_for
from flask_pymongo import PyMongo
import scraping

# Set up Flask
app = Flask(__name__, template_folder='Templates')

# Use flask_pymongo to set up mongo connection
app.config["MONGO_URI"] = "mongodb://localhost:27017/mars_app" # Tells Python to connect to Mongo using URI with port/db name
mongo = PyMongo(app)

# Define the route for the HTML page
@app.route("/") # Tells flask what to display when viewing homepage
def index():
    mars = mongo.db.mars.find_one() # PyMongo searches for "mars" collection in our database (in this case the default: index.html)
    return render_template("index.html", mars=mars) # Flask will return an HTML template using an index.html file

# Define scraping route
@app.route("/scrape") # Define route for Flask
def scrape():
    mars = mongo.db.mars # Variable that directs to location of our database
    mars_data = scraping.scrape_all() # Scrape the data 
    mars.update_one({}, {"$set": mars_data}, upset=True) # Gather new, unique data and update the database
    return redirect('/', code=302) # Navigate back to homepage to see updated content

# Run Flask
if __name__ == "__main__":
    app.run()