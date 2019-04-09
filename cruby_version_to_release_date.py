import datetime

INPUT_FILE = 'cruby_results2.csv'
DATE_FILE = 'cruby_release_dates.txt'
OUTPUT_FILE = 'cruby_results2_date.csv'

def raw_data():
    with open(INPUT_FILE, 'r') as f:
        raw_data = f.read()
    raw_data = raw_data.strip('\n').split('\n')

    for data in raw_data:
        yield data

def mapping():
    with open(DATE_FILE, 'r') as f:
        mapping = f.read()
    mapping = mapping.strip('\n').split('\n')

    version_to_date = {}
    for row in mapping:
        version, date = row.split('\t')
        year, month, day = date.split('-')
        date = datetime.date(
            year=int(year),
            month=int(month),
            day=int(day))

        # the version is of the form
        # Ruby 2.0.0-p594

        ruby, semver = version.split(' ')

        # if semver[0] == '1': # version 1.Y.Z, DC
        #     continue

        # if semver.split('.')[1] == '0': # 2.0.Y, DC
        #     continue

        version_to_date.update({semver: date})

    return version_to_date

version_to_date = mapping()
data = raw_data()

date_row = []
for row in data:
    cruby, version, *other = row.split(',')
    semver = version[5:]

    if semver not in version_to_date:
        print(f'Version {semver} has unknown release date!')
        continue

    version_date = version_to_date[semver]
    date_row.append((version_date, row))

date_row.sort()
earliest = date_row[0][0]

transformed_data = []
for row in date_row:
    days_since = (row[0] - earliest).days
    cruby, version, *other = row[1].split(',')
    transformed_row = [cruby, version, str(days_since), *other]
    transformed_data.append(transformed_row)

with open(OUTPUT_FILE, 'w+') as f:
    for row in transformed_data:
        f.write(','.join(row) + '\n')
