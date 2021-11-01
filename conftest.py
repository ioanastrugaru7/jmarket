import pytest
import os
import tempfile
from market import app, db
from market.modules import User, Item

@pytest.fixture(scope='module')
def n_user():
    user=User(id=1, username='example', email_address='example@example.com', password_hash='poiuyt', budget=600)
    return user

@pytest.fixture(scope='module')
def item_to_buy():
    item=Item(id=2,name='Samsung S21', price=400)
    return item

@pytest.fixture
def test_client():
    
    app.config.update({'TESTING': True})
    with app.test_client() as test_client:
        yield test_client
        
@pytest.fixture()
def attempted_user():
    user=User(id=9, username='alexandra', email_address='alexandra@alexandra.com', password_hash='kkkkkkk', budget=3000)
    return user

@pytest.fixture(scope='module')
def init_database(test_client):
    db.create_all()

    user1=User(id=9, username='alexandra', email_address='alexandra@alexandra.com', password_hash='kkkkkkk', budget=3000)
    user2 = User(id=9, username='alexandra23', email_address='alexandra23@alexandra.com', password_hash='456612', budget=3000)
    db.session.add(user1)
    db.session.add(user2)

    db.session.commit()

    yield  

    db.drop_all()


@pytest.fixture(scope='function')
def login_default_user(test_client):
    test_client.post('/login',
                     data=dict(email='alexandra@alexandra.com', password='kkkkkkk'),
                     follow_redirects=True)

    yield  

    test_client.get('/logout', follow_redirects=True)