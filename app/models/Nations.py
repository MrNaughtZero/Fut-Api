from app.database import db
import app.models.all as Models
from app.helpers.requests import ExternalRequests
import math

class Nations(db.Model):
    __tablename__ = "nations"
    nation_id = db.Column(db.Integer, primary_key=True, nullable=False, unique=True, autoincrement=True)
    nation_name = db.Column(db.String(500), nullable=False, unique=True)
    nation_img = db.Column(db.Text(5000000), nullable=True)

    def add_nation(self, nation_name, nation_img):
        self.nation_name = nation_name
        self.nation_img = nation_img

        db.session.add(self)
        db.session.commit()

        return self

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
            query = self.query.paginate(page=page, per_page=query_limit).items
            
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
                
            raise Exception(e)

    def get_nation_id_by_name(self, nation_name, fut_nation_id = 1):
        q = self.query.filter_by(nation_name=nation_name).first()

        if q:
            return q.nation_id
        else:
            new_nation = self.add_nation(nation_name, ExternalRequests().get_nation_image(fut_nation_id))
            return new_nation.nation_id

        return self.nation_id


    def get_nation_image(self, nation_id):
        q = self.query.filter_by(nation_id=nation_id).first()

        if not q:
            return [False, False]

        return [q.nation_img, True]
