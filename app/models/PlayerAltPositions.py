from app.database import db

class PlayerAltPositions(db.Model):
    __tablename__ = "player_alt_positions"
    id = db.Column(db.Integer, primary_key=True)
    player_id = db.Column(db.Integer, db.ForeignKey("players.id"))
    position = db.Column(db.String(20), nullable=False)

    def add_player_positions(self, id, position):
        self.player_id = id
        self.position = position

        db.session.add(self)
        db.session.commit()

    def get_player_alt_positions(self, player_id):
        positions = []
        q = self.query.filter_by(player_id=player_id).all()
        for i in q:
            positions.append(i.position)
        return positions
