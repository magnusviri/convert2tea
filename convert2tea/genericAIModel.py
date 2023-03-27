# -*- coding: utf-8 -*-

"""
"""

__author__ = "James Reynolds"
__email__ = "magnusviri@me.edu"
__copyright__ = ""
__license__ = "MIT"
__version__ = "0.0.1"

import openai
import os


class OpenAIModel:
    def __init__(self, specific):
        openai.api_key = os.getenv("OPENAI_API_KEY")
        self.model_name = specific

    def query(self, prompt):
        if self.model_name == "gpt-3.5-turbo-0301":
            completion = openai.ChatCompletion.create(
                model="gpt-3.5-turbo-0301",
                messages=[{"role": "user", "content": prompt}],
            )
            self.result = completion.choices[0].message.content

        elif self.model_name == "text-davinci-003":
            completion = openai.Completion.create(
                prompt=prompt,
                engine="text-davinci-003",
                temperature=0.7,
                max_tokens=709,
                top_p=1,
                frequency_penalty=0,
                presence_penalty=0,
            )
            self.result = response.choices[0].text

        return self.result


class GenericAIModel:
    def __init__(self, name, specific):
        if name == "openai":
            self.model = OpenAIModel(specific)

    def query(self, prompt):
        return self.model.query(prompt)
