from app.database import db
import app.models.all as Models
from app.helpers.emails import Emails
import math
from app.helpers.tasks import check_unknown_cards

class Cards(db.Model):
    __tablename__ = "cards"
    id = db.Column(db.Integer, primary_key=True)
    card_id = db.Column(db.Integer, nullable=False, unique=True)
    card_name = db.Column(db.String(500), nullable=False, unique=True)
    card_img = db.relationship("CardImage", backref="card_image", lazy=True)

    def add_card(self, id, name):
        self.card_id = id
        self.card_name = name
        db.session.add(self)
        db.session.commit()

    def get_card(self, card_id):
        q = self.query.filter_by(card_id=card_id).first()

        if not q:
            return [False, False]

        card = {
            "id": card_id,
            "name": q.card_name,
            "player_count" : len(Models.Player().find_players_by_card_type(q.card_name))
        }

        return [card, True]

    def get_card_by_id(self, card_id):
        return self.query.filter_by(card_id=card_id).first()

    def find_cards_with_page_and_limit(self, page, limit):
        try:
            query_limit = 15 if limit == 0 else limit

            total_pages = math.ceil(len(self.query.all()) / limit)
            query = self.query.paginate(page, query_limit).items
            
            if not query:
                return ["Page does not exist", False, 400]
            
            result = []

            for q in query:
                result.append({
                    "id" : q.card_id,
                    "name" : q.card_name
                })
            return [result, True, total_pages]
        except Exception as e:
            if "404" in str(e) or "NotFound" in str(e):
                return [f"Page {str(page)} does not exist.", False, 400]
            raise Exception(e)

    def get_image(self, card_id):
        q = self.query.filter_by(card_id=card_id).first()
        
        if not q:
            return [False, False]

        return [q.card_img[0].img, True]

    def check_for_unknown(self):
        q = self.query.filter_by(card_name="unknown").first()

        if q:
            check_unknown_cards.delay()
  