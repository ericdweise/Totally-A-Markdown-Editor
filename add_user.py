import argparse

from database import (
    db_session,
    init_db,
)
from models import User

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Add a user to auth.db")
    parser.add_argument(
        "username",
        help="A unique username.",
    )
    parser.add_argument(
        "-p",
        "--password",
        help="The users password. Will be hashed before storing in the DB. The default password is Password123",
        default="password123",
    )
    args = parser.parse_args()

    init_db()
    u = User(args.username)
    u.set_password(args.password)

    db_session.add(u)
    db_session.commit()
