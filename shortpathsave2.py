#requires numpy and pygraph

from numpy import *
import os
import wx
import wx.grid


##------------------------------##
##                              ##
##  wxgrid class                ##
##   creates the grid!          ##
##                              ##
##------------------------------##
class bboardgrid(wx.Frame):
    
    def __init__(self,parent,id,G):
        wx.Frame.__init__(self,parent,id,'Breadboard', size=(1194,250))
        grid = wx.grid.Grid(self)
        grid.CreateGrid(10,64)
        grid.SetRowLabelSize(22)
        grid.SetColMinimalAcceptableWidth(10)
        for row in range(10):
            t1=chr(row+97)
            grid.SetRowLabelValue(row,t1)
            for col in range(64):
                t2=str(col+1)
                t=t1+t2
                grid.SetColLabelValue(col,t2)
                grid.SetColSize(col,18)
                grid.SetCellValue(row, col, t)
                grid.SetCellBackgroundColour(row,col,wx.CYAN)
                grid.SetReadOnly(row, col, isReadOnly=True)
        print "Right click where you want to start."

        grid.Bind(wx.grid.EVT_GRID_CELL_LEFT_CLICK, self.OnCellLeftClick)

        print G
    def OnCellLeftClick(self, event):
        print "hello"
        GetCellValue()
        return(2)
            
        

def gridcontrol(G):
    app=wx.PySimpleApp()
    frame=bboardgrid(parent=None,id=-1,G)
    frame.Show()
    app.MainLoop()

##------------------------------##
##                              ##
##  shortest distance from beg  ##
##  to end                      ##
##                              ##
##------------------------------##

def shortpath(G,beg,end):
    # fix this !!!!!!!!!!!!!!!!!!!!!!
    # fix this !!!!!!!!!!!!!!!!!!!!!!
    # fix the way cost is calculated
    

    visited = {beg:0}
    path={}
    #must explicitly copy instead of just using G2=G. Python makes references not copys
    #otherwise: G=G2, altering G changes G2
    G2=dict(G)
    #find all paths!
    while G2:
        shortnode = 0
        for node in G2:
            #find shortest path from a node
            if node in visited:
                if shortnode == 0:
                    #print "found a smaller one"
                    shortnode=node
                elif visited[node] < visited[shortnode]:
                    shortnode = node

        if shortnode == 0:
            print "break"
            break

        tempcost = visited[shortnode]
        for edge in G2[shortnode]:
            cost = tempcost + G2[shortnode][edge]
            if edge not in visited or cost < visited[edge]:
                visited[edge] = cost
                path[edge] = shortnode
                
        del G2[shortnode]

    #shortest path    
    shortestpath = [end]
    cost=0

    while end != beg:
        shortestpath.append(path[end])
        end = path[end]
    shortestpath.reverse()

    #find the cost
    temp=0
    for nodes in shortestpath:
        if temp != 0:
            cost = cost+G[temp][nodes]
        temp=nodes

    print "Your shortest path is: "
    print shortestpath
    print "\n"
    print "At a cost of: ", cost
    
    temp=raw_input('Would you like to append the graph and continue (y/n)?  ')
    if temp == 'y':
        appendpath(shortestpath,G)
    elif temp == 'n':
        start()
        
##------------------------------##
##                              ##
##  append the graph            ##
##                              ##
##------------------------------##        

def appendpath(shortestpath,G):
    for things in shortestpath:
        del G[things]
    adjust(G)
 
##------------------------------##
##                              ##
##  create a user generated     ##
##  graph                       ##
##                              ##
##------------------------------##
    
def graphinput():
    clearscreen()
    
    G={}
    print '###############################################'
    print '#                                             #'
    print '#                 Create a graph              #'
    print '#                                             #'
    print '#     The data you input is placed in         #'
    print '#     dictionarys so it must be typed in      #'
    print '#     the proper format.                      #'
    print '#                                             #'
    print '#     Every edge from every node must be      #'
    print '#     inputed.                                #'
    print '#                                             #'
    print '#     ex: node 1 goes to 3,4, and 5 at a      #'
    print '#         weight of 1 would be inputed as     #'
    print '#                                             #'
    print '#     Node: 1                                 #'
    print '#     Paths from node:  3                     #'
    print '#     Path 1: 3                               #'
    print '#     Weight 1:  1                            #'
    print '#     Path2:  4                               #'
    print '#     Weight 2:  1                            #'
    print '#     Path 3:  5                              #'
    print '#     Weight 3:  1                            #'
    print '#                                             #'
    print '#     Node 3 must also go back to 1, 4 to 1   #'
    print '#     and 5 to 1 unless it is one way.        #'
    print '#                                             #'
    print '###############################################'
    print '\n'
    print '\n'
    
    numNode = input("how many nodes are there:  ")
    G={}
    for ii in range(1,numNode+1):
        temp=str(ii)
        tempStr1 = "Node "+temp+":  "
        tempNode = raw_input(tempStr1)
        tempStr2 = "How many paths from node "+tempNode+":  "
        tempPaths = input(tempStr2)
        # Fix this !!!!!!!!!!!!!
        # fix this !!!!!!!!!!!!!
        #could probably reset this somewhere else
        tempDict={}
        for jj in range(1,tempPaths+1):
            temp=str(jj)
            tempStr1 = "Path "+temp+":   "
            tempNodePath = raw_input(tempStr1)
            tempStr2 = "Weight "+tempNodePath+":   "
            tempWeight = input(tempStr2)
            tempDict[tempNodePath]=tempWeight
        G[tempNode]=tempDict
    adjust(G)
    
##------------------------------##
##                              ##
##  generate the default graph  ##
##                              ##
##------------------------------##
 
