from tkinter import Tk,Canvas
import math

Idtbl=[None,None,None,None,None,None,None,None,None,None]
cantouch=[None,None,None,None,None,None,None,None,None,None]
notnull=[]
allrooms=[]
prngNum = int(input("What is the seed? "))
#resolution = int(input('What is the resolution (10 is recommended): '))   Will change later
roomamt= int(input("how many rooms? "))



def Prng(limit):
    global prngNum
    prngNum = (prngNum*154687469+879190747) % 67280421310721
    return prngNum % limit

def find_dir(dir_index):
    if dir_index==0:
        return (1,0)
    if dir_index== 1:
        return (-1,0)
    if dir_index== 2:
        return (0,1)
    if dir_index== 3:
        return (0,-1)
    if dir_index == 4:
        return (-1,-1)
    if dir_index == 5:
        return (1,-1)
    if dir_index == 6:
        return (-1,1)
    if dir_index == 7:
        return (1,1)
    
    

def dungeon_master():
    """The main man stan that controls the map"""
    while True:
        x = Prng(len(Idtbl))
        y= Prng(len(Idtbl))
        works, typ=format(3, x, y)
        if works == True:
            allrooms.append(Room(3, typ, x, y))
            break
    while True:
        works = False
        """repats until all the rooms needed are created"""
        if len(allrooms) == roomamt:
            break
        moveX,moveY=find_dir( Prng(4) )
        Xpos, Ypos = notnull[ Prng(len(notnull)) ]
        newX, newY = Xpos+moveX, Ypos+moveY
        """creates either a trap room or a boss room"""
        try:
            Idtbl[newX][newY]
        except:
            pass
        else:
            if Idtbl[newX][newY]==0 and cantouch[Xpos][Ypos] == 0:
                if Idtbl[Xpos][Ypos] == 2:
                    size = 4
                    works, typ = format(size, newX, newY)
                if Idtbl[Xpos][Ypos] == 3 or Idtbl[Xpos][Ypos] == 4:
                    size = 2
                    works, typ = format(size, newX,newY)
                if works == True:
                    allrooms.append(Room(size, typ, newX,newY))
                    newdoor(Xpos, Ypos) # adds a new door at the starting values of the place made
                    newdoor(newX, newY) # adds a new door at the new values so they can be connected
                    
    walls()
    draw()




def format(size, sx ,sy):
    for typ in range(4):
        works= True
        for y in range(size):
            for x in range(size):
                """sets a new postion for the room to check all values in the room"""
                if typ == 0:
                    newY= sy+y
                    newX= sx+x
                if typ == 1:
                    newY= sy+y
                    newX = sx-x
                if typ == 2:
                    newY= sy-y
                    newX= sx-x
                if typ == 3:
                    newY= sy-y
                    newX = sx+x
                """Checks if that new values is illegal"""
                if x==0: #stores the row for the row the whole block should be on
                    keepY= newY
                try:
                    if Idtbl[newX][newY] != 0:
                        works=False
                except:
                    works=False
                    break
                if contains_value(notnull,(newX,newY)) or keepY != newY or works==False:
                    works= False
                    break #breaks from X loop
        if works == False:
            break # breaks from Y loop and goes to a new typ
        else:
            return(works,typ)
        
    return (False, typ)  # returns False because none of the types work



class Room:
    def __init__(self,size,how,sX,sY):
        self.tipe= size
        self.blocks=[]
        self.door_count =0
        if size != 3:
            self.monsters= Prng(3)
        else:
            self.monsters= 4  #special code for the boss
        for y in range(size):
            for x in range(size):
                if how == 0:
                    newY= sY+y
                    newX= sX+x
                if how == 1:
                    newY= sY+y
                    newX = sX-x
                if how == 2:
                    newY= sY-y
                    newX= sX-x
                if how == 3:
                    newY= sY-y
                    newX = sX+x
                packedpos=(newX,newY)
                Idtbl[newX][newY]=size
                notnull.append(packedpos)                
                self.blocks.append(packedpos)
        print(self.blocks)
        update()
    
    def rooms(self):
        return self.blocks
    
    def door(self):
        self.door_count+= 1    
    
def newdoor(doorX, doorY):
    for i in allrooms:
        try:
            i.blocks.index((doorX,doorY))
        except:
            pass
        else:
            i.door()
            Idtbl[doorX][doorY] += 5
            break
    


def update():
    for y in range(10):
        for x in range(10):
            pas = True
            for d in range(4):
                dirX, dirY = find_dir(d)
                neighborX, neighborY= dirX + x, dirY + y
                try:
                    Idtbl[neighborX][neighborY]
                except:
                    pas=False
                    break
            if not contains_value(notnull,(neighborX, neighborY)):
                pas=False
                break
            if pas== True and cantouch[x][y]==0:
                cantouch[x][y]=1
                notnull.remove((x,y))
                
def draw():
    master = Tk()
    dungeon= Canvas(master,width=1000,height=1000)
    for y in range(10):
        for x in range (10):
            o='black'
            ide = Idtbl[x][y] % 5
            if ide == 0:
                f= 'gray'
            elif ide == 1:
                f= 'black'
            elif ide == 2:
                f = 'blue'
            elif ide == 3:
                f= 'green'
            elif ide == 4:
                f='red'
            if Idtbl[x][y] > 4:
                o='brown'
            dungeon.create_rectangle(x*10,y*10,(x+1)*10,(y+1)*10,fill=f,outline=o) 
            dungeon.pack()
    master.mainloop()        

                


def contains_value(list_to_check,value):
    """Checks if a value is in a list"""
    for y in list_to_check:
        if y==value:
            return True
    return False


def walls():
    for y in range(10):
        for x in range(10):
            if contains_value(notnull, (x,y)):
                for direction in range(8):
                    nx,ny = find_dir(direction)
                    neighborX, neighborY = nx+x, ny+y
                    try:
                        if Idtbl[neighborX][neighborY]== 0:
                            Idtbl[neighborX][neighborY]=1 
                    except:
                        pass

def setup(): 
    for y in range (10):
        Idtbl[y]=[0,0,0,0,0,0,0,0,0,0]
        cantouch[y]=[0,0,0,0,0,0,0,0,0,0]
    dungeon_master()
setup()






