import json
from datetime import datetime, timedelta
from functools import wraps

import jwt
import pymongo
from flask_cors import CORS
from flask import request, Flask, Response
from werkzeug.security import generate_password_hash, check_password_hash


app = Flask(__name__)
cors = CORS(app)

with open('config.json') as config_file:
    config = json.load(config_file)
    SECRET_KEY = config['SECRET_KEY']

mongo = pymongo.MongoClient("mongodb://mongo:27017")
mongo.drop_database("SecureQuestionnaire") 
DB = mongo["SecureQuestionnaire"]

# Create demo user
DB["user"].insert_one({
    "username": "pete",
    "password": generate_password_hash(
        "123", 
        method="sha256"
    ),
    "count": 0
})


# Verify access token
def token_required(f):
    @wraps(f)
    def _verify(*args, **kwargs):
        auth_headers = request.headers.get('Authorization', '').split()

        if len(auth_headers) != 2:
            return Response(response=json.dumps("failed"), status=401, mimetype="application/json")

        try:
            # [0]: Bearer; [1]: $TOKEN
            token = auth_headers[1]
            data = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
            user = DB["user"].find_one({ "username": data["sub"] })

            return f(*args, **kwargs)

        except jwt.ExpiredSignatureError:
            return Response(response=json.dumps("failed"), status=401, mimetype="application/json")

        except (jwt.InvalidTokenError, Exception) as e:
            return Response(response=json.dumps("failed"), status=401, mimetype="application/json")

    return _verify


def authenticate(username, password):
    hashed_password = generate_password_hash(
        password, 
        method="sha256"
    )

    user = DB["user"].find_one({ "username": username })

    if not user or not check_password_hash(user["password"], password):
        return None

    return user


@app.route("/api/login", methods=["PUT"])
def login():
    status = 200
    data = request.get_json()
    user = authenticate(data["username"], data["password"])

    token = jwt.encode(
        {
            'sub': user["username"],
            'iat': datetime.utcnow(),
            'exp': datetime.utcnow() + timedelta(minutes=30)
        },
        SECRET_KEY,
        algorithm="HS256"
    )

    response = { "token": token }

    return Response(response=json.dumps(response), status=status, mimetype="application/json")

@app.route("/api/user", methods=["GET"])
@token_required
def user():
    token = request.headers.get('Authorization', '').split()[1]
    data = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])

    return Response(response=json.dumps(data["sub"]), status=200, mimetype="application/json")

if __name__ == "__main__":
    app.run()

@app.route("/api/count", methods=["GET", "PUT"])
@token_required
def count():
    users = DB["user"]

    if request.method == "GET":
        count = users.find_one({ "username": request.args.get("username") })["count"]

        return Response(response=json.dumps(count), status=200, mimetype="application/json")

    elif request.method == "PUT":
        user = users.find_one({ "username": request.get_json()["username"] })
        users.delete_one({ "username": request.get_json()["username"] })
        # Increment gift count
        user["count"] += 1
        users.insert_one(user)
        
    return Response(status=200, mimetype="application/json")


if __name__ == "__main__":
    app.run()