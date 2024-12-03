import click
from flask import current_app
from flask.cli import with_appcontext
from HSA import db
from HSA.models import User, RoleEnum

def create_admin_user(name: str, email: str, password: str):
    """
    Creates an admin user with the provided details.

    :param name: The name of the admin user
    :param email: The email of the admin user
    :param password: The password for the admin user
    """
    try:
        # Check if an admin with the same email already exists
        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            print(f"User with email {email} already exists.")
            return

        # Create a new admin user
        admin_user = User(
            name=name,
            email=email,
            role=RoleEnum.admin
        )
        admin_user.set_password(password)  # Hashes the password

        # Add and commit the user to the database
        db.session.add(admin_user)
        db.session.commit()
        print(f"Admin user created: {admin_user}")

    except Exception as e:
        db.session.rollback()
        print(f"Error creating admin user: {e}")

    finally:
        db.session.close()


@click.command('create-admin')
@click.argument('name')
@click.argument('email')
@click.argument('password')
@with_appcontext
def create_admin_command(name, email, password):
    """Flask CLI command to create an admin user"""
    create_admin_user(name, email, password)

