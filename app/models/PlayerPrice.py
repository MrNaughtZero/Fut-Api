from app.database import db

class PlayerPrice(db.Model):
    __tablename__ = "player_price"
    id = db.Column(db.Integer, primary_key=True)
    player_id = db.Column(db.Integer, db.ForeignKey("players.id"))
    pc = db.Column(db.NUMERIC(65), nullable=False)
    console = db.Column(db.NUMERIC(65), nullable=False)

    def add_player_price(self, id):
        self.player_id = id
        self.pc = 0
        self.console = 0

        db.session.add(self)
        db.session.commit()

    def get_player_price(self, player_id):
        positions = []
        q = self.query.filter_by(player_id=player_id).first()
        return {
            "console" : q.console,
            "pc" : q.pc
        }
   