from bs4 import BeautifulSoup
from link import Link
from settings import Settings

class Page(object):
    def __init__(self, link, opener):
        self.opener = opener
        self.suggested = []

        if type(link) == Link:
            vid_page_src = opener.open(link.url)
            self.url = link.url
        else:
            vid_page_src = opener.open(link)
            self.url = link

        if vid_page_src is None:
            raise ValueError('Failed to load ' + self.url)

        self.page = BeautifulSoup(vid_page_src, 'html.parser')

        res = self.page.find_all('a',
                                 attrs={'class': ' content-link spf-link yt-uix-sessionlink spf-link '})
        if len(res) == 0:
            # Sometimes the html class doesnt have spaces and bs4 doesn't strip
            #    so we gotta look again
            res = self.page.find_all('a',
                                     attrs={'class': 'content-link spf-link yt-uix-sessionlink spf-link'})

        if len(res) == 0:
            open('/tmp/dump.html', 'w').write(str(self.page))
            raise ValueError('No suggested links found for ' + self.url)

        # Remove the ' - Youtube' at the end of all titles
        self.title = self.page.title.text[:-10]
        
        for s in res[:Settings.TREE_WIDTH]:
            self.suggested.append(Link(s.attrs['title'], s.attrs['href']))

        res = self.page.find_all('div', attrs={'class': 'watch-view-count'})
        if len(res) == 0:
            open('/tmp/dump.html', 'w').write(str(self.page))
            print(ValueError('No view count found for ' + self.url))
            self.view_count = 1  # Give a default view count
        else:
            res = res[0].text  # Get the first match
            res = res.split()[0]  # Remove the word 'views' and get just the number
            res = ''.join(res.split(','))  # Remove the commas
            self.view_count = int(res)  # Convert into an integer

    def __str__(self):
        return self.title

    def __eq__(self, other):
        # If comparing Pages, only the URL matters
        if isinstance(other, self.__class__):
            return self.url == other.url
        return False
    
    def __ne__(self, other):
        return not self.__eq__(other)

    def load_suggested(self):
        """Fetch and parse all suggested pages
        Will turn self.suggested from a list of Links to a list of Pages
        """
        # Short-circuit function if we've already loaded suggested pages
        if Page in map(type, self.suggested):
            return

        for i in range(len(self.suggested)):
            print('\tPaging', i + 1, 'out of', len(self.suggested), '...', end='', flush=True)
            try:
                self.suggested[i] = Page(self.suggested[i], self.opener)
                print('Done')
            except:
                print('Failed')

    def contains(self, link):
        if type(link) == Link:
            link = link.url

        for s in self.suggested:
            if s.url == link:
                return True

        return False

if __name__ == "__main__":
    import urllib
    from http.cookiejar import CookieJar

    # URL to page we want to parse
    url = 'https://www.youtube.com/watch?v=dQw4w9WgXcQ'

    # Make a Link to test with
    l = Link('Test', '/watch?v=dQw4w9WgXcQ')

    # Make an opener
    opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(CookieJar()))

    print('Load with url')
    p = Page(url, opener)
    print('Loaded:', p.title)

    print('Load with link')
    p = Page(l, opener)
    print('Loaded:', p.title)

    print('Suggest pages:')
    for suggestion in p.suggested:
        print('\t', suggestion)
