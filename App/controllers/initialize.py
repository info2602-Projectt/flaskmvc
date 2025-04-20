from .user import create_user
from App.models import Apartment, AmenityType, User, Review
from App.database import db

def initialize():
    db.drop_all()
    db.create_all()

    amenity_names = [
        "WiFi", "Gym", "Pool", "Air Conditioning",
        "Washer", "Pet Friendly", "Furnished", "Parking"
    ]
    for n in amenity_names:
        db.session.add(AmenityType(name=n))
    db.session.commit() 

    # Create users
    usernames = ["bob", "john", "rick", "aidan", "sham", "dylan", "joe"]
    for username in usernames:
        create_user(username, f"{username}pass")

    bob = User.query.filter_by(username="bob").first()
    john = User.query.filter_by(username="john").first()
    rick = User.query.filter_by(username="rick").first()
    aidan = User.query.filter_by(username="aidan").first()
    sham = User.query.filter_by(username="sham").first()
    dylan = User.query.filter_by(username="dylan").first()
    joe = User.query.filter_by(username="joe").first()

    for user in [bob, rick, aidan]:
        user.role = "landlord"

    for user in [john, sham, joe, dylan]:
        user.role = "tenant"

    # Add apartments
    apartments = [
        Apartment(
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
            image_filename="https://images.unsplash.com/photo-1588880331179-bc9b93a8cb5e",
            owner_id=bob.id
        ),
        Apartment(
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
            image_filename="https://images.unsplash.com/photo-1480074568708-e7b720bb3f09",
            owner_id=rick.id
        ),
        Apartment(
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
            image_filename="https://images.unsplash.com/photo-1522708323590-d24dbb6b0267",
            owner_id=rick.id
        ),
        Apartment(
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
            image_filename="https://images.unsplash.com/photo-1600596542815-ffad4c1539a9",
            owner_id=bob.id
        ),
        Apartment(
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
            image_filename="https://plus.unsplash.com/premium_photo-1664205028267-f93e70476e8d",
            owner_id=rick.id
        ),
        Apartment(
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
            image_filename="https://images.unsplash.com/photo-1508996229940-4d4af8b9f6dc",
            owner_id=bob.id
        ),
        Apartment(
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
            image_filename="https://images.unsplash.com/photo-1480074568708-e7b720bb3f09",
            owner_id=bob.id
        ),
        Apartment(
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
            image_filename="https://images.unsplash.com/photo-1561473941-869cd0e6083a",
            owner_id=aidan.id
        ),
        Apartment(
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
            image_filename="https://images.unsplash.com/photo-1728470879796-419a9a6895b0",
            owner_id=aidan.id
        )
    ]

    db.session.add_all(apartments)
    db.session.flush()  # So we can access apartment IDs

    # Assign amenities individually to each apartment
    def add_amenities(apartment, names):
        for name in names:
            at = AmenityType.query.filter_by(name=name).first()
            if not at:                              # create if it didn’t exist
                at = AmenityType(name=name)
                db.session.add(at)
            if at not in apartment.amenities:
                apartment.amenities.append(at)

    add_amenities(apartments[0], ["Gym", "WiFi", "Pool", "Furnished", "Parking"])
    add_amenities(apartments[1], ["Air Conditioning", "WiFi", "Pool", "Washer", "Furnished"])
    add_amenities(apartments[2], ["WiFi", "Air Conditioning", "Washer", "Pet Friendly", "Furnished"])
    add_amenities(apartments[3], ["Gym", "WiFi", "Furnished", "Parking"])
    add_amenities(apartments[4], ["Air Conditioning", "WiFi"])
    add_amenities(apartments[5], ["Air Conditioning", "WiFi", "Pool", "Washer", "Furnished"])
    add_amenities(apartments[6], ["Air Conditioning", "WiFi", "Washer", "Pet Friendly", "Furnished", "Parking"])
    add_amenities(apartments[7], ["Air Conditioning", "WiFi", "Washer", "Furnished"])
    add_amenities(apartments[8], ["Air Conditioning", "WiFi", "Pool", "Pet Friendly", "Furnished", "Parking"])

    # Add reviews
    db.session.add_all([
        Review(rating=4, comment="Nice and cozy!", apartment_id=apartments[0].id, user_id=sham.id),
        Review(rating=5, comment="Loved the location.", apartment_id=apartments[2].id, user_id=sham.id),
        Review(rating=3, comment="Decent for students.", apartment_id=apartments[3].id, user_id=john.id),
        Review(rating=3, comment="Landlord is a bit rude.", apartment_id=apartments[7].id, user_id=sham.id),
        Review(rating=1, comment="Worst Place EVER!!!", apartment_id=apartments[5].id, user_id=sham.id),
        Review(rating=4, comment="Not too shabby.", apartment_id=apartments[6].id, user_id=sham.id)
    ])

    db.session.commit()
