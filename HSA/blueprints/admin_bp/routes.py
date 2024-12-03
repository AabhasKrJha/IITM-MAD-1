from flask import render_template, Blueprint, g, redirect, url_for

from HSA.models import User, Service

admin = Blueprint("admin", __name__)

@admin.route('/admin')
def admin_dashboard():
    consumers = User.query.filter_by(role='consumer').all()
    providers = User.query.filter_by(role='provider').all()
    services = Service.query.all()
    if g.user and g.user.role=="admin":
        return render_template("pages/admin.html", consumers=consumers, providers=providers, services=services)
    return redirect(url_for('users.login'))