# 暗号化
```bash
gcloud kms encrypt \
--plaintext-file=plain.txt \
--ciphertext-file=plain.txt.enc \
 --keyring=keyringname \
 --key=keyname \
 --location=keylocation
```
