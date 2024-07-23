from flask import Flask, render_template, jsonify
from apscheduler.schedulers.background import BackgroundScheduler
import requests
from bs4 import BeautifulSoup
app = Flask(__name__)
data = []
def scrape_data():
 global data
 url = "https://www.nseindia.com/ "
 response = requests.get(url)
 soup = BeautifulSoup(response.content, 'html.parser')
 # Extract the necessary data here
 new_data = [item.get_text() for item in
soup.select('YOUR_SELECTOR_HERE')]
 data = new_data
scheduler = BackgroundScheduler()
scheduler.add_job(func=scrape_data, trigger="interval", minutes=5)
scheduler.start()
@app.route('/')
def index():
 return render_templates('index.html', data=data)
@app.route('/data', methods=['GET'])
def get_data():
 return jsonify(data)
if __name__ == '__main__':
 scrape_data()
 app.run(debug=True)
