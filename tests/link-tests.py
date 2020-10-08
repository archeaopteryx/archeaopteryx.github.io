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
- all articles all listed in archive
'''

# TODO: implement other tests, consider refactoring

main_dir = Path(Path.cwd()).parent
article_dir = main_dir.joinpath('html')

article_list = list(article_dir.glob('*.html'))


def check_quick_nav(nav_refs, header_ids, name):
    mismatched = []
    if len(list(nav_refs)) != len(list(header_ids)):
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
    print("\n"+20*"="+" Starting quick nav test "+20*"=")
    passed = 1
    for article in article_list:
        name = article.name
        article_obj = ArticlePage(article)
        nav_refs = article_obj.nav_refs
        header_ids = article_obj.header_ids
        link_check = check_quick_nav(nav_refs, header_ids, name)
        if link_check == False:
            passed *= 0
            print(pt.red+"quick_nav_test failed"+pt.reset)
    if passed == 1:
        print(pt.green+"All articles passed"+pt.reset)
    print(20*"="+" quick nav test complete"+20*"=")

'''
archive_path = main_dir.joinpath('archive.html')
archive = ArchivePage(archive_path)
'''

#quick_nav_test()
