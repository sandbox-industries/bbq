import urllib
import os.path
import networkx as nx
from networkx.algorithms import community
import netwulf as nw
from http.cookiejar import CookieJar
from random import sample
from search_page import SearchPage
from page import Page
from settings import Settings

opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(CookieJar()))
# TODO: Change user agentto avoid http er 429

G = nx.Graph()

# If a graph file exists for what we're looking for, load it
if os.path.exists(Settings.KEYWORD+'.gexf'):
    print('Existing graph for keyword(s)', Settings.KEYWORD, 'found...', end='', flush=True)
    G = nx.read_gexf(Settings.KEYWORD+'.gexf', str)
    print('\tLoaded')

search_results = SearchPage(Settings.KEYWORD, opener)
print('Search results loaded')

start_page = Page(search_results.results[0], opener)
print('Start page loaded')
print('Root:', start_page.title)

current_level = [start_page]

G.add_node(start_page.title, size=start_page.view_count)

for i in range(Settings.RECUR_DEPTH):
    print('~='*10,len(current_level), 'pages at depth', i,'~='*10)
    for page in current_level:
        page.load_suggested()

        # Loop through all the suggestions in a page
        for suggestion in page.suggested:
            if not isinstance(suggestion, Page):
                continue  # Skip this suggestion if it's not a fully loaded page

            # Add a node to the graph
            G.add_node(suggestion.title, size=suggestion.view_count)
            # Link this node to the node that suggested it
            # TODO: Edit edge weight based on how many times its been linked
            G.add_edge(page.title, suggestion.title)
            print(suggestion.title, 'added to graph')

    # Put all leaf nodes into a single list
    current_level = [item for sublist in map(lambda x: x.suggested, current_level) for item in sublist if isinstance(item, Page)]
    # Pick out random samples to prevent exponential growth
    samples = sample(current_level, min(Settings.LIMIT_WIDTH, len(current_level)))
    # Clean up some memory
    current_level.clear()
    # Assign the new level
    current_level = samples

print('Fetching done')

nx.write_gexf(G, Settings.KEYWORD+'.gexf')
print('Writing done')

# nw.visualize(G)
