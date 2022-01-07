import pytest
from gourmandapiapp import schemas


def test_home(test_client):
    res = test_client.get('/')
    assert res.status_code == 200

def test_pull_business(test_client,inserted_business):

    res = test_client.get(f'/businesses/{inserted_business.businessid}')
    pg_data = res.json() 

def test_pull_business_redis(test_client, inserted_business):
    res_postgres = test_client.get(f'/businesses/{inserted_business.businessid}')
    res_redis = test_client.get(f'/businesses/{inserted_business.businessid}')
    assert res_postgres.json() == res_redis.json()

@pytest.mark.parametrize("keyword, sort, limit, offset", [
    ("Mcdonalds", "distancetocounty", 2, 0),
    ("Mcdonalds", "distancetocounty", 2, 1)
])
def test_pull_businesses_with_options(test_client, keyword, sort, limit, offset):
    bus_json = {"keyword":keyword, "sort":sort, "limit":limit, "offset":offset}
    res = test_client.get('/businesses', params = bus_json)
    assert res.status_code == 200
    # make a fixture in conftest so I can store a business in a variable and then make sure offset works properly

