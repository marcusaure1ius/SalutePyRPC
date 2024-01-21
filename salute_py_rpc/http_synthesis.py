import os.path
import wave
import requests
from utils import Session

SAMPLE_TEXT = """Это очень маленький текст"""

session = Session()
token = session.get_or_refresh_access_token()


def request_synthesis(input_text, access_token):
    BASE_URL = 'https://smartspeech.sber.ru/rest/v1/text:synthesize'
    resp = requests.post(
        BASE_URL,
        headers={
            'Authorization': f'Bearer {access_token}',
            'Content-Type': 'application/text'
        },
        params={
            'format': 'wav16',
            'voice': 'Bys_24000'
        },
        data=input_text.encode(),
        stream=False,
        verify=os.path.abspath('../russiantrustedca.pem')
    )
    output = b''
    for chunk in resp.iter_content(None):
        output += chunk

    with wave.open("../sound.wav", "wb") as wf:
        wf.setnchannels(1)
        wf.setsampwidth(2)
        wf.setframerate(24000)
        wf.writeframesraw(output)

request_synthesis(SAMPLE_TEXT, token)