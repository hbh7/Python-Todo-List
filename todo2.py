import sqlite3
import sys
import time
import os

fromRetrieve = False

def buildCursor(): # Create a cursor object to use to reference the database
    global conn
    conn = sqlite3.connect('todoList2.db')
    global cursor 
    cursor = conn.cursor()

def cls(): # Clear the screen depending on system and configuration
    global inIdle
    if inIdle == False:
        os.system('cls' if os.name == 'nt' else 'clear')
    else:
        print ("-"*40)

def inputData(): 
    task = input('Task: ')
    priority = input('Priority: ') 
    if priority.isnumeric() == False: 
        print ("Invalid Input")
        time.sleep(1)
        cls()
        return
    completed = False
    # Generate an ID
    list1 = []
    inList = True
    IDPos = 0
    sql = "select id from todoList"
    data = cursor.execute(sql)
    for id1 in data.fetchall():
        id2 = id1[0]
        list1.append(id2)
    while inList == True:
        if list1.count(IDPos) != 0:
            IDPos = IDPos + 1
        else:
            inList = False
    # End 
    sql = ''' INSERT INTO todoList
              (id, task, priority, completed)
              VALUES (:st_id, :st_task, :st_priority, :st_completed)'''
    cursor.execute(sql, {'st_id':IDPos, 'st_task':task, 'st_priority':priority, 'st_completed':completed})
    conn.commit()
    #cls()

def viewData():
    list1 = []
    sql = "select * from todoList"
    data = cursor.execute(sql)
    for task in data.fetchall():
        list1.append(task)
    for item in list1:
        id = item[0]
        Vtask = item[1]
        Vpriority = item[2]
        Vcompleted = item[3]
        if Vcompleted == 0:
            Vcompleted = "No" 
        elif Vcompleted == 1:
            Vcompleted = "Yes"
        else:
            Vcompleted = "ERROR"
        
        print ("----------")
        print ("ID:", id)
        print ("Task:",Vtask)
        print ("Priority:",Vpriority)
        print ("Completed:",Vcompleted)
        
    print ("----------")

    global fromRetrieve
    fromRetrieve = True

def modifyData():
    taskID = input("Which task (ID) do you want to modify? ")
    toModify = input("What do you want to modify? [name, priority, completed] ")
    if (toModify.lower()).strip() == "name" or (toModify.lower()).strip() == "n":
        newText = input("New Name: ")
        cursor.execute("""UPDATE todoList SET task = ? WHERE id = ?""", (newText, taskID))
    elif (toModify.lower()).strip() == "priority" or (toModify.lower()).strip() == "p":
        newPriority = input("New Priority: ")
        if priority.isnumeric() == False: 
            print ("Invalid Input")
            time.sleep(1)
            cls()
            return
        else:
            cursor.execute("""UPDATE todoList SET priority = ? WHERE id = ?""", (newPriority, taskID))
    elif (toModify.lower()).strip() == "completed" or (toModify.lower()).strip() == "c": 
        newCompletedPre = input("Completed? [yes][no] ")
        if newCompletedPre.lower() == "yes":
            newCompleted = 1
        elif newCompletedPre.lower() == "no":
            newCompleted = 0
        else:
            print ("Invalid Input")
        cursor.execute("""UPDATE todoList SET completed = ? WHERE id = ?""", (newCompleted, taskID))
    else:
        print ("Invalid Input")
    conn.commit()
    cls()

def removeData():
    taskID = input("Which task (id) do you want to delete? ")
    cursor.execute("""DELETE FROM todoList WHERE id=?""", (taskID))
    conn.commit()
    cls()

# Start
run = True
buildCursor()
try:
    sql = '''create table todoList (
        id int, 
        task text,
        priority int,
        completed bool)'''
    cursor.execute(sql)
    print ("Database setup invalid, building...")
except:
    print ("Database setup valid, continuing...")
    
print('Running in IDLE' if 'idlelib.run' in sys.modules else 'Not running in IDLE')
if 'idlelib.run' in sys.modules:
    inIdle = True
else:
    inIdle = False 
    
time.sleep(.5)
cls()

while run == True:
    print ("Welcome to your Todo List!")
    viewData()
    control = input("Please select an option. [Input][View][Modify][Remove][Exit]: ")
    if (control.lower()).strip() == "input" or (control.lower()).strip() == "i":
        inputData()
    elif (control.lower()).strip() == "view" or (control.lower()).strip() == "v":
        viewData()
    elif (control.lower()).strip() == "modify" or (control.lower()).strip() == "m":
        modifyData()
    elif (control.lower()).strip() == "remove" or (control.lower()).strip() == "r":
        removeData()
    elif (control.lower()).strip() == "exit" or (control.lower()).strip() == "e":
        run = False
    else:
        print ("Invalid Input")
        time.sleep(1)

cursor.close() 
