# Ihr-Intake-Automated-Scripts


# Steps to convert SmartSheet to the right format before runing the script

1) Save Smartsheet as .csv
2) Remove all columns only have these as columns input (LastName, FirstName, DOB, PolicyId, SubscriberId, RallyId)
3) Convert DOB to this format: mmmm/mm/dd

# Steps to run the script

1) copy the csv file to the base dir.  Current input filename is myList.csv
2) Execute the following command: python CHTest.py 
   or python CHTest.py > results.log


   CHTest.py uses input file myList.csv
   CHTest_Integration.py uses input file myList_Integration.csv
   CHTest_LoadTest.py uses input file myList_LoadTest.csv
   CHTest_BlueSteel.py uses input file myList_BlueSteel.csv




