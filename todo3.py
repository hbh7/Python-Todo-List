import sqlite3
import sys
import time
import os

fromRetrieve = False

def buildCursor(): # Create a cursor object to use to reference the database
    global conn
    conn = sqlite3.connect('todoList3.db')
    global cursor 
    cursor = conn.cursor()

def cls(): # Clear the screen depending on system and configuration
    global inIdle
    if inIdle == False:
        os.system('cls' if os.name == 'nt' else 'clear')
    else:
        print ("-"*40)

def inputData():  # Input new task to the database
    task = input('Task: ') # Task name
    priority = input('Priority: ') # Priority for the task 
    if priority.isnumeric() == False: # Make sure priority is a number
        print ("Invalid Input")
        time.sleep(1) 
        cls()
        return # Exit early if not
    completed = False # Set completed to false because obviously its not done if you just added it
    # Generate an ID
    list1 = [] # Build a list of IDs in use
    inList = True
    IDPos = 0
    sql = "select id from todoList"
    data = cursor.execute(sql)
    for id1 in data.fetchall(): # Iterate through all IDs in database, choose next unused ID. 
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
    conn.commit() # Write to database. 
    cls()

def viewData():
    list1 = []
    sql = "select * from todoList"
    data = cursor.execute(sql)
    for task in data.fetchall(): # Get all items in database, add to list
        list1.append(task)
    for item in list1: # Set up for displaying
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
        # Display retrieved data for each entry 
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
        newText = input("New Name: ") # Get new value, execute
        cursor.execute("""UPDATE todoList SET task = ? WHERE id = ?""", (newText, taskID))
    elif (toModify.lower()).strip() == "priority" or (toModify.lower()).strip() == "p":
        newPriority = input("New Priority: ")  # Get new value
        if priority.isnumeric() == False: # Check that its a number
            print ("Invalid Input")
            time.sleep(1)
            cls()
            return
        else:
            cursor.execute("""UPDATE todoList SET priority = ? WHERE id = ?""", (newPriority, taskID)) # Write to database
    elif (toModify.lower()).strip() == "completed" or (toModify.lower()).strip() == "c": 
        newCompletedPre = input("Completed? [yes][no] ")
        if newCompletedPre.lower() == "yes":
            newCompleted = 1 # Change to 1 for yes, 0 for no
        elif newCompletedPre.lower() == "no":
            newCompleted = 0
        else:
            print ("Invalid Input")
        cursor.execute("""UPDATE todoList SET completed = ? WHERE id = ?""", (newCompleted, taskID)) # Write to database.
    else:
        print ("Invalid Input")
    conn.commit() # Write to database.
    cls()

def removeData():
    taskID = input("Which task (id) do you want to delete? ")
    cursor.execute("""DELETE FROM todoList WHERE id=?""", (taskID))
    conn.commit() # Write to database.
    cls()

# Start
run = True
buildCursor()
try: # Check if database setup is valid or not, if no database found, make one
    sql = '''create table todoList (
        id int, 
        task text,
        priority int,
        completed bool)'''
    cursor.execute(sql)
    print ("Database setup invalid, building...")
except: # if found, then use it. 
    print ("Database setup valid, continuing...")
    
print('Running in IDLE' if 'idlelib.run' in sys.modules else 'Not running in IDLE')
if 'idlelib.run' in sys.modules: # Check if running in idle or not, and set a variable for use in CLS
    inIdle = True
else:
    inIdle = False 
    
time.sleep(.5)
cls()

while run == True: # Main loop
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
# Exit cleanly. 