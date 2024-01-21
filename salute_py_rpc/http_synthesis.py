import wave
import requests
from utils import Session

SAMPLE_TEXT = """ПСБ предоставил частным инвесторам новый сервис «Фундаментальные показатели эмитентов» для оценки потенциальной эффективности инструментов фондового рынка. 

Сервис отражает мультипликаторы и финансовые показатели компаний и позволяет инвестору использовать метод фундаментального анализа при принятии инвестиционных решений.

Чтобы воспользоваться сервисом в приложении «ПСБ Инвестиции», достаточно выбрать интересующую ценную бумагу эмитента и перейти в раздел «Показатели». В разделе отображаются более 25 важнейших индикаторов по эмитентам, таких как выручка, чистая прибыль, долговая нагрузка, капитализация, доля акций в свободном обращении, влияние биржевых индексов на динамику стоимости ценных бумаг и др. Также клиент может отслеживать изменение индикаторов и сравнивать их с аналогичными показателями других компаний."""

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
        verify='../russiantrustedca.pem'
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
