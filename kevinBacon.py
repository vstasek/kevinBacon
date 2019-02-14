#----------------------------------------------------------------------
# kevinBacon.py
# Victor Stasek
# CS361 - TTH 11:00AM
# 10/24/13
#----------------------------------------------------------------------

import sys

#----------------------------------------------------------------------

def createGraph(fname):

    """creates a graph that connects all actors in file fname
    returns connected graph"""

    # initialize graph 'g', current movie 'movie',
    #   and list of actors in 'movie' 'actorList'
    g = {}
    movie = fname.readline().strip('\n')
    actorList = []
    
    for line in fname:
        # we are at a new movie
        if line == '\n':
            # connect actors in previous movie
            connectActorList(g, movie, actorList)
            # emptry actor list for new movie
            actorList = []
            # move on to next movie
            movie = fname.readline().strip('\n')
        # we are at an actor
        else:
            # add actor to actor list
            actorList.append(line.strip('\n'))
            
    return g

#----------------------------------------------------------------------
        
def connectActorList(g, movie, seq):

    """creates a bi-directional edge 'movie' in graph 'g' between all actors in 'seq'"""
    
    for x in seq:
        for y in seq:
            if x != y:
                connectTwoActors(g, x, y, movie)

#----------------------------------------------------------------------
            
def connectTwoActors(g, actor1, actor2, movie):

    """creates an uni-directional edge 'movie' from 'actor1' to 'actor2' in graph 'g'"""

    if actor1 not in g:
        g[actor1] = {actor2:movie}
    else:
        g[actor1][actor2] = movie

#----------------------------------------------------------------------

def shortestPathGraph(g, sourceActor):

    """finds shortest path between 'sourceActor' and all other actors in graph 'g'
    returns graph containing all actors distance from 'sourceActor' and parent"""

    # initialize graph and add source actor to graph
    parentGraph = {}
    parentGraph[sourceActor] = (sourceActor, 0)

    queue = [sourceActor]

    while queue != []:
        currentActor = queue[0]
        del queue[0]

        # iterate over actors adjacent to current actor
        for adj in g[currentActor]:
            # if we haven't hit the actor yet
            if adj not in parentGraph:
                # update adjacent actor's parent/distance & add to queue
                parentGraph[adj] = (currentActor, parentGraph[currentActor][1] + 1)
                queue.append(adj)

    return parentGraph
                
#----------------------------------------------------------------------

def shortestPath(g, parentGraph, actor):

    """uses 'g' and 'parenGraph' to output each step in shortest path
    between 'actor' and sourceActor from shortestPathGraph"""

    # distance from 'actor' to source tells us how many times to iterate
    for i in range(parentGraph[actor][1]):
        # find actor's parent & the movie they're with parent in
        actorParent = parentGraph[actor][0]
        movie = g[actor][actorParent]
        print(actor + ' was in "' + movie + '" with ' + actorParent)

        # update actor
        actor = actorParent
        
#----------------------------------------------------------------------

def main(argv):
    
    if len(argv) > 1:
        fname = argv[1]
    else:
        fname = input('enter a filename: ')

    fname = open(fname, 'rU')

    g = createGraph(fname)
    parentGraph = shortestPathGraph(g, 'Kevin Bacon')

    actor = input('enter actor/actress: ')
    while actor != '':
        if actor in g:
            shortestPath(g, parentGraph, actor)
            print()
            actor = input('enter actor/actress: ')
        else:
            print('actor/actress not in graph\n')
            actor = input('enter actor/actress: ')
    
    fname.close()
    
#----------------------------------------------------------------------

if __name__ == '__main__':
    main(sys.argv)
