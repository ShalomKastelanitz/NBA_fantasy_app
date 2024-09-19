
from flask import Blueprint, jsonify, request
from models import Player

players_bp = Blueprint('players', __name__)

@players_bp.route('', methods=['GET'])
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