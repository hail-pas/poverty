import base64
import hashlib
import hmac
import json
import os
import time
from urllib.parse import urlencode

import OpenSSL
import httpx
import jwt
import requests
from Cryptodome import Random
from Cryptodome.Cipher import AES, PKCS1_v1_5
from Cryptodome.Hash import SHA
from Cryptodome.PublicKey import RSA
from Cryptodome.Util.Padding import pad, unpad
from OpenSSL import crypto
from OpenSSL.crypto import FILETYPE_PEM
from passlib.context import CryptContext


class AESUtil:
    """
    aes 加密与解密
    """

    def __init__(self, key: str, style='pkcs7', mode=AES.MODE_ECB):
        self.mode = mode
        self.style = style
        self.key = base64.b64decode(key.encode())

    def encrypt_data(self, data: str):
        data = data.encode()
        aes = AES.new(self.key, self.mode)
        pad_data = pad(data, AES.block_size, style=self.style)
        return str(base64.encodebytes(aes.encrypt(pad_data)), encoding='utf8').replace('\n', '')

    def decrypt_data(self, data: str):
        data = data.encode()
        aes = AES.new(self.key, self.mode)
        pad_data = pad(data, AES.block_size, style=self.style)
        return str(unpad(aes.decrypt(base64.decodebytes(pad_data)), block_size=AES.block_size).decode('utf8'))

    @staticmethod
    def generate_key(length=256) -> str:
        random_key = os.urandom(length)
        private_key = hashlib.sha256(random_key).digest()
        return base64.b64encode(private_key).decode()


class RSAUtil:
    """
    RSA 加密 签名
    """

    def __init__(self, pub_key_path: str, private_key_path: str, password: str):
        self.password = password
        with open(private_key_path, 'rb') as f:
            self.private_key = f.read()
        with open(pub_key_path, 'rb') as f:
            self.pub_key = f.read()

    def encrypt(self, text: str, length=200) -> str:
        """
        rsa 加密
        """
        key = RSA.import_key(self.pub_key)
        cipher = PKCS1_v1_5.new(key)
        res = []
        for i in range(0, len(text), length):
            text_item = text[i:i + length]
            cipher_text = cipher.encrypt(text_item.encode(encoding="utf-8"))
            res.append(cipher_text)
        return base64.b64encode(b''.join(res)).decode()

    def decrypt(self, text: str):
        """
        rsa 解密
        """
        key = RSA.import_key(self._get_private_key())
        cipher = PKCS1_v1_5.new(key)
        return cipher.decrypt(base64.b64decode(text), Random.new().read(15 + SHA.digest_size)).decode()

    def _get_private_key(self, ):
        """
        从pfx文件读取私钥
        """
        pfx = crypto.load_pkcs12(self.private_key, self.password.encode())
        res = crypto.dump_privatekey(crypto.FILETYPE_PEM, pfx.get_privatekey())
        return res

    def sign(self, text) -> str:
        """
        rsa 签名
        """
        p12 = OpenSSL.crypto.load_pkcs12(self.private_key, self.password.encode())
        pri_key = p12.get_privatekey()
        return base64.b64encode(OpenSSL.crypto.sign(pri_key, text.encode(), 'sha256')).decode()

    def verify(self, sign, data: str):
        """
        验签
        """
        key = OpenSSL.crypto.load_certificate(FILETYPE_PEM, self.pub_key)
        return OpenSSL.crypto.verify(key, base64.b64decode(sign), data.encode(), 'sha256')


class HashUtil:
    @staticmethod
    def md5_encode(s: str) -> str:
        """
        md5加密
        """
        m = hashlib.md5(s.encode(encoding='utf-8'))
        return m.hexdigest()

    @staticmethod
    def hmac_sha256_encode(k: str, s: str) -> str:
        """
        hmacsha256加密
        """
        return hmac.digest(k.encode(), s.encode(), hashlib.sha256).hex()

    @staticmethod
    def sha1_encode(s: str) -> str:
        """
        sha1加密
        """
        m = hashlib.sha1(s.encode(encoding='utf-8'))
        return m.hexdigest()


