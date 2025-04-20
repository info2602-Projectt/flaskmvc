from flask import Blueprint, render_template, request, redirect, url_for, flash, current_app
from werkzeug.utils import secure_filename
import os

from App.models import User, AmenityType, VerifiedTenant
from flask_jwt_extended import jwt_required, get_jwt_identity

from App.controllers.apartment import (
    create_apartment,
    get_all_apartments,
    get_apartment,
    update_apartment,
    delete_apartment,
)
from App.controllers.review import create_review, get_review, delete_review
from App.database import db

apartment_views = Blueprint("apartment_views", __name__, template_folder="../templates")

# ────────────────────────────────────────────────────────────────────────────────
# LISTINGS
# ────────────────────────────────────────────────────────────────────────────────


@apartment_views.route("/apartments", methods=["GET"])
def list_apartments():
    apartments = get_all_apartments()
    return render_template("index.html", apartments=apartments)


# ────────────────────────────────────────────────────────────────────────────────
# CREATE LISTING (LANDLORD‑ONLY)
# ────────────────────────────────────────────────────────────────────────────────


@apartment_views.route("/apartments/create", methods=["GET", "POST"])
@jwt_required()
def create_listing():
    raw_user = get_jwt_identity()
    try:
        user_id = int(raw_user)
    except (TypeError, ValueError):
        user_id = None

    user = User.query.get(user_id)
    if not user or user.role != "landlord":
        flash("Only landlords can create listings.", "error")
        return redirect(url_for("apartment_views.list_apartments"))

    if request.method == "POST":
        # basic details
        title = request.form.get("title")
        description = request.form.get("description")
        address = request.form.get("address")
        city = request.form.get("city")
        state = request.form.get("state")
        zip_code = request.form.get("zip_code")
        price = request.form.get("price")
        bedrooms = request.form.get("bedrooms")
        bathrooms = request.form.get("bathrooms")
        square_feet = request.form.get("square_feet") or None

        # image handling
        image = request.files.get("image")
        image_filename = None
        if image and image.filename:
            filename = secure_filename(image.filename)
            image_filename = filename
            image.save(os.path.join(current_app.config["UPLOAD_FOLDER"], filename))

        # create DB row
        apartment = create_apartment(
            title,
            description,
            address,
            city,
            state,
            zip_code,
            price,
            bedrooms,
            bathrooms,
            user_id,
            square_feet=square_feet,
            image_filename=image_filename,
        )

        # amenities many‑to‑many
        amenity_ids = request.form.getlist("amenities")
        for a_id in amenity_ids:
            try:
                aid = int(a_id)
            except ValueError:
                continue
            amenity = AmenityType.query.get(aid)
            if amenity and amenity not in apartment.amenities:
                apartment.amenities.append(amenity)
        db.session.commit()

        flash("Listing created successfully!", "success")
        return redirect(url_for("apartment_views.list_apartments"))

    amenities = AmenityType.query.all()
    return render_template("create_listing.html", amenities=amenities)


# ────────────────────────────────────────────────────────────────────────────────
# VIEW LISTING
# ────────────────────────────────────────────────────────────────────────────────


@apartment_views.route("/apartments/<int:apartment_id>", methods=["GET"])
def view_apartment(apartment_id):
    apartment = get_apartment(apartment_id)
    if not apartment:
        flash("Listing not found", "error")
        return redirect(url_for("apartment_views.list_apartments"))
    return render_template("view_listing.html", apartment=apartment)


# ────────────────────────────────────────────────────────────────────────────────
# LEAVE REVIEW  (tenant must be verified **for this apartment**)
# ────────────────────────────────────────────────────────────────────────────────


@apartment_views.route("/apartments/<int:apartment_id>/review", methods=["GET", "POST"])
@jwt_required()
def leave_review(apartment_id):
    user_id = int(get_jwt_identity())
    user = User.query.get(user_id)
    apartment = get_apartment(apartment_id)

    # NEW PER‑PROPERTY VERIFICATION
    verified = VerifiedTenant.query.get((apartment_id, user_id))
    if not verified:
        flash("You are not verified for this property.", "error")
        return redirect(url_for("apartment_views.view_apartment", apartment_id=apartment_id))

    if request.method == "POST":
        rating = int(request.form.get("rating"))
        comment = request.form.get("comment")
        create_review(apartment_id, user_id, rating, comment)
        flash("Review submitted!", "success")
        return redirect(url_for("apartment_views.view_apartment", apartment_id=apartment_id))

    return render_template("create_review.html", apartment=apartment)


