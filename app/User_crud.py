from flask import abort, make_response

from app import db
from app.models import User, people_schema, user_schema


def read_all():
    people = User.query.all()
    return people_schema.dump(people)


def create(user):
    new_user = user_schema.load(user, session=db.session)
    db.session.add(new_user)
    db.session.commit()
    return user_schema.dump(new_user), 201


def read_one(user_id):
    user = User.query.get(user_id)

    if user is not None:
        return user_schema.dump(user)
    else:
        abort(404, f"user with ID {user_id} not found")


def update(user_id, user):
    existing_user = User.query.get(user_id)

    if existing_user:
        update_user = user_schema.load(user, session=db.session)
        existing_user.fname = update_user.fname
        existing_user.lname = update_user.lname
        db.session.merge(existing_user)
        db.session.commit()
        return user_schema.dump(existing_user), 201
    else:
        abort(404, f"user with ID {user_id} not found")


def delete(user_id):
    existing_user = User.query.get(user_id)

    if existing_user:
        db.session.delete(existing_user)
        db.session.commit()
        return make_response(f"{user_id} successfully deleted", 200)
    else:
        abort(404, f"user with ID {user_id} not found")
