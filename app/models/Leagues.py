from app.database import db
import math

class Leagues(db.Model):
    __tablename__ = "leagues"
    id = db.Column(db.Integer, primary_key=True)
    league_id = db.Column(db.Integer, nullable=False, unique=True)
    league_name = db.Column(db.String(500), nullable=False, unique=True)
    league_img = db.Column(db.Text(5000000), nullable=False)
    
    def find_leagues_with_page_and_limit(self, page, limit):
        try:
            query_limit = 15 if limit == 0 else limit

            total_pages = math.ceil(len(self.query.all()) / limit)
            query = self.query.paginate(page, query_limit).items
            
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
                
            return ["Something went wrong. Please try again", False, 500]

    def get_league(self, league_id):
        q = self.query.filter_by(league_id=league_id).first()

        if not q:
            return [False, False]

        league = {
            "id": league_id,
            "name": q.league_name,
            "player_count" : len(Player().find_players_by_league_id(league_id))
        }

        return [league, True]

    def get_league_image(self, league_id):
        q = self.query.filter_by(league_id=league_id).first()

        if not q:
            return [False, False]

        return [q.league_img, True]
  