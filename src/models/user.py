from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    
    # Relationship with dice rolls
    dice_rolls = db.relationship('DiceRoll', backref='user', lazy=True)

    def __repr__(self):
        return f'<User {self.username}>'

    def to_dict(self):
        return {
            'id': self.id,
            'username': self.username
        }

class DiceRoll(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    dice1 = db.Column(db.Integer, nullable=False)
    dice2 = db.Column(db.Integer, nullable=False)
    dice3 = db.Column(db.Integer, nullable=False)
    total_score = db.Column(db.Integer, nullable=False)
    rolled_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<DiceRoll {self.user_id}: {self.dice1},{self.dice2},{self.dice3}>'

    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'username': self.user.username if self.user else None,
            'dice1': self.dice1,
            'dice2': self.dice2,
            'dice3': self.dice3,
            'total_score': self.total_score,
            'rolled_at': self.rolled_at.isoformat() if self.rolled_at else None
        }

class Ranking(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    username = db.Column(db.String(80), nullable=False)
    highest_score = db.Column(db.Integer, nullable=False)
    total_rolls = db.Column(db.Integer, default=1)
    last_updated = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationship with user
    user = db.relationship('User', backref='ranking')
    
    def __repr__(self):
        return f'<Ranking {self.username}: {self.highest_score}>'

    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'username': self.username,
            'highest_score': self.highest_score,
            'total_rolls': self.total_rolls,
            'last_updated': self.last_updated.isoformat() if self.last_updated else None
        }

