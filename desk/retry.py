import time

from llm import ModelError


def call_with_retry(model, messages, system=None, tools=None, retries=2, wait=time.sleep):
    attempt = 0
    while True:
        try:
            return model.chat(messages, system=system, tools=tools)
        except ModelError as error:
            if not error.retryable or attempt >= retries:
                raise
            wait(2 ** attempt)
            attempt = attempt + 1
