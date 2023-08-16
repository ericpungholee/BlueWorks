from blueworks import db, login_manager
from flask_login import UserMixin

@login_manager.user_loader
def load_user(user_id):
    user = Consumer.query.get(int(user_id))
    if not user:
        user = Company.query.get(int(user_id))
    return user

class Consumer(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    location_country = db.Column(db.String(50), nullable=False)
    location_province = db.Column(db.String(50), nullable=False)
    location_city = db.Column(db.String(50), nullable=False)
    address = db.Column(db.String(100), nullable=False)  # Adjusted size from 10 to 100, since an address of size 10 might be too restrictive
    profile_picture = db.Column(db.String(60), nullable=False, default='default.jpg')
    ratings = db.relationship('Rating', backref='consumer', lazy=True)  # Adjusted reviews to ratings
    is_consumer = db.Column(db.Boolean, nullable=False, default=True)
    reviews = db.relationship('Review', back_populates="consumer")
class Review(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    author_id = db.Column(db.Integer, nullable=False)  # The ID of the user who wrote the review
    consumer_id = db.Column(db.Integer, db.ForeignKey('consumer.id'), nullable=True)
    company_id = db.Column(db.Integer, db.ForeignKey('company.id'), nullable=True)
    content = db.Column(db.String(500), nullable=False)
    
    # Relationships
    consumer = db.relationship('Consumer', back_populates="reviews")
    company = db.relationship('Company', back_populates="reviews")

class Company(db.Model, UserMixin):
    __tablename__ = 'company'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    phone = db.Column(db.String(120))
    links = db.Column(db.String(1000))
    password = db.Column(db.String(60), nullable=False)
    logo = db.Column(db.String(60), nullable=False, default='default.jpg')
    bio = db.Column(db.String(500))
    location_country = db.Column(db.String(50), nullable=False)
    location_province = db.Column(db.String(50), nullable=False)
    location_city = db.Column(db.String(50), nullable=False)
    address = db.Column(db.String(100), nullable=False)
    ratings = db.Column(db.Float)
    reviews = db.relationship('Review', back_populates="company")
    portfolios = db.relationship('Portfolio', backref='company', lazy=True)
    licenses = db.Column(db.String(500))
    company_type = db.Column(db.String(20), nullable=False)
    is_consumer = db.Column(db.Boolean, nullable=False, default=False)
    total_rating = db.Column(db.Float, default=0.0)  # Sum of all ratings
    ratings_count = db.Column(db.Integer, default=0)  # Number of ratings received

    @property
    def ratings(self):
        if self.ratings_count == 0:
            return 0
        return self.total_rating / self.ratings_count




class Portfolio(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    company_id = db.Column(db.Integer, db.ForeignKey('company.id'), nullable=False)
    project_name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(500), nullable=False)
    picture_1 = db.Column(db.String, nullable=False)  # Required picture
    picture_2 = db.Column(db.String, nullable=True)
    picture_3 = db.Column(db.String, nullable=True)
    picture_4 = db.Column(db.String, nullable=True)
    picture_5 = db.Column(db.String, nullable=True)
    picture_6 = db.Column(db.String, nullable=True)
    picture_7 = db.Column(db.String, nullable=True)
    picture_8 = db.Column(db.String, nullable=True)
    picture_9 = db.Column(db.String, nullable=True)
    picture_10 = db.Column(db.String, nullable=True)
    def __init__(self, company, project_name, description, picture_1, picture_2=None, picture_3=None,
                 picture_4=None, picture_5=None, picture_6=None, picture_7=None, picture_8=None,
                 picture_9=None, picture_10=None):
        self.company_id = company.id
        self.project_name = project_name
        self.description = description
        self.picture_1 = picture_1
        self.picture_2 = picture_2
        self.picture_3 = picture_3
        self.picture_4 = picture_4
        self.picture_5 = picture_5
        self.picture_6 = picture_6
        self.picture_7 = picture_7
        self.picture_8 = picture_8
        self.picture_9 = picture_9
        self.picture_10 = picture_10

class Rating(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    company_id = db.Column(db.Integer, db.ForeignKey('company.id'), nullable=False)
    rating = db.Column(db.Float, nullable=False)  # Rating out of 5
    consumer_id = db.Column(db.Integer, db.ForeignKey('consumer.id'), nullable=False)

