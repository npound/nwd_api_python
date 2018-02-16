from Crypto.Hash import SHA256


class NWD_Crypto:

    def Encrypt(self, password):
        hash = SHA256.new()
        hash.update(password.encode("ascii", "ignore"))
        return hash.hexdigest()