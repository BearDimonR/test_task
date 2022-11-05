# -*- coding: utf-8 -*-
"""
Created on Mon Mar 21 12:59:51 2022

@author: Okhrimchuk Roman & Maksym Veremchuk
for Sierentz Global Merchants


Test task
"""
import re

def lucky(series_sequence):
    match = re.findall(r'6+5+[56]*|5+6+[56]*', series_sequence)
    return max(match) if len(match) > 0 else 0

tests = [
    ('5656556565', '5656556565'),
    ('4556432455665334', '55665'),
    ('55555', 0),
    ('666', 0),
    ('656655565', '656655565')
]

for input_sq, output_sq in tests:
    result = lucky(input_sq)
    string_to_print = f'input_sq: {input_sq}, output_sq: {output_sq}, result: {result}'
    print(string_to_print)
    assert result == output_sq, string_to_print