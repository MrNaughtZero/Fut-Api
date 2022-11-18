from app.database import db
import app.models.all as Models
import math
import datetime
import requests
from app import cache
from app.helpers.cache import DeleteCache

class Player(db.Model):
    __tablename__ = "players"
    id = db.Column(db.Integer, primary_key=True)
    player_id = db.Column(db.Integer, nullable=False, unique=True)
    name = db.Column(db.String(255), nullable=False)
    age = db.Column(db.Integer, nullable=True)
    dob = db.Column(db.String(100), nullable=True)
    card_type = db.Column(db.String(100), nullable=False)
    attributes = db.relationship("PlayerAttributes", backref="player_attributes", lazy=True)
    skill_moves = db.Column(db.Integer, nullable=False)
    weak_foot = db.Column(db.Integer, nullable=False)
    preferred_foot = db.Column(db.String(50), nullable=False)
    height = db.Column(db.Integer, nullable=False)
    weight = db.Column(db.Integer, nullable=False)
    rating = db.Column(db.Integer, nullable=False)
    position = db.Column(db.String(20), nullable=False)
    alt_positions = db.relationship("PlayerAltPositions", backref="player_alt_positions", lazy=True)
    accelerate = db.Column(db.String(50), nullable=True)
    traits = db.relationship("PlayerTraits", backref="player", lazy=True)
    nation = db.Column(db.String(100), nullable=False)
    nation_id = db.Column(db.Integer, nullable=False)
    league = db.Column(db.String(100), nullable=False)
    league_id = db.Column(db.Integer, nullable=False)
    club = db.Column(db.String(255), nullable=False)
    club_id = db.Column(db.Integer, nullable=False)
    price = db.relationship("PlayerPrice", backref="player_prices", lazy=True)
    sbc = db.Column(db.Boolean, nullable=True)
    fut_player_id = db.Column(db.Integer, nullable=False)
    fut_resource_id = db.Column(db.Integer, nullable=False)
    fut_android_id = db.Column(db.Integer, nullable=True)
    added_on = db.Column(db.String(100), nullable=False)
    created_on = db.Column(db.DateTime, server_default=db.func.now())
    updated_on = db.Column(
        db.DateTime, server_default=db.func.now(), server_onupdate=db.func.now()
    )

    def update_prices(self):
        all_players = self.query.all()

        for index, player in enumerate(all_players):
            pc_uri = f"https://www.futbin.org/futbin/api/23/fetchPlayerInformationAndroid?ID={str(player.fut_android_id)}&platform=PC"
            console_uri = f"https://www.futbin.org/futbin/api/23/fetchPlayerInformationAndroid?ID={player.fut_android_id}&platform=PS"
            headers = {
                "Accept" : "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
                "Accept-Encoding" : "gzip, deflate, br",
                "DNT" : "1",
                "Host" : "futbin.org",
                "TE" : "trailers",
                "Upgrade-Insecure-Requests" : "1",
                "User-Agent" : "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:107.0) Gecko/20100101 Firefox/107.0"
            }

            pc_request = requests.get(pc_uri, headers=headers)
            
            
            if pc_request.status_code == 304 or pc_request.status_code == 200 :
                response = pc_request.json()
                for obj in response["data"]:
                    if "Player_Resource" in obj and obj["Player_Resource"] == player.fut_resource_id:
                        player.price[0].pc = obj["LCPrice"]
                        db.session.commit()
            else:
                return False

            ps_request = requests.get(console_uri, headers=headers)
            if ps_request.status_code == 304 or ps_request.status_code == 200:
                response = ps_request.json()
                for obj in response["data"]:
                    if "Player_Resource" in obj and obj["Player_Resource"] == player.fut_resource_id:
                        player.price[0].console = obj["LCPrice"]
                        db.session.commit()
            else:
                return False

            return True

    def add_player(self, data):
        self.player_id = data["id"],
        self.name = data["name"]
        self.age = data["age"]
        self.dob = data["dob"]
        self.card_type = data["cardType"]
        self.skill_moves = data["skillMoves"]
        self.weak_foot = data["weakFoot"]
        self.preferred_foot = data["preferredFoot"]
        self.height = data["height"]
        self.weight = data["weight"]
        self.rating = data["rating"]
        self.position = data["position"]
        self.accelerate = data["acceleRATE"]
        self.nation = data["nation"]
        self.nation_id = data["nation_id"]
        self.league = data["league"]
        self.league_id = data["league_id"]
        self.club = data["club"]
        self.club_id = data["club_id"]
        self.fut_player_id = data["futPlayerId"]
        self.fut_resource_id = data["futSourceId"]
        self.added_on = data["addedOn"]

        player = db.session.add(self)
        db.session.commit()

        Models.PlayerAttributes().add_attributes(self.id, data["attributes"], self.position)
        
        if(len(data["altPositions"]) > 0):
            for position in data["altPositions"]:
                Models.PlayerAltPositions().add_player_positions(self.id, position)

        if(len(data["traits"]) > 0):
            for trait in data["traits"]:
                Models.PlayerTraits().add_player_traits(self.id, trait)

        Models.PlayerPrice().add_player_price(self.id)

        Models.PlayerImage().add_image(player.player_id, player.fut_resource_id, data["img"])

        cache.clear()

    def find_players_with_page_and_limit(self, page, limit):
        try:
            query_limit = 15 if limit == 0 else limit

            total_pages = math.ceil(len(self.query.all()) / limit)
            query = self.query.paginate(page, query_limit).items
            
            if not query:
                return ["Page does not exist", False, 400]
            
            result = []

            for q in query:
                structured = self.structure_player_data(q)
                result.append(structured)
            return [result, True, total_pages]
        except Exception as e:
            return ["Something went wrong. Please try again", False, 500]

    def find_players_by_nation_with_page_and_limit(self, page, limit, nation_id):
        try:
            query_limit = 15 if limit == 0 else limit

            total_pages = math.ceil(len(self.query.filter_by(nation_id=nation_id).all()) / limit)
            query = self.query.filter_by(nation_id=nation_id).paginate(page, query_limit).items
            
            if not query:
                return ["Page does not exist", False, 400]
            
            result = []

            for q in query:
                structured = self.structure_player_data(q)
                result.append(structured)
            return [result, True, total_pages]
        except Exception as e:
            return ["Something went wrong. Please try again", False, 500]

    def find_players_by_league_with_page_and_limit(self, page, limit, league_id):
        try:
            query_limit = 15 if limit == 0 else limit

            total_pages = math.ceil(len(self.query.filter_by(league_id=league_id).all()) / limit)
            query = self.query.filter_by(league_id=league_id).paginate(page, query_limit).items
            
            if not query:
                return ["Page does not exist", False, 400]
            
            result = []

            for q in query:
                structured = self.structure_player_data(q)
                result.append(structured)
            return [result, True, total_pages]
        except Exception as e:
            return ["Something went wrong. Please try again", False, 500]

    def find_players_by_club_with_page_and_limit(self, page, limit, club_id):
        try:
            query_limit = 15 if limit == 0 else limit

            total_pages = math.ceil(len(self.query.filter_by(club_id=int(club_id)).all()) / limit)
            query = self.query.filter_by(club_id=int(club_id)).paginate(page, query_limit).items
            
            if not query:
                return ["Page does not exist", False, 400]
            
            result = []

            for q in query:
                structured = self.structure_player_data(q)
                result.append(structured)
            return [result, True, total_pages]
        except Exception as e:
            return ["Something went wrong. Please try again", False, 500]

    def find_player_by_id(self, player_id):
        try:
            query = self.query.filter_by(player_id=int(player_id)).first()
            
            if not query:
                return ["Invalid Player ID", False, 404]
                        
            return [self.structure_player_data(query), True, True]
        except Exception as e:
            print(e)
            return ["Something went wrong. Please try again", False, 500]

    def find_players_by_nation_id(self, nation_id):
        return self.query.filter_by(nation_id=nation_id).all()

    def find_players_by_club_id(self, club_id):
        return self.query.filter_by(club_id=club_id).all()

    def find_players_by_league_id(self, league_id):
        return self.query.filter_by(league_id=league_id).all()

    def find_players_by_card_type(self, card_type):
        return self.query.filter_by(card_type=card_type).all()

    def get_player_price(self, player_id):
        try:
            query = self.query.filter_by(player_id=int(player_id)).first()
            
            if not query:
                return ["Invalid Player ID", False, 404]

            prices = {
                "pc" : query.price[0].pc,
                "console" : query.price[0].console
            }
                        
            return [prices, True, True]
        except Exception as e:
            return ["Something went wrong. Please try again", False, 500]

    def update_player_prices(self, player_id):
        try:
            player = self.query.filter_by(player_id=player_id).first()
            
            pc_uri = f"https://www.futbin.org/futbin/api/23/fetchPlayerInformationAndroid?ID={str(player.fut_android_id)}&platform=PC"
            console_uri = f"https://www.futbin.org/futbin/api/23/fetchPlayerInformationAndroid?ID={player.fut_android_id}&platform=PS"
            
            headers = {
                "Accept" : "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
                "Accept-Encoding" : "gzip, deflate, br",
                "DNT" : "1",
                "Host" : "futbin.org",
                "TE" : "trailers",
                "Upgrade-Insecure-Requests" : "1",
                "User-Agent" : "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:107.0) Gecko/20100101 Firefox/107.0"
            }

            pc_request = requests.get(pc_uri, headers=headers)
            
            if pc_request.status_code == 304 or pc_request.status_code == 200 :
                response = pc_request.json()
                for obj in response["data"]:
                    if "Player_Resource" in obj and obj["Player_Resource"] == player.fut_resource_id:
                        player.price[0].pc = obj["LCPrice"]
                        db.session.commit()

            ps_request = requests.get(console_uri, headers=headers)
            if ps_request.status_code == 304 or ps_request.status_code == 200:
                response = ps_request.json()
                for obj in response["data"]:
                    if "Player_Resource" in obj and obj["Player_Resource"] == player.fut_resource_id:
                        player.price[0].console = obj["LCPrice"]
                        db.session.commit()

            DeleteCache().update_players_cache()
        except Exception as e:
            pass

    def latest_players(self, page, limit, player_id):
        try:
            query = self.query.filter_by(player_id=int(player_id)).first()
            
            if not query:
                return ["Invalid Player ID", False, 404]

            query_limit = 15 if limit == 0 else limit
            total_pages = math.ceil(len(self.query.filter(Player.id > query.id).all()) / limit)

            latest = self.query.filter(Player.id > query.id).paginate(page, query_limit).items

            result = []

            for q in latest:
                try:
                    structured = self.structure_player_data(q)
                    result.append(structured)
                except:
                    pass

            return [result, True, total_pages]
        except Exception as e:
            return ["Something went wrong. Please try again", False, 500]

    def search_players(self, json):
        try:
            data = {}
            for key, value in json.items():
                if value != None:
                    data[key] = value

            if "name" in data:
                if len(data["name"]) < 3:
                    raise Exception("Invalid Name")

            all_players = self.query.filter(
                Player.name.contains(data["name"])
            ).all()

            matching_players = []

            for player in all_players:
                if "min_age" in data:
                    if player.age < int(data["min_age"]):
                        continue

                if "max_age" in data:
                    if player.age > int(data["max_age"]):
                        continue

                if "card_type" in data:
                    card = Models.Cards().get_card(data["card_type"])
                    if not card:
                        raise Exception("Invalid Card")
                    if card.card_type != player.card_type:
                        continue

                if "attributes" in data:
                    if "pace" in data["attributes"]:
                        if "min_overall" in data["attributes"]["pace"]:
                            if player.attributes[0].pace_overall < int(data["attributes"]["pace"]["min_overall"]):
                                continue
                        if "max_overall" in data["attributes"]["pace"]:
                            if player.attributes[0].pace_overall > int(data["attributes"]["pace"]["max_overall"]):
                                continue
                        if "min_acceleration" in data["attributes"]["pace"]:
                            if player.attributes[0].pace_acceleration < int(data["attributes"]["pace"]["min_acceleration"]):
                                continue
                        if "max_acceleration" in data["attributes"]["pace"]:
                            if player.attributes[0].pace_acceleration > int(data["attributes"]["pace"]["max_acceleration"]):
                                continue
                        if "min_sprint_speed" in data["attributes"]["pace"]:
                            if player.attributes[0].pace_sprint_speed < int(data["attributes"]["pace"]["min_sprint_speed"]):
                                continue
                        if "max_sprint_speed" in data["attributes"]["pace"]:
                            if player.attributes[0].pace_sprint_speed > int(data["attributes"]["pace"]["max_sprint_speed"]):
                                continue
                    if "shooting" in data["attributes"]:
                        if "min_overall" in data["attributes"]["shooting"]:
                            if player.attributes[0].shooting_overall < int(data["attributes"]["shooting"]["min_overall"]):
                                continue
                        if "max_overall" in data["attributes"]["shooting"]:
                            if player.attributes[0].shooting_overall > int(data["attributes"]["shooting"]["max_overall"]):
                                continue
                        if "min_positioning" in data["attributes"]["shooting"]:
                            if player.attributes[0].shooting_positioning < int(data["attributes"]["shooting"]["min_positioning"]):
                                continue
                        if "max_overall" in data["attributes"]["shooting"]:
                            if player.attributes[0].shooting_positioning > int(data["attributes"]["shooting"]["max_positioning"]):
                                continue
                        if "min_finishing" in data["attributes"]["shooting"]:
                            if player.attributes[0].shooting_finishing < int(data["attributes"]["shooting"]["min_finishing"]):
                                continue
                        if "max_finishing" in data["attributes"]["shooting"]:
                            if player.attributes[0].shooting_finishing > int(data["attributes"]["shooting"]["max_finishing"]):
                                continue
                        if "min_shot_power" in data["attributes"]["shooting"]:
                            if player.attributes[0].shooting_shot_power < int(data["attributes"]["shooting"]["min_shot_power"]):
                                continue
                        if "max_shot_power" in data["attributes"]["shooting"]:
                            if player.attributes[0].shooting_shot_power > int(data["attributes"]["shooting"]["max_shot_power"]):
                                continue
                        if "min_long_shots" in data["attributes"]["shooting"]:
                            if player.attributes[0].shooting_long_shots < int(data["attributes"]["shooting"]["min_long_shots"]):
                                continue
                        if "max_long_shots" in data["attributes"]["shooting"]:
                            if player.attributes[0].shooting_long_shots > int(data["attributes"]["shooting"]["max_long_shots"]):
                                continue
                        if "min_volleys" in data["attributes"]["shooting"]:
                            if player.attributes[0].shooting_volleys < int(data["attributes"]["shooting"]["min_volleys"]):
                                continue
                        if "max_volleys" in data["attributes"]["shooting"]:
                            if player.attributes[0].shooting_volleys > int(data["attributes"]["shooting"]["max_volleys"]):
                                continue
                        if "min_penalties" in data["attributes"]["shooting"]:
                            if player.attributes[0].shooting_penalties < int(data["attributes"]["shooting"]["min_penalties"]):
                                continue
                        if "max_penalties" in data["attributes"]["shooting"]:
                            if player.attributes[0].shooting_penalties > int(data["attributes"]["shooting"]["max_penalties"]):
                                continue

                    if "passing" in data["attributes"]:
                        if "min_overall" in data["attributes"]["passing"]:
                            if player.attributes[0].passing_overall < int(data["attributes"]["passing"]["min_overall"]):
                                continue
                        if "max_overall" in data["attributes"]["passing"]:
                            if player.attributes[0].passing_overall > int(data["attributes"]["passing"]["max_overall"]):
                                continue
                        if "min_vision" in data["attributes"]["passing"]:
                            if player.attributes[0].passing_vision < int(data["attributes"]["passing"]["min_vision"]):
                                continue
                        if "max_vision" in data["attributes"]["passing"]:
                            if player.attributes[0].passing_vision > int(data["attributes"]["passing"]["max_vision"]):
                                continue
                        if "min_crossing" in data["attributes"]["passing"]:
                            if player.attributes[0].passing_crossing < int(data["attributes"]["passing"]["min_crossing"]):
                                continue
                        if "max_crossing" in data["attributes"]["passing"]:
                            if player.attributes[0].passing_crossing > int(data["attributes"]["passing"]["max_crossing"]):
                                continue
                        if "min_freekick_accuracy" in data["attributes"]["passing"]:
                            if player.attributes[0].passing_freekick_accuracy < int(data["attributes"]["passing"]["min_freekick_accuracy"]):
                                continue
                        if "max_freekick_accuracy" in data["attributes"]["passing"]:
                            if player.attributes[0].passing_freekick_accuracy > int(data["attributes"]["passing"]["max_freekick_accuracy"]):
                                continue
                        if "min_short_passing" in data["attributes"]["passing"]:
                            if player.attributes[0].passing_short_passing < int(data["attributes"]["passing"]["min_short_passing"]):
                                continue
                        if "max_short_passing" in data["attributes"]["passing"]:
                            if player.attributes[0].passing_short_passing > int(data["attributes"]["passing"]["max_short_passing"]):
                                continue
                        if "min_long_passing" in data["attributes"]["passing"]:
                            if player.attributes[0].passing_long_passing < int(data["attributes"]["passing"]["min_long_passing"]):
                                continue
                        if "max_long_passing" in data["attributes"]["passing"]:
                            if player.attributes[0].passing_long_passing > int(data["attributes"]["passing"]["max_long_passing"]):
                                continue
                        if "min_curve" in data["attributes"]["passing"]:
                            if player.attributes[0].passing_curve < int(data["attributes"]["passing"]["min_curve"]):
                                continue
                        if "max_curve" in data["attributes"]["passing"]:
                            if player.attributes[0].passing_curve > int(data["attributes"]["passing"]["max_curve"]):
                                continue

                    if "dribbling" in data["attributes"]:
                        if "min_overall" in data["attributes"]["dribbling"]:
                            if player.attributes[0].dribbling_overall < int(data["attributes"]["dribbling"]["min_overall"]):
                                continue
                        if "max_overall" in data["attributes"]["dribbling"]:
                            if player.attributes[0].dribbling_overall > int(data["attributes"]["dribbling"]["max_overall"]):
                                continue
                        if "min_agility" in data["attributes"]["dribbling"]:
                            if player.attributes[0].dribbling_agility < int(data["attributes"]["dribbling"]["min_agility"]):
                                continue
                        if "max_agility" in data["attributes"]["dribbling"]:
                            if player.attributes[0].dribbling_agility > int(data["attributes"]["dribbling"]["max_agility"]):
                                continue
                        if "min_balance" in data["attributes"]["dribbling"]:
                            if player.attributes[0].dribbling_balance < int(data["attributes"]["dribbling"]["min_balance"]):
                                continue
                        if "max_balance" in data["attributes"]["dribbling"]:
                            if player.attributes[0].dribbling_balance > int(data["attributes"]["dribbling"]["max_balance"]):
                                continue
                        if "min_reactions" in data["attributes"]["dribbling"]:
                            if player.attributes[0].dribbling_reactions < int(data["attributes"]["dribbling"]["min_reactions"]):
                                continue
                        if "max_reactions" in data["attributes"]["dribbling"]:
                            if player.attributes[0].dribbling_reactions > int(data["attributes"]["dribbling"]["max_reactions"]):
                                continue
                        if "min_ball_control" in data["attributes"]["dribbling"]:
                            if player.attributes[0].dribbling_ball_control < int(data["attributes"]["dribbling"]["min_ball_control"]):
                                continue
                        if "max_ball_control" in data["attributes"]["dribbling"]:
                            if player.attributes[0].dribbling_ball_control > int(data["attributes"]["dribbling"]["max_ball_control"]):
                                continue
                        if "min_dribbling" in data["attributes"]["dribbling"]:
                            if player.attributes[0].dribbling_dribbling < int(data["attributes"]["dribbling"]["min_dribbling"]):
                                continue
                        if "max_dribbling" in data["attributes"]["dribbling"]:
                            if player.attributes[0].dribbling_dribbling > int(data["attributes"]["dribbling"]["max_dribbling"]):
                                continue
                        if "min_composure" in data["attributes"]["dribbling"]:
                            if player.attributes[0].dribbling_composure < int(data["attributes"]["dribbling"]["min_composure"]):
                                continue
                        if "max_composure" in data["attributes"]["dribbling"]:
                            if player.attributes[0].dribbling_composure > int(data["attributes"]["dribbling"]["max_composure"]):
                                continue

                    if "defending" in data["attributes"]:
                        if "min_overall" in data["attributes"]["defending"]:
                            if player.attributes[0].defending_overall < int(data["attributes"]["defending"]["min_overall"]):
                                continue
                        if "max_overall" in data["attributes"]["defending"]:
                            if player.attributes[0].defending_overall > int(data["attributes"]["defending"]["max_overall"]):
                                continue
                        if "min_interceptions" in data["attributes"]["defending"]:
                            if player.attributes[0].defending_interceptions < int(data["attributes"]["defending"]["min_interceptions"]):
                                continue
                        if "max_interceptions" in data["attributes"]["defending"]:
                            if player.attributes[0].defending_interceptions > int(data["attributes"]["defending"]["max_interceptions"]):
                                continue
                        if "min_heading_accuracy" in data["attributes"]["defending"]:
                            if player.attributes[0].defending_heading_accuracy < int(data["attributes"]["defending"]["min_heading_accuracy"]):
                                continue
                        if "max_heading_accuracy" in data["attributes"]["defending"]:
                            if player.attributes[0].defending_heading_accuracy > int(data["attributes"]["defending"]["max_heading_accuracy"]):
                                continue
                        if "min_def_awareness" in data["attributes"]["defending"]:
                            if player.attributes[0].defending_def_awareness < int(data["attributes"]["defending"]["min_def_awareness"]):
                                continue
                        if "max_def_awareness" in data["attributes"]["defending"]:
                            if player.attributes[0].defending_def_awareness > int(data["attributes"]["defending"]["max_def_awareness"]):
                                continue
                        if "min_standing_tackle" in data["attributes"]["defending"]:
                            if player.attributes[0].defending_standing_tackle < int(data["attributes"]["defending"]["min_standing_tackle"]):
                                continue
                        if "max_standing_tackle" in data["attributes"]["defending"]:
                            if player.attributes[0].defending_standing_tackle > int(data["attributes"]["defending"]["max_standing_tackle"]):
                                continue

                        if "min_sliding_tackle" in data["attributes"]["defending"]:
                            if player.attributes[0].defending_sliding_tackle < int(data["attributes"]["defending"]["min_sliding_tackle"]):
                                continue
                        if "max_sliding_tackle" in data["attributes"]["defending"]:
                            if player.attributes[0].defending_sliding_tackle > int(data["attributes"]["defending"]["max_sliding_tackle"]):
                                continue

                    if "physical" in data["attributes"]:
                        if "min_overall" in data["attributes"]["physical"]:
                            if player.attributes[0].physical_overall < int(data["attributes"]["physical"]["min_overall"]):
                                continue
                        if "max_overall" in data["attributes"]["physical"]:
                            if player.attributes[0].physical_overall > int(data["attributes"]["physical"]["max_overall"]):
                                continue
                        if "min_jumping" in data["attributes"]["physical"]:
                            if player.attributes[0].physical_jumping < int(data["attributes"]["physical"]["min_jumping"]):
                                continue
                        if "max_jumping" in data["attributes"]["physical"]:
                            if player.attributes[0].physical_jumping > int(data["attributes"]["physical"]["max_jumping"]):
                                continue
                        if "min_stamina" in data["attributes"]["physical"]:
                            if player.attributes[0].physical_stamina < int(data["attributes"]["physical"]["min_stamina"]):
                                continue
                        if "max_stamina" in data["attributes"]["physical"]:
                            if player.attributes[0].physical_stamina > int(data["attributes"]["physical"]["max_stamina"]):
                                continue
                        if "min_strength" in data["attributes"]["physical"]:
                            if player.attributes[0].physical_strength < int(data["attributes"]["physical"]["min_strength"]):
                                continue
                        if "max_strength" in data["attributes"]["physical"]:
                            if player.attributes[0].physical_strength > int(data["attributes"]["physical"]["max_strength"]):
                                continue

                        if "min_aggression" in data["attributes"]["physical"]:
                            if player.attributes[0].physical_aggression < int(data["attributes"]["physical"]["min_aggression"]):
                                continue
                        if "max_aggression" in data["attributes"]["physical"]:
                            if player.attributes[0].physical_aggression > int(data["attributes"]["physical"]["max_aggression"]):
                                continue

                    if "gk_diving" in data["attributes"]:
                        if "min_overall" in data["attributes"]["gk_diving"]:
                            if player.attributes[0].gk_diving_overall < int(data["attributes"]["gk_diving"]["min_overall"]):
                                continue
                        if "max_overall" in data["attributes"]["gk_diving"]:
                            if player.attributes[0].gk_diving_overall > int(data["attributes"]["gk_diving"]["max_overall"]):
                                continue
                        if "min_diving" in data["attributes"]["gk_diving"]:
                            if player.attributes[0].gk_diving < int(data["attributes"]["gk_diving"]["min_diving"]):
                                continue
                        if "max_diving" in data["attributes"]["gk_diving"]:
                            if player.attributes[0].gk_diving > int(data["attributes"]["gk_diving"]["max_diving"]):
                                continue

                    if "gk_handling" in data["attributes"]:
                        if "min_overall" in data["attributes"]["gk_handling"]:
                            if player.attributes[0].gk_handling_overall < int(data["attributes"]["gk_handling"]["min_overall"]):
                                continue
                        if "max_overall" in data["attributes"]["gk_handling"]:
                            if player.attributes[0].gk_handling_overall > int(data["attributes"]["gk_handling"]["max_overall"]):
                                continue
                        if "min_handling" in data["attributes"]["gk_handling"]:
                            if player.attributes[0].gk_handling < int(data["attributes"]["gk_handling"]["min_handling"]):
                                continue
                        if "max_handling" in data["attributes"]["gk_handling"]:
                            if player.attributes[0].gk_handling > int(data["attributes"]["gk_handling"]["max_handling"]):
                                continue

                    if "gk_kicking" in data["attributes"]:
                        if "min_overall" in data["attributes"]["gk_kicking"]:
                            if player.attributes[0].gk_kicking_overall < int(data["attributes"]["gk_kicking"]["min_overall"]):
                                continue
                        if "max_overall" in data["attributes"]["gk_kicking"]:
                            if player.attributes[0].gk_kicking_overall > int(data["attributes"]["gk_kicking"]["max_overall"]):
                                continue
                        if "min_kicking" in data["attributes"]["gk_kicking"]:
                            if player.attributes[0].gk_kicking < int(data["attributes"]["gk_kicking"]["min_kicking"]):
                                continue
                        if "max_kicking" in data["attributes"]["gk_kicking"]:
                            if player.attributes[0].gk_kicking > int(data["attributes"]["gk_kicking"]["max_kicking"]):
                                continue

                    if "gk_reflexes" in data["attributes"]:
                        if "min_overall" in data["attributes"]["gk_reflexes"]:
                            if player.attributes[0].gk_reflexes_overall < int(data["attributes"]["gk_reflexes"]["min_overall"]):
                                continue
                        if "max_overall" in data["attributes"]["gk_reflexes"]:
                            if player.attributes[0].gk_reflexes_overall > int(data["attributes"]["gk_reflexes"]["max_overall"]):
                                continue
                        if "min_reflexes" in data["attributes"]["gk_reflexes"]:
                            if player.attributes[0].gk_reflexes < int(data["attributes"]["gk_reflexes"]["min_reflexes"]):
                                continue
                        if "max_reflexes" in data["attributes"]["gk_reflexes"]:
                            if player.attributes[0].gk_reflexes > int(data["attributes"]["gk_reflexes"]["max_reflexes"]):
                                continue

                    if "gk_speed" in data["attributes"]:
                        if "min_overall" in data["attributes"]["gk_speed"]:
                            if player.attributes[0].gk_speed_overall < int(data["attributes"]["gk_speed"]["min_overall"]):
                                continue
                        if "max_overall" in data["attributes"]["gk_speed"]:
                            if player.attributes[0].gk_speed_overall > int(data["attributes"]["gk_speed"]["max_overall"]):
                                continue
                        if "min_acceleration" in data["attributes"]["gk_speed"]:
                            if player.attributes[0].gk_speed_acceleration < int(data["attributes"]["gk_speed"]["min_acceleration"]):
                                continue
                        if "max_acceleration" in data["attributes"]["gk_speed"]:
                            if player.attributes[0].gk_speed_acceleration > int(data["attributes"]["gk_speed"]["max_acceleration"]):
                                continue
                        if "min_sprint_speed" in data["attributes"]["gk_speed"]:
                            if player.attributes[0].gk_speed_sprint_speed < int(data["attributes"]["gk_speed"]["min_sprint_speed"]):
                                continue
                        if "max_sprint_speed" in data["attributes"]["gk_speed"]:
                            if player.attributes[0].gk_speed_sprint_speed > int(data["attributes"]["gk_speed"]["max_sprint_speed"]):
                                continue

                    if "gk_positioning" in data["attributes"]:
                        if "min_overall" in data["attributes"]["gk_positioning"]:
                            if player.attributes[0].gk_positioning_overall < int(data["attributes"]["gk_positioning"]["min_overall"]):
                                continue
                        if "max_overall" in data["attributes"]["gk_positioning"]:
                            if player.attributes[0].gk_positioning_overall > int(data["attributes"]["gk_positioning"]["max_overall"]):
                                continue
                        if "min_positioning" in data["attributes"]["gk_positioning"]:
                            if player.attributes[0].gk_positioning < int(data["attributes"]["gk_positioning"]["min_positioning"]):
                                continue
                        if "max_positioning" in data["attributes"]["gk_positioning"]:
                            if player.attributes[0].gk_positioning > int(data["attributes"]["gk_positioning"]["max_positioning"]):
                                continue

                if "min_skill_moves" in data:
                    if player.skill_moves < int(data["min_skill_moves"]):
                        continue
                if "max_skill_moves" in data:
                    if player.skill_moves > int(data["max_skill_moves"]):
                        continue

                if "min_weak_foot" in data:
                    if player.weak_foot < int(data["min_weak_foot"]):
                        continue
                if "max_weak_foot" in data:
                    if player.weak_foot > int(data["max_weak_foot"]):
                        continue

                if "preferred_foot" in data:
                    if data["preferred_foot"].lower() != player.preferred_foot.lower():
                        continue

                if "min_height" in data:
                    if player.height < int(data["min_height"]):
                        continue
                if "max_height" in data:
                    if player.height > int(data["max_height"]):
                        continue

                if "min_weight" in data:
                    if player.weight < int(data["min_weight"]):
                        continue
                if "max_weight" in data:
                    if player.weight > int(data["max_weight"]):
                        continue

                if "min_rating" in data:
                    if player.rating < int(data["min_rating"]):
                        continue
                if "max_rating" in data:
                    if player.rating > int(data["max_rating"]):
                        continue

                if "alt_positions" in data:
                    positions = Models.PlayerAltPositions().get_player_alt_positions(player.player_id)
                    for position in data["alt_positions"]:
                        if position not in positions:
                            continue

                if "traits" in data:
                    traits = Models.PlayerTraits().get_all_player_traits(player.player_id)
                    for trait in data["traits"]:
                        if trait not in traits:
                            continue

                if "price" in data:
                    if "console" in data["price"]:
                        if player.price[0].console < int(data["price"]["console"]["min_price"]):
                            continue
                        if player.price[0].console > int(data["price"]["console"]["max_price"]):
                            continue
                    if "pc" in data["price"]:
                        if player.price[0].console < int(data["price"]["pc"]["min_price"]):
                            continue
                        if player.price[0].console > int(data["price"]["pc"]["max_price"]):
                            continue

                if "accelerate" in data:
                    if data["accelerate"].lower() != player.accelerate.lower():
                        continue

                if "nation_id" in data:
                    if int(data["nation_id"]) != player.nation_id:
                        continue

                if "league_id" in data:
                    if int(data["league_id"]) != player.league_id:
                        continue
                
                if "club_id" in data:
                    if int(data["club_id"]) != player.club_id:
                        continue

                if "added_after" in data:
                    split_date = data["added_after"].split("/")
                    db_split_date = player.added_after.split("/")
                    queried_date = datetime.datetime(int(split_date[0]), int(split_date[1]), int(split_date[2]))
                    db_date = datetime.datetime(int(queried_date[0]), int(queried_date[1]), int(queried_date[2]))

                    if db_date < queried_date:
                        continue

                matching_players.append(player)

            result = []

            for player in matching_players:
                result.append(self.structure_player_data(player))

            return [result, True, True] 

        except Exception as e:
            if "Invalid Name" in str(e):
                return ["Name must be at least 3 characters. ", False, 400]
            if "Invalid Card" in str(e):
                return ["Invalid card type ", False, 400]
            return ["Something went wrong. Please try again", False, 500]

    def structure_player_data(self, player):
        data = {
            "id" : player.player_id,
            "name" : player.name,
            "age" : player.age,
            "dob" : player.dob,
            "card_type" : player.card_type,
            "attributes" : {
                "pace" : {
                    "overall" : player.attributes[0].pace_overall,
                    "acceleration" : player.attributes[0].pace_acceleration,
                    "sprint_speed" : player.attributes[0].pace_sprint_speed,
                },
                "shooting" : {
                    "overall" : player.attributes[0].shooting_overall,
                    "positioning" : player.attributes[0].shooting_positioning,
                    "finishing" : player.attributes[0].shooting_finishing,
                    "shot_power" : player.attributes[0].shooting_shot_power,
                    "long_shots" : player.attributes[0].shooting_long_shots,
                    "volleys" : player.attributes[0].shooting_volleys,
                    "penalties" : player.attributes[0].shooting_penalties,
                },
                "passing" : {
                    "overall" : player.attributes[0].passing_overall,
                    "vision" : player.attributes[0].passing_vision,
                    "crossing" : player.attributes[0].passing_crossing,
                    "freekick_accuracy" : player.attributes[0].passing_freekick_accuracy,
                    "short_passing" : player.attributes[0].passing_short_passing,
                    "long_passing" : player.attributes[0].passing_long_passing,
                    "curve" : player.attributes[0].passing_curve
                },
                "dribbling" : {
                    "overall" : player.attributes[0].dribbling_overall,
                    "agility" : player.attributes[0].dribbling_agility,
                    "balance" : player.attributes[0].dribbling_balance,
                    "reactions" : player.attributes[0].dribbling_reactions,
                    "ball_control" : player.attributes[0].dribbling_ball_control,
                    "dribbling" : player.attributes[0].dribbling_dribbling,
                    "composure" : player.attributes[0].dribbling_composure,
                },
                "defending" : {
                    "overall" : player.attributes[0].defending_overall,
                    "interceptions" : player.attributes[0].defending_interceptions,
                    "heading_accuracy" : player.attributes[0].defending_heading_accuracy,
                    "def_awareness" : player.attributes[0].defending_def_awareness,
                    "standing_tackle" : player.attributes[0].defending_standing_tackle,
                    "sliding_tackle" : player.attributes[0].defending_sliding_tackle
                },
                "physical" : {
                    "overall" : player.attributes[0].physical_overall,
                    "jumping" : player.attributes[0].physical_jumping,
                    "stamina" : player.attributes[0].physical_stamina,
                    "strength" : player.attributes[0].physical_strength,
                    "aggression" : player.attributes[0].physical_aggression,
                }
            },
            "skill_moves" : player.skill_moves,
            "weak_foot" : player.weak_foot,
            "preferred_foot" : player.preferred_foot,
            "height" : player.height,
            "weight" : player.weight,
            "rating" : player.rating,
            "position" : player.position,
            "alt_positions" : Models.PlayerAltPositions().get_player_alt_positions(player.player_id),
            "accelerate" : player.accelerate,
            "traits" : [], ## Add in once I fix traits
            "nation" : player.nation,
            "nation_id" : player.nation_id,
            "league" : player.league,
            "league_id" : player.league_id,
            "club" : player.club,
            "club_id" : player.club_id,
            "price" : Models.PlayerPrice().get_player_price(player.player_id),
            "isSbc" : player.sbc,
            "added_on" : player.added_on
        }

        if "gk" in player.position.lower():
            data["attributes"]["gk_diving"] = {
                "overall" : player.attributes[0].gk_diving_overall,
                "diving" : player.attributes[0].gk_diving
            }

            data["attributes"]["gk_handling"] = {
                "overall" : player.attributes[0].gk_handling_overall,
                "handling" : player.attributes[0].gk_handling
            }

            data["attributes"]["gk_kicking"] = {
                "overall" : player.attributes[0].gk_kicking_overall,
                "kicking" : player.attributes[0].gk_kicking
            }

            data["attributes"]["gk_reflexes"] = {
                "overall" : player.attributes[0].gk_reflexes_overall,
                "reflexes" : player.attributes[0].gk_reflexes
            }

            data["attributes"]["gk_speed"] = {
                "overall" : player.attributes[0].gk_speed_overall,
                "acceleration" : player.attributes[0].gk_speed_acceleration,
                "sprint_speed" : player.attributes[0].gk_speed_sprint_speed
            }

            data["attributes"]["gk_positioning"] = {
                "overall" : player.attributes[0].gk_positioning_overall,
                "positioning" : player.attributes[0].gk_positioning,
            }

        return data
