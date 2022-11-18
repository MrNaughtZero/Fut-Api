from app.database import db

class PlayerImage(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    player_id = db.Column(db.Integer, db.ForeignKey("players.id"))
    player_resource_id = db.Column(db.Integer, nullable=False)
    img = db.Column(db.Text(5000000), nullable=False)

    def add_image(self, player_id, resource_id, img):
        self.player_id = player_id
        self.player_resource_id = resource_id
        self.img = img

        db.session.add(self)
        db.session.commit()

    def get_image_by_id(self, player_id):
        q = self.query.filter_by(player_id=player_id).first()

        if not q:
            return ["Invalid Player ID", False, 404]

        return [q.img, True, True]
