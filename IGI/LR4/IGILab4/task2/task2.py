import re
from inputfunctions import inputCheck, TYPES
from zipfile import ZipFile
from task import Task


class FileZipper:
    _zip_name = r'task2\case1.zip'
    _filename = r'task2\case1.txt'

    @property
    def zip_name(self):
        return self._zip_name

    @zip_name.setter
    def zip_name(self, zip_name):
        self._zip_name = zip_name

    @property
    def filename(self):
        return self._filename

    @filename.setter
    def filename(self, filename):
        self._filename = filename

    def zipFile(self):
        with ZipFile(self._zip_name, 'w') as zf:
            zf.write(self._filename)


class TextLoader:
    @staticmethod
    def read_from_file(filename):
        f = None
        try:
            f = open(filename, 'r')
            text = f.read()
            return text
        except Exception as e:
            print('error while working with file:', e)
        finally:
            if f:
                f.close()
        return ''

    @staticmethod
    def write_to_file(text, filename):
        f = None
        try:
            f = open(filename, 'w')
            f.write(text)
        except Exception as e:
            print('error while working with file:', e)
        finally:
            if f:
                f.close()


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
        return self.count_declarative_sentences() + self.count_incentive_sentences() + \
            self.count_interrogative_sentences()

    def count_declarative_sentences(self):
        return len(re.findall(r'\.\W?', self._text))

    def count_interrogative_sentences(self):
        return len(re.findall(r'\?\W?', self._text))

    def count_incentive_sentences(self):
        return len(re.findall(r'!\W?', self._text))

    def calculate_sentence_average_length(self):
        sentences_list = re.split(r'\.\W? |\?\W? |!\W?', self._text)
        word_list = [re.findall(r'\w+', sen) for sen in sentences_list]
        sum_ = 0
        for words in word_list:
            sum_ += sum(len(word) for word in words)
        return sum_/(len(sentences_list) - 1)

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
        email_pattern = re.compile(r'[a-zA-Z0-9]+@[a-zA-Z0-9]+\.?[a-zA-Z]+')
        emails = re.fullmatch(email_pattern, self._text)
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


class Task2(Task):
    @staticmethod
    def perform():
        """function for performing second task"""
        textHandler = TextHandler()
        fileZipper = FileZipper()
        zips = []
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
                    fileZipper.zipFile()

                    if r'task2\case1.zip' not in zips:
                        zips.append(r'task2\case1.zip')
                case 2:
                    string = input("please input string: ")
                    textHandler.text = string
                    result = textHandler.find_words_including_from_g_to_o()
                    print(result)

                    TextLoader.write_to_file(str(result), r'task2\case2.txt')
                    fileZipper.zip_name = r'task2\case2.zip'
                    fileZipper.filename = r'task2\case2.txt'
                    fileZipper.zipFile()

                    if r'task2\case2.zip' not in zips:
                        zips.append(r'task2\case2.zip')
                case 3:
                    email = input("please email address: ")
                    textHandler.text = email
                    result = textHandler.validate_email_address()
                    print(result)

                    TextLoader.write_to_file(str(result), r'task2\case3.txt')
                    fileZipper.zip_name = r'task2\case3.zip'
                    fileZipper.filename = r'task2\case3.txt'
                    fileZipper.zipFile()

                    if r'task2\case3.zip' not in zips:
                        zips.append(r'task2\case3.zip')
                case 4:
                    string = input("please input string: ")
                    textHandler.text = string
                    result = textHandler.calculate_count_of_words_in_string()
                    print(result)

                    TextLoader.write_to_file(str(result), r'task2\case4.txt')
                    fileZipper.zip_name = r'task2\case4.zip'
                    fileZipper.filename = r'task2\case4.txt'
                    fileZipper.zipFile()

                    if r'task2\case4.zip' not in zips:
                        zips.append(r'task2\case4.zip')
                case 5:
                    string = input("please input string: ")
                    textHandler.text = string
                    result = textHandler.find_longest_word_and_position()
                    print(result)

                    TextLoader.write_to_file(str(result), r'task2\case5.txt')
                    fileZipper.zip_name = r'task2\case5.zip'
                    fileZipper.filename = r'task2\case5.txt'
                    fileZipper.zipFile()

                    if r'task2\case5.zip' not in zips:
                        zips.append(r'task2\case5.zip')
                case 6:
                    string = input("please input string: ")
                    textHandler.text = string
                    result = textHandler.find_every_odd_word()
                    print(result)

                    TextLoader.write_to_file(str(result), r'task2\case6.txt')
                    fileZipper.zip_name = r'task2\case6.zip'
                    fileZipper.filename = r'task2\case6.txt'
                    fileZipper.zipFile()

                    if r'task2\case6.zip' not in zips:
                        zips.append(r'task2\case6.zip')
                case 0:
                    break
                case _:
                    print('please choose from 0 to 6:')
                    continue

        for zip_ in zips:
            print(zip_ + ':')
            with ZipFile(zip_, 'r') as zp:
                for item in zp.infolist():
                    print(f'filename: {item.filename}, date: {item.date_time}, size: {item.file_size}')