def breadboard():
    clearscreen()
    print '###############################################'
    print '#                                             #'
    print '#                 Breadboard                  #'
    print '#                                             #'
    print '#  This creates a graph based on a simple     #'
    print '#  breadboard with rows a-j, columns 1-64     #'
    print '#                                             #'
    print '#  Holes are labeled a1 through j64           #'
    print '#                                             #'
    print '###############################################'
    print '\n'
    print '\n'
    input=raw_input("Press enter to continue")
    G={}
    #grid=zeros((10,64))
    for ii in range(1,10+1):
        for kk in range(1,64+1):
            #grid[ii-1][kk-1]=chr(ii+96)+str(kk)
            temp=chr(ii+96)+str(kk)
            #top row
            if ii == 1:
                if kk == 1:
                    G[temp]={chr(ii+96)+str(kk+1):1, chr(ii+97)+str(kk):1}
                elif kk == 64:
                    G[temp]={chr(ii+96)+str(kk-1):1, chr(ii+97)+str(kk):1}
                else:
                    G[temp]={chr(ii+96)+str(kk-1):1, chr(ii+96)+str(kk+1):1, chr(ii+97)+str(kk):1}
            #bottom row
            elif ii == 10:
                if kk == 1:
                    G[temp]={chr(ii+96)+str(kk+1):1, chr(ii+95)+str(kk):1}
                elif kk == 64:
                    G[temp]={chr(ii+96)+str(kk-1):1, chr(ii+95)+str(kk):1}
                else:
                    G[temp]={chr(ii+96)+str(kk-1):1, chr(ii+96)+str(kk+1):1, chr(ii+95)+str(kk):1}
            #every other row
            else:
                if kk == 1:
                    G[temp]={chr(ii+96)+str(kk+1):1, chr(ii+95)+str(kk):1, chr(ii+97)+str(kk):1}
                elif kk == 64:
                    G[temp]={chr(ii+96)+str(kk-1):1, chr(ii+95)+str(kk):1, chr(ii+97)+str(kk):1}
                else:
                    G[temp]={chr(ii+96)+str(kk-1):1, chr(ii+96)+str(kk+1):1, chr(ii+95)+str(kk):1, chr(ii+97)+str(kk):1}               

    print "\n"
    temp=raw_input("Would you like to use the grid? (y/n)  ")
    if temp == 'y':
        gridcontrol(G)
    adjust(G)


##--------------------------##
##                          ##
## clear the screen         ##
##                          ##
##--------------------------##
def clearscreen():
    if os.name == 'nt':
        os.system("cls")
    else:
        os.system("clear")      

##--------------------------##
##                          ##
##  continue to minipulate  ##
##  a graph                 ##
##                          ##
##--------------------------##

def adjust(G):
    clearscreen()
    print G
    print '\n'
    print '\n'
    beg = raw_input('Where do you want to start?  ')
    end = raw_input('Where do you want to end?    ')
    shortpath(G,beg,end)

##--------------------------##
##                          ##
##  Some info on the script ##
##                          ##
##--------------------------##  
def info():
    clearscreen()
    print '###############################################'
    print '#                                             #'
    print '#                 Info                        #'
    print '#                                             #'
    print '#     This script finds the shortest path of  #'
    print '#     a graph. Graphs are stored as           #'
    print '#     dictonaries of dictionarys as follows:  #'
    print '#                                             #'
    print '#                   1                         #'
    print '#                  / \                        #'
    print '#                 /   \                       #'
    print '#                2     3---4                  #'
    print '#                                             #'
    print '# =={1:{2:1,3:1},2:{1:1},3:{1:1,4:1},4:{3:1}} #'
    print '#                                             #'
    print '###############################################'
    print '\n'
    print '\n'
    temp = raw_input("Press enter to continue.")
    start()
##--------------------------##
##                          ##
##  This is main()          ##
##                          ##
##--------------------------##        
def start():

    clearscreen()

    print '###############################################'
    print '#                                             #'
    print '#                 Make a selection            #'
    print '#                                             #'
    print '#     0:  Information                         #'
    print '#     1:  Create a graph                      #'
    print '#     2:  Breadboard Graph                    #'
    print '#     3:  Test a simple graph                 #'
    print '#     4:  close                               #'
    print '#                                             #'
    print '###############################################'
    print '\n'
    print '\n'

    G = {'1':{'2':5,'3':8,'4':1}, '2':{'1':5,'3':3,'5':1}, '3':{'1':8,'7':1,'6':1}, '4':{'1':1,'4':1,'5':1,'6':1,'7':1},'5':{'2':1,'4':1},'6':{'3':1,'4':1,'7':1},'7':{'3':1,'4':1,'6':1,'8':1},'8':{'7':1}}
    G2 = {'AUGUSTA':{'ATLANTA':120,'AIKEN':30}, 'AIKEN':{'AUGUSTA':30, 'COLUMBIA':50}, 'COLUMBIA':{'AIKEN':50,'GREENVILLE':60,'CHARLOTTE':50,'CHARLESTON':100,'FLORENCE':80},
          'GREENVILLE':{'COLUMBIA':60}, 'CHARLOTTE':{'COLUMBIA':50},'CHARLESTON':{'COLUMBIA':100,'SAVANNAH':40},'FORENCE':{'COLUMBIA':80},
          'ATLANTA':{'AUGUSTA':120,'MACON':50},'MACON':{'ATLANTA':50,'SAVANNAH':100,'TIFTON':80}, 'SAVANNAH':{'CHARLESTON':40,'MACON':100}}

    choice = input("What do you want to do?   ")
    if choice == 1:
        graphinput()
    elif choice == 2:
        breadboard()
    elif choice == 3:
        adjust(G)
    elif choice == 0:
        info()
        
start()



