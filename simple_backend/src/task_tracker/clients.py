import requests
from loguru import logger

class CloudFlareClient:

    inputs = [
    {"role": "system", "content":
        "Отвечай по-русски, кратко (1–2 предложения),"
        "как лучше выполнить задачу из списка дел. Без приветствий и воды."
        "Отвечай естественно, без вводных фраз вроде «Для выполнения задачи…», «Чтобы сделать…», «Следует…»."
        "Сразу переходи к сути,"
        "Если в задаче есть действие, пиши как"
        " будто даёшь понятную инструкцию или совет, а не академическое объяснение"} ]

    def __init__(self, api_token, account_id):
        self.api_url = f"https://api.cloudflare.com/client/v4/accounts/{account_id}/ai/run/"
        self.headers = {
            "Authorization": f"Bearer {api_token}",
            "Content-Type": "application/json"
        }


    def generate_answer(self,task):
        data = {"messages": CloudFlareClient.inputs + [{"role": "user", "content": task}]}
        try:
            response = requests.post(f"{self.api_url}@cf/meta/llama-3-8b-instruct", headers=self.headers, json=data)
            response.raise_for_status()
            result = response.json()
            response_text = result["result"]["response"]

            if not response_text:
                raise ValueError("Пустой или некорректный ответ от CloudFlare AI")
            return response_text

        except requests.exceptions.HTTPError as e:
            logger.error(f'Ошибка при запросе к Cloudflare AI: {e}')
            raise
        except requests.exceptions.ConnectionError as e:
            logger.error(f'Ошибка соединения Cloudflare AI: {e}')
            raise