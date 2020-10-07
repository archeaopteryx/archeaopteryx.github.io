from bs4 import BeautifulSoup
from collections import deque
from pathlib import Path

from prettyTerm import PrettyTerm as pt

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

def check_quick_nav(path):
    quick_nav_refs = deque()
    header_ids = deque()
    mismatched = []
    with open(path) as f:
        soup = BeautifulSoup(f, 'html.parser')
    for ref in soup.find_all('li'):
        anchor = next(ref.children)
        quick_nav_refs.append(anchor.get('href'))
    for header in soup.find_all(['h1', 'h2', 'h3']):
        id_value = header.get('id')
        if id_value is None:
            continue
        id_value = "#"+str(id_value)
        header_ids.append(id_value)
    if len(list(quick_nav_refs)) != len(list(header_ids)):
        print("{0} has an unequal number of quickNav links and header ids".format(path.name))
        return False
    try:
        qn = quick_nav_refs.pop()
        h = header_ids.pop()
        if qn != h:
            mismatched.append((qn, h))
    except IndexError:
        pass
    if len(mismatched) == 0:
        return True
    else:
        print("{0} had mismatches: {1}".format(path.name, mismatched))
        return False

def quick_nav_test():
    print("\n"+20*"="+" Starting quick nav test "+20*"=")
    passed = 1
    for article in article_list:
        link_check = check_quick_nav(article)
        if link_check == False:
            passed *= 0
            print(pt.red+"{0} failed"+pt.reset)
    if passed == 1:
        print(pt.green+"All articles passed"+pt.reset)
    print(20*"="+" quick nav test complete"+20*"=")


quick_nav_test()
