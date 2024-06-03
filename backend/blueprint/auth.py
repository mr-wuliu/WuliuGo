from flask import (
    Blueprint, jsonify, request, session
)
from flask_login import (
    login_user
)
from backend.models import db, User
bp = Blueprint("auth", __name__, url_prefix='/user')

@bp.route("/register", methods=['POST'])
def register():
    if request.method == "POST":
        data = request.get_json()
        username = data.get("username")
        password = data.get("password")
        email = data.get("email")
        new_user = User(username=username, password=password, email=email)
        db.session.add(new_user)
        db.session.commit()
        return jsonify({"message":"User register successfully."}), 200

@bp.route("/login", methods=['POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        if not username or not password:
            return jsonify({"message":"Username and passwor 6can not be null."}), 404
        
        user : User = User.query.filter_by(username = username).first()
        
        if user is None:
            return jsonify({"message":"User can not be found."}), 404
        
        if username == user.username and user.verify_password(password):
            login_user(user)
            return jsonify({"message":"User login successfully."}), 200

@bp.route("/logout", methods=['GET'])
def login():
    if request.method == 'GET':
        session.clear()
        return jsonify({"message":"User logout successfully."}), 200
    