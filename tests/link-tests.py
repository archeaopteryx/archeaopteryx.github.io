from bs4 import BeautifulSoup
from collections import deque
from pathlib import Path

from prettyTerm import PrettyTerm as pt
from pageObjects import Page, ArticlePage, ArchivePage

'''
automate link testing
check that:
- the quickNav on articles links to all sections
- all pages except index link to home when clicking on the archeaopteryx
- all pages excpet index have 'home', 'archive', 'about' and 'rss' links in top bar
- index has 'archive', 'about' and 'rss' links
- all articles listed in archive
'''

# TODO: header link tests

main_dir = Path(Path.cwd()).parent
article_dir = main_dir.joinpath('html')
article_list = list(article_dir.glob('*.html'))

article_obj_list = []
for article in article_list:
    article_obj_list.append(ArticlePage(article))

archive_path = main_dir.joinpath('archive.html')
archive = ArchivePage(archive_path)
about_path = main_dir.joinpath('about.html')
about = Page(about_path)
home_path = main_dir.joinpath('index.html')
home = Page(home_path)


def check_quick_nav(nav_refs, header_ids, name):
    mismatched = []
    if len(nav_refs) != len(header_ids):
        print("{0} has an unequal number of quickNav links and header ids".format(name))
        return False
    while True:
        try:
            nr = nav_refs.pop()
            hi = header_ids.pop()
            if nr != hi:
                mismatched.append((nr, hi))
        except IndexError:
            break
    if len(mismatched) != 0:
        print("{0} had mismatches: {1}".format(name, mismatched))
        return False
    return True

def quick_nav_test():
    '''
    Check that the article quick nav links match up to section header ids
    '''
    print("\n"+20*"="+" Starting quick nav test "+20*"=")
    passed = 1
    for article in article_obj_list:
        name = article.name
        nav_refs = article.nav_refs
        header_ids = article.header_ids
        link_check = check_quick_nav(nav_refs, header_ids, name)
        if link_check == False:
            passed *= 0
            print(pt.red+"quick_nav_test failed"+pt.reset)
    if passed == 1:
        print(pt.green+"All articles passed"+pt.reset)
    print(65*"=")


def archive_links_test():
    '''
    Check that all links in the archive are unique and that every article has a
    link in the archive
    '''
    links = archive.article_links

    article_set = set()
    for article in article_list:
        name = article.name
        name = "html/"+name
        article_set.add(name)

    links_set = set(links)
    diff = article_set - links_set
    passed = 1

    print("\n"+21*"="+" starting archive test "+21*"=")
    if len(links_set) != len(links):
        passed *= 0
        print(pt.red+"Duplicate link in archive"+pt.reset)

    if len(diff) != 0:
        passed *=0
        print(pt.red+"Missing link or file for {}".format(diff)+pt.reset)

    if passed == 1:
        print(pt.green+"Archive passed"+pt.reset)
    print(65*"=")


def article_header_test():
    '''
    Check that all articles have the correct header links
    '''
    link_dict = {"img":"../index.html", "home":"../index.html", "archive": "../archive.html", "about": "../about.html"}
    passed = 1
    print("\n"+18*"="+" starting article header test "+17*"=")
    for article in article_obj_list:
        article_dict = {"img":article.img_home, "home":article.home, "archive":article.archive, "about":article.about}
        for key in article_dict:
            if article_dict[key] != link_dict[key]:
                passed*=0
                print(pt.red+"Header link error "+pt.reset+"{0} missing link for {1}".format(article.name, key))
    if passed == 1:
        print(pt.green+"Articles passed"+pt.reset)
    print(65*"=")


def general_header_check(page, page_dict):
    '''
    Check that non-article pages have correct header links
    '''
    link_dict = {"img":"index.html", "home":"index.html", "archive": "archive.html", "about": "about.html", "rss":"https://archeaopteryx.github.io/rss.xml"}
    passed = 1
    for key in page_dict:
        if page_dict[key] != link_dict[key]:
            passed*=0
            print(pt.red+"Header link error"+pt.reset+"{0} missing link for {1}".format(page.name, key))
    return passed


def general_header_test():
    home_dict = {"archive":home.archive, "about":home.about, "rss":home.rss}
    archive_dict = {"img":archive.img_home, "home":archive.img_home, "about":archive.about, "rss":archive.rss}
    about_dict = {"img":about.img_home, "home":about.img_home, "archive":about.archive, "rss":about.rss}
    passed = 1
    print("\n"+18*"="+" starting general header test "+17*"=")
    passed *= general_header_check(home, home_dict)
    passed *= general_header_check(archive, archive_dict)
    passed *= general_header_check(about, about_dict)
    if passed == 1:
        print(pt.green+"General pages passed"+pt.reset)
    print(65*"=")




archive_links_test()
quick_nav_test()
article_header_test()
general_header_test()
