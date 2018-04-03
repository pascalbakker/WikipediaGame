import math
from queue import PriorityQueue
import heapq
import wikipediaapi
import time

visited = set()
wiki= wikipediaapi.Wikipedia('en')

#FUNCTIONS

#Get a random wikipedia article
def getRandomArticle():
    article = None
    while article is None:
        try:
            article = wiki.page(wiki.random(pages=1))
        except:
            pass
    return article

#If goal is reached
def isGoal(pageA,pageB):
    return pageA.title == pageB.title


#TFIDF hueristic
def hueristicIs1(pageA, pageB):
    if(pageA.title == pageB.title): return 1000

    pageASummary = pageA.text
    pageBSummary = pageB.text


    pageASummarySplit = pageASummary.split()
    pageASummaryLength = len(pageASummarySplit)
    sum = 0
    for term in pageASummarySplit:
        idfcount = 2
        tf = pageASummary.count(term)/pageASummaryLength
        if(pageBSummary.count(term)!=0):
            idfcount = 1
        idf = math.log(2/idfcount)
        tfidf = tf*idf
        sum+=tfidf

    if sum==0: return 0

    return 1/sum

#Runs astar algorithm
def astar(start, goal,hueristic):
    t0 = time.time()
    if(isGoal(start,goal)):
        return []


    pq = []
    g = {start.title:0}
    f ={start.title:hueristic(start,goal)}

    came_from = {}

    heapq.heappush(pq, (f[start.title], start.title))
    visited.add(start.title)

    while True:
        priority,toplink = heapq.heappop(pq)
        top = wiki.page(toplink)
        print(top.links)
        print(top.title)
        if isGoal(top,goal):
            t1 = time.time()
            print("goal reached "+t1-t0)
            return f[top.title],came_from[top.title]

        #Get All Children
        childnodes = top.links
        i = 0
        for childlink in childnodes.keys():
            if(childlink not in visited):
                i+=1
                visited.add(childlink)
                if(childlink not in top.text):
                    continue
                print("Adding Node(Unexplored): "+childlink)

                childpage = childnodes[childlink]
                g[childpage.title] = g[top.title] + hueristic(top, childpage)
                f[childpage.title] = g[childpage.title] + hueristic(childpage, goal)
                heapq.heappush(pq,(f[childpage.title],childpage.title))

                came_from[childlink]=top.title

                if(childlink==goal.title):
                    return came_from[childlink]

        print("queue size: "+str(len(pq)))





#main function
def executeAStar(random=True,pageA=None,pageB=None,userhueristic=hueristicIs1,printResult=True,timeResult=False):
    #Initialize the start and end goal
    startPage=wiki.page("West Pullman, Chicago")
    endPage=wiki.page("Economics")
    if(random):
        startPage = getRandomArticle()
        endPage = getRandomArticle()
        print("start page: " + startPage.title)
        print("end page: " + endPage.title)
    elif(not random and pageA!=None and pageB!=None):
        startPage = pageA
        endPage = pageB
    else:
        print("Invalid parameters!")



    path = astar(startPage,endPage,userhueristic)

    if(not printResult):
        return

    print("path: \n"+path)

executeAStar(random=False)


