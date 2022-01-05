from flask import Flask, request, jsonify, send_from_directory
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
import os
from sqlalchemy import and_, func

app = Flask(__name__, static_url_path='')
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'grades.sqlite')
db = SQLAlchemy(app)
ma = Marshmallow(app)


class Game(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime, server_default=db.func.now())
    player = db.Column(db.String(25))
    score = db.Column(db.Integer)

    def __init__(self, player, score):
        self.player = player
        self.score = score

class GameSchema(ma.Schema):
    class Meta:
        # Fields to expose
        fields = ('id', 'timestamp', 'player', 'score')


game_schema = GameSchema()
games_schema = GameSchema(many=True)


# endpoint to create new game
@app.route("/game", methods=["POST"])
def add_game():
    player = request.json['player']
    score = request.json['score']

    print(player, score)
    new_game = Game(player, score)

    db.session.add(new_game)
    db.session.commit()

    return game_schema.jsonify(new_game)

@app.route("/static/<path:path>")
def send_static(path):
    return send_from_directory('static', path)

# endpoint to show highscores 
@app.route("/highscores", methods=["GET"])
def get_game():
    page = request.args.get('page', 1, type=int)

    q = db.session.query(Game.id, Game.timestamp, Game.player, func.max(Game.score).label('score')).group_by(Game.player).order_by(Game.score.desc(), Game.timestamp.desc())
#    print(q.statement)

    all_games = q.paginate(page, 20, False)
    result = games_schema.dump(all_games.items)
    return jsonify(result)


# endpoint to show player games
@app.route("/highscores/<player>", methods=["GET"])
def game_detail(player):
    game = db.session.query(Game).filter(and_(Game.player == player, Game.score > 0)).order_by(Game.score.desc()).limit(10)
    result = games_schema.dump(game)
    return jsonify(result)


if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0', port=80)
