from flask import Flask, jsonify
from models import db
from BBCNewsScrapper import BBCNewsScrapper
from models import News, SportsNews, db
from flask_cors import CORS
from utils import news_categories, sports_category

app = Flask(__name__)
CORS(app)

# Configure app for sqlite database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///scraped_data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize db
db.init_app(app)


@app.route('/scrape-news', methods=['GET'])
def scrape_data():
    """Route to trigger scraping and storing news data"""
    scrapper = BBCNewsScrapper()

    # Delete the previous data to avoid duplicates
    News.query.delete()
    SportsNews.query.delete()


    for category in news_categories:
        news_data = scrapper.get_news(category=category)
        
        # Store the scraped data in the database
        for item in news_data:
            news = News(
                headline=item['headline'],
                description=item.get('description'),
                category=category,
                image_url=item.get('image_url'),
                news_link=item.get('news_link'),
                last_updated=item.get('last_updated'),
                tag=item.get('tag')
            )
            db.session.add(news)


    for category in sports_category:
        sports_news = scrapper.get_sports_news(category=category)

        for item in sports_news:
            sport_news = SportsNews(
                headline=item['headline'],
                news_link=item['news_link'],
                image_url=item['image_url'],
                tag=item['tag'],
                last_updated=item['last_updated'],
                category=category
            )
            db.session.add(sport_news)
    
    db.session.commit()
    
    scrapper.close_driver()  # Close the scraper after use
    return jsonify({"message": "Data scraped and stored successfully!"})


@app.route('/data', methods=['GET'])
@app.route('/data/<category>', methods=['GET'])
def get_data(category=None):
    """Retrieve scraped data from the database."""
    if not category:
        news_data = News.query.all()
    else:
        news_data = News.query.filter_by(category=category).all()
    data = []
    for news in news_data:
        data.append({
            "id": news.id,
            "headline": news.headline,
            "description": news.description,
            "image_url": news.image_url,
            "news_link": news.news_link,
            "last_updated": news.last_updated,
            "tag": news.tag,
        })

    return jsonify(data)


@app.route('/sports-data', methods=['GET'])
@app.route('/sports-data/<category>', methods=['GET'])
def get_sports_data(category=None):
    """Retrieve scraped data from the database."""
    if not category:
        sports_data = SportsNews.query.all()
    else:
        sports_data = SportsNews.query.filter_by(category=category).all()
    
    data = []
    for item in sports_data:
        data.append({
            "id": item.id,
            "headline": item.headline,
            "image_url": item.image_url,
            "news_link": item.news_link,
            "last_updated": item.last_updated,
            "tag": item.tag,
        })

    return jsonify(data)


@app.route("/delete/<id>", methods=["DELETE"])
def delete_news(id):
    """Delete News from DB""" 
    news_item = db.session.get(News, id)
    if news_item:
        db.session.delete(news_item)
        db.session.commit()
        return jsonify({"message": "News item deleted successfully", "id": id})

    sports_news_item = db.session.get(SportsNews, id)
    if sports_news_item:
        db.session.delete(sports_news_item)
        db.session.commit()
        return jsonify({"message": "Sports news item deleted successfully", "id": id})

    return jsonify({"error": "News item not found"})
  

if __name__ == "__main__":
    # Create database and tables in models.py if does not exists. 
    with app.app_context():
        db.create_all()
    app.run(debug=True)

