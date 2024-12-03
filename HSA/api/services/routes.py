from flask import Blueprint, request, redirect

from HSA import db
from HSA.models import Service

services_api = Blueprint("services", __name__, url_prefix="/services")

@services_api.route("/", methods=["POST"])
def add_service():
    service_name = request.form.get('service-name').lower()
    base_price = request.form.get('base-price')

    new_service = Service(name=service_name, base_price=float(base_price))
    db.session.add(new_service)
    db.session.commit()

    return redirect("/admin")

@services_api.route("/<int:service_id>/delete", methods=["POST"])
def delete_service(service_id):
    service = Service.query.get(service_id)
    db.session.delete(service)
    db.session.commit()

    return redirect("/admin")