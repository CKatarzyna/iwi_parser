from bs4 import BeautifulSoup
import urllib.request
import requests
from collections import defaultdict
from pyvis.network import Network
import pandas as pd
import os

# https://api-lab.dimensions.ai/cookbooks/8-organizations/3-Organizations-Collaboration-Network.html
# https://pyvis.readthedocs.io/en/latest/documentation.html


class Viewer:
    def __init__(self):
        self.file_name_html = "books_connection_viewer.html"
        self.net = Network(height="100%", width="100%", bgcolor="black", font_color="white")
        self.net.barnes_hut()
        self.threshold = 0

    def load_data_form_csv_file(self, file_name):
        self.data = pd.read_csv(file_name, encoding='mac_roman')

    def set_threshold(self, threshold):
        self.threshold = threshold

    def generate_graph(self):
        sources = self.data['Source']
        targets = self.data['Target']
        weights = self.data['Weight']

        edge_data = zip(sources, targets, weights)
        weight_dist = defaultdict(list)
        for edge in edge_data:
            source = edge[0]
            target = edge[1]
            weight = edge[2]
            if self.threshold < weight:
                self.net.add_node(source, source, title=f"<h4>{source}</h4>", shape="dot", value=weight)
                self.net.add_node(target, target, title=f"<h4>{target}</h4>", shape="dot", value=weight)
                self.net.add_edge(source, target, width=1)
                weight_dist[source].append(weight)

        neighbor_map = self.net.get_adj_list()
        for node in self.net.nodes:
            node["title"] += "<li>" + "</li><li>".join('{} [{}]'.format(file, file_w) for file, file_w in zip(neighbor_map[node["id"]],[str("%.2f"%w) for w in weight_dist[node["id"]]]))
            node["value"] = len(neighbor_map[node["id"]])

    def customize_graph(self):
        self.net.show_buttons(filter_=['physics'])
        # self.net.show_buttons(filter_=['edges'])
        # self.net.show_buttons(filter_=['nodes'])

    def show_graph(self):
        self.net.show(self.file_name_html)

    def customize_site_html(self):
        base = os.path.dirname(os.path.abspath(__file__))
        html = open(os.path.join(base, self.file_name_html))
        soup = BeautifulSoup(html, 'html.parser')
        soup.find('body')['style'] = "background-color:black;"
        soup.find('h1').replace_with('')

        with open(self.file_name_html, "wb") as f_output:
            f_output.write(soup.prettify("utf-8"))


if __name__ == '__main__':
    viewer_books = Viewer()
    viewer_books.load_data_form_csv_file("books_similarity.csv")
    viewer_books.set_threshold(0.5)
    viewer_books.generate_graph()
    viewer_books.show_graph()
    viewer_books.customize_site_html()
