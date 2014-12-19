devreg-py
=========

Device Registration and signing utility application in Python.

# Installing

This software requires [PyJWT](https://github.com/progrium/pyjwt/), so
you must install:

```
$ pip install PyCrypto ecdsa PyJWT
```

# Using

## Registration

```
python dev_sign.py -r
```

Which returns:
```
eyJhbGciOiJFUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOnsidmVyc2lvbiI6IjEiLCJjcnlwdG9TZXJpYWwiOiIwMDAwMDAwMDAwMDAwMDAwMDAiLCJkZXZpY2VTZXJpYWwiOiJFUlJPUjAwMDAwMDAwMCIsInB1YktleSI6Ii0tLS0tQkVHSU4gUFVCTElDIEtFWS0tLS0tXG5NRmt3RXdZSEtvWkl6ajBDQVFZSUtvWkl6ajBEQVFjRFFnQUV6dXJrUlRFV2IveUtMQ3VNajExNW8yaHBqS3VzXG5saVVwTFdPdDRkWFJOSzk5VFYyaEhoWDlram5lL20vRVlEZllmNFl6T2Z1ZjVkY2hsSzk2YlFDa1BnPT1cbi0tLS0tRU5EIFBVQkxJQyBLRVktLS0tLSJ9LCJuYmYiOjE0MTg5NTEyMzB9.MEYCIQClB32dsRqsekjfjYfMLWMei27I4qPvZPikSz7ZnBTbFQIhAOkQ79zSGg-zStUKg2-CKClFyfdlnf5yKhADK7a3Jx0M
```

Which is a [JSON Web Token](http://jwt.io/). Whose claim is:

```
{
  "iss": {
    "version": "1",
    "cryptoSerial": "000000000000000000",
    "deviceSerial": "ERROR000000000",
    "pubKey": "-----BEGIN PUBLIC KEY-----\nMFkwEwYHKoZIzj0CAQYIKoZIzj0DAQcDQgAEzurkRTEWb/yKLCuMj115o2hpjKus\nliUpLWOt4dXRNK99TV2hHhX9kjne/m/EYDfYf4YzOfuf5dchlK96bQCkPg==\n-----END PUBLIC KEY-----"
  },
  "nbf": 1418951230
}
```

Currently, your keys are created in software and store unprotected on disk in `~/.reg_sk.pem` and `~/.reg_vk.pem` for your private and public key respectively.


## Signing data

```
echo 10 | python dev_sign.py
```

Produces another JWT object:

```
eyJhbGciOiJFUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOnsidmVyc2lvbiI6IjEiLCJjcnlwdG9TZXJpYWwiOiIwMDAwMDAwMDAwMDAwMDAwMDAiLCJkZXZpY2VTZXJpYWwiOiJFUlJPUjAwMDAwMDAwMCIsInB1YktleSI6Ii0tLS0tQkVHSU4gUFVCTElDIEtFWS0tLS0tXG5NRmt3RXdZSEtvWkl6ajBDQVFZSUtvWkl6ajBEQVFjRFFnQUV6dXJrUlRFV2IveUtMQ3VNajExNW8yaHBqS3VzXG5saVVwTFdPdDRkWFJOSzk5VFYyaEhoWDlram5lL20vRVlEZllmNFl6T2Z1ZjVkY2hsSzk2YlFDa1BnPT1cbi0tLS0tRU5EIFBVQkxJQyBLRVktLS0tLSJ9LCJkYXRhIjoiMTAiLCJuYmYiOjE0MTg5NTExNjcsImV4cCI6MTQxODk1MTI4N30.MEYCIQCopsxDgd0OZtDceLZzzqtT1uki3ciF0WgKFRLZ6xEBpwIhALOE2spw3xJOvucQxD6vwnYhYlN5zqWEYXDSlpczD5xD
```

Whose claims are:

```
{
  "iss": {
    "version": "1",
    "cryptoSerial": "000000000000000000",
    "deviceSerial": "ERROR000000000",
    "pubKey": "-----BEGIN PUBLIC KEY-----\nMFkwEwYHKoZIzj0CAQYIKoZIzj0DAQcDQgAEzurkRTEWb/yKLCuMj115o2hpjKus\nliUpLWOt4dXRNK99TV2hHhX9kjne/m/EYDfYf4YzOfuf5dchlK96bQCkPg==\n-----END PUBLIC KEY-----"
  },
  "data": "10",
  "nbf": 1418951167,
  "exp": 1418951287
}
```
