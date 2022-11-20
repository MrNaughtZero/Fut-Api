from app.database import db
import app.models.all as Models
from app.helpers.requests import ExternalRequests
import math

class Leagues(db.Model):
    __tablename__ = "leagues"
    league_id = db.Column(db.Integer, primary_key=True, nullable=False, unique=True, autoincrement=True)
    league_name = db.Column(db.String(500), nullable=False, unique=True)
    league_img = db.Column(db.Text(5000000), nullable=False)

    def add_league(self, league_name, league_img):
        self.league_name = league_name
        self.league_img = league_img

        db.session.add(self)
        db.session.commit()

        return self
    
    def find_leagues_with_page_and_limit(self, page, limit):
        try:
            query_limit = 15 if limit == 0 else limit

            total_pages = math.ceil(len(self.query.all()) / limit)
            query = self.query.paginate(page=page, per_page=query_limit).items
            
            if not query:
                return ["Page does not exist", False, 400]
            
            result = []

            for q in query:
                result.append({
                    "id" : q.league_id,
                    "name" : q.league_name
                })
            return [result, True, total_pages]
        except Exception as e:
            if "404" in str(e) or "NotFound" in str(e):
                return [f"Page {str(page)} does not exist.", False, 400]
                
            raise Exception(e)

    def get_league(self, league_id):
        q = self.query.filter_by(league_id=league_id).first()

        if not q:
            return [False, False]

        league = {
            "id": league_id,
            "name": q.league_name,
            "player_count" : len(Models.Player().find_players_by_league_id(league_id))
        }

        return [league, True]

    def get_league_id_by_name(self, league_name, fut_league_id = 1):
        q = self.query.filter_by(league_name=league_name).first()

        if q:
            return q.league_id
        else:
            new_league = self.add_league(league_name, ExternalRequests().get_league_image(league_name))
            return new_league.league_id

        return self.league_id

    def get_league_image(self, league_id):
        q = self.query.filter_by(league_id=league_id).first()

        if not q:
            return [False, False]

        return [q.league_img, True]
  