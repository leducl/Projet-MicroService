from flask import Blueprint, request, jsonify
from app.auth import require_jwt
from app import db
from app.models import Message, Reaction

bp = Blueprint('messages', __name__)

def serialize_message(msg):
    return {
        'id': msg.id,
        'user_id': msg.user_id,
        'username': msg.username,
        'channel': msg.channel,
        'recipient': msg.recipient,
        'text': msg.text,
        'reply_to': msg.reply_to,
        'pinned': msg.pinned,
        'timestamp': msg.timestamp.isoformat(),
        'reactions': [{'user_id': r.user_id, 'emoji': r.emoji} for r in msg.reactions]
    }

@bp.route('/msg', methods=['POST'])
@require_jwt
def post_message():
    data = request.get_json() or {}
    text = data.get('text')
    if not text:
        return jsonify({'error': 'Text is required'}), 400
    msg = Message(
        user_id=request.user.get('user_id'),
        username=request.user.get('username', 'unknown'),
        channel=data.get('channel'),
        recipient=data.get('recipient'),
        text=text,
        reply_to=data.get('reply_to')
    )
    db.session.add(msg)
    db.session.commit()
    return jsonify({'status': 'ok', 'message': serialize_message(msg)}), 201

@bp.route('/msg', methods=['GET'])
@require_jwt
def list_messages():
    channel = request.args.get('channel')
    offset = int(request.args.get('offset', 0))
    limit = int(request.args.get('limit', 50))
    query = Message.query
    if channel:
        query = query.filter_by(channel=channel)
    msgs = query.order_by(Message.timestamp.desc()).offset(offset).limit(limit).all()
    return jsonify([serialize_message(m) for m in msgs]), 200

@bp.route('/msg/reaction', methods=['POST'])
@require_jwt
def add_reaction():
    data = request.get_json() or {}
    msg_id = data.get('message_id')
    emoji = data.get('emoji')
    if not msg_id or not emoji:
        return jsonify({'error': 'message_id and emoji required'}), 400
    msg = Message.query.get(msg_id)
    if not msg:
        return jsonify({'error': 'Message not found'}), 404
    reaction = Reaction(message_id=msg_id, user_id=request.user['user_id'], emoji=emoji)
    db.session.add(reaction)
    try:
        db.session.commit()
    except Exception:
        db.session.rollback()
    return jsonify({'status': 'ok'}), 201

@bp.route('/msg/reaction', methods=['DELETE'])
@require_jwt
def remove_reaction():
    data = request.get_json() or {}
    msg_id = data.get('message_id')
    emoji = data.get('emoji')
    reaction = Reaction.query.filter_by(
        message_id=msg_id, user_id=request.user['user_id'], emoji=emoji
    ).first()
    if reaction:
        db.session.delete(reaction)
        db.session.commit()
    return jsonify({'status': 'ok'}), 200

@bp.route('/msg/<int:msg_id>', methods=['PUT'])
@require_jwt
def update_message(msg_id):
    msg = Message.query.get(msg_id)
    if not msg:
        return jsonify({'error': 'Message not found'}), 404
    if msg.user_id != request.user['user_id']:
        return jsonify({'error': 'Forbidden'}), 403
    data = request.get_json() or {}
    msg.text = data.get('text', msg.text)
    db.session.commit()
    return jsonify(serialize_message(msg)), 200

@bp.route('/msg/<int:msg_id>', methods=['DELETE'])
@require_jwt
def delete_message(msg_id):
    msg = Message.query.get(msg_id)
    if not msg:
        return jsonify({'error': 'Message not found'}), 404
    if msg.user_id != request.user['user_id']:
        return jsonify({'error': 'Forbidden'}), 403
    db.session.delete(msg)
    db.session.commit()
    return jsonify({'status': 'deleted'}), 200

@bp.route('/msg/thread/<int:msg_id>', methods=['GET'])
@require_jwt
def get_thread(msg_id):
    replies = Message.query.filter_by(reply_to=msg_id).all()
    return jsonify([serialize_message(r) for r in replies]), 200

@bp.route('/msg/pinned', methods=['GET'])
@require_jwt
def get_pinned():
    channel = request.args.get('channel')
    msgs = Message.query.filter_by(channel=channel, pinned=True).all()
    return jsonify([serialize_message(m) for m in msgs]), 200

@bp.route('/msg/private', methods=['GET'])
@require_jwt
def get_private():
    frm = request.args.get('from')
    to = request.args.get('to')
    msgs = Message.query.filter(
        Message.recipient==to,
        Message.username==frm
    ).order_by(Message.timestamp).all()
    return jsonify([serialize_message(m) for m in msgs]), 200

@bp.route('/msg/search', methods=['GET'])
@require_jwt
def search_messages():
    q = request.args.get('q')
    msgs = Message.query.filter(Message.text.ilike(f'%{q}%')).all()
    return jsonify([serialize_message(m) for m in msgs]), 200

def register_routes(app):
    app.register_blueprint(bp)
