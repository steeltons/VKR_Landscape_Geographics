import logging
import uuid

from fastapi import APIRouter, Depends, status, Response
from jwt_guard import JwtPrincipal
from sqlalchemy.orm import Session

from app.core.jwt_guard import require_access_token
from app.models.models import UserAuthorityType
from app.service.decorators.require_authorities_decorator import require_authorities

from app.db.dependencies import get_db
from app.service.users.dto.user_dto import UserRsDto, AddUserRqDto, UserAuthoritiesRqDto, FullyCreateUserRqDto, \
    FullUserRsDto
from app.service.users.user_service import get_all_users, get_by_email, get_by_login, add_user, grant_authorities, \
    revoke_authorities, add_full_user, get_user_profile_by_id
from app.utils.jwt_utils import get_authorities

logger = logging.getLogger(__name__)

router = APIRouter(
    prefix= "/api/v1/users",
    tags= ["users"],
)

@router.get("", response_model=list[UserRsDto], dependencies= [Depends(require_access_token)])
def get_users(db: Session = Depends(get_db)) -> list[UserRsDto]:
    return get_all_users(db)

@router.get("/{user_id}", response_model=FullUserRsDto, dependencies= [Depends(require_access_token)])
def get_user_profile(user_id: uuid.UUID, db: Session = Depends(get_db)) -> FullUserRsDto:
    return get_user_profile_by_id(user_id=user_id, db=db)

@router.post(
    "",
    response_model= UserRsDto,
    dependencies= [Depends(require_authorities(UserAuthorityType.ADD_USERS))]
)
def add_new_user(
        body: AddUserRqDto,
        db: Session = Depends(get_db),
        principal: JwtPrincipal = Depends(require_access_token)) -> UserRsDto:

    logger.info("START user_controller::add_new_user login=%s, new_login=%s, new_email=%s",principal.login, body.login, body.email)
    authorities = get_authorities(principal)
    result = add_user(authorities, body, db)
    logger.info("END user_controller::add_new_user login=%s, new_login=%s, new_email=%s, result=%s",principal.login, body.login, body.email, str(result))
    return result

@router.put(
    "/{user_id}/authorities/grant",
    status_code= status.HTTP_204_NO_CONTENT,
    dependencies= [Depends(require_authorities(UserAuthorityType.GRANT_PERMISSIONS))]
)
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

@router.put(
    "/{user_id}/authorities/revoke",
    status_code= status.HTTP_204_NO_CONTENT,
    dependencies= [Depends(require_authorities(UserAuthorityType.REVOKE_PERMISSIONS))]
)
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

@router.post(
    '/full',
    response_model= UserRsDto,
    dependencies= [Depends(require_authorities(UserAuthorityType.ADD_USERS, UserAuthorityType.GRANT_PERMISSIONS))]
)
def add_new_full_user(body: FullyCreateUserRqDto, db: Session = Depends(get_db), principal: JwtPrincipal = Depends(require_access_token)):
    logger.info("START user_controller::add_full_user login=%s, body=%s",principal.login, body)
    result = add_full_user(body, db)
    logger.info("END user_controller::add_full_user login=%s, body=%s, result=%s",principal.login, body, result)
    return result

@router.get("/email/{email}", response_model=list[UserRsDto])
def get_user_by_email(email: str, db: Session = Depends(get_db)) -> UserRsDto:
    return get_by_email(email, db)

@router.get("/login/{login}", response_model=UserRsDto | None)
def get_user_by_login(login: str, db: Session = Depends(get_db)) -> UserRsDto | None:
    return get_by_login(login, db)