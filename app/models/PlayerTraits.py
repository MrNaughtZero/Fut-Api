from app.database import db

class PlayerTraits(db.Model):
    __tablename__ = "player_traits"
    id = db.Column(db.Integer, primary_key=True)
    player_id = db.Column(db.Integer, db.ForeignKey("players.id"))
    trait = db.Column(db.String(100), nullable=False)

    def add_player_traits(self, id, trait):
        self.player_id = id
        self.trait = trait

        db.session.add(self)
        db.session.commit()

    def get_by_trait_and_id(self, player_id, trait):
        return self.query.filter_by(player_id=player_id, trait=trait).first()

    def get_all_player_traits(self, player_id):
        traits = []
        q = self.query.filter_by(player_id=player_id).all()
        if q:
            for trait in q:
                traits.append(trait.trait.lower())

        return traits
