import datetime

# ruby-2.0.0-p195
EARLIEST_DATE = datetime.date(2013, 5, 14)

INPUT_FILE = 'jruby_results3.csv'
DATE_FILE = 'jruby_release_dates.txt'
OUTPUT_FILE = 'jruby_results3_date.csv'

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
        version, date = row.split(',')
        month, day, year = date.split('-')
        date = datetime.date(
            year=int(year),
            month=int(month),
            day=int(day))

        # the version is of the form
        # 1.7.9

        version_to_date.update({version: date})

    return version_to_date

version_to_date = mapping()
data = raw_data()

date_row = []
for row in data:
    jruby, version, *other = row.split(',')
    semver = version[6:]

    if semver not in version_to_date:
        print(f'Version {semver} has unknown release date!')
        continue

    version_date = version_to_date[semver]
    date_row.append((version_date, row))

date_row.sort()

transformed_data = []
for row in date_row:
    days_since = (row[0] - EARLIEST_DATE).days
    jruby, version, *other = row[1].split(',')
    transformed_row = [jruby, version, str(days_since), *other]
    transformed_data.append(transformed_row)

print(date_row[0])

with open(OUTPUT_FILE, 'w+') as f:
    for row in transformed_data:
        f.write(','.join(row) + '\n')
