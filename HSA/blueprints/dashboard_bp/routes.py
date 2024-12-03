from flask import render_template, Blueprint, g, redirect

from HSA.models import User, ServiceRequest

dashboard = Blueprint("dashboard", __name__)

@dashboard.route('/dashboard')
def dashboard_view():
    if (not g.user):
        return redirect("/login")
    if  g.user.role=="admin":
        return redirect("/admin")
    if  g.user.role=="consumer":
        return redirect("/profile")
    user = User.query.filter_by(id = g.user.id).first()
    service_requests = ServiceRequest.query.filter_by(provider_id=user.id).all()
    if (not user.approved):
        return render_template("pages/not_approved.html")
    return render_template("pages/dashboard.html", requests = service_requests)

@dashboard.route('/profile')
def profile_view():
    if (not g.user):
        return redirect("/login")
    if  g.user.role=="admin":
        return redirect("/admin")
    if  g.user.role=="provider":
        return redirect("/dashboard")
    # user = User.query.filter_by(id = g.user.id).first()
    service_requests = ServiceRequest.query.filter_by(user_id=g.user.id).all()
    return render_template("pages/profile.html", requests = service_requests)