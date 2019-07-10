import pytest
import random
import string


@pytest.fixture
def host():
    return 'http://localhost:8000'

@pytest.fixture
def rand_str():
    return  lambda n: ''.join([random.choice(string.ascii_lowercase) for i in range(n)])

@pytest.fixture
def json_headers():
    return  {"Authorization" : "Bearer tokentokentoken1",
             "Content-Type" : "application/json",
            }

@pytest.fixture
def invalid_token_headers(rand_str):
    return  { "authorization" : "bearer {}".format(rand_str(16)),
              "content-type" : "application/json",
            }

@pytest.fixture
def no_token_headers():
    return { "content-type" : "application/json",
           }