from Queue import Queue

__author__ = 'calthorpe_associates'

from footprint.main.urls  import urlpatterns

queue = Queue()
def show_urls(urllist=urlpatterns, depth=0):
    """
    Inspects the URL regexes
    :param urllist:
    :param depth:
    :return:
    """
    if (depth > 50):
        return
    for entry in urllist:
        queue.put(entry)
    while not queue.empty():
        entry = queue.get()
        print "{0} - {1}".format("  " * depth, entry.regex.pattern)
        if hasattr(entry, 'url_patterns'):
            show_urls(entry.url_patterns, depth + 1)

