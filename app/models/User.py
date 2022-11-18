from app.database import db
import datetime
import random
import string

class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    api_key = db.Column(db.String(255), nullable=False)
    subscription = db.Column(db.String(255), nullable=False, default="free")
    start_date = db.Column(db.DateTime, server_default=db.func.now(), nullable=False)
    end_date = db.Column(db.DateTime, nullable=True)
    created_on = db.Column(db.DateTime, server_default=db.func.now())
    updated_on = db.Column(
        db.DateTime, server_default=db.func.now(), server_onupdate=db.func.now()
    )
    limit = db.relationship("Limiter", backref="limit", lazy=True)

    def add_user(self, data):
        self.api_key = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(52))
        self.subscription = data["subscription"]
        self.end_date = data["end_date"]

        db.session.add(self)
        db.session.commit()

        Limiter().setup(self.id)

        return self.api_key

    def validate_api_key(self, api_key):
        q = self.query.filter_by(api_key=api_key).first()
        
        if not q:
            return False

        return True
    
    def validate_premium_api_key(self, api_key):
        q = self.query.filter_by(api_key=api_key).first()
        
        if not q:
            return [{}, False]

        if q.subscription != "premium":
            return [
                {
                    "error" : "The API key provided is a free membership. A premium API is required to access this endpoint."
                }, 
                False
            ]

        if datetime.datetime.now() > q.end_date:
            return [
                {
                    "error" : "Your premium membership has expired. You can not access this endpoint until you renew your membership"
                }, 
                False
            ]

        return [True, True]
            
    def check_if_limited(self, api_key):
        q = self.query.filter_by(api_key=api_key).first()

        if not q:
            return ["Invalid API Key", False]

        if not Limiter().check_limit(q.id, q.subscription):
            return ["Sorry, you've reached your daily limit of requests allowed within a 24 hour period.", False]

        return [True, True]
