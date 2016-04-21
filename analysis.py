from datetime import datetime
import csv

with open('ped.csv', 'r') as f:

    rows = csv.reader(f)

    headers = next(rows)
    print(headers)

    for row in rows:
        name = row[0]
        date = row[1]
        date = datetime.strptime(date, '%d/%M/%Y')
        print(name, date)
