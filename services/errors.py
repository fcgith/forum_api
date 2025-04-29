# Errors go here
from fastapi import HTTPException

not_found = HTTPException(status_code=404, detail="Not found")
access_denied = HTTPException(status_code=403, detail="Access denied")
not_implemented = HTTPException(status_code=501, detail="Not implemented")
internal_error = HTTPException(status_code=500, detail="Internal error")


#auth errors
invalid_username = HTTPException(status_code=401, detail="Invalid username")
invalid_password = HTTPException(status_code=401, detail="Invalid password")
invalid_token = HTTPException(status_code=401, detail="Invalid token")
registration_username_exists = HTTPException(status_code=401, detail="Registration error: username already exists")
registration_email_exists = HTTPException(status_code=401, detail="Registration error: email already exists")