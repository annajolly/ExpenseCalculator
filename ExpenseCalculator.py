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
            singleExpense = line.split(",")
            expenses.append(singleExpense)
        return [limit,expenses]
    except IOError:
        print "IO Error"
    except:
        print "Unexpected error:", sys.exc_info()[0]
        raise
    ref.close()
"""
def UpdateLimit(address,newLimit)
    try:
        in = open(address,"r")
        input = in.readlines()
        del input[0]
        in.close()
        out = open(address,"w")
        out.write(newLimit)
        for line in input
            out.write(line)
        out.close()
    except IOError:
        print "IO Error"
    except:
        print "Unexpected error:", sys.exc_info()[0]
        raise
"""
#layout webpage
def Layout(name, limit, expenses):
    print "Content-Type: text/html\n"
    print "<html>"
    print "<head>"
    print "<title>Expense Report For %s</title>" % (name,)
    print "</head>"
    print "Current daily allowance: %s" % (limit,)
    print "<form name=\"input\" action=\"./feedPage.py\" method=\"post\">"
    print "Update allowance: <input type=\"text\" name=\"updateAllowance\">"
    print "<input type=\"hidden\" name=\"doUpdate\" value=\"1\">"
    print "<input type=\"hidden\" name=\"name\" value=\"%s\">" % (name,)
    print "</form>"
    print "Previous expenses:"
    print "  YYYY/MM/DD    Amount    Description  "
    for expense in expenses:
        print "  %s    $%s    %s" % (expense[0],expense[1], expense[2],)
    print "<form name=\"input\" action=\"./feedPage.py\" method=\"post\">"
    print "Add an expense:"
    print "Date(YYYY/MM/DD): <input type=\"text\" name=\"date\">"
    print "Amount: $ <input type=\"text\" name=\"amount\">"
    print "Description: <input type=\"text\" name=\"description\">"
    print "<input type=\"hidden\" name=\"addExpense\" value=\"1\">"
    print "<input type=\"hidden\" name=\"name\" value=\"%s\">" % (name,)
    print "</form>"
    print "</html>"
    
name = form["name"].value
fileName = "/home/2014/ajolly3/public_html/" + name + ".csv"

if "import" in form:
    limitAndExpenses = ReadUserInfo(fileName)
    limit = limitAndExpenses[0]
    expenses = limitAndExpenses[1]

if "updateLimit" in form:
    UpdateLimit(name, form["newLimit"].value)
Layout(name, limit, expenses)
