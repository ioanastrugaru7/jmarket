


def test_user_login_route(test_client):
    response = test_client.get('/login')
    assert response.status_code == 200
    assert b'Login' in response.data
    assert b'Email' in response.data
    assert b'Password' in response.data


# def test_valid_login_logout(test_client, init_database):
    
#     response = test_client.post('/login',
#                                 data=dict(email='alexandra@alexandra.com', password='kkkkkkk'),
#                                 follow_redirects=True)
#     assert response.status_code == 200
#     assert b'Login successful! Welcome alexandra@alexandra.com!' in response.data
    
#     assert b'Logout successful' in response.data
#     assert b'Incorrect username or password, please try again' not in response.data


def test_user_login_route(test_client):
    response = test_client.post ('/login')
    assert response.status_code == 200

def test_user_register_route(test_client):
    response = test_client.get('/register')
    assert response.status_code == 200
  
def test_user_register_route_2(test_client):
    response = test_client.post('/register')
    assert response.status_code == 200

def test_user_logout_route(test_client):
    response = test_client.get('/logout')
    assert response.status_code == 302

def test_user_market_route(test_client):
    response = test_client.get('/market')
    assert response.status_code == 302

def test_user_market_route_2(test_client):
    response = test_client.post('/market')
    assert response.status_code == 302