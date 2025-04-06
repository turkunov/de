from faker import Faker
import random
import time
import requests
import logging


logger = logging.getLogger(__name__)


def gen_metadata() -> dict:
    is_male = bool(random.randint(0, 1))
    dummy_generator = Faker()
    return {
        'gender': 'male' if is_male else 'female',
        'name': dummy_generator.first_name_male() if is_male else \
            dummy_generator.first_name_female(),
        'surname': dummy_generator.last_name()
    }


def gen_image(gender: str) -> dict:
    curtime = int(time.time() * 1000.0)
    payload = {
        'time': curtime,
        'gender': gender,
        'age': 'all', 'ethnic': 'all'
    }
    img_url = ''
    try:
        res = requests.get('https://this-person-does-not-exist.com/new',params=payload).json()
        if res:
            if 'name' in res.keys():
                img_url = f"https://this-person-does-not-exist.com/img/{res['name']}"
    except Exception as e:
        logger.info(f'Encountered error in `gen_image`: {e}')
    return img_url