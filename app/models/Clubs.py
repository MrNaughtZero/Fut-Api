from app.database import db
import app.models.all as Models
from app.helpers.requests import ExternalRequests
import math

class Clubs(db.Model):
    __tablename__ = "clubs"
    club_id = db.Column(db.Integer, primary_key=True, nullable=False, unique=True, autoincrement=True)
    club_name = db.Column(db.String(500), nullable=False, unique=True)
    club_img = db.Column(db.Text(5000000), nullable=False)

    def add_club(self, club_name, club_img):
        self.club_name = club_name
        self.club_img = club_img

        db.session.add(self)
        db.session.commit()

        return self
    
    def find_clubs_with_page_and_limit(self, page, limit):
        try:
            query_limit = 15 if limit == 0 else limit

            total_pages = math.ceil(len(self.query.all()) / limit)
            query = self.query.paginate(page=page, per_page=query_limit).items
            
            if not query:
                return ["Page does not exist", False, 400]
            
            result = []

            for q in query:
                result.append({
                    "id" : q.club_id,
                    "name" : q.club_name
                })
            return [result, True, total_pages]
        except Exception as e:
            if "404" in str(e) or "NotFound" in str(e):
                return [f"Page {str(page)} does not exist.", False, 400]
            raise Exception(e)
        
    def get_club(self, club_id):
        q = self.query.filter_by(club_id=club_id).first()

        if not q:
            return [False, False]

        club = {
            "id": club_id,
            "name": q.club_name,
            "player_count" : len(Models.Player().find_players_by_club_id(club_id))
        }

        return [club, True]

    def get_club_id_by_name(self, club_name, fut_club_id = 1):
        q = self.query.filter_by(club_name=club_name).first()

        if q:
            return q.club_id
        else:
            new_club = self.add_club(club_name, ExternalRequests().get_club_image(fut_club_id))
            return new_club.club_id

        return self.club_id

    def get_club_image(self, club_id):
        q = self.query.filter_by(club_id=club_id).first()

        if not q:
            return [False, False]

        return [q.club_img, True]
