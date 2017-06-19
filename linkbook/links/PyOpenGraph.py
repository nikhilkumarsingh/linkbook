import requests
from html.parser import HTMLParser

class PyOpenGraph(object):
   
    def __init__(self, url):
        html = requests.get(url).text
        p = PyOpenGraphParser()
        p.feed(html)
        self.url = p.properties['url']
        self.site_name = p.properties['site_name']
        self.title = p.properties['title']
        self.description = p.properties['description']
        self.image = p.properties['image']
        self.image_height = p.properties['image:height']
        self.image_width = p.properties['image:width']

        p.close()
    
    def is_valid(self):
        if any([self.title, self.image, self.description]):
            return True
        else:
            return False
    
    def __str__(self):
        return self.title
    

class PyOpenGraphParser(HTMLParser):
    
    def __init__(self):
        HTMLParser.__init__(self)
        self.properties = {'url': None, 'site_name': None, 'title':None, 'description': None, 
                           'image': None, 'image:height':None, 'image:width': None}
    
    def handle_starttag(self, tag, attrs):
        if tag == 'meta':
            attrdict = dict(attrs)
            if 'property' in attrdict and attrdict['property'].startswith('og:') and 'content' in attrdict:
                self.properties[attrdict['property'].replace('og:', '')] = attrdict['content']

    def handle_endtag(self, tag):
        pass
    
    def error(self, msg):
        pass
