from app.database import db
import datetime

class Limiter(db.Model):
    __tablename__ = "limiter"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False, unique=True)
    requests = db.Column(db.Integer(), default=0)
    limited = db.Column(db.Boolean, default=False)
    limit_expiry = db.Column(db.DateTime, nullable=True)

    def setup(self, user_id):
        self.user_id = user_id
        db.session.add(self)
        db.session.commit()

    def check_limit(self, user_id, subscription):
        q = self.query.filter_by(user_id=user_id).first()
        now = datetime.datetime.now()
        if subscription == "free" and q.requests >= 1000000:
            if not q.limit_expiry:
                q.limit_expiry = now + datetime.timedelta(minutes=3)
                db.session.commit()
                return False
            if now > q.limit_expiry:
                q.requests = 0
                q.limit_expiry = None
                db.session.commit()
                return True
            return False
        if subscription == "premium" and q.requests >= 20000:
            if not q.limit_expiry:
                q.limit_expiry = now + datetime.timedelta(minutes=3)
                db.session.commit()
                return False
            if now > q.limit_expiry:
                q.requests = 0
                q.limit_expiry = None
                db.session.commit()
                return True
            return False

        q.requests = q.requests + 1
        db.session.commit()

        return True 
