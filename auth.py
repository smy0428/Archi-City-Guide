import os
import json
from functools import wraps
from flask import request, session
from jose import jwt
from urllib.request import urlopen
import constants


ALGORITHMS = ['RS256']
AUTH0_DOMAIN = constants.AUTH0_DOMAIN
AUTH0_AUDIENCE = constants.AUTH0_AUDIENCE


# ---------------------------------------------------------------------------#
# AuthError Exception.
# ---------------------------------------------------------------------------#

class AuthError(Exception):
    def __init__(self, error, status_code):
        self.error = error
        self.status_code = status_code

# ---------------------------------------------------------------------------#
# Token in header.
# ---------------------------------------------------------------------------#


def get_token_auth_header():
    # for user already logged in
    if session.get('jwt_payload'):
        print('******', session.get('jwt_payload'), '******')
        return session.get('jwt_payload')

    print('****** NO token has been loaded ******')
    # for the test case
    auth = request.headers.get('Authorization', None)
    if auth is None:
        raise AuthError({
            'code': 'authorization_header_missing',
            'description': 'Authorization header is expected.'
        }, 401)

    parts = auth.split()
    if parts[0].lower() != 'bearer':
        raise AuthError({
            'code': 'invalid_header',
            'description': 'Authrization header must start with "Bearer".'
        }, 401)

    elif len(parts) == 1:
        raise AuthError({
            'code': 'invalid_header',
            'description': 'Token not found.'
        }, 401)

    elif len(parts) > 2:
        raise AuthError({
            'code': 'invalid_header',
            'description': 'Authorization header must be bearer token.'
        }, 401)

    token = parts[1]
    return token

# ---------------------------------------------------------------------------#
# Token verify with Auth0.
# ---------------------------------------------------------------------------#


def verifty_decode_jwt(token):
    '''
    urlopen has a common certificate error described here:
    https://stackoverflow.com/questions/50236117/scraping-ssl-certificate-verify-failed-error-for-http-en-wikipedia-org

    If you're using macOS go to Macintosh HD > Applications >
    Python3.6 folder (or whatever version of python you're using)
    > double click on "Install Certificates.command" file.
    '''
    josnurl = urlopen(("https://" + AUTH0_DOMAIN + "/.well-known/jwks.json"))
    jwks = json.loads(josnurl.read())

    unverified_header = jwt.get_unverified_header(token)

    rsa_key = {}
    if 'kid' not in unverified_header:
        raise AuthError({
            'code': 'invalid_header',
            'description': 'Authorization malformed.'
        }, 401)

    for key in jwks['keys']:
        if key['kid'] == unverified_header['kid']:
            rsa_key = {
                'kty': key['kty'],
                'kid': key['kid'],
                'use': key['use'],
                'n': key['n'],
                'e': key['e']
            }

    if rsa_key:
        try:
            payload = jwt.decode(
                token,
                rsa_key,
                algorithms=ALGORITHMS,
                audience=AUTH0_AUDIENCE,
                issuer='https://' + AUTH0_DOMAIN + '/'
            )

            return payload

        except jwt.ExpiredSignatureError:
            raise AuthError({
                'code': 'token_expired',
                'description': 'Token expired.'
            }, 401)

        except jwt.JWTClaimsError:
            raise AuthError({
                'code': 'invalid_claim',
                'description': 'Incorrect claim, ' +
                'please check the audience and issure.'
            }, 401)

        except Exception:
            raise AuthError({
                'code': 'invalid_header',
                'description': 'Unable to parse authentication token.'
            }, 400)

    raise AuthError({
        'code': 'invalid_header',
        'description': 'Unable to find the appropriate key.'
    }, 400)


def check_permissions(permission, payload):
    if 'permissions' not in payload:
        raise AuthError({
            'code': 'invalid_claim',
            'description': 'Permissions not included in JWT.'
        }, 400)

    if permission not in payload['permissions']:
        raise AuthError({
            'code': 'unauthorized',
            'description': 'Permission not found.'
        }, 403)

    return True


def requires_auth(permission=''):
    def requires_auth_decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            token = get_token_auth_header()
            payload = verifty_decode_jwt(token)
            check_permissions(permission, payload)

            return f(payload, *args, **kwargs)
        return wrapper
    return requires_auth_decorator
