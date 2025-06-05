from app.extensions import db
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(120), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128))
    role = db.Column(db.String(50))
    gender = db.Column(db.String(50))
    address = db.Column(db.String(200))
    phone = db.Column(db.String(20))
    profile_image_url = db.Column(db.String(200), nullable=True)
    profile_complete = db.Column(db.Boolean, default=False)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


class Expert(db.Model):
    __tablename__ = 'experts'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    profile_picture = db.Column(db.String(255), nullable=True)  # URL to profile picture
    specialization = db.Column(db.String(100), nullable=False)
    bio = db.Column(db.Text, nullable=True)
    
    bookings = db.relationship("Booking", back_populates="expert", overlaps="expert_ref")

    def __repr__(self):
        return f'<Expert {self.name}>'