from fastapi import Request, status
from fastapi.responses import Response, JSONResponse
from uuid import uuid4
import jwt


SECRET_KEY = 'you will never guess'


async def sessionMiddleware(request: Request, call_next) -> Response:
    session = request.cookies.get('session', None)
    if not session:
        response = JSONResponse({'error': 'Unauthorized'}, status_code=status.HTTP_407_PROXY_AUTHENTICATION_REQUIRED)
        response.headers['WWW-Authentication': 'URI /auth']
        return response
    else:
        request.state = get_player_uuid(session)
        response = await call_next(request)

    return response


def get_player_uuid(jwt_token, claim: str = 'player'):
    try:
        decoded_token = _decode_jwt_token(jwt_token)
        return decoded_token['player']
    except jwt.exceptions.MissingRequiredClaimError as exc:
        raise exc


def _decode_jwt_token(jwt_token):
    try:
        return jwt.decode(jwt_token, SECRET_KEY, algorithms='HS256')
    except jwt.exceptions.InvalidSignatureError as exc:
        raise exc


def create_session():
    payload = {'player': uuid4()}
    return jwt.encode(payload, SECRET_KEY, algorithm='HS256')