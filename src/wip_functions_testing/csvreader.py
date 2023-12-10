# simple script to read data from csv file of radii and angles
import csv

with open('armcntdata.csv') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    radii = []
    angles = []
    line_count = 0
    for row in csv_reader:
        radii.append(row[4])
        angles.append(row[3])
        line_count += 1
    del radii[0]
    del angles[0]
    for x in range(len(radii)):
        radii[x] = float(radii[x])
    for y in range(len(angles)):
        angles[y] = float(angles[y])
    print(radii)
    print(angles)
    print(f'Processed {line_count} lines.')