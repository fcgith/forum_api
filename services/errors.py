# Errors go here
from fastapi import HTTPException

not_found = HTTPException(status_code=404, detail="Not found")
access_denied = HTTPException(status_code=403, detail="Access denied")
not_implemented = HTTPException(status_code=501, detail="Not implemented")
internal_error = HTTPException(status_code=500, detail="Internal error")


#auth errors
invalid_credentials = HTTPException(status_code=403, detail="Invalid credentials")
invalid_token = HTTPException(status_code=401, detail="Invalid token")
registration_user_exists = HTTPException(status_code=401, detail="Registration error: User with this username or email already exists")