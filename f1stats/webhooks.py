import requests
import time
import threading

class Client:
    def __init__(self, callback_url: str):
        self.callback_url: str = callback_url
        self.in_use: bool = True

    def notify_laps(self):
        for i in range(21):
            self.send_webhook({
                "desc": "Current race lap counter",
                "lap": i
            })
            time.sleep(1)
        self.in_use = False

    def send_webhook(self, json):
        return requests.post(
            self.callback_url,
            headers={"Content-Type": "application/json"},
            json=json
        )

class WebhooksManager:
    def __init__(self):
        self._clients: list[Client] = []

    def add_client(self, callback_url: str):
        self._clients.append(Client(callback_url))

        thread = threading.Thread(target=self._clients[-1].notify_laps)
        thread.start()
