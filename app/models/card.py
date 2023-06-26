from app import db

class Card(db.Model):
    card_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    message = db.Column(db.String)
    likes_count = db.Column(db.Integer, default=0)

    def to_dict(self):
        card_dict = {
            "id": self.card_id,
            "message": self.message,
            "likes": self.likes_count
        }

        return card_dict
