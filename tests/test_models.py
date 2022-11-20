import unittest
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_testing import TestCase
from os import environ
from dotenv import load_dotenv
import os, sys
import decimal

currentdir = os.path.dirname(os.path.realpath(__file__))
parentdir = os.path.dirname(currentdir)
sys.path.append(parentdir)

load_dotenv()
from app.models import all as Models
from app.database import setup_db

class TestModel(TestCase):
    def create_app(self):
        app = Flask(__name__)
        app.config['TESTING'] = True

        with app.app_context():
            app.config["SQLALCHEMY_DATABASE_URI"] = f'mysql://{environ.get("DB_USER")}:{environ.get("DB_PASS")}@{environ.get("DB_HOST")}/{environ.get("DB_TEST_NAME")}'
            app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
            self.db = setup_db(app, f'mysql://{environ.get("DB_USER")}:{environ.get("DB_PASS")}@{environ.get("DB_HOST")}/{environ.get("DB_TEST_NAME")}')
            self.db.app = app
            self.db.init_app(app)
            self.db.create_all()

            return app

    def tearDown(self):
        self.db.session.remove()
        self.db.drop_all()

    ##### CARD TESTS #####

    def test_add_card(self):
        card_image = Models.Cards()
        card_image.add_card("gold")
        assert len(Models.Cards.query.all()) == 1

    def test_get_card(self):
        card_image = Models.Cards()
        card_image.add_card("gold")

        assert Models.Cards().get_card(1)[0]["id"] == 1

    def test_find_cards_with_page_and_limit(self):
        card_image = Models.Cards()
        card_image.add_card("gold")

        assert Models.Cards().find_cards_with_page_and_limit(1, 1)[0][0]["id"] == 1

    def test_get_card_image(self):
        card_image = Models.Cards()
        card_image.add_card("gold")

        Models.CardImage().add_img(1, "test")

        assert Models.Cards().get_image(1)[0] == "test"

    def test_unknown_cards(self):
        assert Models.Cards().check_for_unknown() == True

    ##### CLUB TESTS #####

    def test_add_club(self):
        club = Models.Clubs()
        club.add_club("test", "test")

        assert len(Models.Clubs.query.all()) == 1

    def test_find_clubs_with_page_and_limit(self):
        club = Models.Clubs()
        club.add_club("test", "test")

        assert Models.Clubs().find_clubs_with_page_and_limit(1, 1)[0][0]["id"] == 1

    def test_get_club(self):
        club = Models.Clubs()
        club.add_club("test", "test")

        assert Models.Clubs().get_club(1)[0]["id"] == 1

    def test_get_club_id_by_name_success(self):
        club = Models.Clubs()
        club.add_club("test", "test")

        assert Models.Clubs().get_club_id_by_name("test") == 1
    
    def test_get_club_id_by_name_fail(self):
        club = Models.Clubs()
        club.add_club("randomClub", "randomImage")

        assert Models.Clubs().get_club_id_by_name("newClub", 22343) == 2

    def test_get_club_image(self):
        club = Models.Clubs()
        club.add_club("test", "testImg")

        assert Models.Clubs().get_club_image(1)[0] == "testImg"

    ##### LEAGUE TESTS #####

    def test_add_league(self):
        league = Models.Leagues()
        league.add_league("test", "test")

        assert len(Models.Leagues.query.all()) == 1

    def test_find_leagues_with_page_and_limit(self):
        league = Models.Leagues()
        league.add_league("test", "test")

        assert Models.Leagues().find_leagues_with_page_and_limit(1, 1)[0][0]["id"] == 1

    def test_get_league(self):
        league = Models.Leagues()
        league.add_league("test", "test")

        assert Models.Leagues().get_league(1)[0]["id"] == 1

    def test_get_league_id_by_name_success(self):
        league = Models.Leagues()
        league.add_league("test", "test")

        assert Models.Leagues().get_league_id_by_name("test") == 1

    def test_get_league_id_by_name_fail(self):
        league = Models.Leagues()
        league.add_league("randomLeague", "randomImage")

        assert Models.Leagues().get_league_id_by_name("newLeague", 22343) == 2

    def test_get_league_image(self):
        league = Models.Leagues()
        league.add_league("test", "testImg")

        assert Models.Leagues().get_league_image(1)[0] == "testImg"

    ##### NATION TESTS #####

    def test_add_nation(self):
        nation = Models.Nations()
        nation.add_nation("test", "test")

        assert len(Models.Nations.query.all()) == 1

    def test_find_nations_with_page_and_limit(self):
        nation = Models.Nations()
        nation.add_nation("test", "test")

        assert Models.Nations().find_nations_with_page_and_limit(1, 1)[0][0]["id"] == 1

    def test_get_nation(self):
        nation = Models.Nations()
        nation.add_nation("test", "test")

        assert Models.Nations().get_nation(1)[0]["id"] == 1

    def test_get_nation_id_by_name_success(self):
        nation = Models.Nations()
        nation.add_nation("test", "test")

        assert Models.Nations().get_nation_id_by_name("test") == 1

    def test_get_nation_id_by_name_fail(self):
        nation = Models.Nations()
        nation.add_nation("randomNation", "randomImage")

        assert Models.Nations().get_nation_id_by_name("newNation", 22343) == 2


    def test_get_nation_image(self):
        nation = Models.Nations()
        nation.add_nation("test", "testImg")

        assert Models.Nations().get_nation_image(1)[0] == "testImg"

    ##### PLAYER TESTS #####

    def test_add_player(self):
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

        assert len(Models.Player.query.all()) == 1

    def test_find_players_with_page_and_limit(self):
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

        assert len(Models.Player().find_players_with_page_and_limit(1, 1)[0]) == 1

    def test_find_players_by_nation_with_page_and_limit(self):
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

        assert len(Models.Player().find_players_by_nation_with_page_and_limit(1, 1, 1)[0]) == 1

    def test_find_players_by_league_with_page_and_limit(self):
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

        assert len(Models.Player().find_players_by_league_with_page_and_limit(1, 1, 1)[0]) == 1

    def test_find_players_by_club_with_page_and_limit(self):
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

        assert len(Models.Player().find_players_by_club_with_page_and_limit(1, 1, 1)[0]) == 1

    def test_find_players_by_id(self):
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

        assert Models.Player().find_player_by_id(1)[0]["name"] == "neil mcnaught"

    def test_find_players_by_nation_id(self):
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

        assert len(Models.Player().find_players_by_nation_id(1)) == 1

    def test_find_players_by_club_id(self):
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

        assert len(Models.Player().find_players_by_club_id(1)) == 1

    def test_find_players_by_league_id(self):
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

        assert len(Models.Player().find_players_by_league_id(1)) == 1

    def test_find_players_by_card_type(self):
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

        assert len(Models.Player().find_players_by_card_type("gold")) == 1

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

        assert isinstance(Models.Player().get_player_price(1)[0]["console"], int) or isinstance(Models.Player().get_player_price(1)[0]["console"], float) or isinstance(Models.Player().get_player_price(1)[0]["console"], decimal.Decimal)

    def test_update_player_price(self):
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

        assert Models.Player().update_player_prices(1, True) == True

    def test_update_all_player_price(self):
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

        assert Models.Player().update_prices() == True

    def test_search_player(self):
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

        for player in Models.Player().search_players({"name" : "neil mcnaught"}):
            if "neil mcnaught" in player[0]["name"]:
                assert True
                return

    def test_update_player_database(self):
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
        
        update_players = Models.Player().update_player_databases(testing=True, range_amount=5)

        assert update_players == True

    def test_age_from_dob(self):
        dob = "08/13/1970"
        age = Models.Player().age_from_dob(dob)
        assert age == 52

    def test_card_type(self):
        card_type = Models.Player().calc_card_type(43, 0, 0)
        assert card_type == "bronze"

    ##### PLAYER ALT POSITIONS TESTS #####

    def test_get_alt_positions(self):
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

        alt_positions = Models.PlayerAltPositions().get_player_alt_positions(1)
        assert alt_positions == ["RW", "LW"]

    ##### PLAYER IMAGE TESTS #####

    def test_get_player_image_by_id(self):
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

        player_image = Models.PlayerImage().get_image_by_id(1)
        assert len(player_image) > 1

    ##### PLAYER TRAITS TESTS #####

    def test_get_all_player_traits(self):
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

        player_traits = Models.PlayerTraits().get_all_player_traits(1)
        assert player_traits == [x.lower() for x in ["Takes Powerful Driven Free Kicks", "Takes Powerful Driven Free Kicks"]]


    


if __name__ == '__main__':
    unittest.main()