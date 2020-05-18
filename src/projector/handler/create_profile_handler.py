import logging
from random import randint

import requests

from configs.loader import load_config
from projector.handler.base_handler import BaseEventHandler

config = load_config()
logger = logging.getLogger('create_profile_event')


class CreateProfileHandler(BaseEventHandler):
    def do_something(self):
        user_id = self.message.get('user_id')
        if not user_id:
            logger.error(f'Invalid event with message {self.message}')
            return

        response = requests.post(url=f'{config.CREATE_PROFILE_URL}',
                                 json={
                                     'nickname':
                                     'user@' +
                                     str(randint(0, 999999)).zfill(6),
                                     'user_id':
                                     user_id
                                 },
                                 timeout=5)

        if response.status_code == 200:
            payload = response.json()

            # 记录 response
            logger.info(payload)
