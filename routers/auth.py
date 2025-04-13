from fastapi import APIRouter, Depends, HTTPException
from services.utils import generate_token, decode_token

router = APIRouter()