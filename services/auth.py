import repo.user as user_db
from models.auth_model import LoginResponse, UserLogin, UserCreate, RegisterResponse
from models.user import User
from services.errors import access_denied, internal_error
from services.utils import AuthToken


def login_user(user_data: UserLogin):
    username = user_data.username
    user = user_db.get_user_by_username(username)
    if user:
        password = user_data.password
        if user.password != password:
            raise access_denied
        token = AuthToken.generate({"sub": username})
        return LoginResponse(access_token=token, token_type="bearer")
    else:
        raise access_denied


def register_user(user_data: UserCreate):
    try:
        data = UserCreate(username=user_data.username,
                          password=user_data.password,
                          email=user_data.email,
                          birthday=user_data.birthday
                          )
        if not data:
            print(data)
            raise internal_error
        else:
            created_id = user_db.insert_user(data)
            return RegisterResponse(message=f"User {created_id} created successfully")

    except Exception as e:
        raise internal_error