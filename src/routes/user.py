from flask import Blueprint, jsonify, request
import random
import os
from datetime import datetime
from src.models.user import User, DiceRoll, Ranking, db
from src.services.google_sheets import sheets_service

user_bp = Blueprint('user', __name__)

# Enable CORS for all routes
@user_bp.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
    return response

@user_bp.route('/users', methods=['OPTIONS'])
@user_bp.route('/users/<int:user_id>', methods=['OPTIONS'])
@user_bp.route('/dice/roll', methods=['OPTIONS'])
@user_bp.route('/rankings', methods=['OPTIONS'])
def handle_options():
    return '', 200

# User management routes
@user_bp.route('/users', methods=['GET'])
def get_users():
    users = User.query.all()
    return jsonify([user.to_dict() for user in users])

@user_bp.route('/users', methods=['POST'])
def create_user():
    data = request.json
    
    # Check if username already exists
    existing_user = User.query.filter_by(username=data['username']).first()
    if existing_user:
        return jsonify({'error': 'Username already exists'}), 400
    
    user = User(username=data['username'])
    db.session.add(user)
    db.session.commit()
    return jsonify(user.to_dict()), 201

@user_bp.route('/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    user = User.query.get_or_404(user_id)
    return jsonify(user.to_dict())

@user_bp.route('/users/by-username/<username>', methods=['GET'])
def get_user_by_username(username):
    user = User.query.filter_by(username=username).first()
    if not user:
        return jsonify({'error': 'User not found'}), 404
    return jsonify(user.to_dict())

# Dice rolling routes
@user_bp.route('/dice/roll', methods=['POST'])
def roll_dice():
    data = request.json
    username = data.get('username')
    
    if not username:
        return jsonify({'error': 'Username is required'}), 400
    
    # Get or create user
    user = User.query.filter_by(username=username).first()
    if not user:
        user = User(username=username)
        db.session.add(user)
        db.session.commit()
    
    # Check if user has already rolled today (for simplicity, we'll allow only one roll per user)
    existing_roll = DiceRoll.query.filter_by(user_id=user.id).first()
    if existing_roll:
        return jsonify({'error': 'You have already rolled the dice!', 'existing_roll': existing_roll.to_dict()}), 400
    
    # Roll three dice
    dice1 = random.randint(1, 6)
    dice2 = random.randint(1, 6)
    dice3 = random.randint(1, 6)
    total_score = dice1 + dice2 + dice3
    
    # Save the roll
    dice_roll = DiceRoll(
        user_id=user.id,
        dice1=dice1,
        dice2=dice2,
        dice3=dice3,
        total_score=total_score
    )
    db.session.add(dice_roll)
    
    # Save to Google Sheets (with error handling)
    sheets_success = False
    sheets_error = None
    try:
        sheets_service.add_dice_roll_record(
            username=username,
            dice1=dice1,
            dice2=dice2,
            dice3=dice3,
            total_score=total_score,
            timestamp=datetime.utcnow().isoformat()
        )
        sheets_success = True
    except Exception as e:
        sheets_error = str(e)
        print(f"Google Sheets error: {e}")  # Log for debugging
    
    # Update or create ranking
    ranking = Ranking.query.filter_by(user_id=user.id).first()
    if ranking:
        if total_score > ranking.highest_score:
            ranking.highest_score = total_score
        ranking.total_rolls += 1
        ranking.last_updated = datetime.utcnow()
    else:
        ranking = Ranking(
            user_id=user.id,
            username=username,
            highest_score=total_score,
            total_rolls=1
        )
        db.session.add(ranking)
    
    db.session.commit()
    
    return jsonify({
        'roll': dice_roll.to_dict(),
        'ranking': ranking.to_dict(),
        'sheets_success': sheets_success,
        'sheets_error': sheets_error
    }), 201

@user_bp.route('/dice/check/<username>', methods=['GET'])
def check_user_roll(username):
    user = User.query.filter_by(username=username).first()
    if not user:
        return jsonify({'has_rolled': False})
    
    existing_roll = DiceRoll.query.filter_by(user_id=user.id).first()
    return jsonify({
        'has_rolled': existing_roll is not None,
        'roll': existing_roll.to_dict() if existing_roll else None
    })

# Ranking routes
@user_bp.route('/rankings', methods=['GET'])
def get_rankings():
    rankings = Ranking.query.order_by(Ranking.highest_score.desc()).limit(10).all()
    
    # Add rank position and highlight info
    current_month = datetime.now().month
    rankings_with_highlight = []
    
    for i, ranking in enumerate(rankings):
        rank_data = ranking.to_dict()
        rank_data['rank'] = i + 1
        # Highlight based on month (1st place in January, 2nd in February, etc.)
        rank_data['is_highlighted'] = (rank_data['rank'] == current_month) or (current_month > 12 and rank_data['rank'] == (current_month % 12))
        rankings_with_highlight.append(rank_data)
    
    return jsonify(rankings_with_highlight)

@user_bp.route('/dice/history', methods=['GET'])
def get_dice_history():
    rolls = DiceRoll.query.order_by(DiceRoll.rolled_at.desc()).all()
    return jsonify([roll.to_dict() for roll in rolls])

# Reset functionality for testing
@user_bp.route('/reset', methods=['POST'])
def reset_data():
    DiceRoll.query.delete()
    Ranking.query.delete()
    User.query.delete()
    db.session.commit()
    
    # Also clear Google Sheets data
    sheets_service.clear_all_data()
    
    return jsonify({'message': 'All data reset successfully'}), 200

# Google Sheets data access routes
@user_bp.route('/sheets/history', methods=['GET'])
def get_sheets_history():
    """Get all dice roll history from Google Sheets"""
    records = sheets_service.get_all_records()
    return jsonify(records)

@user_bp.route('/sheets/leaderboard', methods=['GET'])
def get_sheets_leaderboard():
    """Get leaderboard from Google Sheets data"""
    leaderboard = sheets_service.get_leaderboard(limit=10)
    return jsonify(leaderboard)

@user_bp.route('/sheets/user/<username>', methods=['GET'])
def get_user_sheets_history(username):
    """Get dice roll history for a specific user from Google Sheets"""
    records = sheets_service.get_records_by_username(username)
    return jsonify(records)

@user_bp.route('/sheets/export', methods=['GET'])
def export_sheets_data():
    """Export current data in CSV format for Google Sheets"""
    csv_data = sheets_service.export_for_google_sheets()
    return csv_data, 200, {'Content-Type': 'text/plain'}

@user_bp.route('/sheets/status', methods=['GET'])
def get_sheets_status():
    """Get Google Sheets service status and diagnostics"""
    try:
        # Check if Google Sheets service is working
        status = {
            'service_available': not sheets_service.use_fallback,
            'fallback_mode': sheets_service.use_fallback,
            'spreadsheet_id': sheets_service.SPREADSHEET_ID,
            'has_env_credentials': bool(os.environ.get('GOOGLE_APPLICATION_CREDENTIALS_JSON')),
            'credentials_file_exists': os.path.exists(os.path.join(os.path.dirname(__file__), '..', 'credentials', 'service-account.json'))
        }

        # Try to test the service
        if not sheets_service.use_fallback:
            try:
                # Try to read from the sheet to test connectivity
                test_records = sheets_service.get_all_records()
                status['test_read_success'] = True
                status['record_count'] = len(test_records)
            except Exception as e:
                status['test_read_success'] = False
                status['test_error'] = str(e)
        else:
            status['test_read_success'] = False
            status['test_error'] = 'Using fallback mode - no Google Sheets access'

        return jsonify(status)
    except Exception as e:
        return jsonify({'error': str(e), 'service_available': False}), 500

@user_bp.route('/sheets/latest', methods=['GET'])
def get_latest_for_sheets():
    """Get latest rolls formatted for copying to Google Sheets"""
    limit = request.args.get('limit', 100, type=int)  # Increased default limit
    rows = sheets_service.get_latest_rolls_for_sheets(limit)
    return jsonify({
        'headers': ['Timestamp', 'Username', 'Dice1', 'Dice2', 'Dice3', 'Total Score', 'Date', 'Time'],
        'rows': rows,
        'instructions': 'Copy the rows data and paste into your Google Sheet starting from row 2 (after headers)'
    })

