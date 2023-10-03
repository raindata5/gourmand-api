import pytest
from gourmandapiapp import (
    models,
    utils
)

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

def test_verification_pass():
    message = 'ronald'
    message_hash = utils.get_password_hash(message)
    assert utils.verification(message, message_hash)

def test_verification_fail():
    message = 'ronald'
    message_false = 'ronald123'
    message_hash = utils.get_password_hash(message)
    # with pytest.raises(utils.UnknownHashError):
    assert not utils.verification(message_false, message_hash)