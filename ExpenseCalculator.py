#!/usr/bin/python

import sys
import cgi

form = cgi.FieldStorage()

def isUser(name):
    try:
        ref = open("/home/2014/ajolly3/public_html/users.csv","r")
        #OPTIMIZE THIS LOOP
        foundUser = false
        while (foundUser == false):
            user = ref.readline()
            if (user == name):
                foundUser = true
            [elif user == '\n':
             return false]
        return foundUser
    except IOError:
        print "IO Error"
    except:
        print "Unexpected error:", sys.exc_info()[0]
        raise
    ref.close()

def CreateNewUser(name, limit):
    try:
        fileName = "./" + name + ".csv"
        ref = open(filename, "w")
        ref.write(limit)
        ref2 = open("./users.csv", "a")
        ref2.write(name + '\n')
    except IOError:
        print "IO Error"
    except:
        print "Unexpected error:", sys.exc_info()[0]
        raise
    ref.close()
    ref2.close()

def ReadUserInfo(address):
    try:
        # import set daily allowance and expenses
        ref = open(address,"r")
        limit = ref.readline()
        input = []
        input = ref.readlines()
        if (input != []):
            expenses = []
            for line in input:
                if line != '\n':
                    singleExpense = line.split(",")
                    expenses.append(singleExpense)
            return [limit, expenses]
        [else:
         return [limit, []]]
    except IOError:
        print "IO Error"
    except:
        print "Unexpected error:", sys.exc_info()[0]
        raise
    ref.close()

def UpdateLimit(address, newLimit):
    try:
        inp = open(address,"r")
        input = inp.readlines()
        del input[0]
        inp.close()
        out = open(address,"w")
        out.write(newLimit + '\n')
	counter = 0
        for line in input:
            if line != '\n':
		if (counter == len(input)-1):
		     out.write(line)
		else:
		     out.write(line + '\n')
	    counter += 1
        out.close()
    except IOError:
        print "IO Error"
    except:
        print "Unexpected error:", sys.exc_info()[0]
        raise

def addExpense(name, date, amount, description)
    try:
        ref = open("./" + name + ".csv", "a")
        ref.write(date + "," + amount + "," + description + '\n')
    except IOError:
        print "IOError"
    except:
        print "Unexpected error:", sys.exc_info()[0]
        raise

# create new account webpage
def CreateNewAccount(name, init, error):
    print "Content-Type: text/html\n"
    print "<html>"
    print "<head>"
    print "<title>Create a new account</title>"
    print "</head>"
    if (init == "1"):
        print "That username does not exist."
    [elif (error != "0"):
     print "Error: %s. Try again." % (error,)
    print "If you would like to create an account, fill out the following form and click \"Submit\""
    print "Else, click \"Cancel\" to go back to the sign-in page.<br>"
    print "<form name=\"createNewUser\" action=\"./ExpenseCalculator.py\" method=\"post\">"
    print "Select a username (letters and numbers only): <input type=\"text\" name=\"name\">"
    print "Choose a daily allowance: <input type=\"text\" name=\"limit\">"
    print "<input type=\"submit\" value=\"Submit\">"
    print "</form>"

# REPLACE WITH SIMPLE LINK??:
    
    print "<form name=\"backToLogin\" action=\"./index.html\" method=\"post\">"
    print "<input type=\"cancel\" value=\"Cancel\">"
    print "</form>"
    
# layout webpage
def Layout(name, limit, expenses, error):
    print "Content-Type: text/html\n"
    print "<html>"
    print "<head>"
    print "<title>Expense Report For %s</title>" % (name,)
    print "</head>"
    if (error != "0"):
        print "Error: %s. Try again." % (error,)
    print "Current daily allowance: $%s" % (limit,)
    print "<form name=\"input\" action=\"./ExpenseCalculator.py\" method=\"post\">"
    print "Update allowance: $<input type=\"text\" name=\"newLimit\">"
    print "<input type=\"hidden\" name=\"name\" value=\"%s\">" % (name,)
    print "<input type=\"submit\" value=\"Submit\">"
    print "</form>"
    print "Previous expenses:<br>"
    print "  YYYY/MM/DD    Amount    Description  <br>"
    for expense in expenses:
        print "  %s    $%s    %s" % (expense[0],expense[1], expense[2],)
	print "<br>"
    print "<form name=\"addExpense\" action=\"./expenseCalculator.py\" method=\"post\">"
    print "Add an expense:"
    print "<br>"
    print "Date(YYYY/MM/DD): <input type=\"text\" name=\"date\"><br>"
    print "Amount: $<input type=\"text\" name=\"amount\"><br>"
    print "Description: <input type=\"text\" name=\"description\"><br>"
    print "<input type=\"hidden\" name=\"addExpense\" value=\"1\">"
    print "<input type=\"hidden\" name=\"name\" value=\"%s\">" % (name,)
    print "<input type=\"submit\" value=\"Submit\">"
    print "</form>"
    print "</html>"
    
name = form["name"].value
fileName = "/home/2014/ajolly3/public_html/" + name + ".csv"

limit = ""
expenses = ""
noError = "0"
error= ""

if "import" in form:
    if (isUser(name) == true):
        limitAndExpenses = ReadUserInfo(fileName)
        limit = limitAndExpenses[0]
        expenses = limitAndExpenses[1]
        Layout(name, limit, expenses, noError)
    [else:
     CreateNewAccount(name, "1", "0")]

if "newLimit" in form:
    newLimit = form["newLimit"].value
    
    # need "== true"?
    
    if (!newLimit.isdigit())
        Layout(name, limit, expenses, "Allowance must be a number")
    [else:
     limit = newLimit
     UpdateLimit(fileName, form["newLimit"].value)
     Layout(name, limit, expenses, error)]
    
if "createNewUser" in form:    
    if (!name.isalnum()):
        CreateNewAccount(name, "0", "Username must be alphanumeric characters only")    
    [elif (!form["limit"].value.isdigit()):
     CreateNewAccount(name, "0", "Allowance must be a number")]
    [else:
     CreateNewUser(name, form["limit"].value)]

if "addExpense" in form:
    date = form["date"].value
    amount = form["amount"].value
    description = form["description"].value

    #check valid date
    if (!date.isdigit()):
        Layout(name, limit, expense, "Date must be of format  ")

    [elif (!amount.isdigit()):
        Layout(name, limit, expense, "Amount must be a floating point number")]
    [elif (!description.isalnum()):
     Layout(name, limit, expense, "Description must be an alphanumeric string")]
    [else:
     addExpense(name, date, amount, description)]
