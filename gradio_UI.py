

import argparse
import sys
import os
import random
import subprocess
import re
from datetime import datetime
from typing import List, Union
import gradio as gr
import numpy as np
from gradio.components import Textbox, Video, Image, HTML
from openai import OpenAI
import difflib
import coverage
client = OpenAI(api_key="sk-proj-2bukD0FHxc5cMV1KaW90T3BlbkFJ6nfZBZlPJc9SnImkUysE")

def get_code_coverage(code, test_case):
    # Create directory tmp, main.py and test_main.py 
    if not os.path.exists('tmp'):
        os.makedirs('tmp')
    if os.path.exists('tmp/main.py'):
        os.remove('tmp/main.py')
    if os.path.exists('tmp/test_main.py'):
        os.remove('tmp/test_main.py')

    # Write code to main.py
    with open('tmp/main.py', 'w') as f:
        for line in code.values():
            f.write(line + '\n')
    with open('tmp/test_main.py', 'w') as f:
        for line in test_case.values():
            f.write(line + '\n')
    
    # Run coverage
    os.system('coverage run -m pytest tmp/test_main.py')
    os.system('coverage report -m > tmp/coverage_report.txt')
    cov = coverage.Coverage()
    cov.load()
    coverage_percentage = 100 - 100 * (len(cov.analysis('tmp/main.py')[2]) / len(cov.analysis('tmp/main.py')[1]))
    return str(round(coverage_percentage, 2)) + '%'

def extract_code_from_response(response):
    pattern = r"```python(.*?)```"
    code = re.findall(pattern, response, re.DOTALL)
    return code[0]

def read_file_as_string(file_path):
        with open(file_path, 'r') as file:
            return file.read()
        

# Highlight Differences
def highlight_differences(text1, text2):
    text1_lines = text1.splitlines(keepends=True)
    text2_lines = text2.splitlines(keepends=True)
    differ = difflib.Differ()
    diff = list(differ.compare(text1_lines, text2_lines))

    # <pre> for formatting
    highlighted_diff = ['<pre style="font-family: monospace; white-space: pre-wrap;">']
    for line in diff:
        sanitized_line = line[2:].replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;').replace(' ', '&nbsp;')
        if line.startswith('+ '):
            highlighted_diff.append(f'<div style="background-color: rgba(0, 255, 0, 0.2);">{sanitized_line}</div>')
        elif line.startswith('- '):
            highlighted_diff.append(f'<div style="background-color: rgba(255, 0, 0, 0.2);">{sanitized_line}</div>')
        else:
            highlighted_diff.append(f'<div>{sanitized_line}</div>')
    highlighted_diff.append('</pre>')

    return ''.join(highlighted_diff)

# Generate Prompt
def generate_prompt(user_code, user_test_cases, coverage_report):
    """Generate the model prompt based on user input and coverage report."""
    prompt = f"""
    Given the following code, existing test cases, and coverage report on lines missing test coverage,
    generate more test cases to obtain more test coverage. Only respond with valid Python code that can be appended to the test cases.

    Code:
    {user_code}

    Existing Test Cases:
    {user_test_cases}

    Missing Lines from Coverage Report:
    {coverage_report}
    """
    return prompt

