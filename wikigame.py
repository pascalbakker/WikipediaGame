import heapq
import wptools as wiki
import re, math
from collections import Counter

# Global Variables
WORD = re.compile(r'\w+')
DEBUG = False


# FUNCTIONS

# logging function
def log(s):
    if DEBUG:
        print(s)


# Main heuristic function
# First checks if the page is the end goal
# Then checks if pageA's name is in pageB
# Then uses cosine to assign a priority
def heuristicFunction(pageA, pageB):
    # If it is the same name, prioritize
    if pageA.data['label'] == pageB.data['label']:
        print("Is page: " + pageA.data['label'])
        return 1 / 10000.0
    pageASummary = pageA.data['extext']
    pageBSummary = pageB.data['extext']

    # if pageB contains the name of page A, prioitize page A
    if pageA.data['label'] in pageBSummary or pageB.data['label'] in pageASummary:
        return 1 / 1000.0

    # Cosine Similarity
    vector1 = text_to_vector(pageASummary)
    vector2 = text_to_vector(pageBSummary)

    priority = get_cosine(vector1, vector2)

    # Return inverse of priority
    if priority == 0:
        return 10
    else:
        return 1.0 / priority


# COSINE FUNCTIONS
# https://stackoverflow.com/questions/15173225/calculate-cosine-similarity-given-2-sentence-strings
def get_cosine(vec1, vec2):
    intersection = set(vec1.keys()) & set(vec2.keys())
    numerator = sum([vec1[x] * vec2[x] for x in intersection])

    sum1 = sum([vec1[x] ** 2 for x in vec1.keys()])
    sum2 = sum([vec2[x] ** 2 for x in vec2.keys()])
    denominator = math.sqrt(sum1) * math.sqrt(sum2)

    if not denominator:
        return 0.0
    else:
        return float(numerator) / denominator


def text_to_vector(text):
    words = WORD.findall(text)
    return Counter(words)


# Goal function
# If the page contains a link to the goal article, return true
# Else return false
def isArticle(title, links):
    for link in links:
        if title.lower() == link.lower():
            return True
    return False


# Runs astar algorithm
def astar(start, goal, hueristic, debug=True):
    # Initialize datasets
    visited = set()
    start.get_query()
    goal.get_query()
    pq = []
    g = {start.data['label']: 0}
    f = {start.data['label']: hueristic(start, goal)}
    came_from = {}
    heapq.heappush(pq, (f[start.data['label']], start.data['label']))
    visited.add(start.data['label'])

    # Start A* Search
    while True:
        priority, toplink = heapq.heappop(pq)
        top = wiki.page(toplink, silent=True)
        top.get_query()

        # Log data
        log(top.data['links'])
        log("Current Node:" + top.data['label'])
        log("Similarity to Goal Node: " + str(hueristic(top, goal)))

        # Get All Children
        childnodes = top.data['links']
        for childlink in childnodes:
            try:
                if childlink not in visited:
                    visited.add(childlink)

                    log("Adding Node(Unexplored): " + childlink)

                    childpage = wiki.page(childlink, silent=True)
                    childpage.get_query()
                    # If child link is the goal, then print
                    if isArticle(goal.data['label'], childpage.data['links']):
                        print(toplink)
                        print(childlink)
                        print(goal.data['label'])
                        return "End"


                    elif childlink not in top.data['extext']:
                        continue

                    # g[childpage.data['label']] = g[top.data['label']] + hueristic(top, childpage)
                    # f[childpage.data['label']] = g[childpage.data['label']] + hueristic(childpage, goal)
                    f[childpage.data['label']] = hueristic(childpage, goal)
                    heapq.heappush(pq, (f[childpage.data['label']], childpage.data['label']))

                    came_from[childlink] = top.data['label']
            except LookupError:
                continue

        log("queue size: " + str(len(pq)))


# Execute astar with parameters
def executeAStar(pageA=None, pageB=None, printResult=True, userheuristic=heuristicFunction, random=True,
                 timeResult=False, debug=True):
    # Initialize the start and end goal
    DEBUG = debug
    startPage = wiki.page("West Pullman, Chicago", silent=True)
    endPage = wiki.page('Midwestern United States', silent=True)

    path = astar(startPage, endPage, userheuristic)


# Main function
if __name__ == '__main__':
    executeAStar(debug=False)
