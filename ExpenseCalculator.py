#!/usr/bin/python

import sys
import cgi
import re
import subprocess

form = cgi.FieldStorage()

def isUser(name):
    try:
        ref = open("./users.csv","r")
        #OPTIMIZE THIS LOOP
        foundUser = False
        while (foundUser == False):
            user = ref.readline()
            if (user == (name+'\n')):
		return True
            elif user == '\n':
                return False
    except IOError:
        print "IO Error"
    except:
        print "Unexpected error:", sys.exc_info()[0]
        raise
    ref.close()

def CreateNewUser(name, limit):
    try:
        fileName = "./" + name + ".csv"
        ref = open(fileName, "w")
        ref.write(limit)
        ref2 = open("./users.csv", "a")
        ref2.write(name + "\n")
    except IOError:
        print "IO Error"
    except:
        print "Unexpected error:", sys.exc_info()[0]
        raise
    ref.close()
    ref2.close()
    subprocess.call(['chmod', '0755', fileName])

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
        else:
	    return [limit, []]
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

def addExpense(name, date, amount, description):
    try:
        ref = open("./" + name + ".csv", "a")
        ref.write(date + "," + amount + "," + description + '\n')
    except IOError:
        print "IOError"
    except:
        print "Unexpected error:", sys.exc_info()[0]
        raise
    ref.close()

# create new account webpage
def CreateNewAccount(name, init, error):
    print "Content-Type: text/html\n"
    print "<html>"
    print "<head>"
    print "<title>Create a new account</title>"
    print "</head>"
    if (init == "1"):
        print "That username does not exist.<br>"
    elif (error != "0"):
        print "Error: %s. Try again." % (error,)
    print "If you would like to create an account, fill out the following form and click \"Submit\".<br>"
    print "Else, click \"Cancel\" to go back to the sign-in page.<br>"
    print "<form name=\"createNewUser2\" action=\"./ExpenseCalculator.py\" method=\"post\">"
    print "<input type=\"hidden\" name=\"createNewUser\" value=\"1\">"
    print "Select a username (letters and numbers only): <input type=\"text\" name=\"name\">"
    print "Choose a daily allowance: <input type=\"text\" name=\"limit\">"
    print "<input type=\"submit\" value=\"Submit\">"
    print "</form>"
    print "<form action=\"./index.html\">"
    print "<input type=\"submit\" value=\"Cancel\">"
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
    print "<form name=\"addExpense\" action=\"./ExpenseCalculator.py\" method=\"post\">"
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
fileName = "./" + name + ".csv"

limit = ""
expenses = ""
noError = "0"
error= ""

if "import" in form:
    if (isUser(name) == True):
        limitAndExpenses = ReadUserInfo(fileName)
        limit = limitAndExpenses[0]
        expenses = limitAndExpenses[1]
        Layout(name, limit, expenses, noError)
    else:
        CreateNewAccount(name, "1", "0")

if "newLimit" in form:
    
    newLimit = form["newLimit"].value
    limitAndExpenses = ReadUserInfo(fileName)
    expenses = limitAndExpenses[1]
    if (not (re.search(r'[0-9]*[\.][0-9][0-9]',newLimit))):
	Layout(name, limit, expenses, "Allowance must be a number of form 12.00")
    else:
        limit = newLimit
        UpdateLimit(fileName, limit)
	Layout(name, limit, expenses, noError)
    
if "createNewUser" in form:
    if (not name.isalnum()):
        CreateNewAccount(name, "0", "Username must be alphanumeric characters only")    
    elif (not (re.search(r'[0-9]*[\.][0-9][0-9]',form["limit"].value))):
        CreateNewAccount(name, "0", "Allowance must be a number of form 12.00")
    else:
        CreateNewUser(name, form["limit"].value)
        limitAndExpenses = ReadUserInfo(fileName)
        limit = limitAndExpenses[0]
        expenses = limitAndExpenses[1]
        Layout(name, limit, expenses, noError)

if "addExpense" in form:
    date = form["date"].value
    amount = form["amount"].value
    description = form["description"].value
    limitAndExpenses = ReadUserInfo(fileName)
    expenses = limitAndExpenses[1]
    #check valid date 
    if (not (re.search(r'2[0-9][0-9][0-9][/][0-1][0-9][/][0-3][0-9]',date))):
        Layout(name, limit, expenses, "Date must be of format YYYY/MM/DD")
    elif (not (re.search(r'[0-9]*[\.][0-9][0-9]',amount))):
        Layout(name, limit, expenses, "Amount must be a floating point number")
    elif (not description.isalnum()):
        Layout(name, limit, expenses, "Description must be an alphanumeric string")
    else:
        addExpense(name, date, amount, description)
	Layout(name, limit, expenses, noError)
