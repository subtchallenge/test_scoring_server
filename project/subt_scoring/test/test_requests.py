import requests
import random

def test_token_access_no_token(host, no_token_headers):
    url = "{}/api/status".format(host)
    response = requests.get(url, headers=no_token_headers)
    assert response.status_code == 401

def test_token_access_invalid(host, invalid_token_headers):
    url = "{}/api/status".format(host)
    response = requests.get(url, headers=invalid_token_headers)
    assert response.status_code == 401

def test_get_status(host, json_headers):
    url = "{}/api/status".format(host)
    response = requests.get(url, headers=json_headers)
    assert response.status_code == 200


def test_post_artifact_report_valid(host, json_headers):
    url = "{}/api/artifact_reports".format(host)
    
    valid_data = {
        "x" : 100,
        "y" : 100,
        "z" : 100,
        "type" : 'test',
    }

    response = requests.post(url, json=valid_data, headers=json_headers)
    assert response.status_code == 201

    assert type(response.json()["url"]) is str
    assert type(response.json()["id"]) is int
    try:
        float(response.json()["x"])
        float(response.json()["y"])
        float(response.json()["z"])
        assert True
    except ValueError:
        assert False
    assert type(response.json()["type"]) is str
    assert type(response.json()["submitted_datetime"]) is str
    assert type(response.json()["run_clock"]) is float
    assert type(response.json()["team"]) is str
    assert type(response.json()["run"]) is str
    assert type(response.json()["report_status"]) is str
    assert type(response.json()["score_change"]) is int


def test_post_artifact_report_valid_random_float(host, rand_str, json_headers):
    url = "{}/api/artifact_reports".format(host)

    min_= 0
    max_ = 100
    str_len = 5

    valid_data = {
        "x" : random.uniform(min_,max_),
        "y" : random.uniform(-1 * max_,min_),
        "z" : random.uniform(min_,max_),
        "type" : rand_str(str_len),
    }

    response = requests.post(url, json=valid_data, headers=json_headers)

    assert response.status_code == 201

    assert type(response.json()["url"]) is str
    assert type(response.json()["id"]) is int
    try:
        float(response.json()["x"])
        float(response.json()["y"])
        float(response.json()["z"])
        assert True
    except ValueError:
        assert False
    assert type(response.json()["type"]) is str
    assert type(response.json()["submitted_datetime"]) is str
    assert type(response.json()["run_clock"]) is float
    assert type(response.json()["team"]) is str
    assert type(response.json()["run"]) is str
    assert type(response.json()["report_status"]) is str
    assert type(response.json()["score_change"]) is int

def test_post_artifact_report_invalid_missing_key(host, json_headers):
    url = "{}/api/artifact_reports".format(host)

    invalid_data = {}
    response = requests.post(url, json=invalid_data, headers=json_headers)

    assert response.status_code == 422
