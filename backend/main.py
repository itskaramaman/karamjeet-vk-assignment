from flask import Flask, jsonify, request
from flask_cors import CORS
from sqlalchemy.exc import SQLAlchemyError

from BBCNewsScrapper import BBCNewsScrapper
from models import News, db
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

    try:
        with db.session.begin():
            # Delete previous data to avoid duplicates
            db.session.query(News).delete()
    
            # Scrape general news
            for category in news_categories:
                news_data = scrapper.get_news(category=category)

                # Store the scraped data in the database
                for item in news_data:
                    news = News(
                        headline=item['headline'],
                        description=item.get('description'),
                        category=category,  # Example: "General", "Technology"
                        sub_category=None,  # No subcategory for general news
                        image_url=item.get('image_url'),
                        news_link=item.get('news_link'),
                        last_updated=item.get('last_updated'),
                        tag=item.get('tag')
                    )
                    db.session.add(news)

            # Scrape sports news with subcategories
            for sub_category in sports_category:
                sports_news = scrapper.get_sports_news(category=sub_category)

                for item in sports_news:
                    sport_news = News(
                        headline=item['headline'],
                        description=None,  # Sports news may not have a description
                        category="sports",  # All sports news belongs to the "sports" category
                        sub_category=sub_category,  # Example: "Football", "Cricket"
                        image_url=item.get('image_url'),
                        news_link=item.get('news_link'),
                        last_updated=item.get('last_updated'),
                        tag=item.get('tag')
                    )
                    db.session.add(sport_news)

   
        scrapper.close_driver()  # Close the scraper after use
        return jsonify({"message": "Data scraped and stored successfully!"})
    
    except SQLAlchemyError as e:
        db.session.rollback()  # Rollback changes on failure
        scrapper.close_driver()  # Ensure the scraper is closed
        return jsonify({"error": "Database error occurred", "details": str(e)}), 500



@app.route('/data', methods=['GET'])
@app.route('/data/<category>', methods=['GET'])
@app.route('/data/<category>/<sub_category>', methods=['GET'])
def get_data(category=None, sub_category=None):
    """Retrieve news data, including sports with subcategories, with pagination."""

    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 12, type=int)

    query = db.session.query(News)
    
    if category:
        query = query.filter_by(category=category)  # Example: category="Sports"
    
    if sub_category:
        query = query.filter_by(sub_category=sub_category)  # Example: sub_category="Football"

    paginated_news = query.paginate(page=page, per_page=per_page, error_out=False)

    data = [
        {
            "id": news.id,
            "headline": news.headline,
            "description": news.description,
            "image_url": news.image_url,
            "news_link": news.news_link,
            "last_updated": news.last_updated,
            "tag": news.tag,
            "category": news.category,  # Include category in the response
            "sub_category": news.sub_category,  # Include subcategory in response
        }
        for news in paginated_news.items
    ]

    return jsonify({
        "news": data,
        "total": paginated_news.total,
        "page": paginated_news.page,
        "per_page": paginated_news.per_page,
        "pages": paginated_news.pages,
        "has_next": paginated_news.has_next,
        "has_prev": paginated_news.has_prev
    })


@app.route("/delete/<id>", methods=["DELETE"])
def delete_news(id):
    """Delete News from DB (General or Sports)"""
    try:
        news_item = db.session.get(News, id)
        if not news_item:
            return jsonify({"error": "News item not found"}), 404
        
        db.session.delete(news_item)
        db.session.commit()
        return jsonify({"message": "News item deleted successfully", "id": id})

        return jsonify({"error": "News item not found"})
    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({"error": "Database error occurred", "details": str(e)}), 500


if __name__ == "__main__":
    # Create database and tables in models.py if does not exists.
    with app.app_context():
        db.create_all()
    app.run(debug=True)
