import repo.user as user_db
from models.auth_model import LoginResponse, UserLogin, UserCreate, RegisterResponse
from models.user import UserPublic
from services.errors import access_denied, internal_error, registration_user_exists, invalid_credentials, not_found, \
    invalid_token
from services.utils import AuthToken
import bcrypt

hash_key = "faiosjfoiawjrgfioawhf98wa4hf943ht9824hf97234hf928"


class AuthService:
    @classmethod
    def login_user(cls, user_data: UserLogin) -> LoginResponse | None:
        username = user_data.username
        user = user_db.get_user_by_username(username)
        if user:
            if bcrypt.checkpw(user_data.password.encode('utf-8'), user.password.encode('utf-8')):
                token = AuthToken.generate({"sub": username})
                return LoginResponse(access_token=token, token_type="bearer")
        raise invalid_credentials

    @classmethod
    def register_user(cls, user_data: UserCreate) -> RegisterResponse:
        if user_db.user_exists((user_data.username, user_data.email)):
            raise registration_user_exists

        # Hash the password before storage
        hashed_password = bcrypt.hashpw(user_data.password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

        # Create a new UserCreate instance with the hashed password
        data = UserCreate(
            username=user_data.username,
            password=hashed_password,  # Store hashed password
            email=user_data.email,
            birthday=user_data.birthday
        )

        # Insert the user into the database
        created_id = user_db.insert_user(data)
        return RegisterResponse(message=f"User {created_id} created successfully")

    @classmethod
    def decode_token_username(cls, token) -> UserPublic | None:
        if AuthToken.validate_expiry(token):
            user = AuthToken.validate(token, public=True)
            return user
        raise invalid_token