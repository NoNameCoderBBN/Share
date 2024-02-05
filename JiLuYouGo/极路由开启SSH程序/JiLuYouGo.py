import base64
import hashlib
import hmac
import json
import urllib.request


def urlopen(url):
    r = urllib.request.urlopen(url)
    j = json.loads(r.read())
    return j


def get_hmac_sha1(message, key):
    result = hmac.new(key, message, hashlib.sha1).digest()
    return base64.b64encode(result).decode()


def sha1(data):
    return hashlib.sha1(data).digest()


if __name__ == '__main__':
    local_token = urlopen("http://10.1.199.1//local-ssh/api?method=get")["data"]
    print("local token:" + local_token)
    mac, ssh, t, hmacstr = base64.b64decode(local_token).split(b",", 3)
    message = "{},ssh,{}".format(mac.decode(), int(t) + 1).encode()

    uuid = urlopen("http://10.1.199.1/cgi-bin/turbo/proxy/router_info")["data"]["uuid"]
    print("uuid:" + uuid)
    key = sha1(uuid.encode())
    h = get_hmac_sha1(message, key)
    print("cloud token:" + h)

    print("result >> " + urlopen("http://10.1.199.1/local-ssh/api?method=valid&data=" + h)["data"])
