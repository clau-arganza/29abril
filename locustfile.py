from locust import HttpUser, task, between


class FactUser(HttpUser):
    wait_time = between(1, 2)

    @task(2)
    def fact_cache_on(self):
        self.client.get("/fact?cache=on", name="/fact cache ON")

    @task(1)
    def fact_cache_off(self):
        self.client.get("/fact?cache=off", name="/fact cache OFF")

    @task(1)
    def health(self):
        self.client.get("/health")