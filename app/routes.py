from flask import Blueprint, request, jsonify, make_response, abort
from app import db
from app.models.board import Board
from app.models.card import Card

# example_bp = Blueprint('example_bp', __name__)

boards_bp = Blueprint("boards", __name__, url_prefix="/boards")
cards_bp = Blueprint("cards", __name__, url_prefix="/cards")

def validate_item(model, item_id):
    try:
        item_id = int(item_id)
    except:
        abort(make_response({"message": f"Invalid id: {model.__name__} {id}"}), 400)

    item = model.query.get(item_id)

    if not item:
        abort(make_response({"message": f"Id {item_id} not found."}, 400))

    return item

@boards_bp.route("", methods=["GET"])
def get_all_boards():

    boards = Board.query.all()

    board_response = []

    for board in boards:
        board_response.append(board.to_dict())

    return jsonify(board_response), 200

@boards_bp.route("/<id>", methods=["GET"])
def get_one_board(id):
    board = validate_item(Board, id)

    return make_response({"board": board.to_dict()})

@boards_bp.route("", methods=["POST"])
def add_board(): 
    request_body = request.get_json()

    try: 
        new_board = Board(
            title = request_body["title"],
            owner = request_body["owner"]
        )
    
    except KeyError: 
        return make_response({"Message": "Invalid Data"}), 400
    
    db.session.add(new_board)
    db.session.commit()

    return {"board": new_board.to_dict()}, 201

@cards_bp.route("", methods=["GET"])
def get_all_cards():

    cards = Card.query.all()

    card_response = []

    for card in cards:
        card_response.append(card.to_dict())

    return jsonify(card_response), 200
