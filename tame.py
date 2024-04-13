#!/usr/bin/env python3

import argparse
import os

from flask import (
    Blueprint,
    Flask,
    Response,
    flash,
    redirect,
    render_template,
    request,
    send_from_directory,
    url_for,
)
from flask_login import (
    LoginManager,
    login_required,
    login_user,
    logout_user,
)
from sqlalchemy import select
from uuid import uuid4

from database import (
    db_session,
    init_db,
)
from models import User
from note_ops import (
    make_site_dir,
    render_note,
    read_note_title,
    read_raw_note,
    save_note,
)


# Create Blueprints
main_bp = Blueprint("main", "tame")
auth_bp = Blueprint("auth", "tame")


############
# USER OPS #
############

@auth_bp.route("/login", methods=["GET"])
def login():
    return render_template("login.html")


@auth_bp.route("/login", methods=["POST"])
def login_post():
    username = request.form.get('username')
    password = request.form.get('password')
    remember = True if request.form.get('remember') else False

    statement = select(User).filter_by(username=username)
    # e = db_session.execute(statement)
    user = None
    try:
        user = db_session.scalars(statement).one()
    except Exception:
        print("FAILED TO GET USER")
        return login_fail()

    if not user or not user.check_password(password):
        print(f"PW check: {user.check_password(password)}")
        return login_fail()

    login_user(user, remember=remember)
    return redirect("/")


def login_fail():
    flash('Invalid login')
    return redirect(url_for('auth.login'))


@auth_bp.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect("auth.login")


##########################
# Routes hidden by login #
##########################

@main_bp.route('/', methods=['GET'])
@login_required
def index():
    return redirect("/view")


@main_bp.route('/view', methods=['GET'])
@login_required
def view_note():
    return render_template('view.html')


@main_bp.route('/edit', methods=['GET'])
@login_required
def edit_note():
    return render_template('edit.html')


@main_bp.route('/favicon.ico', methods=['GET'])
def favicon():
    return send_from_directory(
        os.path.join(main_bp.root_path, 'static'),
        'favicon.ico',
        mimetype='image/vnd.microsoft.icon')


# TODO: wrap in to load-note endpoint
@main_bp.route('/get-title', methods=['GET'])
@login_required
def get_note_title():
    return read_note_title(request.args.get('note'))


@main_bp.route("/load-note", methods=['GET'])
@login_required
def load_note():
    return render_note(request.args.get('note'))


@main_bp.route("/load-raw", methods=['GET'])
@login_required
def load_raw_note():
    return read_raw_note(request.args.get('note'))


@main_bp.route("/save", methods=['POST'])
@login_required
def post_note():
    try:
        save_note(
                request.form.get('note'),
                request.form.get('raw')
            )
        return Response("", status=201)
    except Exception:
        return Response("", status=500)


@main_bp.route("/site-directory", methods=['GET'])
@login_required
def sitedir():
    return make_site_dir()


@main_bp.route("/profile", methods=['GET'])
@login_required
def profile():
    return render_template("profile.html")


def create_app():
    app = Flask("tame")

    app.config['SECRET_KEY'] = uuid4().hex
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///auth.db'

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(user_id):
        return db_session.get(User, user_id)

    # blueprint for auth routes
    app.register_blueprint(auth_bp)

    # blueprint for non-auth routes
    app.register_blueprint(main_bp)

    return app


if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "-H",
        "--host",
        default="0.0.0.0",
        help="The host to serve to",
    )
    parser.add_argument(
        "-p",
        "--port",
        type=int,
        default=8088,
        help="The TCP to listen on",
    )
    parser.add_argument(
        "-D",
        "--debug",
        action="store_true",
        help="Run Flask in debug mode",
    )

    args = parser.parse_args()

    print(args)

    app = create_app()

    @app.teardown_appcontext
    def shutdown_session(exception=None):
        db_session.remove()

    # Init DB file
    init_db()
