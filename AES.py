"""
    AES算法用于文本信息的加密与解密
"""

import logging
import base64
import binascii
from Crypto.Cipher import AES

class AESCrypt:
    """
    AES/CBC/PKCS5Padding 加密
    """
    def __init__(self, key):
        """
        使用密钥,加密模式进行初始化
        :param key:
        """
        if len(key) != 16:
            raise RuntimeError('密钥长度非16位!!!')

        self.key = str.encode(key)
        self.iv = bytes(16)
        self.MODE = AES.MODE_CBC
        self.block_size = 16

        self.padding = lambda data: data + (self.block_size - len(data.encode('utf-8')) % self.block_size) * chr(
            self.block_size - len(data.encode('utf-8')) % self.block_size)
        # 截断函数
        self.unpadding = lambda data: data[:-ord(data[-1])]

    def aes_encrypt(self, plaintext):
        """
        加密函数
        :param plaintext: 明文
        :return:
        """
        try:
            # 填充16位
            padding_text = self.padding(plaintext).encode("utf-8")
            # 初始化加密器
            cryptor = AES.new(self.key, self.MODE, self.iv)
            # 进行AES加密
            encrypt_aes = cryptor.encrypt(padding_text)
            # 进行BASE64转码
            encrypt_text = (base64.b64encode(encrypt_aes)).decode()
            return encrypt_text
        except Exception as e:
            logging.exception(e)

    def aes_decrypt(self, ciphertext):
        """
        解密函数
        :param ciphertext: 密文
        :return:
        """
        try:
            cryptor = AES.new(self.key, self.MODE, self.iv)
            # 进行BASE64转码
            plain_base64 = base64.b64decode(ciphertext)
            # 进行ASE解密
            decrypt_text = cryptor.decrypt(plain_base64)
            # 截取
            plain_text = self.unpadding(decrypt_text.decode("utf-8"))
            return plain_text
        except UnicodeDecodeError as e:
            logging.error('解密失败,请检查密钥是否正确!')
            logging.exception(e)
        except binascii.Error as e:
            logging.exception(e)
        except Exception as e:
            logging.exception(e)


