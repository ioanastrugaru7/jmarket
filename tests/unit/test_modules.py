from flask_login import current_user
from flask_wtf import form
from conftest import item_to_buy, n_user

from market.modules import User
import unittest

def test_can_purchase(n_user, item_to_buy):
    assert n_user.can_purchase(item_to_buy) == True


# def test_can_sell(n_user, item_to_buy):
#     item_to_buy.buy(n_user)
#     assert n_user.can_sell(item_to_buy) == True

def test_new_user(n_user):
    assert n_user.username == 'example'
    assert n_user.email_address == 'example@example.com'
    assert n_user.password_hash == 'poiuyt'
  
#Login password has to be equal to the password assigned for the user
def test_check_password(n_user):
    n_user.attempted_password='marvel'
    n_user.correct_password = 'poiuyt'
    assert n_user.password_hash != n_user.attempted_password
    assert n_user.password_hash == n_user.correct_password
