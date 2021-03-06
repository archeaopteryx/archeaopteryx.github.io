from bs4 import BeautifulSoup, SoupStrainer
from collections import deque
from pathlib import Path

class Page():
    """
    Object organizing the link information in the archeaopteryx pages
    """

    def __init__(self, path):
        """
        instance variables:
        name -- file name with extension
        page_type -- home, about, archive or article
        ing_home -- link anchored to the archeaopteryx image
        home -- link anchored to 'home' in the menu bar
        archive -- link anchored to 'archive' in the menu bar
        about -- link anchored to 'about' in the menu bar
        rss -- link anchored to 'rss' in the menu bar
        """
        self.name = path.name
        self.page_type = self.get_page_type(self.name)
        self.img_home, self.home, self.archive, self.about, self.rss = self.get_header_links(path)

    def get_page_type(self, name):
        '''
        Return if page is home, about, archive, or an article
        '''
        dict = {"index.html": "home", "about.html": "about", "archive.html": "archive"}
        return dict.get(name, "article")

    def get_header_links(self, path):
        only_header = SoupStrainer("header")
        dict = {"img_home": "archea-container", "home": "home", "archive": "archive", "about": "about", "rss": "rss"}
        with open(path) as f:
            soup = BeautifulSoup(f, "html.parser", parse_only=only_header)
        for key in dict:
            div = soup.find('div', dict[key])
            if not div is None:
                try:
                    anchor = next(div.children)
                    dict[key] = anchor.get('href')
                except StopIteration:
                    dict[key] = None
            else:
                 dict[key] = None
        links = (dict["img_home"], dict["home"], dict["archive"], dict["about"], dict["rss"])
        return links


class ArticlePage(Page):
    """
    Extends Page class to include Navigation links and header ids
    """

    def __init__(self, path):
        """
        instance variables:
        nav_refs -- deque of all links in the navigation bar
        header_ids -- deque of all ids in h1, h2 and h3 elements

        other instance variables inherited from Page class
        """
        self.nav_refs = self.get_nav_links(path)
        self.header_ids = self.get_h_ids(path)
        Page.__init__(self, path)


    def get_nav_links(self, path):
        only_toc = SoupStrainer('li')
        nav_refs = deque()
        with open(path) as f:
            soup = BeautifulSoup(f, 'html.parser', parse_only=only_toc)
        anchor_list = soup.find_all('a')
        for anchor in anchor_list:
            nav_refs.append(anchor.get('href'))
        return nav_refs

    def get_h_ids(self, path):
        only_headers = SoupStrainer(['h1', 'h2', 'h3', 'h4'])
        header_ids = deque()
        with open(path) as f:
            soup = BeautifulSoup(f, 'html.parser', parse_only=only_headers)
        for ref in soup:
            if ref.string == "Contents:":
                continue
            id = ref.get('id')
            id = "#" + str(id)
            header_ids.append(id)
        return header_ids



class ArchivePage(Page):

    def __init__(self, path):
        self.article_links = self.get_article_links(path)
        Page.__init__(self, path)

    def get_article_links(self, path):
        only_article_links = SoupStrainer('li', {'class':"archive-li"} )
        article_links = deque()
        with open(path) as f:
            soup = BeautifulSoup(f, 'html.parser', parse_only=only_article_links)
        for ref in soup:
            try:
                anchor = next(ref.children)
                article_links.append(anchor.get('href'))
            except StopIteration:
                pass
        return article_links
