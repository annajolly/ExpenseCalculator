#!/usr/bin/python

import sys
import cgi

form = cgi.FieldStorage()


def ReadUserInfo(address):
    try:
        # import set daily allowance and expenses
        ref = open(address,"r")
        limit = ref.readline()
        input = ref.readlines()
        expenses = []
        for line in input:
            if line != '\n':
		singleExpense = line.split(",")
        	expenses.append(singleExpense)
        return [limit,expenses]
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

#layout webpage
def Layout(name, limit, expenses):
    print "Content-Type: text/html\n"
    print "<html>"
    print "<head>"
    print "<title>Expense Report For %s</title>" % (name,)
    print "</head>"
    print "Current daily allowance: $%s" % (limit,)
    print "<form name=\"input\" action=\"./ExpenseCalculator.py\" method=\"post\">"
    print "Update allowance: $<input type=\"text\" name=\"newLimit\">"
    print "<input type=\"hidden\" name=\"import\" value=\"1\">"
    print "<input type=\"hidden\" name=\"name\" value=\"%s\">" % (name,)
    print "<input type=\"submit\" value=\"Submit\">"
    print "</form>"
    print "Previous expenses:<br>"
    print "  YYYY/MM/DD    Amount    Description  <br>"
    for expense in expenses:
        print "  %s    $%s    %s" % (expense[0],expense[1], expense[2],)
	print "<br>"
    print "<form name=\"input\" action=\"./expenseCalculator.py\" method=\"post\">"
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

if "newLimit" in form:
    UpdateLimit(fileName, form["newLimit"].value)

if "import" in form:
    limitAndExpenses = ReadUserInfo(fileName)
    limit = limitAndExpenses[0]
    expenses = limitAndExpenses[1]

Layout(name, limit, expenses)
