from flask import Flask,render_template,Markup
import pymongo
import mission_to_mars

app=Flask(__name__)

conn = "mongodb://localhost:27017"
client = pymongo.MongoClient(conn)
db = client.marsDB

@app.route("/")
def home():
    mars_dic=db.mars.find_one()
    return render_template("index.html",mars=mars_dic)

@app.route("/scrape")
def scraper():
    db.mars.drop()
    mars_data=mission_to_mars.scrape()
    db.mars.insert(mars_data)
    return render_template("index.html", mars=mars_data)

if __name__ == "__main__":
    app.run(debug=True)