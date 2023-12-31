from NSSGolf import db
from flask_login import UserMixin
from werkzeug.security import generate_password_hash
from datetime import datetime

class ImageLike(db.Model):
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)
    image_id = db.Column(db.Integer, db.ForeignKey('image.id'), primary_key=True)

class TutorialLike(db.Model):
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)
    tutorial_id = db.Column(db.Integer, db.ForeignKey('tutorial.id'), primary_key=True)

class Notification(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    message = db.Column(db.String(500), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    user = db.relationship('User', backref='notifications', lazy=True)
    read = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    type = db.Column(db.String(20), nullable=True)
    
class Tutorial(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(50), nullable=False)
    video_link = db.Column(db.String(120), nullable=False)
    category = db.Column(db.String(20), nullable=False)

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    user = db.relationship('User', backref='tutorials', lazy=True)

    like_count = db.Column(db.Integer, default=0, nullable=False)

    approved = db.Column(db.Boolean, default=False)

    def is_liked_by(self, user):
        return TutorialLike.query.filter_by(tutorial_id=self.id, user_id=user.id).first() is not None

class Image(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120), nullable=False)
    img_file = db.Column(db.String(120), nullable=False)
    youtube_link = db.Column(db.String(120), nullable=False)

    hole_number = db.Column(db.Integer, nullable=False)
    wind_speed = db.Column(db.Integer, nullable=False)
    wind_speed_units = db.Column(db.String(3), nullable=False)
    wind_direction = db.Column(db.String(2), nullable=False)
    flag_position = db.Column(db.String(10), nullable=False)
    shot_distance = db.Column(db.Integer, nullable=False)
    distance_units = db.Column(db.String(3), nullable=False)

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    user = db.relationship('User', backref='images', lazy=True)

    like_count = db.Column(db.Integer, default=0, nullable=False)

    approved = db.Column(db.Boolean, default=False)

    def is_liked_by(self, user):
        return ImageLike.query.filter_by(image_id=self.id, user_id=user.id).first() is not None

class Role(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), unique=True)

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable = False)
    password = db.Column(db.String(60), nullable = False)
    role_id = db.Column(db.Integer, db.ForeignKey('role.id'), default=1)

    role = db.relationship('Role', backref=db.backref('users', lazy='dynamic'))

    @staticmethod
    def create_user(username, password):
        # Hash the password for security
        hashed_password = generate_password_hash(password)

        # Create a new user with the hashed password and default role
        user = User(username=username, password=hashed_password, role_id=Role.query.filter_by(name='user').first().id)

        # Add the new user to the database session and commit it
        db.session.add(user)
        db.session.commit()

        # Return the new user
        return user