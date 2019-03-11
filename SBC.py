#!/usr/bin/env python3

import re
import itertools
import copy

ROLLNUM_REGEX = "201[0-9]{4}"

class Graph(object):
    name = "Tanya"
    email = "tanya18109@iiitd.ac.in"
    roll_num = "2018109"

    def __init__ (self, vertices, edges):
        """
        Initializes object for the class Graph

        Args:
            vertices: List of integers specifying vertices in graph
            edges: List of 2-tuples specifying edges in graph
        """

        self.vertices = vertices
        
        ordered_edges = list(map(lambda x: (min(x), max(x)), edges))
        
        self.edges    = ordered_edges
        
        self.validate()

    def validate(self):
        """
        Validates if Graph if valid or not

        Raises:
            Exception if:
                - Name is empty or not a string
                - Email is empty or not a string
                - Roll Number is not in correct format
                - vertices contains duplicates
                - edges contain duplicates
                - any endpoint of an edge is not in vertices
        """

        if (not isinstance(self.name, str)) or self.name == "":
            raise Exception("Name can't be empty")

        if (not isinstance(self.email, str)) or self.email == "":
            raise Exception("Email can't be empty")

        if (not isinstance(self.roll_num, str)) or (not re.match(ROLLNUM_REGEX, self.roll_num)):
            raise Exception("Invalid roll number, roll number must be a string of form 201XXXX. Provided roll number: {}".format(self.roll_num))

        if not all([isinstance(node, int) for node in self.vertices]):
            raise Exception("All vertices should be integers")

        elif len(self.vertices) != len(set(self.vertices)):
            duplicate_vertices = set([node for node in self.vertices if self.vertices.count(node) > 1])

            raise Exception("Vertices contain duplicates.\nVertices: {}\nDuplicate vertices: {}".format(vertices, duplicate_vertices))

        edge_vertices = list(set(itertools.chain(*self.edges)))

        if not all([node in self.vertices for node in edge_vertices]):
            raise Exception("All endpoints of edges must belong in vertices")

        if len(self.edges) != len(set(self.edges)):
            duplicate_edges = set([edge for edge in self.edges if self.edges.count(edge) > 1])

            raise Exception("Edges contain duplicates.\nEdges: {}\nDuplicate vertices: {}".format(edges, duplicate_edges))

    def dict1(self):
        #This function creates a dictionary of all the vertices and the value of them will be a list of those vertices directly connected to them.
        l=[]
        for i in self.edges:
            i=list(i)
            l.append(i)

        d={}
        for i in l:
            if i[0] not in d:
                d[i[0]]=[]
            if i[1] not in d:
                d[i[1]]=[]

        for i in l:
            for k in d:
                if i[0]==k:
                    d[k].append(i[1])
                elif i[1]==k:
                    d[k].append(i[0])
                else:
                    pass
        return d
    
        
            
    def shortestpath(self,start,end):            #this function finds the shortest path between the start vertices and end vertices.
        d=self.dict1()
        l1=[]
        a=start
        for i in d[a]:
            l1.append([a,i])
            if i==end:
                return [a,i]               #returns the path when start and end are directly connected (dis=1)
        a1=0
        while a1==0:
            for i in l1:
                n=len(i)
                for j in d[i[n-1]]:
                    if j not in i:
                        i2=copy.deepcopy(i)
                        i2.append(j)
                        l1.append(i2)            #appends the vertices point being used in the shortest path
                    
                        if j==end:               #returns the shortest path
                            return i2
                        else:
                            a1=0
                            i2=[]
            
        if a1==0:
            return None                      #if there is no shortest path, none is returned . But one pre condition here is that the graph is connected , thus None will never be returned.

    def min_dist(self, start_node, end_node):
        '''
        Finds minimum distance between start_node and end_node

        Args:
            start_node: Vertex to find distance from
            end_node: Vertex to find distance to

        Returns:
            An integer denoting minimum distance between start_node
            and end_node
        '''
       

                
        short=self.shortestpath(start_node,end_node)            #finds the shortest path between start node and end node.
        if short==None:
            return None
        else:
            shortlength=len(short)                           #length of shortest path gives us min_dist
            return shortlength
                
        raise NotImplementedError

    def all_shortest_paths(self,start_node, end_node):
        """
        Finds all shortest paths between start_node and end_node

        Args:
            start_node: Starting node for paths
            end_node: Destination node for paths

        Returns:
            A list of path, where each path is a list of integers.
        """
        
        mindist=self.min_dist(start_node,end_node)                #finds the minimum distance between start and end node.
        path=[]
        a=self.all_paths(start_node,end_node,mindist,path)      #finds all the paths between start and end node that have len=mindist (i.e finds all the shortest path)
        return a
        

        raise NotImplementedError

    def all_paths(self,node, destination, dist, path):
        """
        Finds all paths from node to destination with length = dist

        Args:
            node: Node to find path from
            destination: Node to reach
            dist: Allowed distance of path
            path: path already traversed

        Returns:
            List of path, where each path is list ending on destination

            Returns None if there no paths
        """
        d=self.dict1()
        l=[]
        l.append(node)
        path.append(l)
        d1=0
        while d1<int(dist-1):                 #execute loop till mentioned distance is not reached . One is subtracted because the starting node is already appended in the list
            path2=list(path)
            for i in path2:
                for j in d[i[d1]]:        #j takes the value of all consecutive vertices
                    i2=list(i)
                    if j not in i:        #if the node is already not in the path , then append it to the path list.
                        i2.append(j)
                        path.append(i2)
            d1+=1
            path3=list(path)
            for i in path3:
                if i in path2:
                    path.remove(i)         #removes the path(incomplete path) got from previous loop
        mainpath=[]
        for i in path:
            if i[dist-1]==destination:
                mainpath.append(i)    #path is appended only if last node is equal to the destination
        if mainpath==[]:
            return None
        else:
            return mainpath
            

        raise NotImplementedError

    def X(self,l):                                 #finds the number of shortest path between two coordinates
        x=l[0]
        y=l[1]
        a=self.all_shortest_paths(x,y)
        n=len(a)
        return n

    def Y(self,l,node):                         #finds the number of shortest path between two coordinates passing through a node
        x=l[0]
        y=l[1]
        a=self.all_shortest_paths(x,y)
        b=[]
        for i in a:
            if node in i:
                b.append(i)
        n=len(b)
        return n

    def betweenness_centrality(self, node):
        """
        Find betweenness centrality of the given node

        Args:
            node: Node to find betweenness centrality of.

        Returns:
            Single floating point number, denoting betweenness centrality
            of the given node
        """
        NodePairs=[]
        n=len(self.vertices)
        for i in self.vertices:
            for j in self.vertices:
                if i!=j and i!=node and j!=node:                            #checking if these nodes are not equal to each other or to the node whose betweenness centrality is to be found
                    if [i,j] not in NodePairs and [j,i] not in NodePairs:   #checking if these node pairs do not already exist
                        NodePairs.append([i,j])                              #creating node pairs
        
        s=0
        for i in NodePairs:
            nx=self.X(i)
            ny=self.Y(i,node)
            nyx=ny/nx
            s+=nyx
        g=(s*2)/((n-1)*(n-2))                                              #calculating betweenness centrality by substituting correct values in the formula.
        return g
            
        
            

        raise NotImplementedError

    def top_k_betweenness_centrality(self,m=[]):
        """
        Find top k nodes based on highest equal betweenness centrality.

        
        Returns:
            List  integers, denoting top k nodes based on betweenness
            centrality and their value 
        """
        l={}
        for i in self.vertices:
            l[i]=self.betweenness_centrality(i)                            #dict of nodes and their betweenness centrality value
        max1=max(list(l.values()))                                         #max1 stores the max betweenness centrality value
        
        for i in l:
            if l[i]==max1:                                               #checking if the BC value equal to the max value , if yes it is appended in list m 
                m.append(i)
        return (m,max1)
                     
        raise NotImplementedError
    
    def answer(self):
        (a,max1)=self.top_k_betweenness_centrality()
        k=len(a)                                   #tells number of top nodes
        a=str(a)
        a=a.replace("[","")                       #removing brackets from a to change format of output
        a=a.replace("]","")
        if k==1:
            print("Answer:k= 1 , SBC=",max1,", Top '1' node:",a)
        else:
            print("Answer:k=",k,", SBC=",max1,", Top '",k,"' nodes:",a)
        return
        
        



if __name__ == "__main__":
    vertices =[1, 2, 3, 4, 5, 6]
    edges = [[1, 2], [1, 5], [2, 3], [2, 5], [3, 4], [4, 5], [4, 6]]
    graph = Graph(vertices, edges)
    s=graph.answer()
    
