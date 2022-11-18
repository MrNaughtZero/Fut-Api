from app.database import db
import app.models.all as Models
import math

class Nations(db.Model):
    __tablename__ = "nations"
    id = db.Column(db.Integer, primary_key=True)
    nation_id = db.Column(db.Integer, nullable=False, unique=True)
    nation_name = db.Column(db.String(500), nullable=False, unique=True)
    nation_img = db.Column(db.Text(5000000), nullable=True)

    def get_all_nations(self):
        all_nations = {}
        q = self.query.all()
        for nation in q:
            all_nations[nation.nation_id] = nation.nation_name

        return all_nations

    def get_nation(self, nation_id):
        q = self.query.filter_by(nation_id=nation_id).first()

        if not q:
            return [False, False]

        nation = {
            "id": nation_id,
            "name": q.nation_name,
            "player_count" : len(Models.Player().find_players_by_nation_id(nation_id))
        }

        return [nation, True]

    def find_nations_with_page_and_limit(self, page, limit):
        try:
            query_limit = 15 if limit == 0 else limit

            total_pages = math.ceil(len(self.query.all()) / limit)
            query = self.query.paginate(page, query_limit).items
            
            if not query:
                return ["Page does not exist", False, 400]
            
            result = []

            for q in query:
                result.append({
                    "id" : q.nation_id,
                    "name" : q.nation_name
                })
            return [result, True, total_pages]
        except Exception as e:
            if "404" in str(e) or "NotFound" in str(e):
                return [f"Page {str(page)} does not exist.", False, 400]
                
            return ["Something went wrong. Please try again", False, 500]

    def get_nation_image(self, nation_id):
        q = self.query.filter_by(nation_id=nation_id).first()

        if not q:
            return [False, False]

        return [q.nation_img, True]
