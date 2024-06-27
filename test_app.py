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

def test_post_empty_string(client):
    rv = client.post('/', data={'content': ''}, follow_redirects=True)
    assert rv.status_code == 200
    assert b'No records found' in rv.data

def test_post_long_string(client):
    long_string = 'a' * 1000
    rv = client.post('/', data={'content': long_string}, follow_redirects=True)
    assert rv.status_code == 200
    assert long_string.encode() in rv.data

def test_post_sql_injection(client):
    sql_injection_string = "'; DROP TABLE StringRecord; --"
    rv = client.post('/', data={'content': sql_injection_string}, follow_redirects=True)
    assert rv.status_code == 200
    assert b"&#39;; DROP TABLE StringRecord; --" in rv.data
