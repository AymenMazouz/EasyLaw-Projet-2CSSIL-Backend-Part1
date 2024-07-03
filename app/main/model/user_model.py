from app.main import db, flask_bcrypt


class User(db.Model):  # type: ignore

    __tablename__ = "user"

    id: int = db.Column(db.Integer, primary_key=True, autoincrement=True)
    firstname: str = db.Column(db.String(60), nullable=False)
    lastname: str = db.Column(db.String(60), nullable=False)
    email: str = db.Column(db.String(255), unique=True, nullable=False)
    password_hash: str = db.Column(db.String(100), nullable=False)
    created_at = db.Column(db.DateTime(), server_default=db.func.now())
    updated_at = db.Column(
        db.DateTime(), server_default=db.func.now(), server_onupdate=db.func.now()
    )
    active = db.Column(db.Boolean(), default=True)
    # role can be user or admin or moderator
    role: str = db.Column(db.String(20), default="user")

    def __init__(
        self, firstname: str, lastname: str, email: str, password: str, role=None
    ):
        self.firstname = firstname
        self.lastname = lastname
        self.email = email
        self.password = password
        if role is not None:  # Check if role is provided during instantiation
            self.role = role

    @property
    def password(self):
        raise AttributeError("Password is not a readable attribute")

    @password.setter
    def password(self, password: str):
        self.password_hash = flask_bcrypt.generate_password_hash(password).decode(
            "utf-8"
        )

    def check_password(self, password: str) -> bool:
        return flask_bcrypt.check_password_hash(self.password_hash, password)

    def check_role(self, role: str) -> bool:
        return self.role == role

    def check_active_status(self) -> bool:
        return self.active

    def __repr__(self):
        return "<User '{}'>".format(self.email)
