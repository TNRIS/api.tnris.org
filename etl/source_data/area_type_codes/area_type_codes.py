# script to apply fips, quad, and qquad area_code field in the area_type table
import csv

# set aside county fips
county_dict = {}
with open('counties.csv') as counties:
    reader = csv.DictReader(counties)
    for row in reader:
        county_dict[row['CNTY_NM']] = row['FIPS']

# set aside quad numbers
quad_dict = {}
with open('quads.csv') as quads:
    reader = csv.DictReader(quads)
    for row in reader:
        quad_dict[row['quadname']] = row['quadnum']

# set aside qquad number
qquad_dict = {
    'NE': '2',
    'NW': '1',
    'SE': '4',
    'SW': '3'
}

errors = []

# open original for reading
with open('area_type_original.csv') as orig:
    reader = csv.DictReader(orig)
    header = reader.fieldnames
    # open new file
    with open('area_type_codes.csv', 'w') as output:
        writer = csv.DictWriter(output, fieldnames=header)
        writer.writeheader()
        for row in reader:
            area_type = row['area_type']
            area_type_name = row['area_type_name']
            try:
                if area_type == 'state':
                    row['area_code'] = '48'
                    writer.writerow(row)
                elif area_type == 'county':
                    row['area_code'] = county_dict[area_type_name]
                    writer.writerow(row)
                elif area_type == 'quad':
                    row['area_code'] = quad_dict[area_type_name]
                    writer.writerow(row)
                elif area_type == 'qquad':
                    quad_name = area_type_name.split('|')[0]
                    quarter = area_type_name.split('|')[1]
                    qquad = quad_dict[quad_name] + qquad_dict[quarter]
                    row['area_code'] = qquad
                    writer.writerow(row)
                else:
                    print("uh oh, weird area_type:")
                    print(row)
            except Exception as e:
                errors.append((area_type, area_type_name))

# print errors
for e in errors:
    print(e)
print('%s total errors' % len(errors))

print("that's all folks!!")
