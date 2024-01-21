import datetime
import requests
import uuid
import os
from dotenv import set_key, load_dotenv


class Session:
    load_dotenv()
    oauth_url = 'https://ngw.devices.sberbank.ru:9443/api/v2/oauth'
    auth_data = os.environ.get('AUTH_DATA')

    def __get_current_auth_values(self):
        access_token = os.environ.get('access_token')
        token_expires_timestamp = os.environ.get('expires_at')

        return access_token, token_expires_timestamp

    def __get_request_uuid(self):
        request_uuid = f'{uuid.uuid4()}'

        return request_uuid

    def __refresh_access_token(self):
        request = requests.post(
            self.oauth_url,
            headers={
                'Authorization': self.auth_data,
                'RqUID': self.__get_request_uuid(),
                'Content-Type': 'application/x-www-form-urlencoded'
            },
            data={
                'scope': 'SALUTE_SPEECH_PERS'
            },
            verify='russiantrustedca.pem'
        )

        json_response = request.json()
        access_token = json_response['access_token']
        expires_at = json_response['expires_at']

        set_key(dotenv_path='.env', key_to_set='access_token', value_to_set=access_token)
        set_key(dotenv_path='.env', key_to_set='expires_at', value_to_set=expires_at, quote_mode="never")

        return access_token

    def get_or_refresh_access_token(self):
        access_token, token_expires_timestamp = self.__get_current_auth_values()

        token_timestamp = int(token_expires_timestamp)
        current_timestamp = datetime.datetime.now().timestamp() * 1000
        delta = token_timestamp - current_timestamp

        if delta > 0:
            new_access_token = self.__refresh_access_token()
            return new_access_token
        else:
            return access_token
