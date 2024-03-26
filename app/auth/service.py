from fastapi.security.api_key import APIKeyHeader, APIKeyCookie, APIKeyQuery
from fastapi.security import HTTPBasicCredentials, HTTPBasic
from fastapi import Security, status, HTTPException, Depends
from app.config import settings


docs_auth = HTTPBasic()
api_key = settings.api_key

api_key_query_1 = APIKeyQuery(name='access_token', auto_error=False)
api_key_header_1 = APIKeyHeader(name='access_token', auto_error=False)


async def get_api_key(
        api_key_query: str = Security(api_key_query_1),
        api_key_header: str = Security(api_key_header_1)
):
    if api_key_query is not None and api_key_query == api_key:
        return api_key_query
    elif api_key_header is not None and api_key_header == api_key:
        return api_key_header
    else:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Could not validate credentials")


def get_docs_username(credentials: HTTPBasicCredentials = Depends(docs_auth)):
    correct_username = (credentials.username == settings.docs_auth_username)
    correct_password = (credentials.password == settings.docs_auth_password)
    if not (correct_username and correct_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Basic"},
        )
    return credentials.username
