import jwt
from fastapi import Depends, HTTPException, status
from jwt import PyJWTError

from app.db import models, schemas, session
from app.db.crud import (
    get_pessoa_by_email,
    create_pessoa,
    get_pessoa_by_username,
)
from app.core import security

from typing import Optional

from datetime import date


async def get_current_pessoa(
    db=Depends(session.get_db), token: str = Depends(security.oauth2_scheme)
):
    """
        Get the current logged in user.

        Validates the jwt token and returns the user data from database.

        Args:
            db: Database Local Session. sqlalchemy.orm.sessionmaker instance
            token: The JWT token using the oauth2_scheme from security

        Returns:
            A Pessoa object from database. Each object is represented as a
            dict.
            For example:
            {
                id: 1,
                nome: Lucas,
                email: lucas@email.com
            }

        Raises:
            credentials_exception: HTTPException status 401. If token is invalid or is not
            present
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Não foi possível validar as credenciais",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(
            token, security.SECRET_KEY, algorithms=[security.ALGORITHM]
        )
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
        permissions: str = payload.get("permissions")
        token_data = schemas.TokenData(email=email, permissions=permissions)
    except PyJWTError:
        raise credentials_exception
    pessoa = get_pessoa_by_email(db, token_data.email)
    if pessoa is None:
        raise credentials_exception
    return pessoa


async def get_current_active_pessoa(
    current_pessoa: models.Pessoa = Depends(get_current_pessoa),
):
    if not current_pessoa.ativo:
        raise HTTPException(status_code=400, detail="Pessoa Inativa")
    return current_pessoa


async def get_current_active_superuser(
    current_pessoa: models.Pessoa = Depends(get_current_pessoa),
) -> models.Pessoa:
    if not current_pessoa.superusuario:
        raise HTTPException(
            status_code=403, detail="A pessoa não tem os privilégios necessarios"
        )
    return current_pessoa


def authenticate_pessoa(db, email: str, senha: str):
    pessoa = get_pessoa_by_email(db, email)
    pessoa_username = get_pessoa_by_username(db, email)

    username_message = {"message": "Nome de usuário incorreto"}
    password_message = {"message": "Senha incorreta"}
    if not pessoa:
        if not pessoa_username:
            return username_message
        if not security.verify_password(senha, pessoa_username.senha):
            return password_message
        else:
            return pessoa_username
    if not security.verify_password(senha, pessoa.senha):
        return password_message
    return pessoa


def sign_up_new_pessoa(
    db,
    email: str,
    senha: str,
    usuario: str,
    telefone: Optional[str] = None,
    nome: Optional[str] = None,
    data_nascimento: Optional[date] = None
):
    pessoa = get_pessoa_by_email(db, email)
    pessoa_username = get_pessoa_by_username(db, usuario)

    if pessoa and pessoa_username:
        return False  # Pessoa already exists
    new_pessoa = create_pessoa(
        db,
        schemas.PessoaCreate(
            data_nascimento=data_nascimento,
            email=email,
            telefone=telefone,
            nome=nome,
            senha=senha,
            usuario=usuario,
            ativo=True,
            superusuario=False,
        ),
    )
    return new_pessoa