# ────────────────────────────────────────────────────────────────────────────────
# DELETE REVIEW (author only)
# ────────────────────────────────────────────────────────────────────────────────


@apartment_views.route("/apartments/<int:apartment_id>/review/<int:review_id>/delete", methods=["POST"])
@jwt_required()
def remove_review(apartment_id, review_id):
    current_user_id = int(get_jwt_identity())
    review = get_review(review_id)

    if not review or review.user_id != current_user_id:
        flash("You do not have permission to delete this review.", "error")
    else:
        delete_review(review_id)
        flash("Review deleted successfully!", "success")

    next_page = request.form.get("next")
    return redirect(next_page) if next_page else redirect(url_for("apartment_views.view_apartment", apartment_id=apartment_id))


# ────────────────────────────────────────────────────────────────────────────────
# EDIT LISTING (landlord only)
# ────────────────────────────────────────────────────────────────────────────────


@apartment_views.route("/apartments/<int:apartment_id>/edit", methods=["GET", "POST"])
@jwt_required()
def edit_listing(apartment_id):
    user_id = int(get_jwt_identity())
    user = User.query.get(user_id)

    if not user or user.role != "landlord":
        flash("Only landlords can edit listings.", "error")
        return redirect(url_for("apartment_views.list_apartments"))

    apartment = get_apartment(apartment_id)
    if not apartment or apartment.owner_id != user_id:
        flash("You do not have permission to edit this listing.", "error")
        return redirect(url_for("apartment_views.list_apartments"))

    if request.method == "POST":
        data = {
            "title": request.form["title"],
            "description": request.form["description"],
            "address": request.form["address"],
            "city": request.form["city"],
            "state": request.form["state"],
            "zip_code": request.form["zip_code"],
            "price": request.form["price"],
            "bedrooms": request.form["bedrooms"],
            "bathrooms": request.form["bathrooms"],
            "square_feet": request.form.get("square_feet") or None,
        }

        # replace image if a new one is uploaded
        image = request.files.get("image")
        if image and image.filename:
            old_fn = apartment.image_filename
            if old_fn:
                old_path = os.path.join(current_app.config["UPLOAD_FOLDER"], old_fn)
                if os.path.exists(old_path):
                    os.remove(old_path)
            filename = secure_filename(image.filename)
            image.save(os.path.join(current_app.config["UPLOAD_FOLDER"], filename))
            data["image_filename"] = filename

        update_apartment(apartment_id, **data)

        # update amenities
        apartment.amenities.clear()
        for a_id in request.form.getlist("amenities"):
            try:
                aid = int(a_id)
            except ValueError:
                continue
            amenity = AmenityType.query.get(aid)
            if amenity:
                apartment.amenities.append(amenity)
        db.session.commit()

        flash("Listing updated successfully!", "success")
        return redirect(url_for("apartment_views.view_apartment", apartment_id=apartment_id))

    amenities = AmenityType.query.all()
    return render_template("edit_listing.html", apartment=apartment, amenities=amenities)


# ────────────────────────────────────────────────────────────────────────────────
# DELETE LISTING (landlord only)
# ────────────────────────────────────────────────────────────────────────────────


@apartment_views.route("/apartments/<int:apartment_id>/delete", methods=["GET", "POST"])
@jwt_required()
def delete_listing(apartment_id):
    current_user_id = int(get_jwt_identity())
    user = User.query.get(current_user_id)
    apartment = get_apartment(apartment_id)

    if not apartment or apartment.owner_id != current_user_id:
        flash("You do not have permission to delete this listing.", "error")
        return redirect(url_for("index_views.dashboard"))

    if request.method == "POST":
        password = request.form.get("password", "")
        if not user.check_password(password):
            flash("Incorrect password. Please try again.", "error")
            return render_template("confirm_delete_listing.html", apartment=apartment)

        fn = apartment.image_filename
        if fn:
            path = os.path.join(current_app.config["UPLOAD_FOLDER"], fn)
            if os.path.exists(path):
                os.remove(path)

        delete_apartment(apartment_id)
        flash("Listing deleted successfully.", "success")
        return redirect(url_for("index_views.dashboard"))

    return render_template("confirm_delete_listing.html", apartment=apartment)