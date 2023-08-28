from fastapi.security.api_key import APIKeyHeader, APIKeyCookie, APIKeyQuery
from fastapi import Security, status, HTTPException
from app.config import settings

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

