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


# BOARDS ROUTES
@boards_bp.route("", methods=["GET"])
def get_all_boards():

    boards = Board.query.all()

    board_response = []

    for board in boards:
        board_response.append(board.to_dict())

    return jsonify(board_response), 200


@boards_bp.route("/<board_id>", methods=["GET"])
def get_one_board(board_id):
    board = validate_item(Board, board_id)

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


@boards_bp.route("/<board_id>", methods=["POST"])
def add_card(board_id): 
    board = validate_item(Board, board_id)

    request_body = request.get_json()

    try: 
        new_card = Card(
            message = request_body["message"],
            board_id = board_id,
        )
    
    except KeyError: 
        return make_response({"Message": "Invalid Data"}), 400
    
    db.session.add(new_card)
    db.session.commit()

    return {"card": new_card.to_dict()}, 201


@boards_bp.route("/<board_id>/cards", methods=["GET"])
def get_all_cards(board_id):
    board = validate_item(Board, board_id)

    return board.to_dict(), 200

@boards_bp.route("/<board_id>", methods=["DELETE"])
def delete_one_board(board_id):
    board = validate_item(Board, board_id)

    db.session.delete(board)
    db.session.commit()

    return make_response({"Message": f"Board {board_id} successfully deleted"})


# CARDS ROUTES

@cards_bp.route("/<card_id>", methods=["DELETE"])
def delete_card(card_id):
    card = validate_item(Card, card_id)

    db.session.delete(card)
    db.session.commit()

    return make_response({"Details": f'Card {id} "{card.message}" successfully deleted'})


@cards_bp.route("/<card_id>", methods=["PATCH"])
def change_like_count(card_id):
    card = validate_item(Card, card_id) 

    request_body = request.get_json()

    card.likes_count = request_body["likes"]

    db.session.commit()

    return make_response({"card": card.to_dict()})