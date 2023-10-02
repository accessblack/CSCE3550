from flask import Flask, jsonify, request, abort
from datetime import datetime, timedelta
import jwt
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization

app = Flask(__name__)
keys = []

# Key generation function
def generate_key():
    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048
    )
    public_key = private_key.public_key()
    kid = f"{len(keys) + 1}"
    expiry = datetime.utcnow() + timedelta(days=365)
    keys.append({
        "kid": kid,
        "private": private_key,
        "public": public_key,
        "expiry": expiry
    })
    return kid

generate_key()  # Generate initial key

@app.route("/jwks", methods=["GET"])
def jwks():
    valid_keys = [k for k in keys if k["expiry"] > datetime.utcnow()]
    jwks_data = {
        "keys": [{
            "kty": "RSA",
            "kid": key["kid"],
            "n": key["public"].public_numbers().n,
            "e": key["public"].public_numbers().e
        } for key in valid_keys]
    }
    return jsonify(jwks_data)

@app.route("/auth", methods=["POST"])
def authenticate():
    data = request.json
    if data["username"] != "userABC" or data["password"] != "password123":
        abort(401)
    expired = request.args.get("expired", None)
    if expired:
        key_data = [k for k in keys if k["expiry"] < datetime.utcnow()][0]
    else:
        key_data = [k for k in keys if k["expiry"] > datetime.utcnow()][0]

    token = jwt.encode({"user": "userABC", "kid": key_data["kid"]}, key_data["private"], algorithm="RS256", headers={"kid": key_data["kid"]})
    return jsonify({"token": token.decode('utf-8')})

if __name__ == "__main__":
    app.run(port=8080)
