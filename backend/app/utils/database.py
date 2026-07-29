# dependency so i dont have to type a long line every time
from fastapi import Depends
from app.database import get_db


db_dependency = Depends(get_db)