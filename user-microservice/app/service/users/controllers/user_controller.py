import logging
import uuid

from fastapi import APIRouter, Depends, status, Response
from jwt_guard import JwtPrincipal
from sqlalchemy.orm import Session

from app.core.jwt_guard import require_access_token

from app.db.dependencies import get_db
from app.service.users.dto.user_dto import UserRsDto, AddUserRqDto, UserAuthoritiesRqDto
from app.service.users.user_service import get_all_users, get_by_email, get_by_login, add_user, grant_authorities, revoke_authorities
from app.utils.jwt_utils import get_authorities

logger = logging.getLogger(__name__)

router = APIRouter(
    prefix= "/api/v1/users",
    tags= ["users"],
    dependencies= [Depends(require_access_token)]
)

@router.get("", response_model=list[UserRsDto])
def get_users(db: Session = Depends(get_db)) -> list[UserRsDto]:
    return get_all_users(db)

@router.post("", response_model= UserRsDto)
def add_new_user(
        body: AddUserRqDto,
        db: Session = Depends(get_db),
        principal: JwtPrincipal = Depends(require_access_token)) -> UserRsDto:

    logger.info("START user_controller::add_new_user login=%s, new_login=%s, new_email=%s",principal.login, body.login, body.email)
    authorities = get_authorities(principal)
    result = add_user(authorities, body, db)
    logger.info("END user_controller::add_new_user login=%s, new_login=%s, new_email=%s, result=%s",principal.login, body.login, body.email, str(result))
    return result

@router.put("/{user_id}/authorities/grant", status_code= status.HTTP_204_NO_CONTENT)
def grant_user_authorities(
        user_id: uuid.UUID,
        body: UserAuthoritiesRqDto,
        db: Session = Depends(get_db),
        principal: JwtPrincipal = Depends(require_access_token)):

    logger.info("START user_controller::grant_user_authorities login=%s, user_id=%, permissions=%s",principal.login, user_id, body.authorities)
    authorities = get_authorities(principal)
    grant_authorities(user_id, authorities, body, db)
    logger.info("END user_controller::grant_user_authorities login=%s, user_id=%, permissions=%s",principal.login, user_id, body.authorities)
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@router.put("/{user_id}/authorities/revoke", status_code= status.HTTP_204_NO_CONTENT)
def revoke_user_permissions(
        user_id: uuid.UUID,
        body: UserAuthoritiesRqDto,
        db: Session = Depends(get_db),
        principal: JwtPrincipal = Depends(require_access_token)):

    logger.info("START user_controller::revoke_user_permissions login=%s, user_id=%, permissions=%s",principal.login, user_id, body.authorities)
    authorities = get_authorities(principal)
    revoke_authorities(user_id, authorities, body, db)
    logger.info("END user_controller::revoke_user_permissions login=%s, user_id=%, permissions=%s",principal.login, user_id, body.authorities)
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@router.get("/email/{email}", response_model=list[UserRsDto])
def get_user_by_email(email: str, db: Session = Depends(get_db)) -> UserRsDto:
    return get_by_email(email, db)

@router.get("/login/{login}", response_model=UserRsDto | None)
def get_user_by_login(login: str, db: Session = Depends(get_db)) -> UserRsDto | None:
    return get_by_login(login, db)