from app.extensions import db
from datetime import datetime

class Booking(db.Model):
    __tablename__ = 'bookings'
    
    id = db.Column(db.Integer, primary_key=True)
    session_datetime = db.Column(db.DateTime, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    expert_id = db.Column(db.Integer, db.ForeignKey('experts.id'), nullable=False)
    status = db.Column(db.String(50), default='Pending')  # Added for managing status
    
    user = db.relationship('User', backref='user_bookings')  # Unique backref for User
    expert = db.relationship("Expert", back_populates="bookings", overlaps="expert_ref")

    def __repr__(self):
        return f'<Booking {self.session_datetime} with Expert {self.expert_id}>'

class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.now)
    booking_id = db.Column(db.Integer, db.ForeignKey('bookings.id'))
    sender_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    is_read = db.Column(db.Boolean, default=False)
    
    # Relationships
    booking = db.relationship('Booking', backref=db.backref('messages', lazy=True))

    sender = db.relationship('User', backref='sent_messages', foreign_keys=[sender_id])

    def __repr__(self):
        return f'<Message from User {self.sender_id} in Booking {self.booking_id}>'
