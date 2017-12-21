from client import AESCipher



def test_encrypt_decrypt_response():
    temp = AESCipher('CrossOver Project')
    CipherText = temp.encrypt("Hello World!")
    OriginalMessage = temp.decrypt(CipherText)
    assert(OriginalMessage == 'Hello World')
