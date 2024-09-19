from flask import Flask, jsonify, request
from db import db
from models import Player
from services1.Bringing_details_players import fetch_and_process_data
from routes.route_player import players_bp
from routes.routes_team import team_bp

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///nba_players.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

with app.app_context():
    db.create_all()

    # Fetch and insert data
    player_data = fetch_and_process_data()
    for player in player_data:
        # בדיקה אם השחקן כבר קיים
        existing_player = Player.query.filter_by(name=player['name']).first()
        if not existing_player:
            new_player = Player(
                name=player['name'],
                position=player['position'],
                points=player['total_points'],
                team=player['team'],
                atr=player['atr'],
                ppg_ratio=player['ppg_ratio'],
                seasons=player['seasons'],  # הוספת רשימת עונות
                two_percent=player['two_percent'],  # אחוזי קליעה לשתיים
                three_percent=player['three_percent'] , # אחוזי קליעה לשלוש
                ppg_ratio_vs_position=player['ppg_ratio']  # יחס הנקודות מול ממוצע העמדה

            )
            db.session.add(new_player)
    db.session.commit()



app.register_blueprint(team_bp, url_prefix='/api/teams')

app.register_blueprint(players_bp, url_prefix='/api/players')
if __name__ == '__main__':
    app.run(debug=True)
