from flask import Blueprint, render_template, jsonify, request, session, flash, redirect, url_for
from App.controllers import initialize
from sqlalchemy import or_
from App.models import Apartment, Review, User, db, VerifiedTenant
from flask_jwt_extended import jwt_required, get_jwt_identity

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
    results = []
    
    if request.method == 'POST':
        query = Apartment.query

        location = request.form.get('location', '')
        min_price = request.form.get('min_price', type=float)
        max_price = request.form.get('max_price', type=float)
        bedrooms = request.form.get('bedrooms', type=int)
        bathrooms = request.form.get('bathrooms', type=int)

        # Filter location
        if location:
            location_term = f"%{location}%"
            query = query.filter(or_(
                Apartment.city.ilike(location_term),
                Apartment.state.ilike(location_term),
                Apartment.zip_code.ilike(location_term)
            ))
        
        # Filter price range
        if min_price is not None:
            query = query.filter(Apartment.price >= min_price)
        if max_price is not None:
            query = query.filter(Apartment.price <= max_price)

        if bedrooms:
            query = query.filter(Apartment.bedrooms >= bedrooms)
        if bathrooms:
            query = query.filter(Apartment.bathrooms >= bathrooms)

        apartments = query.all()

        # Filter by amenities checkboxes
        amenities_filter = {
            "Air Conditioning": request.form.get("has_ac"),
            "Heating": request.form.get("has_heating"),
            "Washer": request.form.get("has_washer_dryer"),
            "Dishwasher": request.form.get("has_dishwasher"),
            "Parking": request.form.get("has_parking"),
            "Gym": request.form.get("has_gym"),
            "Pool": request.form.get("has_pool"),
            "Pet Friendly": request.form.get("has_pet_friendly"),
            "Furnished": request.form.get("has_furnished")
        }

        filtered_apartments = []
        for apartment in apartments:
            amenity_names = [a.name for a in apartment.amenities]
            include_apartment = all(
                amenity in amenity_names
                for amenity, checked in amenities_filter.items() if checked
            )
            if include_apartment:
                filtered_apartments.append(apartment)

        results = filtered_apartments

    return render_template('search.html', results=results)

@index_views.route('/dashboard')
@jwt_required()
def dashboard():
    current_user = get_jwt_identity()
    
    user = User.query.get(current_user)
    
    if user.role == 'landlord':
        listings = Apartment.query.filter_by(owner_id=user.id).all()
        unverified_tenants = User.query.filter_by(role='tenant', is_verified=False).all()
        
        return render_template('dashboard.html', listings=listings, unverified_tenants=unverified_tenants, current_user=user)
    else:
        reviews = Review.query.filter_by(user_id=user.id).all()
        return render_template('dashboard.html', reviews=reviews, current_user=user)

@index_views.route('/verify_by_username', methods=['POST'])
@jwt_required()
def verify_by_username():
    landlord_id = get_jwt_identity()           # landlord’s user id
    landlord    = User.query.get(landlord_id)

    apartment_id = request.form.get('apartment_id', type=int)
    apartment    = Apartment.query.get_or_404(apartment_id)

    if apartment.owner_id != landlord.id:
        flash("That’s not your listing.", "error")
        return redirect(url_for('index_views.dashboard'))

    username = request.form.get('username')
    tenant   = User.query.filter_by(username=username, role='tenant').first()
    if not tenant:
        flash("User not found or not a tenant.", "error")
        return redirect(url_for('index_views.dashboard'))

    exists = VerifiedTenant.query.get((apartment.id, tenant.id))
    if not exists:
        vt = VerifiedTenant(apartment_id=apartment.id,
                            tenant_id=tenant.id,
                            verified_by=landlord.id)
        db.session.add(vt)

        if not tenant.is_verified:
            tenant.is_verified = True

        db.session.commit()
        flash(f"{tenant.username} is now verified for “{apartment.title}”.",
              "success")
    else:
        flash("Tenant already verified for this listing.", "info")

    return redirect(url_for('index_views.dashboard'))