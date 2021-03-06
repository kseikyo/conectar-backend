from fastapi import (APIRouter, Request, Depends, Response,
                     encoders, UploadFile, File, Form)
import typing as t
from app.db.habilidade.schemas import PessoaHabilidadeCreate
from app.db.area.schemas import ProjetoAreaCreate

from app.db.session import get_db
from app.db.projeto.crud import (
    create_projeto,
    get_projetos,
    get_projeto,
    delete_projeto,
    edit_projeto,
)
from app.db.projeto.schemas import ProjetoCreate, Projeto, ProjetoOut, ProjetoEdit
from app.core.auth import get_current_active_pessoa

projeto_router = r = APIRouter()


@r.get(
    "/projetos", response_model=t.List[Projeto], response_model_exclude_none=True,
)
async def projetos_list(
    response: Response,
    db=Depends(get_db),
    current_pessoa=Depends(get_current_active_pessoa),
):
    """
    Get all projetos
    """
    projetos = get_projetos(db)
    # This is necessary for react-admin to work
    response.headers["Content-Range"] = f"0-9/{len(projetos)}"
    return projetos


@r.get(
    "/projeto/{projeto_id}", response_model=Projeto, response_model_exclude_none=True,
)
async def projeto_details(
    request: Request,
    projeto_id: int,
    db=Depends(get_db),
    current_pessoa=Depends(get_current_active_pessoa),
):
    """
    Get any pessoa details
    """
    projeto = get_projeto(db, projeto_id)
    return projeto



@r.post("/projeto", response_model_exclude_none=True)
async def projeto_create(
    request: Request,
    db=Depends(get_db),
    nome: str = Form(...),
    descricao: str = Form(...),
    visibilidade: bool = Form(...),
    objetivo: str = Form(...),
    foto_capa: t.Optional[UploadFile] = File(None),
    current_pessoa=Depends(get_current_active_pessoa),
):
    """
    Create a new projeto
    """
    try:
        projeto = await create_projeto(db, nome=nome,
                                       descricao=descricao, visibilidade=visibilidade,
                                       objetivo=objetivo, foto_capa=foto_capa)
        return projeto
    except Exception as e:
        raise e


# @r.post("/projeto", response_model=Projeto, response_model_exclude_none=True)
# async def projeto_create(
#     request: Request,
#     projeto: ProjetoCreate,
#     db=Depends(get_db),
#     current_pessoa=Depends(get_current_active_pessoa),
# ):
#     """
#     Create a new projeto
#     """
#     return await create_projeto(db, projeto)


@r.put(
    "/projeto/{projeto_id}",
    response_model=Projeto,
    response_model_exclude_none=True,
)
async def projeto_edit(
    request: Request,
    projeto: ProjetoEdit,
    projeto_id: int,
    db=Depends(get_db),
    current_pessoa=Depends(get_current_active_pessoa),
):

    return await edit_projeto(db, projeto_id, projeto, current_pessoa.id)


@r.delete(
    "/projeto/{projeto_id}", response_model=Projeto, response_model_exclude_none=True
)
async def projeto_delete(
    request: Request,
    projeto_id: int,
    db=Depends(get_db),
    current_pessoa=Depends(get_current_active_pessoa),
):
    """
    Delete existing user
    """
    return delete_projeto(db, projeto_id)
