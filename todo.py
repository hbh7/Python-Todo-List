import sqlite3
import sys
import time
import os

fromRetrieve = False

def buildCursor():
    global conn
    conn = sqlite3.connect('todoList.db')
    global cursor 
    cursor = conn.cursor()

def cls():
    global inIdle
    if inIdle == False:
        os.system('cls' if os.name == 'nt' else 'clear')
    else:
        print ("-"*40)

def inputData():
    task = input('Task: ')
    priority = input('Priority: ')
    completed = False
    sql = ''' INSERT INTO todoList
              (task, priority, completed)
              VALUES (:st_task, :st_priority, :st_completed)'''
    cursor.execute(sql, {'st_task':task, 'st_priority':priority, 'st_completed':completed})
    conn.commit()
    cls()

def viewData():
    list1 = []
    sql = "select * from todoList"
    data = cursor.execute(sql)
    for task in data.fetchall():
        list1.append(task)
    for item in list1:
        Vtask = item[0]
        Vpriority = item[1]
        Vcompleted = item[2]
        if Vcompleted == 0:
            Vcompleted = "No" 
        elif Vcompleted == 1:
            Vcompleted = "Yes"
        else:
            Vcompleted = "ERROR"
        
        print ("----------")
        print ("Task:",Vtask)
        print ("Priority:",Vpriority)
        print ("Completed:",Vcompleted)
        
    print ("----------")

    global fromRetrieve
    fromRetrieve = True

def modifyData():
    task = input("Which task do you want to modify? ")
    toModify = input("What do you want to modify? [name, priority, completed] ")
    if (toModify.lower()).strip() == "name" or (toModify.lower()).strip() == "n":
        newText = input("New Name: ")
        cursor.execute("""UPDATE todoList SET task = ? WHERE task = ?""", (newText, task))
    elif (toModify.lower()).strip() == "priority" or (toModify.lower()).strip() == "p":
        newPriority = input("New Priority: ")
        cursor.execute("""UPDATE todoList SET priority = ? WHERE task = ?""", (newPriority, task))
    elif (toModify.lower()).strip() == "completed" or (toModify.lower()).strip() == "c": 
        newCompletedPre = input("Completed? [yes][no] ")
        if newCompletedPre.lower() == "yes":
            newCompleted = 1
        elif newCompletedPre.lower() == "no":
            newCompleted = 0
        else:
            print ("Invalid Input")
        cursor.execute("""UPDATE todoList SET completed = ? WHERE task = ?""", (newCompleted, task))
    else:
        print ("Invalid Input")
    conn.commit()
    cls()

def removeData():
    task = input("Which task do you want to delete? ")
    cursor.execute("""DELETE FROM todoList WHERE task=?""", (task,))
    conn.commit()
    cls()

# Start
run = True
buildCursor()
try:
    sql = '''create table todoList (
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
    
time.sleep(.75)
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
