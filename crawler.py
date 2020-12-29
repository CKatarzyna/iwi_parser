import urllib.request
import requests

from bs4 import BeautifulSoup


class Crawler:
    def __init__(self):
        self.directory_root = "books\\"
        self.base_uri = "https://www.gutenberg.org"

        self.main_page = requests.get("https://www.gutenberg.org/browse/scores/top#authors-last30")
        self.main_soup = BeautifulSoup(self.main_page.content, 'html.parser')

    def download_books(self):
        for header in self.main_soup.select('h2#books-last30'):
            para = header.find_next_sibling('ol')

            for book_uri in para.find_all('li'):
                download_book_uri = self.base_uri + book_uri.find('a')['href']
                download_book_page = requests.get(download_book_uri)
                download_book_soup = BeautifulSoup(download_book_page.content, 'html.parser')

                for download_book_page_a_href in download_book_soup.select('tr'):
                    for download_book_page_th in download_book_page_a_href.find_all('th'):
                        if download_book_page_th.get_text() == "Title":
                            download_book_description_title = download_book_page_a_href.get_text(). \
                                replace("Title", '').replace('\n', '').replace(':', '').replace(';', '').replace(',','')
                            download_book_description_title = download_book_description_title.split("\r")[0]
                            break

                for download_book_page_a_href in download_book_soup.select('td.unpadded.icon_save a'):
                    if download_book_page_a_href.get_text() == "Plain Text UTF-8":
                        final_download_book_uri = self.base_uri + download_book_page_a_href['href']
                        urllib.request.urlretrieve(final_download_book_uri,
                                                   self.directory_root + download_book_description_title + ".txt")


if __name__ == '__main__':
    crawler_books = Crawler()
    crawler_books.download_books()

