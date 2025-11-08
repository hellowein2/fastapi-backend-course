import requests


class CloudFlareClient:
    def __init__(self, api_token, account_id):
        self.api_url = f"https://api.cloudflare.com/client/v4/accounts/{account_id}/ai/run/"
        self.headers = {
            "Authorization": f"Bearer {api_token}",
            "Content-Type": "application/json"
        }
        self.inputs = [
        {"role": "system", "content":
            "Отвечай по-русски, кратко (1–2 предложения),"
            "как лучше выполнить задачу из списка дел. Без приветствий и воды."
            "Отвечай естественно, без вводных фраз вроде «Для выполнения задачи…», «Чтобы сделать…», «Следует…»."
            "Сразу переходи к сути,"
            "Если в задаче есть действие, пиши как"
            " будто даёшь понятную инструкцию или совет, а не академическое объяснение"}
    ]

    def generate_answer(self,task):
        data = {"messages": self.inputs + [{"role": "user", "content": task}]}
        response = requests.post(f"{self.api_url}@cf/meta/llama-3-8b-instruct", headers=self.headers, json=data)


        if response.status_code != 200:
            print("Ошибка запроса:", response.status_code, response.text)
            return None

        result = response.json()
        return result.get("result", {}).get("response", "⚠️ Нет ответа в JSON")