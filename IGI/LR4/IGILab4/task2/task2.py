import re
from inputfunctions import inputCheck, TYPES


class TextLoader:
    @staticmethod
    def read_from_file(filename):
        f = open(filename, 'r')
        text = f.read()
        f.close()
        return text

    @staticmethod
    def write_to_file(text, filename):
        f = open(filename, 'w')
        f.write(text)
        f.close()
        return


class TextHandler:
    def __init__(self, text: str = ''):
        self._text = text

    @property
    def text(self):
        return self._text

    @text.setter
    def text(self, someText):
        self._text = someText

    def count_sentences(self):
        return self._text.count('.') + self._text.count('!') + self._text.count('?')

    def count_declarative_sentences(self):
        return self._text.count('.')

    def count_interrogative_sentences(self):
        return self._text.count('?')

    def count_incentive_sentences(self):
        return self._text.count('!')

    def calculate_sentence_average_length(self):
        sentences_list = re.split(r'\. |\? |!', self._text)
        sentences_list = sentences_list[:len(sentences_list) - 1:]
        word_list = [re.findall(r'\w+', sen) for sen in sentences_list]
        sum_ = 0
        for words in word_list:
            sum_ += sum(len(word) for word in words)
        return sum_/(len(word_list))

    def calculate_word_average_length(self):
        words_list = re.findall(r'\w+', self._text)
        sum_ = 0
        for word in words_list:
            sum_ += len(word)
        return sum_/(len(words_list))

    def calculate_smiles_count(self):
        smile_pattern = re.compile(r'[;:]-*[()\[\]]+')
        smiles = re.findall(smile_pattern, self._text)
        return len(smiles)

    def find_words_including_from_g_to_o(self):
        words_list = re.findall(r'\w+', self._text)
        matching_words = ([re.findall(r'\w*[g-o]\w*', word) for word in words_list])
        return [matching_word for matching_word in matching_words if matching_word != []]

    def validate_email_address(self):
        email_pattern = re.compile(r'\w+@[A-Za-z.]+')
        emails = re.match(email_pattern, self._text)
        return True if emails else False

    def calculate_count_of_words_in_string(self):
        words_list = re.findall(r'\w+', self._text)
        return len(words_list)

    def find_longest_word_and_position(self):
        words_list = re.findall(r'\w+', self._text)
        max_len_word = max(words_list, key=len)
        return max_len_word, words_list.index(max_len_word) + 1

    def find_every_odd_word(self):
        words_list = re.findall(r'\w+', self._text)
        return [word for word in words_list if (words_list.index(word) + 1) % 2]

class Task2:
    @staticmethod
    def perform():
        textHandler = TextHandler()
        while True:
            choice = inputCheck('Please, choose option:\n'
                                '1: general task performing\n'
                                '2: printing all words in string, that include symbols, laying in g-o range\n'
                                '3: email address validator\n'
                                '4: calculating count of words in string\n'
                                '5: finding the longest word in string and it number\n'
                                '6: printing every odd word in string\n'
                                '0: exit\n', TYPES.INT)

            match choice:
                case 1:
                    textLoader = TextLoader()
                    text = textLoader.read_from_file(r'task2\input.txt')
                    textHandler.text = text
                    result = ''

                    print(f'count of sentences: {textHandler.count_sentences()}')
                    result += str(textHandler.count_sentences())

                    print(f'count of declarative sentences: {textHandler.count_declarative_sentences()}')
                    result += '\n' + str(textHandler.count_declarative_sentences())

                    print(f'count of interrogative sentences: {textHandler.count_interrogative_sentences()}')
                    result += '\n' + str(textHandler.count_interrogative_sentences())

                    print(f'count of incentive sentences: {textHandler.count_incentive_sentences()}')
                    result += '\n' + str(textHandler.count_incentive_sentences())

                    print(f'average sentence length: {textHandler.calculate_sentence_average_length()}')
                    result += '\n' + str(textHandler.calculate_sentence_average_length())

                    print(f'average word length: {textHandler.calculate_word_average_length()}')
                    result += '\n' + str(textHandler.calculate_word_average_length())

                    print(f'count of smiles: {textHandler.calculate_smiles_count()}')
                    result += '\n' + str(textHandler.calculate_smiles_count())

                    textLoader.write_to_file(result, r'task2\case1.txt')
                case 2:
                    string = input("please input string: ")
                    textHandler.text = string
                    result = textHandler.find_words_including_from_g_to_o()
                    print(result)
                    TextLoader.write_to_file(str(result), r'task2\case2.txt')
                case 3:
                    email = input("please email address: ")
                    textHandler.text = email
                    result = textHandler.validate_email_address()
                    print(result)
                    TextLoader.write_to_file(str(result), r'task2\case3.txt')
                case 4:
                    string = input("please input string: ")
                    textHandler.text = string
                    result = textHandler.calculate_count_of_words_in_string()
                    print(result)
                    TextLoader.write_to_file(str(result), r'task2\case4.txt')
                case 5:
                    string = input("please input string: ")
                    textHandler.text = string
                    result = textHandler.find_longest_word_and_position()
                    print(result)
                    TextLoader.write_to_file(str(result), r'task2\case5.txt')
                case 6:
                    string = input("please input string: ")
                    textHandler.text = string
                    result = textHandler.find_every_odd_word()
                    print(result)
                    TextLoader.write_to_file(str(result), r'task2\case6.txt')
                case 0:
                    break
                case _:
                    print('please choose from 0 to 6:')
                    continue