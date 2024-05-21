

import argparse
import sys
import os
import random
import subprocess
from datetime import datetime
from typing import List, Union
import gradio as gr
import numpy as np
from gradio.components import Textbox, Video, Image
from openai import OpenAI
client = OpenAI(api_key="sk-proj-2bukD0FHxc5cMV1KaW90T3BlbkFJ6nfZBZlPJc9SnImkUysE")

# The main workflow for the server
def generate_testcase(user_code, user_test_case):
    # take the prompt and test case as input from the user
    #TODO subtask 1: use the current test case and code to generate a test coverage report, store it as pred_coverage_report
    # pred_coverage_report = subprocess.run("some command to get coverage")
    pred_coverage_report = "Test coverage 80%"

    #TODO subtask 2: organize the user input into reasonable llm prompt as following format
    #code = {1: 'from dataclasses import dataclass', 2: '', 3: '@dataclass()', 4: 'class Product:', 5: '', 6: '    id: int', 7: '    name: str', 8: '    price: float', 9: '    stock: int', 10: '', 11: '    def increase_stock(self, stock_to_add: int):', 12: '        self.check_positive_number(stock_to_add)', 13: '        self.stock: int = self.stock + stock_to_add', 14: '', 15: '    def decrease_stock(self, stock_to_reduce):', 16: '        self.check_positive_number(stock_to_reduce)', 17: '        new_stock = self.stock - stock_to_reduce', 18: '        self.check_negative_stock(new_stock)', 19: '        self.stock = self.stock - stock_to_reduce', 20: '', 21: '    def check_positive_number(self, value):', 22: '        if value <= 0:', 23: '            raise Exception("Number must be positive")', 24: '', 25: '    def check_negative_stock(self, value):', 26: '        if value < 0:', 27: '            raise Exception("Stock must be greater than or equal to 0")', 28: ''}

    gpt_prompt = "Given the following code, and existing test cases, generate more comprehensive test cases, make sure the test cases are valid, try to increase test code coverage. Only respond with code, do not return explanation. The returned cpde should be valid Python code starting with code: from main import Product from dataclasses import is_dataclass import pytest @pytest.fixture def product(): return Product(1, 'foo', 1.0, 10) def test_constructor(product): assert product.id == 1 assert product.name == 'foo'"
    #message=[{"role": "system", "content": "You are a helpful programmer writing test.py."},{"role": "assistant", "content": gpt_prompt + "\n" + "\n".join(code.values()) + user_test_case}]
    message=[{"role": "system", "content": "You are a helpful programmer writing test.py."},{"role": "assistant", "content": gpt_prompt + "\n" + "user's code: " + user_code + "existing test cases: " + user_test_case}]

    response = client.chat.completions.create(
        model="gpt-4o",
        messages = message,
    )
    #TODO subtask 3: after receive the feedback from llm, organize it into a human readable output format, as responseText shown to user
    responseText = response.choices[0].message.content
    # get rid of the first 10 characters and the last 3 characters
    responseText = responseText[10:]
    responseText = responseText[:-3]
    responseText
    
    #TODO subtask 4: after receive the feedback from llm, organize it into a machine processable format and use model to check the updated test case coverage, store as succ_coverage_report
    # succ_coverage_report = subprocess.run("some command to get coverage")
    succ_coverage_report = "Test coverage 80%"
    #TODO subtask 5: highlight the output shown in the UI to tell the user what difference we made. (new test we added, previous test case we modified, test coverage changes)
    return responseText, pred_coverage_report, succ_coverage_report

if __name__ == '__main__':

    demo = gr.Interface(
        fn=generate_testcase,
        inputs=[Textbox(label="Enter you coder",
                        placeholder="Please enter your code. \n"),
                Textbox(label="Enter you test case",
                        placeholder="Please enter your test case. \n"),
                ],
        outputs=[
                #  Video(label="Vid", width=512, height=512),
                 Textbox(label="generated test cases"),
                 Textbox(label="report for previoustest case coverage"),
                 Textbox(label="report for new test case coverage"),
                #  gr.Slider(label='seed')
                 ],
        # title=title_markdown, description=DESCRIPTION, theme=gr.themes.Default(), css=block_css,
        # examples=examples,
    )
    demo.launch()