from app.database import db

class CardImage(db.Model):
    __tablename__ = "card_images"
    id = db.Column(db.Integer, primary_key=True)
    card_id = db.Column(db.Integer, db.ForeignKey("cards.card_id"))
    img = db.Column(db.Text(5000000), nullable=False)

    def add_img(self, id, img):
        self.card_id = id
        self.img = img
        db.session.add(self)
        db.session.commit()
