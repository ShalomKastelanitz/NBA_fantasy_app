from db import db
import json

class Player(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    position = db.Column(db.String(50), nullable=False)
    points = db.Column(db.Integer, nullable=False)
    team = db.Column(db.String(50), nullable=False)
    atr = db.Column(db.Float, nullable=False)
    ppg_ratio = db.Column(db.Float, nullable=False)
    seasons = db.Column(db.Text, nullable=False)  # שינוי ל-Text
    two_percent = db.Column(db.Float, nullable=False)
    three_percent = db.Column(db.Float, nullable=False)
    ppg_ratio_vs_position = db.Column(db.Float, nullable=False)  # יחס מול ממוצע העמדה


    def __init__(self, name, position, points, team, atr, ppg_ratio, seasons, two_percent, three_percent,ppg_ratio_vs_position):
        self.name = name
        self.position = position
        self.points = points
        self.team = team
        self.atr = atr
        self.ppg_ratio = ppg_ratio
        self.seasons = json.dumps(seasons)  # המרת הרשימה ל-JSON
        self.two_percent = two_percent
        self.three_percent = three_percent
        self.ppg_ratio_vs_position = ppg_ratio_vs_position
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'position': self.position,
            'points': self.points,
            'team': self.team,
            'atr': self.atr,
            'ppg_ratio': self.ppg_ratio,
            'seasons': json.loads(self.seasons),  # המרת ה-JSON חזרה לרשימה
            'two_percent': self.two_percent,
            'three_percent': self.three_percent,
            'ppg_ratio_vs_position': self.ppg_ratio_vs_position
        }


class Team(db.Model):
    __tablename__ = 'teams'

    id = db.Column(db.Integer, primary_key=True)
    team_name = db.Column(db.String(100), unique=True, nullable=False)

    # מזהי השחקנים בקבוצה (5 שחקנים)
    player1_id = db.Column(db.Integer, nullable=False)
    player2_id = db.Column(db.Integer, nullable=False)
    player3_id = db.Column(db.Integer, nullable=False)
    player4_id = db.Column(db.Integer, nullable=False)
    player5_id = db.Column(db.Integer, nullable=False)

    def __init__(self, team_name, player1_id, player2_id, player3_id, player4_id, player5_id):
        self.team_name = team_name
        self.player1_id = player1_id
        self.player2_id = player2_id
        self.player3_id = player3_id
        self.player4_id = player4_id
        self.player5_id = player5_id

    def to_dict(self):
        return {
            'id': self.id,
            'team_name': self.team_name,
            'player1_id': self.player1_id,
            'player2_id': self.player2_id,
            'player3_id': self.player3_id,
            'player4_id': self.player4_id,
            'player5_id': self.player5_id
        }
