from flask import Blueprint, request, render_template, render_template_string

from HSA import db
from HSA.models import User, Service, ServiceRequest

bookings_api = Blueprint("bookings", __name__)

@bookings_api.route("/search")
def search_services():
    q = request.args.get('q')
    results = []
    if q:
        providers = db.session.query(User, Service).join(Service).filter(
            Service.name.ilike(f"%{q}%"),
            User.flagged == False,          
            User.approved == True            
        ).all()

        for user, service in providers:
            results.append({
                "id": user.id,
                "name": user.name,
                "email": user.email,
                "service": service.name,
                "base_price": service.base_price,
                "state": user.state,
                "city": user.city,
                "experience": user.experience,
            })
    return render_template("/components/search/results.html", results=results)


@bookings_api.route("/bookings/<int:request_id>/accept", methods=["POST"])
def accept_booking(request_id):
    index = request.form.get("index", type=int)
    service_request = ServiceRequest.query.filter_by(id=request_id).first()
    service_request.status = "assigned"
    db.session.commit()

    updated_row_html = render_template_string("""
       <div class="row align-items-center" id="booking-row-{{ service_request.id }}">
                <div class="col-1 fw-bold">{{ index }}</div>
                <div class="col-2" id="date-{{ service_request.id }}">{{ service_request.date_of_request }}</div>
                <div class="col-3">{{ service_request.address }}</div>
                <div class="col-1">{{ service_request.status }}</div>
                <div class="col-1">
                    {% if service_request.status == 'closed' %}
                        <button type="button" class="btn btn-success">Completed</button>
                    {% else %}
                        <button class="btn btn-primary" 
                                hx-post="/api/bookings/{{ service_request.id }}/complete" 
                                hx-vals='{"index": {{ index }}}' 
                                hx-target="#booking-row-{{ service_request.id }}" 
                                hx-swap="outerHTML"
                                >
                                Complete
                        </button>
                    {% endif %}
                </div>
            </div>
    """, service_request=service_request, index=index)

    return updated_row_html

@bookings_api.route("/bookings/<int:request_id>/complete", methods=["POST"])
def complete_booking(request_id):
    index = request.form.get("index", type=int)
    service_request = ServiceRequest.query.filter_by(id=request_id).first()
    service_request.status = "closed"
    db.session.commit()

    updated_row_html = render_template_string("""
       <div class="row align-items-center" id="booking-row-{{ service_request.id }}">
                <div class="col-1 fw-bold">{{ index }}</div>
                <div class="col-2" id="date-{{ service_request.id }}">{{ service_request.date_of_request }}</div>
                <div class="col-3">{{ service_request.address }}</div>
                <div class="col-1">{{ service_request.status }}</div>
                <div class="col-1">
                    <button type="button" class="btn btn-success">Completed</button>
                </div>
            </div>
    """, service_request=service_request, index=index)

    return updated_row_html
