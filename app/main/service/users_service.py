from app.main.model.user_model import User
from app.main.utils.exceptions import BadRequestException
from app.main import db


class UsersService:
    def get_all_users(self, filter_by: dict | None = None) -> list[User]:
        if filter_by is None:
            filter_by = {}
        return User.query.filter_by(**filter_by).all()

    def create_user(
        self,
        email: str,
        password: str,
        firstname: str,
        lastname: str,
        role: str = "user",
    ) -> User:
        user = User.query.filter_by(email=email).first()
        if user:
            raise BadRequestException("User already exists.")

        new_user = User(
            email=email,
            password=password,
            firstname=firstname,
            lastname=lastname,
            role=role,
        )

        db.session.add(new_user)
        db.session.commit()
        return new_user

    def get_user_by_id(self, user_id: int) -> User | None:
        return User.query.filter_by(id=user_id).first()

    def update_user_by_id(self, user_id: int, **kwargs) -> User | None:
        user = User.query.filter_by(id=user_id).first()
        if not user:
            return None

        for key, value in kwargs.items():
            setattr(user, key, value)
        db.session.commit()
        return user

    def delete_user_by_id(self, user_id: int) -> User | None:
        user = User.query.filter_by(id=user_id).first()
        if user:
            db.session.delete(user)
        db.session.commit()
        return user

    def activate_user(self, user_id: int) -> User | None:
        user = User.query.filter_by(id=user_id).first()
        if user:
            user.active = True
        db.session.commit()
        return user

    def deactivate_user(self, user_id: int) -> User | None:
        user = User.query.filter_by(id=user_id).first()
        if user:
            user.active = False
        db.session.commit()
        return user
