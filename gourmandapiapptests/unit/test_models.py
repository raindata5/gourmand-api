import pytest
from gourmandapiapp import (
    models,
    schemas
)

def test_default_user_role():
    test_user = models.AuthUserModelORM(
        email='rainwave5+test_user_123@gmail.com'
    )
    assert test_user.can(schemas.Permission.FOLLOW)
    assert test_user.can(schemas.Permission.COMMENT)
    assert test_user.can(schemas.Permission.WRITE)
    assert not test_user.can(schemas.Permission.MODERATE)
    assert not test_user.can(schemas.Permission.ADMIN)

def test_anonymous_user():
    user_anon = models.AuthUserModelORM(
        email="Guest@gmail.com"
    )
    assert not user_anon.can(schemas.Permission.FOLLOW)
    assert not user_anon.can(schemas.Permission.COMMENT)
    assert not user_anon.can(schemas.Permission.WRITE)
    assert not user_anon.can(schemas.Permission.MODERATE)
    assert not user_anon.can(schemas.Permission.ADMIN)
