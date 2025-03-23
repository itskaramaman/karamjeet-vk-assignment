from flask import Flask, jsonify
from models import db
from BBCNewsScrapper import BBCNewsScrapper
from models import News
from flask_cors import CORS
from flask_cors import cross_origin

app = Flask(__name__)
CORS(app)

# Configure app for sqlite database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///scraped_data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize db
db.init_app(app)


@app.route('/scrape/news', methods=['GET'])
def scrape_data():
    """Route to trigger scraping and storing data"""
    scrapper = BBCNewsScrapper()
    categories = ["", "news", "business", "innovation", "culture", "arts", "travel", "future-planet"]

    # # Delete the previous data to avoid duplicates
    # News.query.delete()

    for category in categories:
        # Scrape news data as per category
        news_data = scrapper.get_news(category=category)
        
        # Store the scraped data in the database
        for item in news_data:
            card = News(
                headline=item['headline'],
                description=item.get('description'),
                category=category,
                image_url=item.get('image_url'),
                news_link=item.get('news_link'),
                last_updated=item.get('last_updated'),
                tag=item.get('tag')
            )
            db.session.add(card)
    
    db.session.commit()
    
    scrapper.close_driver()  # Close the scraper after use
    return jsonify({"message": "Data scraped and stored successfully!"})


@app.route('/data', methods=['GET'])
@app.route('/data/<category>', methods=['GET'])
def get_data(category=None):
    """Retrieve scraped data from the database."""
    print(category)
    if not category:
        news_data = News.query.all()
    else:
        news_data = News.query.filter_by(category=category).all()
    data = []
    for news in news_data:
        data.append({
            "headline": news.headline,
            "description": news.description,
            "image_url": news.image_url,
            "news_link": news.news_link,
            "last_updated": news.last_updated,
            "tag": news.tag,
        })

    return jsonify(data)



if __name__ == "__main__":
    # Create database and tables in models.py if does not exists. 
    with app.app_context():
        db.create_all()
    app.run(debug=True)

