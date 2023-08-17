import jwt
import datetime

from ..utils.constants import Constants
Key = Constants.Key
Url = Constants.Url

import bcrypt

class TokenDetail():
    private_key = None
    expire_duration = None #in hours
    algorithm = None


def generate_token_and_save_in_cookie(self, user):

    token_detail = self.application.token_detail

    if token_detail:

        payload = {
            Key.HOST: self.request.host,
            Key.USER_ID: user[Key.USER_ID],
            Key.EMAIL: user[Key.EMAIL],
            Key.FIRST_NAME: user[Key.FIRST_NAME],
            Key.MIDDLE_NAME: user[Key.MIDDLE_NAME],
            Key.LAST_NAME: user[Key.LAST_NAME],
            Key.FULLNAME: f"{user[Key.FIRST_NAME]}{' '+user[Key.MIDDLE_NAME] if user[Key.MIDDLE_NAME] else ''} {user[Key.LAST_NAME]}",
            Key.EXPIRE_ON: datetime.datetime.utcnow() + datetime.timedelta(hours=token_detail.expire_duration)
        }

        # Generate the JWT token
        try:
            private_key = token_detail.private_key
            token = jwt.encode(payload, private_key, algorithm=token_detail.algorithm)
            print(f'\nGenerated Token for user[id:{user[Key.USER_ID]}]:', token, '\n')

        except Exception as e:
            print(str(e))
            raise RuntimeError("Error encountered while generating token")
        
        if token:
            try:
                set_cookie(self, Key.USER_ID, payload)
                set_cookie(self, Key.EMAIL, payload)
                set_cookie(self, Key.FIRST_NAME, payload)
                set_cookie(self, Key.MIDDLE_NAME, payload)
                set_cookie(self, Key.LAST_NAME, payload)
                set_cookie(self, Key.FULLNAME, payload)
                set_cookie(self, Key.TOKEN, token)

                return payload
        
            except Exception as e:
                print(str(e))
                raise RuntimeError("Error encountered while setting cookies")
        else:
            raise RuntimeError("Could not generate token")
    else:
        raise RuntimeError("Received null token detail from application")

def set_cookie(self, key, payload):
    print(f'Setting cookie for {key} ...')
    self.set_secure_cookie(
        key, 
        str(payload if (key==Key.TOKEN) else payload[key])
    )
    

def get_cookie(self, key):
    print(f'Getting cookie for {key} ...')
    data = self.get_secure_cookie(key)
    return data


def validate_token_from_session(self):
    print("\nValidating token ...")
    decoded_payload = None
    token = get_cookie(self, Key.TOKEN)

    if token:
        token_detail = self.application.token_detail
        if token_detail:

            decoded_payload = None
            try:
                print(f"token: {token}")
                decoded_payload = jwt.decode(token, token_detail.private_key, algorithms=[token_detail.algorithm])
            except jwt.ExpiredSignatureError:
                print("Token has expired")
            except jwt.InvalidTokenError:
                print("Invalid token")

            print(f"decoded_payload: {decoded_payload}")
            if decoded_payload is None:
                print("Payload is None -> Redirecting to login page")
                self.redirect(Url.LOGIN)

        else:
            print("\nReceived null token detail from application")
            self.redirect(Url.LOGIN)
    else:
        print("\nReceived null token from session -> Redirecting to login page")
        self.redirect(Url.LOGIN)
        
    return decoded_payload


class Password():

    def encrypt(password):
        print(f'Encrypting password ...')

        # Generating a salt
        salt = bcrypt.gensalt()
        
        # Hashing the password using the generated salt
        hashed_password = bcrypt.hashpw(password.encode(Constants.PASSWORD_ENCODING_STANDARD), salt)
        return {Key.SALT_VALUE:salt, Key.HASHED_PASSWORD:hashed_password}
    

    def is_valid(stored_password_detail, provided_password):
        if stored_password_detail and provided_password:
            stored_salt = stored_password_detail[Key.SALT_VALUE]
            stored_hashed_password = stored_password_detail[Key.HASHED_PASSWORD]

            # stored_salt = bcrypt.gensalt()

            # Hashing the provided password with the stored salt
            # Comparing the stored encrypted password with the newly hashed password
            return stored_hashed_password.encode(Constants.PASSWORD_ENCODING_STANDARD) == bcrypt.hashpw(provided_password.encode(Constants.PASSWORD_ENCODING_STANDARD), stored_salt.encode(Constants.PASSWORD_ENCODING_STANDARD))
        else:
            raise RuntimeError("Stored password detail or provided password is null")