from app.database import db

class PlayerAttributes(db.Model):
    __tablename__ = "player_attributes"
    id = db.Column(db.Integer, primary_key=True)
    player_id = db.Column(db.Integer, db.ForeignKey("players.id"))
    pace_overall = db.Column(db.Integer, nullable=False)
    pace_acceleration = db.Column(db.Integer, nullable=False)
    pace_sprint_speed = db.Column(db.Integer, nullable=False)
    shooting_overall = db.Column(db.Integer, nullable=False)
    shooting_positioning = db.Column(db.Integer, nullable=False)
    shooting_finishing = db.Column(db.Integer, nullable=False)
    shooting_shot_power = db.Column(db.Integer, nullable=False)
    shooting_long_shots = db.Column(db.Integer, nullable=False)
    shooting_volleys = db.Column(db.Integer, nullable=False)
    shooting_penalties = db.Column(db.Integer, nullable=False)
    passing_overall = db.Column(db.Integer, nullable=False)
    passing_vision = db.Column(db.Integer, nullable=False)
    passing_crossing = db.Column(db.Integer, nullable=False)
    passing_freekick_accuracy = db.Column(db.Integer, nullable=False)
    passing_short_passing = db.Column(db.Integer, nullable=False)
    passing_long_passing = db.Column(db.Integer, nullable=False)
    passing_curve = db.Column(db.Integer, nullable=False)
    dribbling_overall = db.Column(db.Integer, nullable=False)
    dribbling_agility = db.Column(db.Integer, nullable=False)
    dribbling_balance = db.Column(db.Integer, nullable=False)
    dribbling_reactions = db.Column(db.Integer, nullable=False)
    dribbling_ball_control = db.Column(db.Integer, nullable=False)
    dribbling_dribbling = db.Column(db.Integer, nullable=False)
    dribbling_composure = db.Column(db.Integer, nullable=False)
    defending_overall = db.Column(db.Integer, nullable=False)
    defending_interceptions = db.Column(db.Integer, nullable=False)
    defending_heading_accuracy = db.Column(db.Integer, nullable=False)
    defending_def_awareness = db.Column(db.Integer, nullable=False)
    defending_standing_tackle = db.Column(db.Integer, nullable=False)
    defending_sliding_tackle = db.Column(db.Integer, nullable=False)
    physical_overall = db.Column(db.Integer, nullable=False)
    physical_jumping = db.Column(db.Integer, nullable=False)
    physical_stamina = db.Column(db.Integer, nullable=False)
    physical_strength = db.Column(db.Integer, nullable=False)
    physical_aggression = db.Column(db.Integer, nullable=False)
    gk_diving_overall = db.Column(db.Integer, nullable=True)
    gk_diving = db.Column(db.Integer, nullable=True)
    gk_handling_overall = db.Column(db.Integer, nullable=True)
    gk_handling = db.Column(db.Integer, nullable=True)
    gk_kicking_overall = db.Column(db.Integer, nullable=True)
    gk_kicking = db.Column(db.Integer, nullable=True)
    gk_reflexes_overall = db.Column(db.Integer, nullable=True)
    gk_reflexes = db.Column(db.Integer, nullable=True)
    gk_speed_overall = db.Column(db.Integer, nullable=True)
    gk_speed_acceleration = db.Column(db.Integer, nullable=True)
    gk_speed_sprint_speed = db.Column(db.Integer, nullable=True)
    gk_positioning_overall = db.Column(db.Integer, nullable=True)
    gk_positioning = db.Column(db.Integer, nullable=True)

    def add_attributes(self, id, data, position):
        self.player_id = id
        self.pace_overall = data["pace"]["overall"]
        self.pace_acceleration = data["pace"]["acceleration"]
        self.pace_sprint_speed = data["pace"]["sprint_speed"]
        self.shooting_overall = data["shooting"]["overall"]
        self.shooting_positioning = data["shooting"]["positioning"]
        self.shooting_finishing = data["shooting"]["finishing"]
        self.shooting_shot_power = data["shooting"]["shot_power"]
        self.shooting_long_shots = data["shooting"]["long_shots"]
        self.shooting_volleys = data["shooting"]["volleys"]
        self.shooting_penalties = data["shooting"]["penalties"]
        self.passing_overall = data["passing"]["overall"]
        self.passing_vision = data["passing"]["vision"]
        self.passing_crossing = data["passing"]["crossing"]
        self.passing_freekick_accuracy = data["passing"]["fk_accuracy"]
        self.passing_short_passing = data["passing"]["short_passing"]
        self.passing_long_passing = data["passing"]["long_passing"]
        self.passing_curve = data["passing"]["curve"]
        self.dribbling_overall = data["dribbling"]["overall"]
        self.dribbling_agility = data["dribbling"]["agility"]
        self.dribbling_balance = data["dribbling"]["balance"]
        self.dribbling_reactions = data["dribbling"]["reactions"]
        self.dribbling_ball_control = data["dribbling"]["ball_control"]
        self.dribbling_dribbling = data["dribbling"]["dribbling"]
        self.dribbling_composure = data["dribbling"]["composure"]
        self.defending_overall = data["defending"]["overall"]
        self.defending_interceptions = data["defending"]["interceptions"]
        self.defending_heading_accuracy = data["defending"]["heading_accuracy"]
        self.defending_def_awareness = data["defending"]["def_awareness"]
        self.defending_standing_tackle = data["defending"]["standing_tackle"]
        self.defending_sliding_tackle = data["defending"]["sliding_tackle"]
        self.physical_overall = data["physical"]["overall"]
        self.physical_jumping = data["physical"]["jumping"]
        self.physical_stamina = data["physical"]["stamina"]
        self.physical_strength = data["physical"]["strength"]
        self.physical_aggression = data["physical"]["aggression"]

        if(position == "GK"):
            self.gk_diving_overall = data["gk_attributes"]["diving"]["overall"]
            self.gk_diving = data["gk_attributes"]["diving"]["diving"]
            self.gk_handling_overall = data["gk_attributes"]["handling"]["overall"]
            self.gk_handling = data["gk_attributes"]["handling"]["handling"]
            self.gk_kicking_overall = data["gk_attributes"]["kicking"]["overall"]
            self.gk_kicking = data["gk_attributes"]["kicking"]["kicking"]
            self.gk_reflexes_overall = data["gk_attributes"]["reflexes"]["overall"]
            self.gk_reflexes = data["gk_attributes"]["reflexes"]["reflexes"]
            self.gk_speed_overall = data["gk_attributes"]["speed"]["overall"]
            self.gk_speed_acceleration = data["gk_attributes"]["speed"]["acceleration"]
            self.gk_speed_sprint_speed = data["gk_attributes"]["speed"]["sprint_speed"]
            self.gk_positioning_overall = data["gk_attributes"]["positioning"]["overall"]
            self.gk_positioning = data["gk_attributes"]["positioning"]["positioning"]

        db.session.add(self)
        db.session.commit()
    