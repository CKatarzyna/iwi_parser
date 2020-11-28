import re
import os
import codecs
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sn


class Parser:
    def __init__(self):
        self.titles = []
        self.books = []
        self.parsered_books = []
        self.books_dictionary = []
        self.sparse_matrix = []
        self.count_vectorizer = CountVectorizer(stop_words='english')
        self.count_vectorizer = CountVectorizer()
        self.cosine_similarity = []

    def read_books(self):
        path_to_books = os.getcwd() + "\\books"
        self.titles = os.listdir(path_to_books)
        for title in self.titles:
            book = codecs.open(path_to_books + "\\" + title, "r", "utf-8-sig")
            self.books.append(book.read())

    def parse_books(self):
        self.sparse_matrix = self.count_vectorizer.fit_transform(self.books)
        # print(self.sparse_matrix)

    def create_df(self):
        doc_term_matrix = self.sparse_matrix.todense()
        df = pd.DataFrame(doc_term_matrix,
                          columns=self.count_vectorizer.get_feature_names(),
                          index=self.titles)
        return df

    def count_cosine_similarity(self, df):
        self.cosine_similarity = cosine_similarity(df, df)
        print(self.cosine_similarity)

    def draw_correlation_matrix(self):
        df = pd.DataFrame(self.cosine_similarity, columns=self.titles, index=self.titles)
        print(df)
        corr = df
        corr.style.background_gradient(cmap='coolwarm')
        sn.heatmap(corr, annot=True, fmt='g')
        plt.show()

    def read_and_parse(self):
        self.read_books()
        # self.loaded_books()
        self.parse_books()
        df = self.create_df()
        print(df)
        self.count_cosine_similarity(df)
        self.draw_correlation_matrix()

    def loaded_books(self):
        for title in self.titles:
            print(title)


parser = Parser()
parser.read_and_parse()