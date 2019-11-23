import random

import requests
import pytest


@pytest.mark.parametrize("status_endpoint", ['/api/status', '/api/status/'])
def test_token_access_no_token(host, status_endpoint, no_token_headers):
    url = "{}{}".format(host, status_endpoint)
    response = requests.get(url, headers=no_token_headers)
    assert response.status_code == 401


@pytest.mark.parametrize("status_endpoint", ['/api/status', '/api/status/'])
def test_token_access_invalid(host, status_endpoint, invalid_token_headers):
    url = "{}{}".format(host, status_endpoint)
    response = requests.get(url, headers=invalid_token_headers)
    assert response.status_code == 401


@pytest.mark.parametrize("status_endpoint", ['/api/status', '/api/status/'])
def test_get_status(host, status_endpoint, json_headers):
    url = "{}{}".format(host, status_endpoint)
    response = requests.get(url, headers=json_headers)
    assert response.status_code == 200
    assert type(response.json()["score"]) is int
    assert type(response.json()["run_clock"]) is float
    assert type(response.json()["remaining_reports"]) is int
    assert type(response.json()["current_team"]) is str


@pytest.mark.parametrize("artifact_endpoint", ['/api/artifact_reports', '/api/artifact_reports/'])
def test_post_artifact_report_valid(host, artifact_endpoint, json_headers):
    url = "{}{}".format(host, artifact_endpoint)
    
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


@pytest.mark.parametrize("artifact_endpoint", ['/api/artifact_reports', '/api/artifact_reports/'])
def test_post_artifact_report_valid_random_float(host, artifact_endpoint, rand_str, json_headers):
    url = "{}{}".format(host, artifact_endpoint)

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


@pytest.mark.parametrize("artifact_endpoint", ['/api/artifact_reports', '/api/artifact_reports/'])
def test_post_artifact_report_invalid_missing_key(host, artifact_endpoint, json_headers):
    url = "{}{}".format(host, artifact_endpoint)

    invalid_data = {}
    response = requests.post(url, json=invalid_data, headers=json_headers)

    assert response.status_code == 422


@pytest.mark.parametrize("artifact_endpoint", ['/api/artifact_reports', '/api/artifact_reports/'])
@pytest.mark.parametrize("artifact_type", ["survivor", "backpack", "cell phone", "vent", "gas"])
def test_post_artifact_report_types(host, artifact_endpoint, json_headers, artifact_type):
    url = "{}{}".format(host, artifact_endpoint)

    min_= 0
    max_ = 100
    str_len = 5

    valid_data = {
        "x" : random.uniform(min_,max_),
        "y" : random.uniform(-1 * max_,min_),
        "z" : random.uniform(min_,max_),
        "type" : artifact_type,
    }

    response = requests.post(url, json=valid_data, headers=json_headers)

    assert response.status_code == 201
    assert response.json()["score_change"] == 1


@pytest.mark.parametrize("artifact_endpoint", ['/api/artifact_reports', '/api/artifact_reports/'])
def test_post_artifact_report_non_types(host, artifact_endpoint, rand_str, json_headers):
    url = "{}{}".format(host, artifact_endpoint)

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
    assert response.json()["score_change"] == 0