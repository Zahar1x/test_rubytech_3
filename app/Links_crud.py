from flask import abort, make_response

from app import db
from app.models import Links, User, links_schema


def read_one(res_id):
    resource = Links.query.get(res_id)

    if resource is not None:
        return links_schema.dump(resource)
    else:
        abort(404, f"Resources with ID {res_id} not found")


def read_all():
    resources = Links.query.all()
    return links_schema.dump(resources)


def read_all_by_user_id(user_id):
    resources = Links.query.filter(User.uuid == user_id).all()
    if resources:
        return links_schema.dump(resources)
    else:
        return abort(404, f"Resources from user ID {user_id} not found")


def update(res_id, resource):
    existing_res = Links.query.get(res_id)

    if existing_res:
        update_res = links_schema.load(resource, session=db.session)
        existing_res.content = update_res.content
        db.session.merge(existing_res)
        db.session.commit()
        return links_schema.dump(existing_res), 201
    else:
        abort(404, f"Resource with ID {res_id} not found")


def delete(res_id):
    existing_res = Links.query.get(res_id)

    if existing_res:
        db.session.delete(existing_res)
        db.session.commit()
        return make_response(f"{res_id} successfully deleted", 204)
    else:
        abort(404, f"Resource with ID {res_id} not found")


def create(resource):
    user_id = resource.get("user_id")
    user = User.query.get(user_id)

    if user:
        new_res = links_schema.load(resource, session=db.session)
        user.notes.append(new_res)
        db.session.commit()
        return links_schema.dump(new_res), 201
    else:
        abort(404, f"User not found for ID: {user_id}")
