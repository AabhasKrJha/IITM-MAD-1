from flask import Blueprint, g, redirect, url_for, request, render_template, session

from HSA import db
from HSA.models import User, RoleEnum, Service

auth = Blueprint("users", __name__)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    provider_id = request.args.get('book')
    if g.user :
        return redirect(url_for('main.home'))
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        provider_id = request.form.get('provider_id')
        user = User.query.filter_by(email=email).first()
        if user and user.check_password(password):
            session['user'] = {'id': user.id, 'name': user.name, 'role': user.role}
            if provider_id:
                return redirect(f"/booking/{provider_id}")
            return redirect(url_for('main.home'))
        return render_template("pages/login.html", message="Invalid credentials!")
    return render_template("pages/login.html", provider_id=provider_id)

@auth.route('/signup', methods=['GET', 'POST'])
def signup():
    provider_id = request.args.get('book')
    if g.user :
        return redirect(url_for('main.home'))
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        password = request.form.get('password')
        provider_id = request.form.get('provider_id')
        new_user = User(name=name, email=email, role=RoleEnum.consumer)
        new_user.set_password(password)
        try:
            db.session.add(new_user)
            db.session.commit()
            session['user'] = {'id': new_user.id, 'name': new_user.name, 'role': new_user.role}
            if provider_id:
                return redirect(f"/booking/{provider_id}")
            return redirect(url_for('main.home'))
        except:
            return render_template("pages/signup.html", message="Email already exists!")
    return render_template("pages/signup.html", provider_id=provider_id)

@auth.route('/work-with-us', methods=['GET', 'POST'])
def work_with_us():
    if g.user :
        return redirect(url_for('main.home'))
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        password = request.form.get('password')
        service = Service.query.get(request.form.get('service_id'))
        state = request.form.get('state')
        city = request.form.get('city')
        experience = str(request.form.get('experience'))
        new_user = User(name=name, email=email, role=RoleEnum.provider, service=service, state=state, city=city, experience=experience)
        new_user.set_password(password)
        try:
            db.session.add(new_user)
            db.session.commit()
            session['user'] = {'id': new_user.id, 'name': new_user.name, 'role': new_user.role}
            return redirect(url_for('main.home'))
        except:
            return render_template("pages/work-with-us.html", message="Email already exists!")
    services = Service.query.all()
    return render_template("pages/work-with-us.html", services=services)

@auth.route('/logout')
def logout():
    session.clear()
    g.user = None
    return redirect(url_for('main.home'))