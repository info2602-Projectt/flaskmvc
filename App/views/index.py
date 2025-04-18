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

@index_views.route('/search', methods=['GET', 'POST'])
def search():
    form = SearchForm()
    results = []
    
    if request.method == 'POST' and form.validate():
        query = Apartment.query
        
        # Filter by location if provided
        if form.location.data:
            location_term = f"%{form.location.data}%"
            query = query.filter(or_(
                Apartment.city.ilike(location_term),
                Apartment.state.ilike(location_term),
                Apartment.zip_code.ilike(location_term)
            ))
        
        # Filter by price range if provided
        if form.min_price.data:
            query = query.filter(Apartment.price >= form.min_price.data)
        if form.max_price.data:
            query = query.filter(Apartment.price <= form.max_price.data)
        
        # Filter by bedrooms and bathrooms if not 'Any'
        if form.bedrooms.data > 0:
            query = query.filter(Apartment.bedrooms >= form.bedrooms.data)
        if form.bathrooms.data > 0:
            query = query.filter(Apartment.bathrooms >= form.bathrooms.data)
        
        # Get all apartments matching the base filters
        apartments = query.all()
        
        # Filter by amenities manually (since we need to check multiple amenities per apartment)
        filtered_apartments = []
        for apartment in apartments:
            amenity_names = [a.name for a in apartment.amenities]
            
            # Check if all selected amenities are present
            include_apartment = True
            
            if form.has_ac.data and "Air Conditioning" not in amenity_names:
                include_apartment = False
            if form.has_heating.data and "Heating" not in amenity_names:
                include_apartment = False
            if form.has_washer_dryer.data and "Washer/Dryer" not in amenity_names:
                include_apartment = False
            if form.has_dishwasher.data and "Dishwasher" not in amenity_names:
                include_apartment = False
            if form.has_parking.data and "Parking" not in amenity_names:
                include_apartment = False
            if form.has_gym.data and "Gym" not in amenity_names:
                include_apartment = False
            if form.has_pool.data and "Pool" not in amenity_names:
                include_apartment = False
            if form.has_pet_friendly.data and "Pet Friendly" not in amenity_names:
                include_apartment = False
            if form.has_furnished.data and "Furnished" not in amenity_names:
                include_apartment = False
            
            if include_apartment:
                filtered_apartments.append(apartment)
        
        results = filtered_apartments
    
    return render_template('search.html', form=form, results=results)
