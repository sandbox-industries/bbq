
class Link(object):
    """Link class
    Small class that describes a youtube link
    """
    def __init__(self, title, href):
        self.title = title.strip()
        self.url = 'https://www.youtube.com' + href

    def __str__(self):
        return self.title


if __name__ == "__main__":
    # This class gets tested in other class' tests
    pass