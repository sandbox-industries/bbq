import urllib
from bs4 import BeautifulSoup
from link import Link


class SearchPage(object):
    """Youtube search results page
    Fetches and parses youtube search results for a given keyword
    """
    def __init__(self, keyword, opener):
        self.results = []
        self.url = 'https://www.youtube.com/results?search_query='+urllib.parse.quote(keyword)

        vid_page_src = opener.open(self.url)

        if vid_page_src is None:
            raise ValueError('Failed to load ' + self.url)

        self.page = BeautifulSoup(vid_page_src, 'html.parser')

        res = self.page.find_all('a',
                                 attrs={'class': 'yt-uix-tile-link yt-ui-ellipsis yt-ui-ellipsis-2 yt-uix-sessionlink spf-link'})
        if len(res) == 0:
            # Sometimes the html class doesnt have spaces and bs4 doesn't strip
            #    so we gotta look again
            res = self.page.find_all('a',
                                     attrs={'class': 'yt-uix-tile-link yt-ui-ellipsis yt-ui-ellipsis-2 yt-uix-sessionlink spf-link '})

        if len(res) == 0:
            open('/tmp/search_dump.html', 'w').write(str(self.page))
            raise ValueError('No search results found for ' + self.url)
        
        for s in res:
            self.results.append(Link(s.attrs['title'], s.attrs['href']))


if __name__ == "__main__":
    import urllib
    from http.cookiejar import CookieJar

    # What were searching for
    kw = 'dogs'

    # Make an opener
    opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(CookieJar()))

    # Test to make sure we fail when there are no results
    try:
        s = SearchPage('', opener)
    except ValueError:
        print('Failed succesfully')
    except Exception as e:
        print('ERROR', e)

    # Actually search for something
    s = SearchPage(kw, opener)

    print('Results for:', kw)
    for result in s.results:
        print('\t', result)
