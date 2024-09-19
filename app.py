from flask import Flask, jsonify, request
from db import db
from models import Player
from services1.Bringing_details_players import fetch_and_process_data

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///nba_players.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

with app.app_context():
    db.create_all()

    # Fetch and insert data
    player_data = fetch_and_process_data()
    for player in player_data:
        new_player = Player(
            name=player['name'],
            position=player['position'],
            points=player['points'],
            team=player['team'],
            atr=player['atr'],
            ppg_ratio=player['ppg_ratio'],
            seasons=player['seasons'],  # הוספת רשימת עונות
            two_percent=player['two_percent'],  # אחוזי קליעה לשתיים
            three_percent=player['three_percent']  # אחוזי קליעה לשלוש
        )
        db.session.add(new_player)
    db.session.commit()


@app.route('/api/players', methods=['GET'])
def get_players():
    position = request.args.get('position')
    season = request.args.get('season')

    if not position:
        return jsonify({"error": "Position is required"}), 400

    query = Player.query.filter_by(position=position)

    if season:
        query = query.filter(Player.seasons.contains(season))  # סינון לפי עונה אם היא ניתנה

    players = query.all()

    return jsonify([player.to_dict() for player in players])


if __name__ == '__main__':
    app.run(debug=True)
