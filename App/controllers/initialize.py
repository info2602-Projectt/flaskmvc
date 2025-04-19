from .user import create_user
from App.models import Apartment, Amenity, User, Review
from App.database import db

def initialize():
    db.drop_all()
    db.create_all()

    # Create a test user
    create_user("bob", "bobpass")
    bob = User.query.filter_by(username="bob").first()
    create_user("john", "johnpass")
    john = User.query.filter_by(username="john").first()
    create_user("rick", "rickpass")
    rick = User.query.filter_by(username="rick").first()
    create_user("aidan", "aidanpass")
    aidan = User.query.filter_by(username="aidan").first()
    create_user("sham", "shampass")
    sham = User.query.filter_by(username="sham").first()
    create_user("dylan", "dylanpass")
    dylan = User.query.filter_by(username="dylan").first()
    create_user("joe", "joepass")
    joe = User.query.filter_by(username="joe").first()

    apartment1 = Apartment(
        title="Cozy Studio",
        description="Perfect for a sad, lonely person.",
        address="123 Maple Street",
        city="Port of Spain",
        state="Trinidad",
        zip_code="00001",
        price=1500.0,
        bedrooms=1,
        bathrooms=1.0,
        square_feet=450,
        image_filename="https://images.unsplash.com/photo-1588880331179-bc9b93a8cb5e?q=80&w=2070&auto=format&fit=crop&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D",
        owner_id=bob.id
    )

    apartment2 = Apartment(
        title="Spacious Two Bedroom",
        description="Ideal for a people who want two bedrooms\n contact us at 123-4567.",
        address="456 Palm Avenue",
        city="San Fernando",
        state="Trinidad",
        zip_code="00002",
        price=2800.0,
        bedrooms=2,
        bathrooms=1.5,
        square_feet=900,
        image_filename="https://images.unsplash.com/photo-1480074568708-e7b720bb3f09?q=80&w=2074&auto=format&fit=crop&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D",
        owner_id=rick.id
    )

    apartment3 = Apartment(
        title="Luxury Condo",
        description="Elegant and modern with sea view.",
        address="12 Seaside Drive",
        city="Chaguaramas",
        state="Trinidad",
        zip_code="00003",
        price=5000.0,
        bedrooms=3,
        bathrooms=2.5,
        square_feet=1200,
        image_filename="https://images.unsplash.com/photo-1522708323590-d24dbb6b0267?q=80&w=2070&auto=format&fit=crop&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D",
        owner_id=rick.id
    )

    apartment4 = Apartment(
        title="Student Apartment",
        description="Affordable and close to university.",
        address="88 Campus Road",
        city="St. Augustine",
        state="Trinidad",
        zip_code="00004",
        price=1200.0,
        bedrooms=1,
        bathrooms=1.0,
        square_feet=400,
        image_filename="https://images.unsplash.com/photo-1600596542815-ffad4c1539a9?q=80&w=2075&auto=format&fit=crop&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D",
        owner_id=bob.id
    )

    apartment5 = Apartment(
        title="Modern Loft",
        description="Stylish loft with open space design.",
        address="67 Art District",
        city="Port of Spain",
        state="Trinidad",
        zip_code="00005",
        price=3200.0,
        bedrooms=2,
        bathrooms=2.0,
        square_feet=850,
        image_filename="https://plus.unsplash.com/premium_photo-1664205028267-f93e70476e8d?q=80&w=2072&auto=format&fit=crop&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D",
        owner_id=rick.id
    )

    apartment6 = Apartment(
        title="Garden Cottage",
        description="Quiet and peaceful, surrounded by nature.",
        address="9 Garden Lane",
        city="Maraval",
        state="Trinidad",
        zip_code="00006",
        price=1800.0,
        bedrooms=1,
        bathrooms=1.0,
        square_feet=500,
        image_filename="https://images.unsplash.com/photo-1508996229940-4d4af8b9f6dc?q=80&w=2070&auto=format&fit=crop&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D",
        owner_id=bob.id
    )

    apartment7 = Apartment(
        title="City View Flat",
        description="Located on the 10th floor with stunning views.",
        address="501 City Towers",
        city="Port of Spain",
        state="Trinidad",
        zip_code="00007",
        price=3500.0,
        bedrooms=2,
        bathrooms=2.0,
        square_feet=1000,
        image_filename="https://images.unsplash.com/photo-1518780664697-55e3ad937233?q=80&w=1965&auto=format&fit=crop&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D",
        owner_id=bob.id
    )

    apartment8 = Apartment(
        title="Budget Room",
        description="Simple and functional, great for short stays.",
        address="11 Budget Street",
        city="Curepe",
        state="Trinidad",
        zip_code="00008",
        price=800.0,
        bedrooms=1,
        bathrooms=1.0,
        square_feet=300,
        image_filename="https://images.unsplash.com/photo-1561473941-869cd0e6083a?q=80&w=2070&auto=format&fit=crop&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D",
        owner_id=aidan.id
    )

    apartment9 = Apartment(
        title="Beach House",
        description="Steps away from the beach. Great for vacations.",
        address="21 Ocean Breeze Blvd",
        city="Mayaro",
        state="Trinidad",
        zip_code="00009",
        price=4200.0,
        bedrooms=3,
        bathrooms=2.0,
        square_feet=1100,
        image_filename="https://images.unsplash.com/photo-1728470879796-419a9a6895b0?q=80&w=2069&auto=format&fit=crop&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D",
        owner_id=aidan.id
    )

    db.session.add_all([
        apartment1, apartment2, apartment3,
        apartment4, apartment5, apartment6,
        apartment7, apartment8, apartment9
    ])

    db.session.flush()  # get apartment IDs


    db.session.add_all([
        Review(rating=4, comment="Nice and cozy!", apartment_id=apartment1.id, user_id=joe.id),
        Review(rating=5, comment="Loved the location.", apartment_id=apartment3.id, user_id=sham.id),
        Review(rating=3, comment="Decent for students.", apartment_id=apartment4.id, user_id=john.id),
        Review(rating=2, comment="Bit too noisy at night.", apartment_id=apartment8.id, user_id=joe.id)
    ])

    gym = Amenity(name="Gym")
    wifi = Amenity(name="WiFi")
    ac = Amenity(name="Air Conditioning")
    washer = Amenity(name="Washer")
    pool = Amenity(name="Pool")

    apartment1.amenities = [gym, wifi, pool]
    apartment2.amenities = [ac, wifi, pool,washer]
    apartment3.amenities = [wifi, ac, washer]
    apartment4.amenities = [gym, wifi]
    apartment5.amenities = [ac, wifi]
    apartment6.amenities = [ac, wifi, pool, washer]
    apartment7.amenities = [ac, wifi ,washer]
    apartment8.amenities = [ac, wifi, washer]

    db.session.commit()
