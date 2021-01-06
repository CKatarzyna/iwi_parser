import os
import codecs
from sklearn.feature_extraction import text

from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import pandas as pd

CUSTOM_STOP_WORDS = ["a", "able", "about", "across", "after", "all", "almost", "also", "am", "among", "an", "and",
                     "any", "are", "as", "at", "be", "because", "been", "but", "by", "can", "cannot", "chapter", "could", "dear",
                     "did", "do", "does", "either", "else", "ever", "every", "for", "from", "get", "got", "had", "has",
                     "have", "he", "her", "hers", "him", "his", "how", "however", "i", "if", "in", "into", "is", "it",
                     "its", "just", "least", "let", "like", "likely", "may", "me", "might", "miss", "most", "mr",
                     "must", "my", "neither", "no", "nor", "not", "of", "off", "often", "on", "only", "or", "other",
                     "our", "own", "rather", "said", "say", "says", "she", "should", "since", "so", "some", "than",
                     "that", "the", "their", "them", "then", "there", "these", "they", "this", "tis", "to", "too",
                     "twas", "us", "wants", "was", "we", "were", "what", "when", "where", "which", "while", "who",
                     "whom", "why", "will", "with", "would", "yet", "you", "your"]


class Parser:
    def __init__(self,books_directory):
        self.directory_root = books_directory
        self.books_similarity_file_name = 'books_similarity.csv'
        self.titles = []
        self.books = []
        self.books_dictionary = []
        self.sparse_matrix = []
        self.count_vectorizer = CountVectorizer(stop_words=text.ENGLISH_STOP_WORDS.union(CUSTOM_STOP_WORDS))
        self.cosine_similarity = []

    def read_books(self):
        path_to_books = os.getcwd() + self.directory_root
        self.titles = os.listdir(path_to_books)
        if '.gitignore' in self.titles:
            self.titles.remove('.gitignore')
        for title in self.titles:
            book = codecs.open(path_to_books + "/" + title, "r", "utf-8-sig")
            self.books.append(book.read())

    def parse_books(self):
        self.sparse_matrix = self.count_vectorizer.fit_transform(self.books)

    def create_df(self):
        doc_term_matrix = self.sparse_matrix.todense()
        df = pd.DataFrame(doc_term_matrix,
                          columns=self.count_vectorizer.get_feature_names(),
                          index=self.titles)
        return df

    def count_cosine_similarity(self, df):
        self.cosine_similarity = cosine_similarity(df, df)
        print(self.cosine_similarity)

    def create_books_similarity_file(self):
        df = pd.DataFrame(self.cosine_similarity, columns=self.titles, index=self.titles)

        file = open(self.books_similarity_file_name, 'w', encoding='mac_roman')
        file_content = "Source,Target,Weight\n"
        for index, data in df.stack().iteritems():
            if index[0] != index[1]:
                if '{}, {}, {} \n'.format(index[1], index[0], str(data)) not in file_content:
                    file_content += ('{},{},{} \n'.format(index[0], index[1], str(data)))

        file.write(file_content)
        file.close()


if __name__ == '__main__':
    parser_books = Parser("/books")
    parser_books.read_books()
    parser_books.parse_books()
    parser_books.count_cosine_similarity(parser_books.create_df())
    parser_books.create_books_similarity_file()
