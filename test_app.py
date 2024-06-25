import pytest
from App import app, db


@pytest.fixture
def client():
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'

    with app.app_context():
        db.create_all()
        yield app.test_client()
        db.drop_all()


def test_index_get(client):
    rv = client.get('/')
    assert rv.status_code == 200
    assert b'No records found' in rv.data or b'<ul>' in rv.data


def test_index_post(client):
    rv = client.post('/', data={'content': 'Test String'}, follow_redirects=True)
    assert rv.status_code == 200
    assert b'Test String' in rv.data


def test_index_post_and_get(client):
    client.post('/', data={'content': 'Another Test String'}, follow_redirects=True)
    rv = client.get('/')
    assert rv.status_code == 200
    assert b'Another Test String' in rv.data
