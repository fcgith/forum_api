# Errors go here
from fastapi import HTTPException

not_found = HTTPException(status_code=402, detail="Not found")
access_denied = HTTPException(status_code=403, detail="Access denied")
not_implemented = HTTPException(status_code=501, detail="Not implemented")
internal_error = HTTPException(status_code=500, detail="Internal error")
bad_request = HTTPException(status_code=400, detail="Bad request (invalid data provided)")
database_error = HTTPException(status_code=500, detail="Database error")

# user errors
user_not_found = HTTPException(status_code=402, detail="User not found")

# auth errors
invalid_credentials = HTTPException(status_code=403, detail="Invalid credentials.")
invalid_token = HTTPException(status_code=401, detail="Invalid token.")
registration_user_exists = HTTPException(status_code=401,
                                         detail="Registration error: User with this username or email already exists")

# conversation errors
conversation_not_found = HTTPException(status_code=402, detail="The conversation was not found.")

# category errors
category_not_found = HTTPException(status_code=402, detail="The category was not found.")
category_not_accessible = HTTPException(status_code=402,
                                        detail="You don't have permission to access this functionality.")
category_locked = HTTPException(status_code=403, detail="The category is locked.")

# topic errors
topic_not_found = HTTPException(status_code=402, detail="The topic was not found.")
topic_not_accessible = HTTPException(status_code=402, detail="You don't have permission to access this functionality.")
topic_locked = HTTPException(status_code=403, detail="The topic is locked.")

# reply errors
reply_not_found = HTTPException(status_code=402, detail="The reply was not found.")
reply_not_accessible = HTTPException(status_code=403, detail="You don't have permission to access this functionality.")
reply_invalid_data = HTTPException(status_code=400, detail="Invalid reply data.")
