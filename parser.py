import re
import os
import codecs
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sn
import networkx as nx


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
        self.correlation = []

    def read_books(self):
        path_to_books = os.getcwd() + "/books"  # TODO: check if correct on windows
        #path_to_books = os.getcwd() + "/iwi_parser/books"  - need to debug TODO: remove later
        self.titles = os.listdir(path_to_books)
        for title in self.titles:
            book = codecs.open(path_to_books + "/" + title, "r", "utf-8-sig")
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
        plt.savefig('correlation_matrix.png')
        #clear plot
        plt.clf()
        self.correlation= df

    def read_and_parse(self):
        self.read_books()
        # self.loaded_books()
        self.parse_books()
        df = self.create_df()
        print(df)
        self.count_cosine_similarity(df)
        self.draw_correlation_matrix()

    def print_graph(self):   
        # Transform it in a links data frame (3 columns only):
        links = self.correlation.stack().reset_index()
        links.columns = ['var1', 'var2','value']
        G = nx.Graph()
        # Keep only correlation over a threshold and remove self correlation (cor(A,A)=1)
        threshold = 0.81
        links_filtered=links.loc[ (links['value'] > threshold) & (links['var1'] != links['var2'])]

        for i, row in links_filtered.iterrows():
            G.add_edge(row['var1'], row['var2'], weight = round(row['value'],2))

        node_pos=nx.spring_layout(G) # pos = nx.nx_agraph.graphviz_layout(G)
        labels = nx.get_edge_attributes(G,'weight')
        node_col='red'
        # draw graph
        nx.draw_networkx(G, node_pos,node_color= node_col, node_size=40, font_size=6,linewidths=1)
        # Draw weights
        nx.draw_networkx_edge_labels(G, node_pos, edge_labels=labels, font_size=5)
        plt.savefig('plotgraph.png', dpi=600)
 

    def loaded_books(self):
        for title in self.titles:
            print(title)


parser = Parser()
parser.read_and_parse()
parser.print_graph()