import csv

file_loc = "test.csv"

timeList = ["timestamp (date)", "runtime (s)"]

datatypesList = ["co2", "%RH", "last type"]

with open(file_loc, 'a', newline='') as csv_file:
    csv_writer = csv.writer(csv_file)
    csv_writer.writerow(timeList + datatypesList)