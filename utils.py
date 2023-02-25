import hashlib
import os

from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import StatesGroup, State
from bs4 import BeautifulSoup


def hash_password(password):
    salt = os.urandom(32)
    encoded_password = password.encode('utf-8')
    password_hash = hashlib.sha256(salt + encoded_password).hexdigest()
    return password_hash, salt


def check_password(password, password_hash, salt):
    encoded_password = password.encode('utf-8')
    hash_result = hashlib.sha256(salt + encoded_password).hexdigest()
    return hash_result == password_hash


storage = MemoryStorage()


class FBCredentialsStatesGroup(StatesGroup):
    login = State()
    password = State()
    proxy = State()


class InspectFBResponse:

    def __init__(self, raw_response):
        self.response = BeautifulSoup(raw_response, 'lxml')
        self.resp = raw_response

    def find_login_url(self):
        next_url = self.response.find(
            'div', class_='__sw __sz __t3 __ta'
        ).find('a').get('href')
        return next_url

    def find_login_form(self):
        next_url = self.response.find('a', class_='_sv4').get('href')
        return next_url
