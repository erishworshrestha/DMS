# import xlsxwriter module
import xlsxwriter

# Workbook() takes one, non-optional, argument
# which is the filename that we want to create.
workbook = xlsxwriter.Workbook('test.xlsx')

# The workbook object is then used to add new
# worksheet via the add_worksheet() method.
worksheet = workbook.add_worksheet()

# Use the worksheet object to write
# data via the write() method.
worksheet.write('A1', 'length')
worksheet.write('B1', 'breadth')
worksheet.write('C1', 'height')
worksheet.write('D1', 'weight')

# Finally, close the Excel file
# via the close() method.
workbook.close()