# The main workflow for the server
def generate_testcase(user_code, user_test_case):

    # FIXME: comment these part out for live input
    # file_user_code_path = 'main.py'
    # file_user_code_content = read_file_as_string(file_user_code_path)
    # file_user_test_case_path = 'base_test.py'
    # file_user_test_case_content = read_file_as_string(file_user_test_case_path)
    # user_code = file_user_code_content
    # user_test_case = file_user_test_case_content

    # take the prompt and test case as input from the user

    #TODO subtask 2: organize the user input into reasonable llm prompt as following format
    code = {1: 'from dataclasses import dataclass', 2: '', 3: '@dataclass()', 4: 'class Product:', 5: '', 6: '    id: int', 7: '    name: str', 8: '    price: float', 9: '    stock: int', 10: '', 11: '    def increase_stock(self, stock_to_add: int):', 12: '        self.check_positive_number(stock_to_add)', 13: '        self.stock: int = self.stock + stock_to_add', 14: '', 15: '    def decrease_stock(self, stock_to_reduce):', 16: '        self.check_positive_number(stock_to_reduce)', 17: '        new_stock = self.stock - stock_to_reduce', 18: '        self.check_negative_stock(new_stock)', 19: '        self.stock = self.stock - stock_to_reduce', 20: '', 21: '    def check_positive_number(self, value):', 22: '        if value <= 0:', 23: '            raise Exception("Number must be positive")', 24: '', 25: '    def check_negative_stock(self, value):', 26: '        if value < 0:', 27: '            raise Exception("Stock must be greater than or equal to 0")', 28: ''}
    test_code = {1: 'from main import Product', 2: 'from dataclasses import is_dataclass', 3: 'import pytest', 4: '', 5: 'def test_if_it_is_a_dataclass():', 6: '    assert is_dataclass(Product) == True', 7: '', 8: '', 9: '@pytest.fixture', 10: 'def product():', 11: "    return Product(1, 'foo', 1.0, 10)", 12: '', 13: '', 14: 'def test_constructor(product):', 15: '    assert product.id == 1', 16: "    assert product.name == 'foo'", 17: '    assert product.price == 1.0', 18: '    assert product.stock == 10', 19: '', 20: '', 21: 'def test_increase_stock(product):', 22: '    product.increase_stock(10)', 23: '    assert product.stock == 20'}
    missing_lines = {16: '        self.check_positive_number(stock_to_reduce)', 17: '        new_stock = self.stock - stock_to_reduce', 18: '        self.check_negative_stock(new_stock)', 19: '        self.stock = self.stock - stock_to_reduce', 23: '            raise Exception("Number must be positive")', 26: '        if value < 0:', 27: '            raise Exception("Stock must be greater than or equal to 0")'}
    code_txt = "\n".join(code.values())
    test_code_txt = "\n".join(test_code.values())
    missing_lines_txt = "\n".join(missing_lines.values())
    #TODO subtask 1: use the current test case and code to generate a test coverage report, store it as pred_coverage_report
    # pred_coverage_report = subprocess.run("some command to get coverage")
    pred_coverage_report = get_code_coverage(code, test_code)


    gpt_prompt = "Given the following code, existing test cases, and lines missing test coverage, generate more test cases. Make sure the test cases are valid and increase test coverage. Only respond with valid Python code, do not return explanation."

    #gpt_prompt = "Given the following code, and existing test cases, generate more comprehensive test cases, make sure the test cases are valid, try to increase test code coverage. Only respond with code, do not return explanation. The returned cpde should be valid Python code starting with code: from main import Product from dataclasses import is_dataclass import pytest @pytest.fixture def product(): return Product(1, 'foo', 1.0, 10) def test_constructor(product): assert product.id == 1 assert product.name == 'foo'"
    #message=[{"role": "system", "content": "You are a helpful programmer writing test.py."},{"role": "assistant", "content": gpt_prompt + "\n" + "\n".join(code.values()) + user_test_case}]
    message=[{"role": "system", "content": "You are a helpful programmer writing test.py."},{"role": "assistant", "content": gpt_prompt + "\n" + "the code: " + code_txt + "existing test cases: " + test_code_txt + "lines missing test coverage: " + missing_lines_txt}]

    # temporarily commented out
    #gpt_prompt = generate_prompt(user_code, user_test_case, pred_coverage_report)
    #message=[{"role": "system", "content": "You are a helpful programmer writing test.py."},{"role": "assistant", "content": gpt_prompt}]


    response = client.chat.completions.create(
        model="gpt-4o",
        messages = message,
    )
    #TODO subtask 3: after receive the feedback from llm, organize it into a human readable output format, as responseText shown to user
    responseText = extract_code_from_response(response.choices[0].message.content)
    generated_code = {}
    for i, line in enumerate(responseText.split("\n"), 1):
        generated_code[i] = line
    
    #TODO subtask 4: after receive the feedback from llm, organize it into a machine processable format and use model to check the updated test case coverage, store as succ_coverage_report
    # succ_coverage_report = subprocess.run("some command to get coverage")
    succ_coverage_report = get_code_coverage(code, generated_code)
    #TODO subtask 5: highlight the output shown in the UI to tell the user what difference we made. (new test we added, previous test case we modified, test coverage changes)
    responseText = highlight_differences(test_code_txt, responseText)
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
                 HTML(label="generated test cases"),
                 Textbox(label="report for previoustest case coverage"),
                 Textbox(label="report for new test case coverage"),
                #  gr.Slider(label='seed')
                 ],
        # title=title_markdown, description=DESCRIPTION, theme=gr.themes.Default(), css=block_css,
        # examples=examples,
    )
    demo.launch()