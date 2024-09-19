from db import db

class Player(db.Model):
    __tablename__ = 'players'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    position = db.Column(db.String(50), nullable=False)
    points = db.Column(db.Integer)
    team = db.Column(db.String(50))
    atr = db.Column(db.Float)  # יחס אסיסטים לאיבודי כדור
    ppg_ratio = db.Column(db.Float)  # יחס נקודות למשחק
    seasons = db.Column(db.String(100))  # רשימת עונות
    two_percent = db.Column(db.Float)  # אחוזי קליעה לשתיים
    three_percent = db.Column(db.Float)  # אחוזי קליעה לשלוש

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'position': self.position,
            'points': self.points,
            'team': self.team,
            'atr': self.atr,
            'ppg_ratio': self.ppg_ratio,
            'seasons': self.seasons.split(','),  # רשימת עונות
            'two_percent': self.two_percent,
            'three_percent': self.three_percent
        }
