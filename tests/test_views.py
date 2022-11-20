import unittest
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_testing import LiveServerTestCase
from flask_caching import Cache
from os import environ
from dotenv import load_dotenv
import os, sys
import requests
import decimal

currentdir = os.path.dirname(os.path.realpath(__file__))
parentdir = os.path.dirname(currentdir)
sys.path.append(parentdir)

load_dotenv()
from app.models import all as Models
from app.database import setup_db

class TestModel(LiveServerTestCase):
    def create_app(self):
        app = Flask(__name__)
        app.config['TESTING'] = True

        with app.app_context():
            app.config["SQLALCHEMY_DATABASE_URI"] = f'mysql://{environ.get("DB_USER")}:{environ.get("DB_PASS")}@{environ.get("DB_HOST")}/{environ.get("DB_TEST_NAME")}'
            app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

            config = {
                "DEBUG": True,
                "TESTING" : True,
                "CACHE_TYPE": "SimpleCache",
                "CACHE_DEFAULT_TIMEOUT": 300,
            }

            app.config.from_mapping(config)

            cache = Cache(app)
            cache.init_app(app)
            cache.clear()
            
            from app.routes.latest import cards, clubs, leagues, nations, players, users
            app.register_blueprint(cards.api_bp, url_prefix="/v1")
            app.register_blueprint(clubs.api_bp, url_prefix="/v1")
            app.register_blueprint(leagues.api_bp, url_prefix="/v1")
            app.register_blueprint(nations.api_bp, url_prefix="/v1")
            app.register_blueprint(players.api_bp, url_prefix="/v1")
            app.register_blueprint(users.api_bp, url_prefix="/v1")
            
            self.db = setup_db(app, f'mysql://{environ.get("DB_USER")}:{environ.get("DB_PASS")}@{environ.get("DB_HOST")}/{environ.get("DB_TEST_NAME")}')
            self.db.app = app
            self.db.init_app(app)
            self.db.create_all()

            return app

    def tearDown(self):
        self.db.session.remove()
        self.db.drop_all()

    ###### HEADER TESTS ######

    def test_rapid_header_success(self):
        club = Models.Clubs()
        club.add_club(1, "club")
        
        headers = {
            "X-RapidAPI-Proxy-Secret" : environ.get("RAPID_PROXY_SECRET"),
        }

        r = requests.get(f"http://localhost:5000/v1/clubs", headers=headers)

        assert(r.status_code == 200)

    def test_rapid_header_fail(self):
        club = Models.Clubs()
        club.add_club(1, "club")
        
        r = requests.get(f"http://localhost:5000/v1/clubs")

        assert(r.status_code == 400 and r.json()["detail"] == "Invalid Secret")

    ###### CARD TESTS ######

    def test_all_cards(self):
        card = Models.Cards()
        card.add_card("gold")

        headers = {
            "X-RapidAPI-Proxy-Secret" : environ.get("RAPID_PROXY_SECRET"),
        }

        r = requests.get(f"http://localhost:5000/v1/cards", headers=headers)
        
        assert(r.status_code == 200 and r.json()["cards"][0]["name"] == "gold")

    def test_all_cards_with_params(self):
        card = Models.Cards()
        card.add_card("gold")

        cardTwo = Models.Cards()
        cardTwo.add_card("silver")

        headers = {
            "X-RapidAPI-Proxy-Secret" : environ.get("RAPID_PROXY_SECRET"),
        }

        r = requests.get(f"http://localhost:5000/v1/cards?page=1&limit=1", headers=headers)

        assert(r.status_code == 200 and r.json()["cards"][0]["name"] == "gold" and len(r.json()["cards"]) == 1)

    def test_card_id(self):
        card = Models.Cards()
        card.add_card("gold")

        headers = {
            "X-RapidAPI-Proxy-Secret" : environ.get("RAPID_PROXY_SECRET"),
        }

        r = requests.get(f"http://localhost:5000/v1/cards/1", headers=headers)
        
        assert(r.status_code == 200 and r.json()["card"]["name"] == "gold")

    def test_card_image(self):
        card = Models.Cards()
        card.add_card("gold")
        card_image = Models.CardImage()
        card_image.add_img(1, "img")

        headers = {
            "X-RapidAPI-Proxy-Secret" : environ.get("RAPID_PROXY_SECRET"),
        }

        r = requests.get(f"http://localhost:5000/v1/cards/1/image", headers=headers)

        assert(r.status_code == 200 and r.json()["image"] == "img")

    ###### CLUB TESTS ######

    def test_all_clubs(self):
        club = Models.Clubs()
        club.add_club("club", "clubImg")

        headers = {
            "X-RapidAPI-Proxy-Secret" : environ.get("RAPID_PROXY_SECRET"),
        }

        r = requests.get(f"http://localhost:5000/v1/clubs", headers=headers)
        
        assert(r.status_code == 200 and r.json()["clubs"][0]["name"] == "club")

    def test_all_clubs_with_params(self):
        club = Models.Clubs()
        club.add_club("club", "clubImg")

        clubTwo = Models.Clubs()
        clubTwo.add_club("clubTwo", "clubImgTwo")

        headers = {
            "X-RapidAPI-Proxy-Secret" : environ.get("RAPID_PROXY_SECRET"),
        }

        r = requests.get(f"http://localhost:5000/v1/clubs?page=1&limit=1", headers=headers)

        assert(r.status_code == 200 and r.json()["clubs"][0]["name"] == "club" and len(r.json()["clubs"]) == 1)

    def test_club_id(self):
        club = Models.Clubs()
        club.add_club("club", "clubImg")

        headers = {
            "X-RapidAPI-Proxy-Secret" : environ.get("RAPID_PROXY_SECRET"),
        }

        r = requests.get(f"http://localhost:5000/v1/clubs/1", headers=headers)
        
        assert(r.status_code == 200 and r.json()["club"]["name"] == "club")

    def test_club_image(self):
        club = Models.Clubs()
        club.add_club("liverpool", "clubImg")

        headers = {
            "X-RapidAPI-Proxy-Secret" : environ.get("RAPID_PROXY_SECRET"),
        }

        r = requests.get(f"http://localhost:5000/v1/clubs/1/image", headers=headers)

        assert(r.status_code ==200 and r.json()["image"] == "clubImg")

    ###### LEAGUE TESTS ######

    def test_all_leagues(self):
        league = Models.Leagues()
        league.add_league("league", "leagueImg")

        headers = {
            "X-RapidAPI-Proxy-Secret" : environ.get("RAPID_PROXY_SECRET"),
        }

        r = requests.get(f"http://localhost:5000/v1/leagues", headers=headers)
        
        assert(r.status_code == 200 and r.json()["leagues"][0]["name"] == "league")

    def test_all_leagues_with_params(self):
        league = Models.Leagues()
        league.add_league("league", "leagueImg")

        leagueTwo = Models.Leagues()
        leagueTwo.add_league("leagueTwo", "leagueImgTwo")

        headers = {
            "X-RapidAPI-Proxy-Secret" : environ.get("RAPID_PROXY_SECRET"),
        }

        r = requests.get(f"http://localhost:5000/v1/leagues?page=1&limit=1", headers=headers)

        assert(r.status_code == 200 and r.json()["leagues"][0]["name"] == "league" and len(r.json()["leagues"]) == 1)

    def test_league_id(self):
        league = Models.Leagues()
        league.add_league("league", "leagueImg")

        headers = {
            "X-RapidAPI-Proxy-Secret" : environ.get("RAPID_PROXY_SECRET"),
        }

        r = requests.get(f"http://localhost:5000/v1/leagues/1", headers=headers)
        
        assert(r.status_code == 200 and r.json()["league"]["name"] == "league")

    def test_league_image(self):
        league = Models.Leagues()
        league.add_league("league", "leagueImg")

        headers = {
            "X-RapidAPI-Proxy-Secret" : environ.get("RAPID_PROXY_SECRET"),
        }

        r = requests.get(f"http://localhost:5000/v1/leagues/1/image", headers=headers)

        assert(r.status_code == 200 and r.json()["image"] == "leagueImg")

    ###### NATION TESTS ######

    def test_all_nations(self):
        nation = Models.Nations()
        nation.add_nation("nation", "nationImg")

        headers = {
            "X-RapidAPI-Proxy-Secret" : environ.get("RAPID_PROXY_SECRET"),
        }

        r = requests.get(f"http://localhost:5000/v1/nations", headers=headers)
        
        assert(r.status_code == 200 and r.json()["nations"][0]["name"] == "nation")

    def test_all_nations_with_params(self):
        nation = Models.Nations()
        nation.add_nation("nation", "nationImg")

        nationTwo = Models.Nations()
        nationTwo.add_nation("nationTwo", "nationImgTwo")

        headers = {
            "X-RapidAPI-Proxy-Secret" : environ.get("RAPID_PROXY_SECRET"),
        }

        r = requests.get(f"http://localhost:5000/v1/nations?page=1&limit=1", headers=headers)

        assert(r.status_code == 200 and r.json()["nations"][0]["name"] == "nation" and len(r.json()["nations"]) == 1)

    def test_nation_id(self):
        nation = Models.Nations()
        nation.add_nation("nation", "nationImg")

        headers = {
            "X-RapidAPI-Proxy-Secret" : environ.get("RAPID_PROXY_SECRET"),
        }

        r = requests.get(f"http://localhost:5000/v1/nations/1", headers=headers)
        
        assert(r.status_code == 200 and r.json()["nation"]["name"] == "nation")

    def test_nation_image(self):
        nation = Models.Nations()
        nation.add_nation("nation", "nationImg")

        headers = {
            "X-RapidAPI-Proxy-Secret" : environ.get("RAPID_PROXY_SECRET"),
        }

        r = requests.get(f"http://localhost:5000/v1/nations/1/image", headers=headers)

        assert(r.status_code == 200 and r.json()["image"] == "nationImg")

    ###### PLAYER TESTS ######

    def test_all_players(self):
        data = {
            "player_id" : 1,
            "name" : "neil mcnaught",
            "age": 22,
            "dob": "1998-01-01",
            "card_type" : "gold",
            "skill_moves" : 3,
            "weak_foot" : 3,
            "preferred_foot" : "right",
            "height" : 180,
            "weight" : 70,
            "rating" : 80,
            "position" : "ST",
            "accelerate" : "lengthy",
            "nation" : "England",
            "nation_id" : 1,
            "league" : "Premier League",
            "league_id" : 1,
            "club" : "Manchester United",
            "club_id" : 1,
            "fut_player_id" : 51,
            "fut_resource_id" : 51,
            "fut_android_id" : 1,
            "added_on" : "2020-01-01",
            "attributes" : {
                "pace" : {
                    "overall" : 80,
                    "acceleration" : 80,
                    "sprint_speed" : 80,
                },
                "shooting" : {
                    "overall" : 80,
                    "positioning" : 80,
                    "finishing" : 80,
                    "shot_power" : 80,
                    "long_shots" : 80,
                    "volleys" : 80,
                    "penalties" : 80,
                },
                "passing" : {
                    "overall" : 80,
                    "vision" : 80,
                    "crossing" : 80,
                    "fk_accuracy" : 80,
                    "short_passing" : 80,
                    "long_passing" : 80,
                    "curve" : 80,
                },
                "dribbling" : {
                    "overall" : 80,
                    "agility" : 80,
                    "balance" : 80,
                    "reactions" : 80,
                    "ball_control" : 80,
                    "dribbling" : 80,
                    "composure" : 80,
                },
                "defending" : {
                    "overall" : 80,
                    "interceptions" : 80,
                    "heading_accuracy" : 80,
                    "def_awareness" : 80,
                    "standing_tackle" : 80,
                    "sliding_tackle" : 80,
                },
                "physical" : {
                    "overall" : 80,
                    "jumping" : 80,
                    "stamina" : 80,
                    "strength" : 80,
                    "aggression" : 80,
                }
            },
            "alt_positions" : ["RW", "LW"],
            "traits" : ["Takes Powerful Driven Free Kicks", "Takes Powerful Driven Free Kicks"],
        }

        player = Models.Player()
        player.add_player(data=data, testing=True)

        headers = {
            "X-RapidAPI-Proxy-Secret" : environ.get("RAPID_PROXY_SECRET"),
        }

        r = requests.get(f"http://localhost:5000/v1/players", headers=headers)

        assert(r.status_code == 200 and r.json()["players"][0]["name"] == "neil mcnaught")

    def test_all_players_with_params(self):
        data = {
            "player_id" : 1,
            "name" : "neil mcnaught",
            "age": 22,
            "dob": "1998-01-01",
            "card_type" : "gold",
            "skill_moves" : 3,
            "weak_foot" : 3,
            "preferred_foot" : "right",
            "height" : 180,
            "weight" : 70,
            "rating" : 80,
            "position" : "ST",
            "accelerate" : "lengthy",
            "nation" : "England",
            "nation_id" : 1,
            "league" : "Premier League",
            "league_id" : 1,
            "club" : "Manchester United",
            "club_id" : 1,
            "fut_player_id" : 51,
            "fut_resource_id" : 51,
            "fut_android_id" : 1,
            "added_on" : "2020-01-01",
            "attributes" : {
                "pace" : {
                    "overall" : 80,
                    "acceleration" : 80,
                    "sprint_speed" : 80,
                },
                "shooting" : {
                    "overall" : 80,
                    "positioning" : 80,
                    "finishing" : 80,
                    "shot_power" : 80,
                    "long_shots" : 80,
                    "volleys" : 80,
                    "penalties" : 80,
                },
                "passing" : {
                    "overall" : 80,
                    "vision" : 80,
                    "crossing" : 80,
                    "fk_accuracy" : 80,
                    "short_passing" : 80,
                    "long_passing" : 80,
                    "curve" : 80,
                },
                "dribbling" : {
                    "overall" : 80,
                    "agility" : 80,
                    "balance" : 80,
                    "reactions" : 80,
                    "ball_control" : 80,
                    "dribbling" : 80,
                    "composure" : 80,
                },
                "defending" : {
                    "overall" : 80,
                    "interceptions" : 80,
                    "heading_accuracy" : 80,
                    "def_awareness" : 80,
                    "standing_tackle" : 80,
                    "sliding_tackle" : 80,
                },
                "physical" : {
                    "overall" : 80,
                    "jumping" : 80,
                    "stamina" : 80,
                    "strength" : 80,
                    "aggression" : 80,
                }
            },
            "alt_positions" : ["RW", "LW"],
            "traits" : ["Takes Powerful Driven Free Kicks", "Takes Powerful Driven Free Kicks"],
        }
        data_two = {
            "player_id" : 2,
            "name" : "neil mcnaught",
            "age": 22,
            "dob": "1998-01-01",
            "card_type" : "gold",
            "skill_moves" : 3,
            "weak_foot" : 3,
            "preferred_foot" : "right",
            "height" : 180,
            "weight" : 70,
            "rating" : 80,
            "position" : "ST",
            "accelerate" : "lengthy",
            "nation" : "England",
            "nation_id" : 1,
            "league" : "Premier League",
            "league_id" : 1,
            "club" : "Manchester United",
            "club_id" : 1,
            "fut_player_id" : 51,
            "fut_resource_id" : 51,
            "fut_android_id" : 1,
            "added_on" : "2020-01-01",
            "attributes" : {
                "pace" : {
                    "overall" : 80,
                    "acceleration" : 80,
                    "sprint_speed" : 80,
                },
                "shooting" : {
                    "overall" : 80,
                    "positioning" : 80,
                    "finishing" : 80,
                    "shot_power" : 80,
                    "long_shots" : 80,
                    "volleys" : 80,
                    "penalties" : 80,
                },
                "passing" : {
                    "overall" : 80,
                    "vision" : 80,
                    "crossing" : 80,
                    "fk_accuracy" : 80,
                    "short_passing" : 80,
                    "long_passing" : 80,
                    "curve" : 80,
                },
                "dribbling" : {
                    "overall" : 80,
                    "agility" : 80,
                    "balance" : 80,
                    "reactions" : 80,
                    "ball_control" : 80,
                    "dribbling" : 80,
                    "composure" : 80,
                },
                "defending" : {
                    "overall" : 80,
                    "interceptions" : 80,
                    "heading_accuracy" : 80,
                    "def_awareness" : 80,
                    "standing_tackle" : 80,
                    "sliding_tackle" : 80,
                },
                "physical" : {
                    "overall" : 80,
                    "jumping" : 80,
                    "stamina" : 80,
                    "strength" : 80,
                    "aggression" : 80,
                }
            },
            "alt_positions" : ["RW", "LW"],
            "traits" : ["Takes Powerful Driven Free Kicks", "Takes Powerful Driven Free Kicks"],
        }

        player = Models.Player()
        player.add_player(data=data, testing=True)
        playerTwo = Models.Player()
        playerTwo.add_player(data=data_two, testing=True)

        headers = {
            "X-RapidAPI-Proxy-Secret" : environ.get("RAPID_PROXY_SECRET")
        }
        
        r = requests.get("http://localhost:5000/v1/players?page=1&limit=1", headers=headers)
        assert(r.status_code == 200 and len(r.json()["players"]) == 1)

    def test_players_by_nation(self):
        data = {
            "player_id" : 1,
            "name" : "neil mcnaught",
            "age": 22,
            "dob": "1998-01-01",
            "card_type" : "gold",
            "skill_moves" : 3,
            "weak_foot" : 3,
            "preferred_foot" : "right",
            "height" : 180,
            "weight" : 70,
            "rating" : 80,
            "position" : "ST",
            "accelerate" : "lengthy",
            "nation" : "England",
            "nation_id" : 1,
            "league" : "Premier League",
            "league_id" : 1,
            "club" : "Manchester United",
            "club_id" : 1,
            "fut_player_id" : 51,
            "fut_resource_id" : 51,
            "fut_android_id" : 1,
            "added_on" : "2020-01-01",
            "attributes" : {
                "pace" : {
                    "overall" : 80,
                    "acceleration" : 80,
                    "sprint_speed" : 80,
                },
                "shooting" : {
                    "overall" : 80,
                    "positioning" : 80,
                    "finishing" : 80,
                    "shot_power" : 80,
                    "long_shots" : 80,
                    "volleys" : 80,
                    "penalties" : 80,
                },
                "passing" : {
                    "overall" : 80,
                    "vision" : 80,
                    "crossing" : 80,
                    "fk_accuracy" : 80,
                    "short_passing" : 80,
                    "long_passing" : 80,
                    "curve" : 80,
                },
                "dribbling" : {
                    "overall" : 80,
                    "agility" : 80,
                    "balance" : 80,
                    "reactions" : 80,
                    "ball_control" : 80,
                    "dribbling" : 80,
                    "composure" : 80,
                },
                "defending" : {
                    "overall" : 80,
                    "interceptions" : 80,
                    "heading_accuracy" : 80,
                    "def_awareness" : 80,
                    "standing_tackle" : 80,
                    "sliding_tackle" : 80,
                },
                "physical" : {
                    "overall" : 80,
                    "jumping" : 80,
                    "stamina" : 80,
                    "strength" : 80,
                    "aggression" : 80,
                }
            },
            "alt_positions" : ["RW", "LW"],
            "traits" : ["Takes Powerful Driven Free Kicks", "Takes Powerful Driven Free Kicks"],
        }

        player = Models.Player()
        player.add_player(data=data, testing=True)

        headers = {
            "X-RapidAPI-Proxy-Secret" : environ.get("RAPID_PROXY_SECRET"),
        }

        r = requests.get(f"http://localhost:5000/v1/players/nation/1", headers=headers)

        assert(r.status_code == 200 and r.json()["players"][0]["name"] == "neil mcnaught")

    def test_players_by_nation_with_params(self):
        data = {
            "player_id" : 1,
            "name" : "neil mcnaught",
            "age": 22,
            "dob": "1998-01-01",
            "card_type" : "gold",
            "skill_moves" : 3,
            "weak_foot" : 3,
            "preferred_foot" : "right",
            "height" : 180,
            "weight" : 70,
            "rating" : 80,
            "position" : "ST",
            "accelerate" : "lengthy",
            "nation" : "England",
            "nation_id" : 1,
            "league" : "Premier League",
            "league_id" : 1,
            "club" : "Manchester United",
            "club_id" : 1,
            "fut_player_id" : 51,
            "fut_resource_id" : 51,
            "fut_android_id" : 1,
            "added_on" : "2020-01-01",
            "attributes" : {
                "pace" : {
                    "overall" : 80,
                    "acceleration" : 80,
                    "sprint_speed" : 80,
                },
                "shooting" : {
                    "overall" : 80,
                    "positioning" : 80,
                    "finishing" : 80,
                    "shot_power" : 80,
                    "long_shots" : 80,
                    "volleys" : 80,
                    "penalties" : 80,
                },
                "passing" : {
                    "overall" : 80,
                    "vision" : 80,
                    "crossing" : 80,
                    "fk_accuracy" : 80,
                    "short_passing" : 80,
                    "long_passing" : 80,
                    "curve" : 80,
                },
                "dribbling" : {
                    "overall" : 80,
                    "agility" : 80,
                    "balance" : 80,
                    "reactions" : 80,
                    "ball_control" : 80,
                    "dribbling" : 80,
                    "composure" : 80,
                },
                "defending" : {
                    "overall" : 80,
                    "interceptions" : 80,
                    "heading_accuracy" : 80,
                    "def_awareness" : 80,
                    "standing_tackle" : 80,
                    "sliding_tackle" : 80,
                },
                "physical" : {
                    "overall" : 80,
                    "jumping" : 80,
                    "stamina" : 80,
                    "strength" : 80,
                    "aggression" : 80,
                }
            },
            "alt_positions" : ["RW", "LW"],
            "traits" : ["Takes Powerful Driven Free Kicks", "Takes Powerful Driven Free Kicks"],
        }
        data_two = {
            "player_id" : 2,
            "name" : "neil mcnaught",
            "age": 22,
            "dob": "1998-01-01",
            "card_type" : "gold",
            "skill_moves" : 3,
            "weak_foot" : 3,
            "preferred_foot" : "right",
            "height" : 180,
            "weight" : 70,
            "rating" : 80,
            "position" : "ST",
            "accelerate" : "lengthy",
            "nation" : "England",
            "nation_id" : 1,
            "league" : "Premier League",
            "league_id" : 1,
            "club" : "Manchester United",
            "club_id" : 1,
            "fut_player_id" : 51,
            "fut_resource_id" : 51,
            "fut_android_id" : 1,
            "added_on" : "2020-01-01",
            "attributes" : {
                "pace" : {
                    "overall" : 80,
                    "acceleration" : 80,
                    "sprint_speed" : 80,
                },
                "shooting" : {
                    "overall" : 80,
                    "positioning" : 80,
                    "finishing" : 80,
                    "shot_power" : 80,
                    "long_shots" : 80,
                    "volleys" : 80,
                    "penalties" : 80,
                },
                "passing" : {
                    "overall" : 80,
                    "vision" : 80,
                    "crossing" : 80,
                    "fk_accuracy" : 80,
                    "short_passing" : 80,
                    "long_passing" : 80,
                    "curve" : 80,
                },
                "dribbling" : {
                    "overall" : 80,
                    "agility" : 80,
                    "balance" : 80,
                    "reactions" : 80,
                    "ball_control" : 80,
                    "dribbling" : 80,
                    "composure" : 80,
                },
                "defending" : {
                    "overall" : 80,
                    "interceptions" : 80,
                    "heading_accuracy" : 80,
                    "def_awareness" : 80,
                    "standing_tackle" : 80,
                    "sliding_tackle" : 80,
                },
                "physical" : {
                    "overall" : 80,
                    "jumping" : 80,
                    "stamina" : 80,
                    "strength" : 80,
                    "aggression" : 80,
                }
            },
            "alt_positions" : ["RW", "LW"],
            "traits" : ["Takes Powerful Driven Free Kicks", "Takes Powerful Driven Free Kicks"],
        }

        player = Models.Player()
        player.add_player(data=data, testing=True)
        playerTwo = Models.Player()
        playerTwo.add_player(data=data_two, testing=True)

        headers = {
            "X-RapidAPI-Proxy-Secret" : environ.get("RAPID_PROXY_SECRET")
        }
        
        r = requests.get("http://localhost:5000/v1/players/nation/1?page=1&limit=1", headers=headers)
        assert(r.status_code == 200 and len(r.json()["players"]) == 1)

    def test_players_by_league(self):
        data = {
            "player_id" : 1,
            "name" : "neil mcnaught",
            "age": 22,
            "dob": "1998-01-01",
            "card_type" : "gold",
            "skill_moves" : 3,
            "weak_foot" : 3,
            "preferred_foot" : "right",
            "height" : 180,
            "weight" : 70,
            "rating" : 80,
            "position" : "ST",
            "accelerate" : "lengthy",
            "nation" : "England",
            "nation_id" : 1,
            "league" : "Premier League",
            "league_id" : 1,
            "club" : "Manchester United",
            "club_id" : 1,
            "fut_player_id" : 51,
            "fut_resource_id" : 51,
            "fut_android_id" : 1,
            "added_on" : "2020-01-01",
            "attributes" : {
                "pace" : {
                    "overall" : 80,
                    "acceleration" : 80,
                    "sprint_speed" : 80,
                },
                "shooting" : {
                    "overall" : 80,
                    "positioning" : 80,
                    "finishing" : 80,
                    "shot_power" : 80,
                    "long_shots" : 80,
                    "volleys" : 80,
                    "penalties" : 80,
                },
                "passing" : {
                    "overall" : 80,
                    "vision" : 80,
                    "crossing" : 80,
                    "fk_accuracy" : 80,
                    "short_passing" : 80,
                    "long_passing" : 80,
                    "curve" : 80,
                },
                "dribbling" : {
                    "overall" : 80,
                    "agility" : 80,
                    "balance" : 80,
                    "reactions" : 80,
                    "ball_control" : 80,
                    "dribbling" : 80,
                    "composure" : 80,
                },
                "defending" : {
                    "overall" : 80,
                    "interceptions" : 80,
                    "heading_accuracy" : 80,
                    "def_awareness" : 80,
                    "standing_tackle" : 80,
                    "sliding_tackle" : 80,
                },
                "physical" : {
                    "overall" : 80,
                    "jumping" : 80,
                    "stamina" : 80,
                    "strength" : 80,
                    "aggression" : 80,
                }
            },
            "alt_positions" : ["RW", "LW"],
            "traits" : ["Takes Powerful Driven Free Kicks", "Takes Powerful Driven Free Kicks"],
        }

        player = Models.Player()
        player.add_player(data=data, testing=True)

        headers = {
            "X-RapidAPI-Proxy-Secret" : environ.get("RAPID_PROXY_SECRET"),
        }

        r = requests.get(f"http://localhost:5000/v1/players/league/1", headers=headers)

        assert(r.status_code == 200 and r.json()["players"][0]["name"] == "neil mcnaught")

    def test_players_by_league_with_params(self):
        data = {
            "player_id" : 1,
            "name" : "neil mcnaught",
            "age": 22,
            "dob": "1998-01-01",
            "card_type" : "gold",
            "skill_moves" : 3,
            "weak_foot" : 3,
            "preferred_foot" : "right",
            "height" : 180,
            "weight" : 70,
            "rating" : 80,
            "position" : "ST",
            "accelerate" : "lengthy",
            "nation" : "England",
            "nation_id" : 1,
            "league" : "Premier League",
            "league_id" : 1,
            "club" : "Manchester United",
            "club_id" : 1,
            "fut_player_id" : 51,
            "fut_resource_id" : 51,
            "fut_android_id" : 1,
            "added_on" : "2020-01-01",
            "attributes" : {
                "pace" : {
                    "overall" : 80,
                    "acceleration" : 80,
                    "sprint_speed" : 80,
                },
                "shooting" : {
                    "overall" : 80,
                    "positioning" : 80,
                    "finishing" : 80,
                    "shot_power" : 80,
                    "long_shots" : 80,
                    "volleys" : 80,
                    "penalties" : 80,
                },
                "passing" : {
                    "overall" : 80,
                    "vision" : 80,
                    "crossing" : 80,
                    "fk_accuracy" : 80,
                    "short_passing" : 80,
                    "long_passing" : 80,
                    "curve" : 80,
                },
                "dribbling" : {
                    "overall" : 80,
                    "agility" : 80,
                    "balance" : 80,
                    "reactions" : 80,
                    "ball_control" : 80,
                    "dribbling" : 80,
                    "composure" : 80,
                },
                "defending" : {
                    "overall" : 80,
                    "interceptions" : 80,
                    "heading_accuracy" : 80,
                    "def_awareness" : 80,
                    "standing_tackle" : 80,
                    "sliding_tackle" : 80,
                },
                "physical" : {
                    "overall" : 80,
                    "jumping" : 80,
                    "stamina" : 80,
                    "strength" : 80,
                    "aggression" : 80,
                }
            },
            "alt_positions" : ["RW", "LW"],
            "traits" : ["Takes Powerful Driven Free Kicks", "Takes Powerful Driven Free Kicks"],
        }
        data_two = {
            "player_id" : 2,
            "name" : "neil mcnaught",
            "age": 22,
            "dob": "1998-01-01",
            "card_type" : "gold",
            "skill_moves" : 3,
            "weak_foot" : 3,
            "preferred_foot" : "right",
            "height" : 180,
            "weight" : 70,
            "rating" : 80,
            "position" : "ST",
            "accelerate" : "lengthy",
            "nation" : "England",
            "nation_id" : 1,
            "league" : "Premier League",
            "league_id" : 1,
            "club" : "Manchester United",
            "club_id" : 1,
            "fut_player_id" : 51,
            "fut_resource_id" : 51,
            "fut_android_id" : 1,
            "added_on" : "2020-01-01",
            "attributes" : {
                "pace" : {
                    "overall" : 80,
                    "acceleration" : 80,
                    "sprint_speed" : 80,
                },
                "shooting" : {
                    "overall" : 80,
                    "positioning" : 80,
                    "finishing" : 80,
                    "shot_power" : 80,
                    "long_shots" : 80,
                    "volleys" : 80,
                    "penalties" : 80,
                },
                "passing" : {
                    "overall" : 80,
                    "vision" : 80,
                    "crossing" : 80,
                    "fk_accuracy" : 80,
                    "short_passing" : 80,
                    "long_passing" : 80,
                    "curve" : 80,
                },
                "dribbling" : {
                    "overall" : 80,
                    "agility" : 80,
                    "balance" : 80,
                    "reactions" : 80,
                    "ball_control" : 80,
                    "dribbling" : 80,
                    "composure" : 80,
                },
                "defending" : {
                    "overall" : 80,
                    "interceptions" : 80,
                    "heading_accuracy" : 80,
                    "def_awareness" : 80,
                    "standing_tackle" : 80,
                    "sliding_tackle" : 80,
                },
                "physical" : {
                    "overall" : 80,
                    "jumping" : 80,
                    "stamina" : 80,
                    "strength" : 80,
                    "aggression" : 80,
                }
            },
            "alt_positions" : ["RW", "LW"],
            "traits" : ["Takes Powerful Driven Free Kicks", "Takes Powerful Driven Free Kicks"],
        }

        player = Models.Player()
        player.add_player(data=data, testing=True)
        playerTwo = Models.Player()
        playerTwo.add_player(data=data_two, testing=True)

        headers = {
            "X-RapidAPI-Proxy-Secret" : environ.get("RAPID_PROXY_SECRET")
        }
        
        r = requests.get("http://localhost:5000/v1/players/league/1?page=1&limit=1", headers=headers)
        assert(r.status_code == 200 and len(r.json()["players"]) == 1)

    def test_players_by_club_with_params(self):
        data = {
            "player_id" : 1,
            "name" : "neil mcnaught",
            "age": 22,
            "dob": "1998-01-01",
            "card_type" : "gold",
            "skill_moves" : 3,
            "weak_foot" : 3,
            "preferred_foot" : "right",
            "height" : 180,
            "weight" : 70,
            "rating" : 80,
            "position" : "ST",
            "accelerate" : "lengthy",
            "nation" : "England",
            "nation_id" : 1,
            "league" : "Premier League",
            "league_id" : 1,
            "club" : "Manchester United",
            "club_id" : 1,
            "fut_player_id" : 51,
            "fut_resource_id" : 51,
            "fut_android_id" : 1,
            "added_on" : "2020-01-01",
            "attributes" : {
                "pace" : {
                    "overall" : 80,
                    "acceleration" : 80,
                    "sprint_speed" : 80,
                },
                "shooting" : {
                    "overall" : 80,
                    "positioning" : 80,
                    "finishing" : 80,
                    "shot_power" : 80,
                    "long_shots" : 80,
                    "volleys" : 80,
                    "penalties" : 80,
                },
                "passing" : {
                    "overall" : 80,
                    "vision" : 80,
                    "crossing" : 80,
                    "fk_accuracy" : 80,
                    "short_passing" : 80,
                    "long_passing" : 80,
                    "curve" : 80,
                },
                "dribbling" : {
                    "overall" : 80,
                    "agility" : 80,
                    "balance" : 80,
                    "reactions" : 80,
                    "ball_control" : 80,
                    "dribbling" : 80,
                    "composure" : 80,
                },
                "defending" : {
                    "overall" : 80,
                    "interceptions" : 80,
                    "heading_accuracy" : 80,
                    "def_awareness" : 80,
                    "standing_tackle" : 80,
                    "sliding_tackle" : 80,
                },
                "physical" : {
                    "overall" : 80,
                    "jumping" : 80,
                    "stamina" : 80,
                    "strength" : 80,
                    "aggression" : 80,
                }
            },
            "alt_positions" : ["RW", "LW"],
            "traits" : ["Takes Powerful Driven Free Kicks", "Takes Powerful Driven Free Kicks"],
        }
        data_two = {
            "player_id" : 2,
            "name" : "neil mcnaught",
            "age": 22,
            "dob": "1998-01-01",
            "card_type" : "gold",
            "skill_moves" : 3,
            "weak_foot" : 3,
            "preferred_foot" : "right",
            "height" : 180,
            "weight" : 70,
            "rating" : 80,
            "position" : "ST",
            "accelerate" : "lengthy",
            "nation" : "England",
            "nation_id" : 1,
            "league" : "Premier League",
            "league_id" : 1,
            "club" : "Manchester United",
            "club_id" : 1,
            "fut_player_id" : 51,
            "fut_resource_id" : 51,
            "fut_android_id" : 1,
            "added_on" : "2020-01-01",
            "attributes" : {
                "pace" : {
                    "overall" : 80,
                    "acceleration" : 80,
                    "sprint_speed" : 80,
                },
                "shooting" : {
                    "overall" : 80,
                    "positioning" : 80,
                    "finishing" : 80,
                    "shot_power" : 80,
                    "long_shots" : 80,
                    "volleys" : 80,
                    "penalties" : 80,
                },
                "passing" : {
                    "overall" : 80,
                    "vision" : 80,
                    "crossing" : 80,
                    "fk_accuracy" : 80,
                    "short_passing" : 80,
                    "long_passing" : 80,
                    "curve" : 80,
                },
                "dribbling" : {
                    "overall" : 80,
                    "agility" : 80,
                    "balance" : 80,
                    "reactions" : 80,
                    "ball_control" : 80,
                    "dribbling" : 80,
                    "composure" : 80,
                },
                "defending" : {
                    "overall" : 80,
                    "interceptions" : 80,
                    "heading_accuracy" : 80,
                    "def_awareness" : 80,
                    "standing_tackle" : 80,
                    "sliding_tackle" : 80,
                },
                "physical" : {
                    "overall" : 80,
                    "jumping" : 80,
                    "stamina" : 80,
                    "strength" : 80,
                    "aggression" : 80,
                }
            },
            "alt_positions" : ["RW", "LW"],
            "traits" : ["Takes Powerful Driven Free Kicks", "Takes Powerful Driven Free Kicks"],
        }

        player = Models.Player()
        player.add_player(data=data, testing=True)
        playerTwo = Models.Player()
        playerTwo.add_player(data=data_two, testing=True)

        headers = {
            "X-RapidAPI-Proxy-Secret" : environ.get("RAPID_PROXY_SECRET")
        }
        
        r = requests.get("http://localhost:5000/v1/players/club/1?page=1&limit=1", headers=headers)
        assert(r.status_code == 200 and len(r.json()["players"]) == 1)

    def test_players_by_club(self):
        data = {
            "player_id" : 1,
            "name" : "neil mcnaught",
            "age": 22,
            "dob": "1998-01-01",
            "card_type" : "gold",
            "skill_moves" : 3,
            "weak_foot" : 3,
            "preferred_foot" : "right",
            "height" : 180,
            "weight" : 70,
            "rating" : 80,
            "position" : "ST",
            "accelerate" : "lengthy",
            "nation" : "England",
            "nation_id" : 1,
            "league" : "Premier League",
            "league_id" : 1,
            "club" : "Manchester United",
            "club_id" : 1,
            "fut_player_id" : 51,
            "fut_resource_id" : 51,
            "fut_android_id" : 1,
            "added_on" : "2020-01-01",
            "attributes" : {
                "pace" : {
                    "overall" : 80,
                    "acceleration" : 80,
                    "sprint_speed" : 80,
                },
                "shooting" : {
                    "overall" : 80,
                    "positioning" : 80,
                    "finishing" : 80,
                    "shot_power" : 80,
                    "long_shots" : 80,
                    "volleys" : 80,
                    "penalties" : 80,
                },
                "passing" : {
                    "overall" : 80,
                    "vision" : 80,
                    "crossing" : 80,
                    "fk_accuracy" : 80,
                    "short_passing" : 80,
                    "long_passing" : 80,
                    "curve" : 80,
                },
                "dribbling" : {
                    "overall" : 80,
                    "agility" : 80,
                    "balance" : 80,
                    "reactions" : 80,
                    "ball_control" : 80,
                    "dribbling" : 80,
                    "composure" : 80,
                },
                "defending" : {
                    "overall" : 80,
                    "interceptions" : 80,
                    "heading_accuracy" : 80,
                    "def_awareness" : 80,
                    "standing_tackle" : 80,
                    "sliding_tackle" : 80,
                },
                "physical" : {
                    "overall" : 80,
                    "jumping" : 80,
                    "stamina" : 80,
                    "strength" : 80,
                    "aggression" : 80,
                }
            },
            "alt_positions" : ["RW", "LW"],
            "traits" : ["Takes Powerful Driven Free Kicks", "Takes Powerful Driven Free Kicks"],
        }

        player = Models.Player()
        player.add_player(data=data, testing=True)

        headers = {
            "X-RapidAPI-Proxy-Secret" : environ.get("RAPID_PROXY_SECRET"),
        }

        r = requests.get(f"http://localhost:5000/v1/players/club/1", headers=headers)

        assert(r.status_code == 200 and r.json()["players"][0]["name"] == "neil mcnaught")

    def test_player_by_id(self):
        data = {
            "player_id" : 1,
            "name" : "neil mcnaught",
            "age": 22,
            "dob": "1998-01-01",
            "card_type" : "gold",
            "skill_moves" : 3,
            "weak_foot" : 3,
            "preferred_foot" : "right",
            "height" : 180,
            "weight" : 70,
            "rating" : 80,
            "position" : "ST",
            "accelerate" : "lengthy",
            "nation" : "England",
            "nation_id" : 1,
            "league" : "Premier League",
            "league_id" : 1,
            "club" : "Manchester United",
            "club_id" : 1,
            "fut_player_id" : 51,
            "fut_resource_id" : 51,
            "fut_android_id" : 1,
            "added_on" : "2020-01-01",
            "attributes" : {
                "pace" : {
                    "overall" : 80,
                    "acceleration" : 80,
                    "sprint_speed" : 80,
                },
                "shooting" : {
                    "overall" : 80,
                    "positioning" : 80,
                    "finishing" : 80,
                    "shot_power" : 80,
                    "long_shots" : 80,
                    "volleys" : 80,
                    "penalties" : 80,
                },
                "passing" : {
                    "overall" : 80,
                    "vision" : 80,
                    "crossing" : 80,
                    "fk_accuracy" : 80,
                    "short_passing" : 80,
                    "long_passing" : 80,
                    "curve" : 80,
                },
                "dribbling" : {
                    "overall" : 80,
                    "agility" : 80,
                    "balance" : 80,
                    "reactions" : 80,
                    "ball_control" : 80,
                    "dribbling" : 80,
                    "composure" : 80,
                },
                "defending" : {
                    "overall" : 80,
                    "interceptions" : 80,
                    "heading_accuracy" : 80,
                    "def_awareness" : 80,
                    "standing_tackle" : 80,
                    "sliding_tackle" : 80,
                },
                "physical" : {
                    "overall" : 80,
                    "jumping" : 80,
                    "stamina" : 80,
                    "strength" : 80,
                    "aggression" : 80,
                }
            },
            "alt_positions" : ["RW", "LW"],
            "traits" : ["Takes Powerful Driven Free Kicks", "Takes Powerful Driven Free Kicks"],
        }

        player = Models.Player()
        player.add_player(data=data, testing=True)

        headers = {
            "X-RapidAPI-Proxy-Secret" : environ.get("RAPID_PROXY_SECRET"),
        }

        r = requests.get(f"http://localhost:5000/v1/players/1", headers=headers)

        assert(r.status_code == 200 and r.json()["player"]["name"] == "neil mcnaught")

    def test_get_player_image(self):
        data = {
            "player_id" : 1,
            "name" : "neil mcnaught",
            "age": 22,
            "dob": "1998-01-01",
            "card_type" : "gold",
            "skill_moves" : 3,
            "weak_foot" : 3,
            "preferred_foot" : "right",
            "height" : 180,
            "weight" : 70,
            "rating" : 80,
            "position" : "ST",
            "accelerate" : "lengthy",
            "nation" : "England",
            "nation_id" : 1,
            "league" : "Premier League",
            "league_id" : 1,
            "club" : "Manchester United",
            "club_id" : 1,
            "fut_player_id" : 51,
            "fut_resource_id" : 51,
            "fut_android_id" : 1,
            "added_on" : "2020-01-01",
            "attributes" : {
                "pace" : {
                    "overall" : 80,
                    "acceleration" : 80,
                    "sprint_speed" : 80,
                },
                "shooting" : {
                    "overall" : 80,
                    "positioning" : 80,
                    "finishing" : 80,
                    "shot_power" : 80,
                    "long_shots" : 80,
                    "volleys" : 80,
                    "penalties" : 80,
                },
                "passing" : {
                    "overall" : 80,
                    "vision" : 80,
                    "crossing" : 80,
                    "fk_accuracy" : 80,
                    "short_passing" : 80,
                    "long_passing" : 80,
                    "curve" : 80,
                },
                "dribbling" : {
                    "overall" : 80,
                    "agility" : 80,
                    "balance" : 80,
                    "reactions" : 80,
                    "ball_control" : 80,
                    "dribbling" : 80,
                    "composure" : 80,
                },
                "defending" : {
                    "overall" : 80,
                    "interceptions" : 80,
                    "heading_accuracy" : 80,
                    "def_awareness" : 80,
                    "standing_tackle" : 80,
                    "sliding_tackle" : 80,
                },
                "physical" : {
                    "overall" : 80,
                    "jumping" : 80,
                    "stamina" : 80,
                    "strength" : 80,
                    "aggression" : 80,
                }
            },
            "alt_positions" : ["RW", "LW"],
            "traits" : ["Takes Powerful Driven Free Kicks", "Takes Powerful Driven Free Kicks"],
        }

        player = Models.Player()
        player.add_player(data=data, testing=True)

        headers = {
            "X-RapidAPI-Proxy-Secret" : environ.get("RAPID_PROXY_SECRET"),
        }

        r = requests.get(f"http://localhost:5000/v1/players/1/image", headers=headers)
        
        assert(r.status_code == 200 and len(r.json()["image"]) > 2)

    def test_get_player_price(self):
        data = {
            "player_id" : 1,
            "name" : "neil mcnaught",
            "age": 22,
            "dob": "1998-01-01",
            "card_type" : "gold",
            "skill_moves" : 3,
            "weak_foot" : 3,
            "preferred_foot" : "right",
            "height" : 180,
            "weight" : 70,
            "rating" : 80,
            "position" : "ST",
            "accelerate" : "lengthy",
            "nation" : "England",
            "nation_id" : 1,
            "league" : "Premier League",
            "league_id" : 1,
            "club" : "Manchester United",
            "club_id" : 1,
            "fut_player_id" : 51,
            "fut_resource_id" : 51,
            "fut_android_id" : 1,
            "added_on" : "2020-01-01",
            "attributes" : {
                "pace" : {
                    "overall" : 80,
                    "acceleration" : 80,
                    "sprint_speed" : 80,
                },
                "shooting" : {
                    "overall" : 80,
                    "positioning" : 80,
                    "finishing" : 80,
                    "shot_power" : 80,
                    "long_shots" : 80,
                    "volleys" : 80,
                    "penalties" : 80,
                },
                "passing" : {
                    "overall" : 80,
                    "vision" : 80,
                    "crossing" : 80,
                    "fk_accuracy" : 80,
                    "short_passing" : 80,
                    "long_passing" : 80,
                    "curve" : 80,
                },
                "dribbling" : {
                    "overall" : 80,
                    "agility" : 80,
                    "balance" : 80,
                    "reactions" : 80,
                    "ball_control" : 80,
                    "dribbling" : 80,
                    "composure" : 80,
                },
                "defending" : {
                    "overall" : 80,
                    "interceptions" : 80,
                    "heading_accuracy" : 80,
                    "def_awareness" : 80,
                    "standing_tackle" : 80,
                    "sliding_tackle" : 80,
                },
                "physical" : {
                    "overall" : 80,
                    "jumping" : 80,
                    "stamina" : 80,
                    "strength" : 80,
                    "aggression" : 80,
                }
            },
            "alt_positions" : ["RW", "LW"],
            "traits" : ["Takes Powerful Driven Free Kicks", "Takes Powerful Driven Free Kicks"],
        }

        player = Models.Player()
        player.add_player(data=data, testing=True)

        headers = {
            "X-RapidAPI-Proxy-Secret" : environ.get("RAPID_PROXY_SECRET"),
        }

        r = requests.get(f"http://localhost:5000/v1/players/1/price", headers=headers)

        assert(
            r.status_code == 200 and 
            (isinstance(r.json()["prices"]["console"], int) or isinstance(r.json()["prices"]["console"], float) or isinstance(r.json()["prices"]["console"], decimal.Decimal))
        )

    def test_get_player_price_update(self):
        data = {
            "player_id" : 1,
            "name" : "neil mcnaught",
            "age": 22,
            "dob": "1998-01-01",
            "card_type" : "gold",
            "skill_moves" : 3,
            "weak_foot" : 3,
            "preferred_foot" : "right",
            "height" : 180,
            "weight" : 70,
            "rating" : 80,
            "position" : "ST",
            "accelerate" : "lengthy",
            "nation" : "England",
            "nation_id" : 1,
            "league" : "Premier League",
            "league_id" : 1,
            "club" : "Manchester United",
            "club_id" : 1,
            "fut_player_id" : 51,
            "fut_resource_id" : 51,
            "fut_android_id" : 1,
            "added_on" : "2020-01-01",
            "attributes" : {
                "pace" : {
                    "overall" : 80,
                    "acceleration" : 80,
                    "sprint_speed" : 80,
                },
                "shooting" : {
                    "overall" : 80,
                    "positioning" : 80,
                    "finishing" : 80,
                    "shot_power" : 80,
                    "long_shots" : 80,
                    "volleys" : 80,
                    "penalties" : 80,
                },
                "passing" : {
                    "overall" : 80,
                    "vision" : 80,
                    "crossing" : 80,
                    "fk_accuracy" : 80,
                    "short_passing" : 80,
                    "long_passing" : 80,
                    "curve" : 80,
                },
                "dribbling" : {
                    "overall" : 80,
                    "agility" : 80,
                    "balance" : 80,
                    "reactions" : 80,
                    "ball_control" : 80,
                    "dribbling" : 80,
                    "composure" : 80,
                },
                "defending" : {
                    "overall" : 80,
                    "interceptions" : 80,
                    "heading_accuracy" : 80,
                    "def_awareness" : 80,
                    "standing_tackle" : 80,
                    "sliding_tackle" : 80,
                },
                "physical" : {
                    "overall" : 80,
                    "jumping" : 80,
                    "stamina" : 80,
                    "strength" : 80,
                    "aggression" : 80,
                }
            },
            "alt_positions" : ["RW", "LW"],
            "traits" : ["Takes Powerful Driven Free Kicks", "Takes Powerful Driven Free Kicks"],
        }

        player = Models.Player()
        player.add_player(data=data, testing=True)

        headers = {
            "X-RapidAPI-Proxy-Secret" : environ.get("RAPID_PROXY_SECRET"),
        }

        r = requests.get(f"http://localhost:5000/v1/players/1/price?price_update=1&testing=True", headers=headers)

        assert(
            r.status_code == 200 and 
            (isinstance(r.json()["prices"]["console"], int) or isinstance(r.json()["prices"]["console"], float) or isinstance(r.json()["prices"]["console"], decimal.Decimal))
        )

    def test_get_latest_player_since_id(self):
        data = {
            "player_id" : 1,
            "name" : "neil mcnaught",
            "age": 22,
            "dob": "1998-01-01",
            "card_type" : "gold",
            "skill_moves" : 3,
            "weak_foot" : 3,
            "preferred_foot" : "right",
            "height" : 180,
            "weight" : 70,
            "rating" : 80,
            "position" : "ST",
            "accelerate" : "lengthy",
            "nation" : "England",
            "nation_id" : 1,
            "league" : "Premier League",
            "league_id" : 1,
            "club" : "Manchester United",
            "club_id" : 1,
            "fut_player_id" : 51,
            "fut_resource_id" : 51,
            "fut_android_id" : 1,
            "added_on" : "2020-01-01",
            "attributes" : {
                "pace" : {
                    "overall" : 80,
                    "acceleration" : 80,
                    "sprint_speed" : 80,
                },
                "shooting" : {
                    "overall" : 80,
                    "positioning" : 80,
                    "finishing" : 80,
                    "shot_power" : 80,
                    "long_shots" : 80,
                    "volleys" : 80,
                    "penalties" : 80,
                },
                "passing" : {
                    "overall" : 80,
                    "vision" : 80,
                    "crossing" : 80,
                    "fk_accuracy" : 80,
                    "short_passing" : 80,
                    "long_passing" : 80,
                    "curve" : 80,
                },
                "dribbling" : {
                    "overall" : 80,
                    "agility" : 80,
                    "balance" : 80,
                    "reactions" : 80,
                    "ball_control" : 80,
                    "dribbling" : 80,
                    "composure" : 80,
                },
                "defending" : {
                    "overall" : 80,
                    "interceptions" : 80,
                    "heading_accuracy" : 80,
                    "def_awareness" : 80,
                    "standing_tackle" : 80,
                    "sliding_tackle" : 80,
                },
                "physical" : {
                    "overall" : 80,
                    "jumping" : 80,
                    "stamina" : 80,
                    "strength" : 80,
                    "aggression" : 80,
                }
            },
            "alt_positions" : ["RW", "LW"],
            "traits" : ["Takes Powerful Driven Free Kicks", "Takes Powerful Driven Free Kicks"],
        }
        data_two = {
            "player_id" : 2,
            "name" : "owen mcnaught",
            "age": 22,
            "dob": "1998-01-01",
            "card_type" : "gold",
            "skill_moves" : 3,
            "weak_foot" : 3,
            "preferred_foot" : "right",
            "height" : 180,
            "weight" : 70,
            "rating" : 80,
            "position" : "ST",
            "accelerate" : "lengthy",
            "nation" : "England",
            "nation_id" : 1,
            "league" : "Premier League",
            "league_id" : 1,
            "club" : "Manchester United",
            "club_id" : 1,
            "fut_player_id" : 51,
            "fut_resource_id" : 51,
            "fut_android_id" : 1,
            "added_on" : "2020-01-01",
            "attributes" : {
                "pace" : {
                    "overall" : 80,
                    "acceleration" : 80,
                    "sprint_speed" : 80,
                },
                "shooting" : {
                    "overall" : 80,
                    "positioning" : 80,
                    "finishing" : 80,
                    "shot_power" : 80,
                    "long_shots" : 80,
                    "volleys" : 80,
                    "penalties" : 80,
                },
                "passing" : {
                    "overall" : 80,
                    "vision" : 80,
                    "crossing" : 80,
                    "fk_accuracy" : 80,
                    "short_passing" : 80,
                    "long_passing" : 80,
                    "curve" : 80,
                },
                "dribbling" : {
                    "overall" : 80,
                    "agility" : 80,
                    "balance" : 80,
                    "reactions" : 80,
                    "ball_control" : 80,
                    "dribbling" : 80,
                    "composure" : 80,
                },
                "defending" : {
                    "overall" : 80,
                    "interceptions" : 80,
                    "heading_accuracy" : 80,
                    "def_awareness" : 80,
                    "standing_tackle" : 80,
                    "sliding_tackle" : 80,
                },
                "physical" : {
                    "overall" : 80,
                    "jumping" : 80,
                    "stamina" : 80,
                    "strength" : 80,
                    "aggression" : 80,
                }
            },
            "alt_positions" : ["RW", "LW"],
            "traits" : ["Takes Powerful Driven Free Kicks", "Takes Powerful Driven Free Kicks"],
        }

        player = Models.Player()
        player.add_player(data=data, testing=True)
        playerTwo = Models.Player()
        playerTwo.add_player(data=data_two, testing=True)

        headers = {
            "X-RapidAPI-Proxy-Secret" : environ.get("RAPID_PROXY_SECRET"),
        }

        r = requests.get("http://localhost:5000/v1/players/latest/1", headers=headers)

        assert(r.status_code == 200 and r.json()["players"][0]["name"] == "owen mcnaught")

    def test_search_players_success(self):
        data = {
            "player_id" : 1,
            "name" : "neil mcnaught",
            "age": 22,
            "dob": "1998-01-01",
            "card_type" : "gold",
            "skill_moves" : 3,
            "weak_foot" : 3,
            "preferred_foot" : "right",
            "height" : 180,
            "weight" : 70,
            "rating" : 80,
            "position" : "ST",
            "accelerate" : "lengthy",
            "nation" : "England",
            "nation_id" : 1,
            "league" : "Premier League",
            "league_id" : 1,
            "club" : "Manchester United",
            "club_id" : 1,
            "fut_player_id" : 51,
            "fut_resource_id" : 51,
            "fut_android_id" : 1,
            "added_on" : "2020-01-01",
            "attributes" : {
                "pace" : {
                    "overall" : 80,
                    "acceleration" : 80,
                    "sprint_speed" : 80,
                },
                "shooting" : {
                    "overall" : 80,
                    "positioning" : 80,
                    "finishing" : 80,
                    "shot_power" : 80,
                    "long_shots" : 80,
                    "volleys" : 80,
                    "penalties" : 80,
                },
                "passing" : {
                    "overall" : 80,
                    "vision" : 80,
                    "crossing" : 80,
                    "fk_accuracy" : 80,
                    "short_passing" : 80,
                    "long_passing" : 80,
                    "curve" : 80,
                },
                "dribbling" : {
                    "overall" : 80,
                    "agility" : 80,
                    "balance" : 80,
                    "reactions" : 80,
                    "ball_control" : 80,
                    "dribbling" : 80,
                    "composure" : 80,
                },
                "defending" : {
                    "overall" : 80,
                    "interceptions" : 80,
                    "heading_accuracy" : 80,
                    "def_awareness" : 80,
                    "standing_tackle" : 80,
                    "sliding_tackle" : 80,
                },
                "physical" : {
                    "overall" : 80,
                    "jumping" : 80,
                    "stamina" : 80,
                    "strength" : 80,
                    "aggression" : 80,
                }
            },
            "alt_positions" : ["RW", "LW"],
            "traits" : ["Takes Powerful Driven Free Kicks", "Takes Powerful Driven Free Kicks"],
        }

        player = Models.Player()
        player.add_player(data=data, testing=True)

        search_data = {
            "name" : "neil",
            "card_type" : "gold",
        }

        headers = {
            "X-RapidAPI-Proxy-Secret" : environ.get("RAPID_PROXY_SECRET"),
        }

        r = requests.post("http://localhost:5000/v1/players/search", headers=headers, json=search_data)

        assert(r.status_code == 200 and r.json()["players"][0]["name"] == "neil mcnaught")

    def test_search_players_fail(self):
        data = {
            "player_id" : 1,
            "name" : "neil mcnaught",
            "age": 22,
            "dob": "1998-01-01",
            "card_type" : "gold",
            "skill_moves" : 3,
            "weak_foot" : 3,
            "preferred_foot" : "right",
            "height" : 180,
            "weight" : 70,
            "rating" : 80,
            "position" : "ST",
            "accelerate" : "lengthy",
            "nation" : "England",
            "nation_id" : 1,
            "league" : "Premier League",
            "league_id" : 1,
            "club" : "Manchester United",
            "club_id" : 1,
            "fut_player_id" : 51,
            "fut_resource_id" : 51,
            "fut_android_id" : 1,
            "added_on" : "2020-01-01",
            "attributes" : {
                "pace" : {
                    "overall" : 80,
                    "acceleration" : 80,
                    "sprint_speed" : 80,
                },
                "shooting" : {
                    "overall" : 80,
                    "positioning" : 80,
                    "finishing" : 80,
                    "shot_power" : 80,
                    "long_shots" : 80,
                    "volleys" : 80,
                    "penalties" : 80,
                },
                "passing" : {
                    "overall" : 80,
                    "vision" : 80,
                    "crossing" : 80,
                    "fk_accuracy" : 80,
                    "short_passing" : 80,
                    "long_passing" : 80,
                    "curve" : 80,
                },
                "dribbling" : {
                    "overall" : 80,
                    "agility" : 80,
                    "balance" : 80,
                    "reactions" : 80,
                    "ball_control" : 80,
                    "dribbling" : 80,
                    "composure" : 80,
                },
                "defending" : {
                    "overall" : 80,
                    "interceptions" : 80,
                    "heading_accuracy" : 80,
                    "def_awareness" : 80,
                    "standing_tackle" : 80,
                    "sliding_tackle" : 80,
                },
                "physical" : {
                    "overall" : 80,
                    "jumping" : 80,
                    "stamina" : 80,
                    "strength" : 80,
                    "aggression" : 80,
                }
            },
            "alt_positions" : ["RW", "LW"],
            "traits" : ["Takes Powerful Driven Free Kicks", "Takes Powerful Driven Free Kicks"],
        }

        player = Models.Player()
        player.add_player(data=data, testing=True)

        search_data = {
            "name" : "john",
            "card_type" : "gold",
        }

        headers = {
            "X-RapidAPI-Proxy-Secret" : environ.get("RAPID_PROXY_SECRET"),
        }

        r = requests.post("http://localhost:5000/v1/players/search", headers=headers, json=search_data)

        assert(r.status_code == 404 and r.json()["detail"] == "No Matching Players")
    

    



if __name__ == '__main__':
    unittest.main()