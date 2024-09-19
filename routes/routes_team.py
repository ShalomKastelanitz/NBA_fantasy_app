from flask import Blueprint, jsonify, request
from models import db, Team, Player

# יצירת Blueprint לקבוצות
team_bp = Blueprint('teams', __name__)


@team_bp.route('', methods=['POST'])
def create_team():
    data = request.get_json()
    team_name = data.get('team_name')
    player_ids = data.get('player_ids')

    # בדיקה אם סופקו בדיוק 5 שחקנים
    if len(player_ids) != 5:
        return jsonify({'error': 'קבוצה חייבת לכלול בדיוק 5 שחקנים'}), 400

    # בדיקה אם כל השחקנים קיימים
    players = Player.query.filter(Player.id.in_(player_ids)).all()
    if len(players) != 5:
        return jsonify({'error': 'יש שחקנים במזהים שסופקו שאינם קיימים'}), 400

    # בדיקה אם כל עמדה מיוצגת
    positions = {player.position for player in players}
    required_positions = {'PG', 'SG', 'SF', 'PF', 'C'}

    if not required_positions.issubset(positions):
        return jsonify({'error': 'הקבוצה חייבת לכלול שחקן מכל עמדה (PG, SG, SF, PF, C)'}), 400

    # יצירת הקבוצה עם מזהי השחקנים
    new_team = Team(
        team_name=team_name,
        player1_id=player_ids[0],
        player2_id=player_ids[1],
        player3_id=player_ids[2],
        player4_id=player_ids[3],
        player5_id=player_ids[4]
    )

    db.session.add(new_team)
    db.session.commit()

    return jsonify({'message': 'קבוצה נוצרה בהצלחה', 'team_id': new_team.id}), 201

# 2. אנדפוינט לעריכת קבוצה
@team_bp.route('/<int:team_id>', methods=['PUT'])
def update_team(team_id):
    team = Team.query.get_or_404(team_id)
    data = request.get_json()
    player_ids = data.get('player_ids')

    # בדיקה אם סופקו בדיוק 5 שחקנים
    if len(player_ids) != 5:
        return jsonify({'error': 'קבוצה חייבת לכלול בדיוק 5 שחקנים'}), 400

    # עדכון מזהי השחקנים בקבוצה
    team.player1_id = player_ids[0]
    team.player2_id = player_ids[1]
    team.player3_id = player_ids[2]
    team.player4_id = player_ids[3]
    team.player5_id = player_ids[4]

    db.session.commit()
    return jsonify({'message': 'הקבוצה עודכנה בהצלחה'}), 200


# 3. אנדפוינט למחיקת קבוצה
@team_bp.route('/<int:team_id>', methods=['DELETE'])
def delete_team(team_id):
    team = Team.query.get_or_404(team_id)

    db.session.delete(team)
    db.session.commit()

    return jsonify({'message': 'הקבוצה נמחקה בהצלחה'}), 200


# 4. אנדפוינט לקבלת פרטי קבוצה
@team_bp.route('/<int:team_id>', methods=['GET'])
def get_team(team_id):
    team = Team.query.get(team_id)

    if not team:
        return jsonify({'error': 'הקבוצה לא נמצאה'}), 404

    # קבלת כל המזהים של השחקנים בקבוצה
    player_ids = [
        team.player1_id,
        team.player2_id,
        team.player3_id,
        team.player4_id,
        team.player5_id
    ]

    #  שאילתה כדי לקבל את כל פרטי השחקנים לפי המזהים
    players = Player.query.filter(Player.id.in_(player_ids)).all()

    # הפיכת פרטי השחקנים ל-json באמצעות המתודה to_dict() של המודל Player
    player_details = [player.to_dict() for player in players]

    # החזרת פרטי הקבוצה יחד עם פרטי השחקנים
    return jsonify({
        'team_name': team.team_name,
        'players': player_details
    })

# 5. אנדפוינט להשוואת קבוצות
@team_bp.route('/compare', methods=['GET'])
def compare_teams():
    team1_id = request.args.get('team1_id')
    team2_id = request.args.get('team2_id')

    team1 = Team.query.get_or_404(team1_id)
    team2 = Team.query.get_or_404(team2_id)

    def get_team_points(team):
        player_ids = [team.player1_id, team.player2_id, team.player3_id, team.player4_id, team.player5_id]
        total_points = 0
        for player_id in player_ids:
            player = Player.query.get(player_id)
            total_points += player.points if player else 0
        return total_points

    team1_points = get_team_points(team1)
    team2_points = get_team_points(team2)

    comparison = {
        'team1': {
            'team_name': team1.team_name,
            'total_points': team1_points
        },
        'team2': {
            'team_name': team2.team_name,
            'total_points': team2_points
        }
    }

    return jsonify(comparison)
