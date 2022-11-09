from app.database import db
import math
import datetime
import base64
import random
import string
import requests
from time import sleep
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

        PlayerAttributes().add_attributes(self.id, data["attributes"], self.position)
        
        if(len(data["altPositions"]) > 0):
            for position in data["altPositions"]:
                PlayerAltPositions().add_player_positions(self.id, position)

        if(len(data["traits"]) > 0):
            for trait in data["traits"]:
                PlayerTraits().add_player_traits(self.id, trait)

        PlayerPrice().add_player_price(self.id)

        PlayerImage().add_image(player.player_id, player.fut_resource_id, data["img"])

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
                    card = Cards().get_card(data["card_type"])
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
                    positions = PlayerAltPositions().get_player_alt_positions(player.player_id)
                    for position in data["alt_positions"]:
                        if position not in positions:
                            continue

                if "traits" in data:
                    traits = PlayerTraits().get_all_player_traits(player.player_id)
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
            "alt_positions" : PlayerAltPositions().get_player_alt_positions(player.player_id),
            "accelerate" : player.accelerate,
            "traits" : [], ## Add in once I fix traits
            "nation" : player.nation,
            "nation_id" : player.nation_id,
            "league" : player.league,
            "league_id" : player.league_id,
            "club" : player.club,
            "club_id" : player.club_id,
            "price" : PlayerPrice().get_player_price(player.player_id),
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
        self.pace_sprint_speed = data["pace"]["sprintSpeed"]
        self.shooting_overall = data["shooting"]["overall"]
        self.shooting_positioning = data["shooting"]["positioning"]
        self.shooting_finishing = data["shooting"]["finishing"]
        self.shooting_shot_power = data["shooting"]["shotPower"]
        self.shooting_long_shots = data["shooting"]["longShots"]
        self.shooting_volleys = data["shooting"]["volleys"]
        self.shooting_penalties = data["shooting"]["penalties"]
        self.passing_overall = data["passing"]["overall"]
        self.passing_vision = data["passing"]["vision"]
        self.passing_crossing = data["passing"]["crossing"]
        self.passing_freekick_accuracy = data["passing"]["fkAccuracy"]
        self.passing_short_passing = data["passing"]["shortPassing"]
        self.passing_long_passing = data["passing"]["longPassing"]
        self.passing_curve = data["passing"]["curve"]
        self.dribbling_overall = data["dribbling"]["overall"]
        self.dribbling_agility = data["dribbling"]["agility"]
        self.dribbling_balance = data["dribbling"]["balance"]
        self.dribbling_reactions = data["dribbling"]["reactions"]
        self.dribbling_ball_control = data["dribbling"]["ballControl"]
        self.dribbling_dribbling = data["dribbling"]["dribbling"]
        self.dribbling_composure = data["dribbling"]["composure"]
        self.defending_overall = data["defending"]["overall"]
        self.defending_interceptions = data["defending"]["interceptions"]
        self.defending_heading_accuracy = data["defending"]["headingAccuracy"]
        self.defending_def_awareness = data["defending"]["defAwareness"]
        self.defending_standing_tackle = data["defending"]["standingTackle"]
        self.defending_sliding_tackle = data["defending"]["slidingTackle"]
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
            self.gk_speed_sprint_speed = data["gk_attributes"]["speed"]["sprintSpeed"]
            self.gk_positioning_overall = data["gk_attributes"]["positioning"]["overall"]
            self.gk_positioning = data["gk_attributes"]["positioning"]["positioning"]

        db.session.add(self)
        db.session.commit()
            
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
                traits.append(q.trait.lower())

        return traits

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
            "player_count" : len(Player().find_players_by_nation_id(nation_id))
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
        
class Clubs(db.Model):
    __tablename__ = "clubs"
    id = db.Column(db.Integer, primary_key=True)
    club_id = db.Column(db.Integer, nullable=False, unique=True)
    club_name = db.Column(db.String(500), nullable=False, unique=True)
    club_img = db.Column(db.Text(5000000), nullable=False)

    def find_clubs_with_page_and_limit(self, page, limit):
        try:
            query_limit = 15 if limit == 0 else limit

            total_pages = math.ceil(len(self.query.all()) / limit)
            query = self.query.paginate(page, query_limit).items
            
            if not query:
                return ["Page does not exist", False, 400]
            
            result = []

            for q in query:
                result.append({
                    "id" : q.club_id,
                    "name" : q.club_name
                })
            return [result, True, total_pages]
        except Exception as e:
            if "404" in str(e) or "NotFound" in str(e):
                return [f"Page {str(page)} does not exist.", False, 400]
            return ["Something went wrong. Please try again", False, 500]
        
    def get_club(self, club_id):
        q = self.query.filter_by(club_id=club_id).first()

        if not q:
            return [False, False]

        club = {
            "id": club_id,
            "name": q.club_name,
            "player_count" : len(Player().find_players_by_club_id(club_id))
        }

        return [club, True]

    def get_club_image(self, club_id):
        q = self.query.filter_by(club_id=club_id).first()

        if not q:
            return [False, False]

        return [q.club_img, True]

