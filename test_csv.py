import csv

# csv header
fieldnames = ['length', 'breadth', 'height']

# csv data
rows = [
    {'length': 23,
    'breadth': 22,
    'height': 9},
    {'length': 10,
    'breadth': 11,
    'height': 12},
    {'length': 10,
    'breadth': 19,
    'height': 23}
]

with open('data.csv', 'w', encoding='UTF8', newline='') as f:
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(rows)