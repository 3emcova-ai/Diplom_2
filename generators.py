import random

from datetime import datetime, timedelta
from faker import Faker


fake = Faker()

# Генераторы для курьера
def login_generator():
    return fake.user_name()

def password_generator():
    return fake.password()

def firstname_generator():
    return fake.first_name()

# Генераторы для заказа
def lastname_generator():
    return fake.last_name()

def address_generator():
    return fake.address()

def metro_station_generator():
    return random.randint(1, 30)

def phone_generator():
    return fake.phone_number()

def rent_time_generator():
    return random.randint(1, 3)

def delivery_date_generator():
    tomorrow = datetime.now().date() + timedelta(days=1)
    return fake.date_between(start_date=tomorrow, end_date=tomorrow).strftime('%Y-%m-%d')
 
def comment_generator():
    return fake.sentence()
