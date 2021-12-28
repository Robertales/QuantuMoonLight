import csv


def addId(filename):



    with open(filename, 'r') as input, open('IdFeatureDataset.csv', 'w') as output:
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

    with open('IdFeatureDataset.csv') as input, open('IdFeatureDataset_compatted.csv', 'w', newline='') as output:
        writer = csv.writer(output)
        for row in csv.reader(input):
            if any(field.strip() for field in row):
                writer.writerow(row)

    return 0

#print(addId('bupa.csv'))