import re
import os
import codecs

STOP_WORDS = ["a","able","about","across","after","all","almost","also","am","among","an","and","any","are","as","at","be","because","been","but","by","can","cannot","could","dear","did","do","does","either","else","ever","every","for","from","get","got","had","has","have","he","her","hers","him","his","how","however","i","if","in","into","is","it","its","just","least","let","like","likely","may","me","might","miss", "most","mr","must","my","neither","no","nor","not","of","off","often","on","only","or","other","our","own","rather","said","say","says","she","should","since","so","some","than","that","the","their","them","then","there","these","they","this","tis","to","too","twas","us","wants","was","we","were","what","when","where","which","while","who","whom","why","will","with","would","yet","you","your"]
PUNCTUATION_MARKS = [".",",","!","?","(",")",":","\"","\t","-","[","]","{","}","\'","\r","\\"]
NUMBERS =["0","1","2","3","4","5","6","7","8","9"]
APOSTROPHE = ["’","\'"]
NEW_LINE = "\n"

class Parser:
    def __init__(self):
        self.titles = []
        self.books = []
        self.parsered_books = []
        self.books_dictionary = []

# wczytanie książek które są w katalogu books, w ścieżce projektu
    def read_books(self):
        path_to_books =os.getcwd()+"\\books"
        self.titles = os.listdir(path_to_books)
        for title in self.titles:
            book = codecs.open(path_to_books+"\\"+title, "r", "utf-8-sig")
            self.books.append(book.read())


# przetwarzanie poszczególnej książki
    def parse_book(self, book, num):
        # zmiana liter na małe
        parsed_book = book.lower()
        # usunięcie cyfr
        for number in NUMBERS: parsed_book = parsed_book.replace(number, "")
        # usunięcie znaków interpunkcyjnych
        for mark in PUNCTUATION_MARKS : parsed_book = parsed_book.replace(mark, " ")
        # zamiana nowej lini na znaki białe (spacje)
        parsed_book = parsed_book.replace(NEW_LINE, " ")
        # zamiana stringa na listę poszczególnych słów w książce
        book_words_list = parsed_book.split()
        # iteracja po wszystkich słowach w książce i pozbycie się elementów za apostrofem np Jack's -> Jack
        for ap in APOSTROPHE: book_words_list = [re.sub(ap+".*$","", word) for word in book_words_list]
        # dodanie tylko wyrazów które nie należą do listy STOP_WORD oraz są dłuższe niż 1 znak
        self.parsered_books.append([word for word in book_words_list if word not in STOP_WORDS and len(word)>1])
        #print(self.parsered_books[num])
        # stworzenie słownika z liczbą wystąpień wyrazów np: { 'apple' : 3, 'cat' : 4 ... }
        self.books_dictionary.append({word:self.parsered_books[num].count(word) for word in self.parsered_books[num]})
        #print(self.books_dictionary[num])
        self.print_result(num)

# wykonaj parser dla wszystkich książek
    def parse_books(self):
        for i, book in enumerate(self.books):
            self.parse_book(book, i)

# dokonaj wczytania i parsowania książek
    def read_and_parse(self):
        self.read_books()
        self.parse_books()

    def print_result(self,book_num):
            print(self.titles[book_num])
            print(self.parsered_books[book_num])
            print(self.books_dictionary[book_num])
            print("-------------------------")


parser = Parser()
parser.read_and_parse()
