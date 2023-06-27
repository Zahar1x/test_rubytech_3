from datetime import datetime

from marshmallow import fields

from app import db, ma


class Status(db.Model):
    __tablename__ = "status"
    uuid = db.Column(db.Integer, primary_key=True)
    last_answer_code = db.Column(db.Integer, nullable=False)
    resource_status = db.Column(db.String(32))
    answer_last_time = db.Column(db.DateTime)
    resource_id = db.Column(db.Integer, db.ForeignKey("Links.uuid"))

    def __init__(self, last_answer_code, resource_status, answer_last_time, resource_id):
        self.last_answer_code = last_answer_code
        self.resource_status = resource_status
        self.answer_last_time = answer_last_time
        self.resource_id = resource_id


class StatusSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Status
        load_instance = True
        sqla_session = db.session
        include_fk = True


class Params(db.Model):
    __tablename__ = "params"
    uuid = db.Column(db.Integer, primary_key=True)
    key = db.Column(db.String(32), nullable=False)
    value = db.Column(db.String(32), nullable=False)
    fio = db.Column(db.String(60))
    resource_id = db.Column(db.Integer, db.ForeignKey("Links.uuid"))


class ParamsSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Params
        load_instance = True
        sqla_session = db.session
        include_fk = True


class Links(db.Model):
    __tablename__ = "Links"
    uuid = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.uuid"))
    title = db.Column(db.String, nullable=False)
    protocol = db.Column(db.String, nullable=False)
    domain = db.Column(db.String, nullable=False)
    domainZone = db.Column(db.String, nullable=False)
    path = db.Column(db.String, nullable=False)
    screenshot = db.Column(db.LargeBinary, nullable=False)

    statuses = db.relationship(
        Status,
        backref="Links",
        cascade="all, delete, delete-orphan",
        single_parent=True,
    )

    params = db.relationship(
        Params,
        backref="Links",
        cascade="all, delete, delete-orphan",
        single_parent=True,
    )

    def __init__(self, title, protocol, domain, domainZone, path, statuses, params):
        self.title = title
        self.protocol = protocol
        self.domain = domain
        self.domainZone = domainZone
        self.path = path
        self.statuses = statuses
        self.params = params


class LinksSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Links
        load_instance = True
        sqla_session = db.session
        include_fk = True


class User(db.Model):
    __tablename__ = "user"
    uuid = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(32))
    password = db.Column(db.String(32))
    fio = db.Column(db.String(60))

    Links = db.relationship(
        Links,
        backref="user",
        cascade="all, delete, delete-orphan",
        single_parent=True,
    )


class UserSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = User
        load_instance = True
        sqla_session = db.session
        include_relationships = True

    Links = fields.Nested(LinksSchema, many=True)


links_schema = LinksSchema()
user_schema = UserSchema()
status_schema = StatusSchema()
params_schema = ParamsSchema()
people_schema = UserSchema(many=True)
