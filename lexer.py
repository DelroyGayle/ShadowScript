from tokens import Integer, Float, Operation, Declaration
from tokens import Variable, Boolean, Comparison, Reserved
import string

"""
Error handling
"""


class Error:
    def __init__(self, error_name, error_details):
        self.error_name = error_name
        self.error_details = error_details

    def str(self):
        string_result = f'{self.error_name}: {self:error_details}'
        return string_result


class Lexer:
    # Instead of digits = "0123456789" use:
    digits = string.digits
    # Instead of letters = "abcdefghijklmnopqrstuvwxyz" use:
    letters = string.ascii_lowercase
    operations = '+-/*()='
    stopwords = [' ']
    declarations = ['make']
    boolean = ['and', 'or', 'not']
    comparisons = ['>', '<', '>=', '<=', '?=']
    specialCharacters = '><=?'
    reserved = ['if', 'elif', 'else', 'do', 'while']

    def __init__(self, text):
        self.text = text
        self.idx = 0
        self.tokens = []
        self.char = self.text[self.idx]
        self.token = None

    def tokenize(self):
        while self.idx < len(self.text):
            if self.char in Lexer.digits:
                self.token = self.extract_number()

            elif self.char in Lexer.operations:
                self.token = Operation(self.char)
                self.move()

            elif self.char in Lexer.stopwords:
                self.move()
                continue

            elif self.char in Lexer.letters:
                word = self.extract_word()

                if word in Lexer.declarations:
                    self.token = Declaration(word)
                elif word in Lexer.boolean:
                    self.token = Boolean(word)
                elif word in Lexer.reserved:
                    self.token = Reserved(word)
                else:
                    self.token = Variable(word)

            elif self.char in Lexer.specialCharacters:
                comparisonOperator = ''
                while (self.char in Lexer.specialCharacters and
                       self.idx < len(self.text)):
                    comparisonOperator += self.char
                    self.move()

                self.token = Comparison(comparisonOperator)

            self.tokens.append(self.token)

        return self.tokens

    def extract_number(self):
        number = ''
        is_float = False
        while ((self.char in Lexer.digits or self.char == '.') and
               (self.idx < len(self.text))):
            if self.char == '.':
                is_float = True
            number += self.char
            self.move()

        return Integer(number) if not is_float else Float(number)

    def extract_word(self):
        word = ''
        while self.char in Lexer.letters and self.idx < len(self.text):
            word += self.char
            self.move()

        return word

    def move(self):
        self.idx += 1
        if self.idx < len(self.text):
            self.char = self.text[self.idx]
