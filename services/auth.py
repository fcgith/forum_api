import repo.user as user_db
from models.auth_model import LoginResponse, UserLogin, UserCreate, RegisterResponse
from models.user import UserPublic, User
from services.errors import access_denied, internal_error, registration_user_exists, invalid_credentials, not_found
from services.utils import AuthToken

class AuthService:
    @classmethod
    def login_user(cls, user_data: UserLogin) -> LoginResponse | None:
        username = user_data.username
        user = user_db.get_user_by_username(username)
        if user:
            if user.password == user_data.password:
                token = AuthToken.generate({"sub": username})
                return LoginResponse(access_token=token, token_type="bearer")
        raise invalid_credentials

    @classmethod
    def register_user(cls, user_data: UserCreate) -> RegisterResponse:
        data = UserCreate(username=user_data.username,
                          password=user_data.password,
                          email=user_data.email,
                          birthday=user_data.birthday
                          )

        if user_db.user_exists((user_data.username, user_data.email)):
            raise registration_user_exists

        created_id = user_db.insert_user(data)
        return RegisterResponse(message=f"User {created_id} created successfully")

    @classmethod
    def decode_token_username(cls, token) -> UserPublic | None:
        if AuthToken.validate_expiry(token):
            user = AuthToken.validate(token, public=True)
            if not user:
                raise not_found
            return user
        return None