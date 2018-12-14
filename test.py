import base64
import bcrypt
ec="MTIzNDU2Nzg="
test=base64.b64decode(ec.encode())
print(test.decode("utf-8"))