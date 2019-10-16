import string
import random
from functools import partial
from os import path
from PyInquirer import prompt, style_from_dict, Token, Validator, ValidationError

STYLE_SHEET_CHECKBOX = style_from_dict({
    Token.Separator: '#6C6C6C',
    Token.QuestionMark: '#FF9D00 bold',
    #Token.Selected: '',
    Token.Selected: '#5F819D',
    Token.Pointer: '#FF9D00',
    Token.Instruction: '',
    Token.Answer: '#5F819D bold',
    Token.Question: '',
})

PASSWORDS_NUM = 10
PASSWORDS_FILENAME = 'passwords.txt'


class IntNumberValidator(Validator):
    def validate(self, document):
        if not document.text.isdigit():
            raise ValidationError(
                message='Enter valid number 1 - 100',
                cursor_position=len(document.text)
            )
        elif int(document.text)<1:
            raise ValidationError(
                message='Enter valid number 1 - 100',
                cursor_position=len(document.text)
            )


def symbols_request():
    questions = [
        {
            'type': 'checkbox',
            'qmark': '>>>>',
            'message': 'Select password symbols',
            'name': 'symbols',
            'choices': [
                {
                    'name': 'lower case symbols',
                    'checked': True
                },
                {
                    'name': 'UPPER case symbols',
                    'checked': True
                },
                {
                    'name': 'punctuations symbols',
                    'checked': True
                },
                {
                    'name': 'numbers symbols',
                    'checked': True
                },
            ],
        }
    ]
    answers = prompt(questions, style=STYLE_SHEET_CHECKBOX)
    return answers


def generate_pass_symbols(answer_list: list):
    symbols = ''
    if 'lower case symbols' in answer_list:
        symbols += string.ascii_lowercase
    if 'UPPER case symbols' in answer_list:
        symbols += string.ascii_uppercase
    if 'punctuations symbols' in answer_list:
        symbols += string.punctuation
    if 'numbers symbols' in answer_list:
        symbols += string.digits
    return symbols


def pass_lenght_request():
    questions = [
        {
            'type': 'input',
            'name': 'length',
            'message': 'Password length',
            'default': '8',
            'validate': IntNumberValidator
        }
    ]
    answers = prompt(questions, style=STYLE_SHEET_CHECKBOX)
    return answers


def generate_pass(symbols_list, pass_len, passwords_num=PASSWORDS_NUM):
    some_symbol = partial(random.choice, symbols_list)
    passwords = [''.join([some_symbol() for _ in range(pass_len)]) for _ in range(passwords_num)]
    return passwords


def pass_save_request(passwords):
    questions = [
         {
            'type': 'list',
            'name': 'password',
            'message': 'Select password to save',
            'choices': passwords,
         }
    ]

    answers = prompt(questions, style=STYLE_SHEET_CHECKBOX)
    return answers


def add_password_to_file(password, filename=PASSWORDS_FILENAME):
    with open(filename, 'a') as f:
        f.write(f"{password}\n")
    print(f'password saved to {path.abspath(filename)}')


def entrypoint():
    symbols_answer_list = []
    while not symbols_answer_list:
        symbols_answer_list = symbols_request()['symbols']
        if not symbols_answer_list:
            print('You most check one more')
    symbols = generate_pass_symbols(symbols_answer_list)
    pass_len = int(pass_lenght_request()['length'])
    passwords = generate_pass(symbols, pass_len)
    password_to_save = pass_save_request(passwords)['password']
    add_password_to_file(password_to_save)


if __name__ == '__main__':
    entrypoint()
