
import csv


def aggIdTesting(filename='Data_testing.csv'):
    with open(filename, 'r') as input, open('IdData_Testing.csv', 'w') as output:
        reader = csv.reader(input, delimiter=',')
        writer = csv.writer(output, delimiter=',')

        all = []
        row = next(reader)
        row.insert(0, 'Id')
        all.append(row)
        count = 0
        for row in reader:
            count += 1
            row.insert(0, count)
            all.append(row)
        writer.writerows(all)

    with open('IdData_Testing.csv') as input, open('IdData_Testing_compatted.csv', 'w', newline='') as output:
        writer = csv.writer(output)
        for row in csv.reader(input):
            if any(field.strip() for field in row):
                writer.writerow(row)