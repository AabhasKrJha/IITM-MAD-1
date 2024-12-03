from sqlalchemy import Enum, ForeignKey
from sqlalchemy.orm import relationship
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, timezone

from HSA import db

class RoleEnum(Enum):
    admin = "admin"
    consumer = "consumer"
    provider = "provider"

class Service(db.Model):
    __tablename__ = "services"
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    base_price = db.Column(db.Float, nullable=False)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

    
    def __repr__(self):
        return f"<Service {self.name}>"

class User(db.Model):
    __tablename__ = "users"
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String, nullable=False)
    role = db.Column(Enum(RoleEnum.admin, RoleEnum.consumer, RoleEnum.provider, name="role_enum"), nullable=False, default=RoleEnum.consumer)
    service_id = db.Column(db.Integer, ForeignKey("services.id"), nullable=True)
    state = db.Column(db.Text, nullable=True)
    city = db.Column(db.Text, nullable=True)
    price = db.Column(db.Float, nullable=True)
    experience = db.Column(db.String(255), nullable=True)
    description = db.Column(db.Text, nullable=True)
    time_required = db.Column(db.String(50), nullable=True)
    flagged = db.Column(db.Boolean, nullable=False, default=False)
    approved = db.Column(db.Boolean, nullable=False, default=False)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))


    # Relationships
    service = relationship("Service", backref="provider", uselist=False)

    def __repr__(self):
        return f"<User {self.email}>"

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)
    
class ServiceRequest(db.Model):
    __tablename__ = "service_requests"
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, ForeignKey("users.id"), nullable=False)
    service_id = db.Column(db.Integer, ForeignKey("services.id"), nullable=False)
    provider_id = db.Column(db.Integer, ForeignKey("users.id"), nullable=False)
    date_of_request = db.Column(db.DateTime, nullable=False)
    address = db.Column(db.Text, nullable=True)
    date_of_completion = db.Column(db.DateTime, nullable=True)
    status = db.Column(Enum("requested", "assigned", "closed", name="status_enum"), nullable=False, default="requested")
    remarks = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))


    # Relationships
    consumer = relationship("User", foreign_keys=[user_id], backref="service_requests")
    provider = relationship("User", foreign_keys=[provider_id], backref="provided_requests")
    service = relationship("Service", backref="service_requests")

    def __repr__(self):
        return f"<ServiceRequest {self.id} - Status: {self.status}>"