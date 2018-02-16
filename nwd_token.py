import python_jwt as jwt, jwcrypto.jwk as jwk, datetime
from nwd_db import NWD_DB


class NWD_JWT:

    def GetToken(self, username,password):
        try:
            db = NWD_DB()

            sub = db.authenticate_user(username,password)[0]

            if sub != '':
                key = jwk.JWK.generate(kty='RSA', size=2048)

                userinfo = db.get_user_info(sub)

                payload = { 
                    'fname': userinfo['fname'],
                    'lname': userinfo['lname'],
                    'phone': userinfo['phone'],
                    'email': userinfo['email'],
                    'datejoined': userinfo['datejoined'],
                    'sub': userinfo['user_id'],
                }

                token = jwt.generate_jwt(payload, key, 'PS256', datetime.timedelta(days=1))
                header, claims = jwt.verify_jwt(token, key, ['PS256'])
                for k in payload: assert claims[k] == payload[k]
                return token
            else:
                return ''
        except:
            return ''

            
    def CheckToken(token):

        try:
            jwt.verify_jwt(token, key, ['PS256'])
            return True
        except:
            return False