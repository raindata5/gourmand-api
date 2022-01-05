import pytest

@pytest.mark.parametrize("businessid", [
    (10),
    (20)
])
def test_pull_businessholdings_business(test_client, businessid):
    res = test_client.get(f'/businessholdings/{businessid}')
    assert res.status_code == 200
    print(res.json())

@pytest.mark.parametrize("sort, limit, offset", [
    ("reviewcount", 2, 0),
    ("businessrating", 2, 1)
])
def test_pull_businessholdings_with_options(test_client, sort, limit, offset):
    bushodl_json = {"sort":sort, "limit":limit, "offset":offset}
    res = test_client.get('/businessholdings', params = bushodl_json)
    print(len(res.json()))
    print(res.json())