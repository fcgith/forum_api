# Errors go here
from fastapi import HTTPException

not_found = HTTPException(status_code=404, detail="Not found")
access_denied = HTTPException(status_code=403, detail="Access denied")
not_implemented = HTTPException(status_code=501, detail="Not implemented")