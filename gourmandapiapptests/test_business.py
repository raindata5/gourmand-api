import pytest



def test_home(test_client):
    res = test_client.get('/')
    assert res.status_code == 200

def test_pull_business(test_client):
    res = test_client.get('/businesses/1')
    print(res.json())


@pytest.mark.parametrize("keyword, sort, limit, offset", [
    ("Mcdonalds", "distancetocounty", 2, 0),
    ("Mcdonalds", "distancetocounty", 2, 1)
])
def test_pull_businesses_with_options(test_client, keyword, sort, limit, offset):
    bus_json = {"keyword":keyword, "sort":sort, "limit":limit, "offset":offset}
    res = test_client.get('/businesses', params = bus_json)
    assert res.status_code == 200
    # make a fixture in conftest so I can store a business in a variable and then make sure offset works properly

