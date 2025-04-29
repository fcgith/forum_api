import repo.user as user_db
from models.auth_model import LoginResponse, UserLogin, UserCreate, RegisterResponse
from services.errors import access_denied, internal_error
from services.utils import AuthToken

class AuthService:
    @classmethod
    def login_user(cls, user_data: UserLogin) -> LoginResponse | None:
        username = user_data.username
        user = user_db.get_user_by_username(username)
        if user:
            if user.password != user_data.password:
                raise access_denied
            token = AuthToken.generate({"sub": username})
            return LoginResponse(access_token=token, token_type="bearer")
        else:
            raise access_denied

    @classmethod
    def register_user(cls, user_data: UserCreate) -> RegisterResponse:
        try:
            data = UserCreate(username=user_data.username,
                              password=user_data.password,
                              email=user_data.email,
                              birthday=user_data.birthday
                              )
            if not data:
                raise internal_error
            else:
                created_id = user_db.insert_user(data)
                if created_id:
                    return RegisterResponse(message=f"User {created_id} created successfully")
                else:
                    raise internal_error

        except Exception as e:
            print(e)
            raise internal_error

    @classmethod
    def decode_token_username(cls, token):
        if AuthToken.validate_expiry(token):
            data = AuthToken.decode(token)
            if data:
                return {"username": data["sub"]}
        return {"error": "Invalid token"}