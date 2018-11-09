import csv
import os
import psycopg2
import datetime
import uuid


database = os.environ.get('DB_NAME')
username = os.environ.get('DB_USER')
password = os.environ.get('DB_PASSWORD')
host = os.environ.get('DB_HOST')
port = os.environ.get('DB_PORT')

conn_string = "dbname='%s' user='%s' host='%s' password='%s' port='%s'" % (database, username, host, password, port)

# connect to database
conn = psycopg2.connect(conn_string)
cur = conn.cursor()

# clear out collection_county_relate table
newQuery = "DELETE FROM collection_county_relate"
print(newQuery)
cur.execute(newQuery)
conn.commit()


# quad uuid to area_code relationship
quad_code = {}
query = "SELECT * FROM area_type WHERE area_type = 'quad';"
cur.execute(query)
response = cur.fetchall()
for r in response:
    # quad_code[area_code] = area_type_id
    quad_code[r[6]] = r[0]
print('quad area_code ref built')

# qquad to quad relationship
qq_ref = {}
query = "SELECT * FROM area_type WHERE area_type = 'qquad';"
cur.execute(query)
response = cur.fetchall()
for r in response:
    # all but last character should be the area_code of the quad it belongs to
    code = r[6][:-1]
    # get quad area_type_id based on area_code
    quad_uuid = quad_code[code]
    # qq_ref[qquad area_type_id] = quad area_type_id
    qq_ref[r[0]] = quad_uuid
print('qquad to quad built')

# quad to county relationship
quad_cnty_ref = {}
with open('county_quad.csv', newline='') as file:
    reader = csv.DictReader(file)
    for r in reader:
        quad_id = r['area_type1']
        cnty_id = r['area_type_']
        if quad_id not in quad_cnty_ref:
            quad_cnty_ref[quad_id] = [cnty_id]
        else:
            current =  quad_cnty_ref[quad_id]
            current.append(cnty_id)
            quad_cnty_ref[quad_id] = current
print('quad to county built')

# get county UUIDs from area_type table for use with statewide datasets
all_county_uuids = []
query = "SELECT * FROM area_type WHERE area_type = 'county';"
cur.execute(query)
response = cur.fetchall()
for r in response:
    all_county_uuids.append(r[0])
print('county uuid list created')

# get all collections with joined template for the interation
query = "select collection.collection_id, template_type.template from collection left join template_type on template_type.template_type_id=collection.template_type_id;"
cur.execute(query)
response = cur.fetchall()
bad_areas = []
for r in response:
    coll_id = r[0]
    template = r[1]
    # if template is tnris-order, skip. these need to be done manually
    if template == 'tnris-order':
        print('order ' + coll_id)
        continue
    # if template is outside-entity, apply all Counties
    if template == 'outside-entity':
        print('outside entity ' + coll_id)
        for c in all_county_uuids:
            # insert into the Database
            newUuid = uuid.uuid4()
            timestamp = datetime.datetime.now()
            newQuery = "INSERT INTO collection_county_relate (id, created, last_modified, collection_id, area_type_id) VALUES ('%s', '%s', '%s', '%s', '%s')" % (newUuid, timestamp, timestamp, coll_id, c)
            cur.execute(newQuery)
            conn.commit()
    # if template is tnris-download, lookup resources
    if template == 'tnris-download':
        print('download ' + coll_id)
        # check for state, if so - apply all counties
        q = "select resource.collection_id, resource.area_type_id, area_type.area_type from resource left join area_type on area_type.area_type_id=resource.area_type_id WHERE collection_id = '%s' and area_type.area_type = 'state'" % (coll_id)
        cur.execute(q)
        res = cur.fetchall()
        if len(res) != 0:
            print('statewide')
            for c in all_county_uuids:
                # insert into the Database
                newUuid = uuid.uuid4()
                timestamp = datetime.datetime.now()
                newQuery = "INSERT INTO collection_county_relate (id, created, last_modified, collection_id, area_type_id) VALUES ('%s', '%s', '%s', '%s', '%s')" % (newUuid, timestamp, timestamp, coll_id, c)
                cur.execute(newQuery)
                conn.commit()
        else:
            print('piece mealz')
            # since not definitively statewide, create list of counties based
            # on county, quad, and qquad coverage
            q = "select resource.collection_id, resource.area_type_id, area_type.area_type from resource left join area_type on area_type.area_type_id=resource.area_type_id WHERE collection_id = '%s' and area_type.area_type != 'state'" % (coll_id)
            cur.execute(q)
            res = cur.fetchall()
            these_county_uuids = []
            print(these_county_uuids)
            for t in res:
                a_t_id = t[1]
                a_t = t[2]
                print(a_t, a_t_id)
                # if a county add to the list
                if a_t == 'county':
                    # but only add to the list if not already in there
                    if a_t_id not in these_county_uuids:
                        these_county_uuids.append(a_t_id)
                # if quad, lookup county and add it to the list
                elif a_t == 'quad':
                    try:
                        related_cnty_uuid_list = quad_cnty_ref[a_t_id]
                        for rcul in related_cnty_uuid_list:
                            # but only add to the list if not already in there
                            if rcul not in these_county_uuids:
                                these_county_uuids.append(rcul)
                    except:
                        print('bad related quad: ' + related_quad)
                        bad_areas.append(related_quad)
                # if qquad, lookup related quad, then use it to lookup county
                # and add it to the list
                elif 'qquad':
                    related_quad = qq_ref[a_t_id]
                    print(related_quad)
                    try:
                        related_cnty_uuid_list = quad_cnty_ref[related_quad]
                        for rcul in related_cnty_uuid_list:
                            # but only add to the list if not already in there
                            if rcul not in these_county_uuids:
                                these_county_uuids.append(rcul)
                    except:
                        print('bad qquad related quad: ' + related_quad)
                        bad_areas.append(related_quad)
                else:
                    # not a county, quad, or qquad? that shouldn't be possible
                    print("WHAAAAA?????")
                    print(t)
            print(these_county_uuids)
            for c in these_county_uuids:
                # insert into the Database
                newUuid = uuid.uuid4()
                timestamp = datetime.datetime.now()
                print(c)
                newQuery = "INSERT INTO collection_county_relate (id, created, last_modified, collection_id, area_type_id) VALUES ('%s', '%s', '%s', '%s', '%s')" % (newUuid, timestamp, timestamp, coll_id, c)
                print(newQuery)
                cur.execute(newQuery)
                conn.commit()

###########
cur.close()
conn.close()
print('--------------------------------')
print(bad_areas)
print("that's all folks!!")
