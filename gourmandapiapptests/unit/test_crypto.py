import pytest
from gourmandapiapp import models


def test_pass_hash_verified():
    user = models.AuthUserModelORM(
        userid = "",
        email = "",
        password = "natalia"
    )
    print(vars(user))
    user.passy = 'natalia'
    assert user.check_password('natalia')
    print(vars(user))

def test_pass_hash_unsuccessful():
    user = models.AuthUserModelORM(
        userid = "",
        email = "",
        password = ""
    )
    print(vars(user))
    user.passy = 'natalia'
    assert not user.check_password('natalia12345')
    print(vars(user))