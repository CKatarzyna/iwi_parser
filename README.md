# Visualization of document similarities

This academic projects is focused on visualization of documents similarities. The main metric is based on the cosine similarity between words. Dataset for books was retrieved from [Project Gutenberg Site](https://www.gutenberg.org/). Application consists of three modules. First of them **Crawler**, is responsible for downloading books. **Parser** includes main logic for processing content of the books and couting similarity metric. The last one **Viewer** ensures proper visualization of the achived results. 

### Prerequisites

* [Beautiful Soup](https://www.crummy.com/software/BeautifulSoup/bs4/doc/)
* [pyvis](https://pyvis.readthedocs.io/en/latest)
* [pandas](https://pandas.pydata.org/)
* [requests](https://requests.readthedocs.io/en/master/)
* [urllib.request](https://docs.python.org/3/library/urllib.request.html)
* [codecs](https://docs.python.org/3/library/codecs.html)
* [scikit-learn](https://scikit-learn.org/stable/)

## Running the application

1. Crawler - dataset of books will be downloaded and saved in `books/` directory.
2. Parser - module will generate `books_similarity.csv` file.
3. Viewer - input as a `books_connection_viewer.html` will be generated.

Demo of the generated `books_connection_viewer.html` site.

<p align="center">
  <br/>
  <img src="https://github.com/CKatarzyna/iwi_parser/blob/main/resource/demo.gif">
</p>
 
## Authors

* [krzyGa](https://github.com/krzyGa)
* [Kopryk](https://github.com/Kopryk)
* [CKatarzyna](https://github.com/CKatarzyna)
