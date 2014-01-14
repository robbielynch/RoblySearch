
class Website(object):
    url = ""
    title = ""
    h1s = []
    links = []
    images = []
    non_html = ""



    def __init__(self, url, title, h1s, links, images, non_html):
        self.url = url
        self.title = title
        self.h1s = h1s
        self.links = links
        self.images = images
        self.non_html = non_html
    