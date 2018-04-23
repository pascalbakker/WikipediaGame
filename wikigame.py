import math
import heapq
#import wikipediaapi
import time
import wptools as wiki

#FUNCTIONS

visited = set()
#wiki= wikipediaapi.Wikipedia('en')


#If goal is reached
def isGoal(pageA,pageB):

    return pageA.data['label'] == pageB.data['label']



def hueristic(pageA, pageB):
    return hueristicIs1(pageA,pageB)


#TFIDF hueristic
def hueristicIs1(pageA, pageB):
    if(pageA.data['label'] == pageB.data['label']): return 1000

    pageASummary = pageA.data['extext']
    pageBSummary = pageB.data['extext']


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
    start.get_query()
    goal.get_query()

    t0 = time.time()
    if(isGoal(start,goal)):
        return []


    pq = []
    g = {start.data['label']:0}
    f ={start.data['label']:hueristic(start,goal)}

    came_from = {}

    heapq.heappush(pq, (f[start.data['label']], start.data['label']))
    visited.add(start.data['label'])

    while True:
        priority,toplink = heapq.heappop(pq)
        top = wiki.page(toplink,silent=True)
        top.get_query()
        print(top.data['links'])
        print(top.data['label'])
        if isGoal(top,goal):
            t1 = time.time()
            print("goal reached "+t1-t0)
            return f[top.data['label']],came_from[top.data['label']]

        #Get All Children
        childnodes = top.data['links']
        i = 0
        for childlink in childnodes:
            if(childlink not in visited):
                i+=1
                visited.add(childlink)
                if(childlink not in top.data['extext']):
                    continue
                print("Adding Node(Unexplored): "+childlink)

                childpage = wiki.page(childlink,silent=True)
                childpage.get_query()
                g[childpage.data['label']] = g[top.data['label']] + hueristic(top, childpage)
                f[childpage.data['label']] = g[childpage.data['label']] + hueristic(childpage, goal)
                heapq.heappush(pq,(f[childpage.data['label']],childpage.data['label']))

                came_from[childlink]=top.data['label']

                if(childlink==goal.data['label']):
                    return came_from[childlink]

        print("queue size: "+str(len(pq)))





#main function
def executeAStar(random=True,pageA=None,pageB=None,userhueristic=hueristicIs1,printResult=True,timeResult=False):
    #Initialize the start and end goal
    startPage=wiki.page("West Pullman, Chicago",silent=True)
    endPage=wiki.page("Economics",silent=True)



    path = astar(startPage,endPage,userhueristic)

    if(not printResult):
        return

    print("path: \n"+path)


executeAStar()


