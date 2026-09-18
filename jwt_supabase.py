from datetime import datetime , timedelta, timezone
from fastapi import FastAPI, HTTPException, Depends, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
import jwt
from supabase import create_client, Client
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

SECRET_KEY = "cle_secrete_du_frigo"
ALGORITHM = "HS256"

SUPABASE_URL = "https://lhukyensutqylsnosqja.supabase.co"
SUPABASE_KEY = "sb_publishable_FIkeUK-dMRp5jtGsiShLFw_TtoYBSM-"
supabase : Client = create_client(SUPABASE_URL, SUPABASE_KEY)
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

@app.post("/signup")
def register_user(form_data: OAuth2PasswordRequestForm = Depends()):
    existing_user = supabase.table("users").select("*").eq("email", form_data.username).execute()
    if existing_user.data:
        raise HTTPException(status_code=400, detail="Utilisateur déjà existant")

    new_user_data = {
        "username": form_data.username,
        "password": form_data.password 
    }

    new_user = supabase.table("users").insert(new_user_data).execute()

    return{"message": f"Utilisateur {form_data.username} enregistré avec succès."}


def get_current_ser(token : str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token invalide")
        return username
    except jwt.PyJWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token invalide")
    
