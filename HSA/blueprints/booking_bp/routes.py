from flask import render_template, Blueprint, g, redirect, request
from datetime import datetime

from HSA import db
from HSA.models import User, ServiceRequest

booking = Blueprint("booking", __name__)

@booking.route('/search')
def home():
    return render_template("pages/search.html")

@booking.route('/booking/<int:provider_id>', methods=['GET', 'POST'])
def booking_page(provider_id):
    if g.user == None:
        return redirect(f"/login?book={provider_id}")
    user_id = g.user.id
    service_id = User.query.filter_by(id=provider_id).first().service_id
    if request.method == "POST":
        date_of_request = datetime.strptime(request.form.get("date_of_request"), '%Y-%m-%dT%H:%M')
        address = request.form.get("address")
        new_request = ServiceRequest(
                user_id=user_id,
                service_id=service_id,
                provider_id=provider_id,
                date_of_request=date_of_request,
                address=address
            )
        db.session.add(new_request)
        db.session.commit()
        return redirect("/profile")
        
    return render_template('pages/booking.html')