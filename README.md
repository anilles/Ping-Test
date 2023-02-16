# Ping-Test
A program I created to pull hostname and IP addresses from an .xlsx file run ping test on the data and return the results of the test to the .xlsx file as a new column.

Running Pinglest

In your Ticket Queue make sure you have the following columns.

Number, Configuration item

Export your spreadsheet from ServiceNow as a .xlsx file.

Move the .xlsx file to the same directory as the PingTest.exe file.

Close any windows accessing that .xlsx file as the program will replace the file upon completion.

When you run the program it will open a terminal window and ask what file you would like to import.

Enter the filename including the file .format. Example (SheetName.xlsx)
It will find the “Configuration item” column, ping each device, and then append the spreadsheet.

When you open the spreadsheet there will now be a new column called "Response" This will show the result of the Ping test and the hostname/ip that was pinged if you entered “y” when prompted.
If your .xlsx file is read as a Page and not a Sheet then a new Sheet will be created as “Sheet” on the bottom of your Excel window.
