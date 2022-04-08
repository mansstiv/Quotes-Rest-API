import json

try:
    from app import app
    import pytest
except Exception as ex:
    print(ex)


@pytest.fixture
def tester():
    return app.test_client()

def test_create_quote_unhappy(tester):
    """
    Test function for endpoint /quotes && method=post. 
    Invalid request. Trying to create a quote, with no mandatory 
    "text" field given. Statuscode should be 400.
    """
    data = {
        "author": "Manos"
    }
    response = tester.post('/quotes', json=data)
    assert response.status_code == 400
    assert isinstance(response.json, dict)
    assert b"Field 'text' is mandatory" in response.data

def test_get_quotes_happy(tester):
    """
    Test function for endpoint /quotes && method=get.
    Valid request. Should return all quotes with statuscode should be 200.
    """
    response = tester.get("/quotes")
    assert response.status_code == 200

def test_get_quote_unhappy(tester):
    """
    Test function for endpoint /quotes/<id> && method=get.
    Invalid request, due to not valid id. Statuscode should be 200.
    """
    response = tester.get("/quotes/asdadfhfdusdafhsadfjklsda")
    assert response.status_code == 400
    assert b'Id is invalid' in response.data

def test_update_quote_unhappy(tester):
    """
    Test function for endpoint /quotes/<id> && method=put. 
    Invalid request. Trying to update quote with specific id, but
    there is an invalid value type in body request. Statuscode should be 400.
    """
    data = {
        "author": "Manos", 
        "text": 12 # invalid type
    }
    response = tester.put("/quotes/62484e1cae6196db6f6929eb", json=data)
    assert response.status_code == 400
    assert b'Fields must be in string format' in response.data

def test_update_quote_happy(tester):
    """
    Test function for endpoint quotes/<id> && method=put.
    Valid request. Statuscode should be 200.
    """
    data = {
        "author": "Manos", 
        "text": "Keep Going!"
    }
    response = tester.put("/quotes/62484e1cae6196db6f6929eb", json=data)
    assert response.status_code == 200

if __name__ == "__main__":
    pytest.main()