class Cards(db.Model):
    __tablename__ = "cards"
    id = db.Column(db.Integer, primary_key=True)
    card_id = db.Column(db.Integer, nullable=False, unique=True)
    card_name = db.Column(db.String(500), nullable=False, unique=True)
    card_img = db.relationship("CardImage", backref="card_image", lazy=True)

    def add_card(self, id, name):
        self.card_id = id
        self.card_name = name
        db.session.add(self)
        db.session.commit()

    def get_card(self, card_id):
        q = self.query.filter_by(card_id=card_id).first()

        if not q:
            return [False, False]

        card = {
            "id": card_id,
            "name": q.card_name,
            "player_count" : len(Player().find_players_by_card_type(q.card_name))
        }

        return [card, True]

    def get_card_by_id(self, card_id):
        return self.query.filter_by(card_id=card_id).first()

    def find_cards_with_page_and_limit(self, page, limit):
        try:
            query_limit = 15 if limit == 0 else limit

            total_pages = math.ceil(len(self.query.all()) / limit)
            query = self.query.paginate(page, query_limit).items
            
            if not query:
                return ["Page does not exist", False, 400]
            
            result = []

            for q in query:
                result.append({
                    "id" : q.card_id,
                    "name" : q.card_name
                })
            return [result, True, total_pages]
        except Exception as e:
            if "404" in str(e) or "NotFound" in str(e):
                return [f"Page {str(page)} does not exist.", False, 400]
            return ["Something went wrong. Please try again", False, 500]

    def get_image(self, card_id):
        q = self.query.filter_by(card_id=card_id).first()
        
        if not q:
            return [False, False]

        return [q.card_img[0].img, True]
                
class CardImage(db.Model):
    __tablename__ = "card_images"
    id = db.Column(db.Integer, primary_key=True)
    card_id = db.Column(db.Integer, db.ForeignKey("cards.card_id"))
    img = db.Column(db.Text(5000000), nullable=False)

    def add_img(self, id, img):
        self.card_id = id
        self.img = img
        db.session.add(self)
        db.session.commit()

class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    api_key = db.Column(db.String(255), nullable=False)
    subscription = db.Column(db.String(255), nullable=False, default="free")
    start_date = db.Column(db.DateTime, server_default=db.func.now(), nullable=False)
    end_date = db.Column(db.DateTime, nullable=True)
    created_on = db.Column(db.DateTime, server_default=db.func.now())
    updated_on = db.Column(
        db.DateTime, server_default=db.func.now(), server_onupdate=db.func.now()
    )
    limit = db.relationship("Limiter", backref="limit", lazy=True)

    def add_user(self, data):
        self.api_key = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(52))
        self.subscription = data["subscription"]
        self.end_date = data["end_date"]

        db.session.add(self)
        db.session.commit()

        Limiter().setup(self.id)

        return self.api_key

    def validate_api_key(self, api_key):
        q = self.query.filter_by(api_key=api_key).first()
        
        if not q:
            return False

        return True
    
    def validate_premium_api_key(self, api_key):
        q = self.query.filter_by(api_key=api_key).first()
        
        if not q:
            return [{}, False]

        if q.subscription != "premium":
            return [
                {
                    "error" : "The API key provided is a free membership. A premium API is required to access this endpoint."
                }, 
                False
            ]

        if datetime.datetime.now() > q.end_date:
            return [
                {
                    "error" : "Your premium membership has expired. You can not access this endpoint until you renew your membership"
                }, 
                False
            ]

        return [True, True]
            
    def check_if_limited(self, api_key):
        q = self.query.filter_by(api_key=api_key).first()

        if not q:
            return ["Invalid API Key", False]

        if not Limiter().check_limit(q.id, q.subscription):
            return ["Sorry, you've reached your daily limit of requests allowed within a 24 hour period.", False]

        return [True, True]

class Limiter(db.Model):
    __tablename__ = "limiter"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False, unique=True)
    requests = db.Column(db.Integer(), default=0)
    limited = db.Column(db.Boolean, default=False)
    limit_expiry = db.Column(db.DateTime, nullable=True)

    def setup(self, user_id):
        self.user_id = user_id
        db.session.add(self)
        db.session.commit()

    def check_limit(self, user_id, subscription):
        q = self.query.filter_by(user_id=user_id).first()
        now = datetime.datetime.now()
        if subscription == "free" and q.requests >= 1000000:
            if not q.limit_expiry:
                q.limit_expiry = now + datetime.timedelta(minutes=3)
                db.session.commit()
                return False
            if now > q.limit_expiry:
                q.requests = 0
                q.limit_expiry = None
                db.session.commit()
                return True
            return False
        if subscription == "premium" and q.requests >= 20000:
            if not q.limit_expiry:
                q.limit_expiry = now + datetime.timedelta(minutes=3)
                db.session.commit()
                return False
            if now > q.limit_expiry:
                q.requests = 0
                q.limit_expiry = None
                db.session.commit()
                return True
            return False

        q.requests = q.requests + 1
        db.session.commit()

        return True 
