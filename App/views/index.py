from flask import Blueprint, render_template, jsonify
from App.models import Apartment  # make sure Apartment is imported
from App.controllers import initialize

index_views = Blueprint('index_views', __name__, template_folder='../templates')

@index_views.route('/', methods=['GET'])
def index_page():
    # Get the latest apartments (e.g., most recent 6)
    apartments = Apartment.query.order_by(Apartment.created_at.desc()).limit(6).all()
    return render_template('index.html', apartments=apartments)

@index_views.route('/init', methods=['GET'])
def init():
    initialize()
    return jsonify(message='db initialized!')

@index_views.route('/health', methods=['GET'])
def health_check():
    return jsonify({'status': 'healthy'})
