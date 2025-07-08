from datetime import datetime
from app import db

class Message(db.Model):
    __tablename__ = 'messages'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, nullable=False)
    username = db.Column(db.String(50), nullable=False)
    channel = db.Column(db.String(50), nullable=True)
    recipient = db.Column(db.String(50), nullable=True)
    text = db.Column(db.Text, nullable=False)
    reply_to = db.Column(db.Integer, db.ForeignKey('messages.id'), nullable=True)
    pinned = db.Column(db.Boolean, default=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

    reactions = db.relationship('Reaction', backref='message', cascade='all, delete-orphan')

class Reaction(db.Model):
    __tablename__ = 'reactions'
    id = db.Column(db.Integer, primary_key=True)
    message_id = db.Column(db.Integer, db.ForeignKey('messages.id'), nullable=False)
    user_id = db.Column(db.Integer, nullable=False)
    emoji = db.Column(db.String(10), nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

    __table_args__ = (
        db.UniqueConstraint('message_id', 'user_id', 'emoji', name='uq_reaction'),
    )
