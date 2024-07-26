from flask import Flask, request, redirect, render_template
from flask_sqlalchemy import SQLAlchemy
import string
import random

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///urls.db'
db = SQLAlchemy(app)

class URLMapping(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    original_url = db.Column(db.String(500), nullable=False)
    short_url = db.Column(db.String(10), unique=True, nullable=False)
    clicks = db.Column(db.Integer, default=0)

def generate_short_url(length=6):
    characters = string.ascii_letters + string.digits
    return ''.join(random.choice(characters) for _ in range(length))

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        original_url = request.form['url']
        short_url = generate_short_url()
        new_url_mapping = URLMapping(original_url=original_url, short_url=short_url)
        db.session.add(new_url_mapping)
        db.session.commit()
        return render_template('index.html', short_url=short_url)
    return render_template('index.html')

@app.route('/<short_url>')
def redirect_url(short_url):
    url_mapping = URLMapping.query.filter_by(short_url=short_url).first_or_404()
    url_mapping.clicks += 1
    db.session.commit()
    return redirect(url_mapping.original_url)

@app.route('/analytics')
def analytics():
    url_mappings = URLMapping.query.all()
    return render_template('analytics.html', url_mappings=url_mappings)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # Create database tables
    app.run(debug=True)
