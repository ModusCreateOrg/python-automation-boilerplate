import random
from datetime import timedelta, datetime

from faker import Faker

# pylint: disable=invalid-name
faker = Faker()


class DataUtils:

    # pylint: disable=no-member
    @staticmethod
    def get_random_name(key):
        # easy way
        # if key == "FIRST_NAME":
        #    return faker.first_name()
        # if key == "LAST_NAME":
        #    return faker.last_name()
        # smart way
        func = getattr(faker, key.lower())
        return func()

    @staticmethod
    def get_random_number(x=1000000, y=9999999):
        return random.randint(x, y)

    @staticmethod
    def get_random_password(length=10):
        return faker.password(length, special_chars=False, digits=True, lower_case=True)

    @staticmethod
    def get_random_incomplete_password(length=7):
        return faker.password(length)

    @staticmethod
    def get_random_letter_password(length=10):
        return faker.password(length, special_chars=False, digits=False)

    @staticmethod
    def get_random_sentence(length=4):
        return faker.sentence(length)

    @staticmethod
    def get_random_text(length=8):
        return faker.text(length)

    @staticmethod
    def get_random_title(max_nb_chars=10):
        return faker.text(max_nb_chars)

    @staticmethod
    def get_random_notebook(folder):
        notebook = random.choice(folder)
        return notebook

    @staticmethod
    def get_random_new_note(button):
        button = random.choice(button)
        return button

    @staticmethod
    def get_random_large_title(min_chars=251, max_chars=255):
        return faker.pystr(min_chars, max_chars)

    @staticmethod
    def get_random_location():
        return faker.city()

    @staticmethod
    def get_random_large_location(min_chars=101, max_chars=105):
        return faker.pystr(min_chars, max_chars)

    @staticmethod
    def get_random_datetime(days=0, hours=1):
        current_datetime = datetime.utcnow() \
                               .replace(minute=0, second=0, microsecond=0) + timedelta(days=days, hours=hours)
        next_datetime_displayed = current_datetime.strftime('Today' + ' ' + '%b %-d %-I:%M %p')
        return next_datetime_displayed

    @staticmethod
    def get_random_recipients(connections, number_of_recipients):
        chosen_recipient = []
        count = 0
        while count < number_of_recipients:
            choice = random.choice(connections)
            if choice not in chosen_recipient:
                chosen_recipient.append(choice)
                count += 1
        return chosen_recipient