class SignAuth:
    """
    内部签名工具
    """

    def __init__(self, private_key: str):
        self.private_key = private_key

    def verify(self, data: str, sign: str):
        """
        校验sign
        """
        sign_tmp = self.generate_sign(data)
        return sign.upper() == sign_tmp.upper()

    def generate_sign(self, data: str) -> str:
        """
        生成sign
        """
        return HashUtil.hmac_sha256_encode(self.private_key, data, )


class Password:
    """
    密码工具
    """
    pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')

    @classmethod
    def verify_password(cls, plain_password, hashed_password):
        return cls.pwd_context.verify(plain_password, hashed_password)

    @classmethod
    def get_password_hash(cls, password):
        return cls.pwd_context.hash(password)


class Jwt:
    """
    jwt 工具
    """
    algorithm = 'HS256'

    def __init__(self, secret: str):
        self.secret = secret

    def get_jwt(self, payload: dict) -> str:
        return jwt.encode(payload, self.secret, algorithm=self.algorithm)

    def decode(self, credentials) -> dict:
        return jwt.decode(credentials, self.secret, algorithm=self.algorithm)


class Request:
    """
    加密请求工具
    """

    def __init__(self, secret: str):
        self.secret = secret

    def _get_headers(self, data: str):
        """
        头部处理 - 增加校验值 signature+时间戳
        :param data:
        :return:
        """
        timestamp = str(int(time.time()))
        headers = {
            'x-timestamp': timestamp
        }
        sign_str = data + f'.{timestamp}'
        headers['x-signature'] = SignAuth(self.secret).generate_sign(sign_str)
        return headers

    def get(self, url, params: dict = None, **kwargs):
        query_str = urlencode(params or {})
        headers = self._get_headers(query_str)
        headers.update(kwargs.pop('headers', {}))
        return requests.get(url=url, params=params, headers=headers, **kwargs)

    def post(self, url, payload: dict = None, **kwargs):
        data = json.dumps(payload or {}, ensure_ascii=False)
        headers = self._get_headers(data)
        headers.update(kwargs.pop('headers', {}))
        return requests.post(url=url, data=data.encode(), headers=headers, **kwargs)

    def put(self, url, payload: dict = None, **kwargs):
        data = json.dumps(payload or {}, ensure_ascii=False)
        headers = self._get_headers(data)
        headers.update(kwargs.pop('headers', {}))
        return requests.put(url=url, data=data.encode(), headers=headers, **kwargs)

    def delete(self, url, params: dict = None, **kwargs):
        data = json.dumps(params or {}, ensure_ascii=False)
        headers = self._get_headers(data)
        headers.update(kwargs.pop('headers', {}))
        return requests.delete(url=url, params=params, headers=headers, **kwargs)


class AsyncRequest(Request):
    """
    加密请求工具
    """

    async def get(self, url, params: dict = None, **kwargs):
        query_str = urlencode(params or {})
        headers = self._get_headers(query_str)
        headers.update(kwargs.pop('headers', {}))
        async with httpx.AsyncClient() as client:
            return await client.get(url=url, params=params, headers=headers, **kwargs)

    async def post(self, url, payload: dict = None, **kwargs):
        data = json.dumps(payload or {}, ensure_ascii=False)
        headers = self._get_headers(data)
        headers.update(kwargs.pop('headers', {}))
        async with httpx.AsyncClient() as client:
            return await client.post(url=url, data=data.encode(), headers=headers, **kwargs)

    async def put(self, url, payload: dict = None, **kwargs):
        data = json.dumps(payload or {}, ensure_ascii=False)
        headers = self._get_headers(data)
        headers.update(kwargs.pop('headers', {}))
        async with httpx.AsyncClient() as client:
            return await client.put(url=url, data=data.encode(), headers=headers, **kwargs)

    async def delete(self, url, params: dict = None, **kwargs):
        query_str = urlencode(params or {})
        headers = self._get_headers(query_str)
        headers.update(kwargs.pop('headers', {}))
        async with httpx.AsyncClient() as client:
            return await client.delete(url=url, params=params, headers=headers, **kwargs)
