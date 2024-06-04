import main

import pytest
from main import app as flask_app

@pytest.fixture
def app():
    yield flask_app

@pytest.fixture
def client(app):
    return app.test_client()

def test_home(client):
    response = client.get('/')
    assert response.status_code == 200
    assert response.json == {'message': 'Hello, world!'}

def test_about(client):
    response = client.get('/about')
    assert response.status_code == 200
    assert response.data == b'About page'

# Since we cannot directly test app.run(debug=True) within the pytest framework,
# because it starts a blocking thread, we can mock this call in a different context.
def test_app_run(mocker):
    mock_run = mocker.patch.object(flask_app, 'run')
    if __name__ == "__main__":
        flask_app.run(debug=True)
    mock_run.assert_called_with(debug=True)

