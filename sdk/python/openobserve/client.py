import requests


class OpenObserve:

    def __init__(
        self,
        api_url,
        token,
        application,
        service,
        environment="production"
    ):
        
        if not token:
            raise ValueError(
                "OpenObserve token is required"
            )

        self.api_url = api_url
        self.token = token
        self.application = application
        self.service = service
        self.environment = environment


    def send(
        self,
        level,
        message,
        context=None
    ):

        payload = {
            "application": self.application,
            "service": self.service,
            "level": level,
            "message": message,
            "environment": self.environment,
            "context": context or {}
        }


        headers = {
            "Authorization": f"Bearer {self.token}",
            "Content-Type": "application/json"
        }


        response = requests.post(
            self.api_url,
            json=payload,
            headers=headers,
            timeout=5
        )


        response.raise_for_status()

        return response.json()



    def info(self, message, context=None):
        return self.send(
            "INFO",
            message,
            context
        )


    def warning(self, message, context=None):
        return self.send(
            "WARNING",
            message,
            context
        )


    def error(self, message, context=None):
        return self.send(
            "ERROR",
            message,
            context
        )