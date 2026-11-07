from faker import Faker


fake = Faker()

# Генераторы для пользователя
def email_generator():
    return fake.email()

def password_generator():
    return fake.password()

def name_generator():
    return fake.name()
