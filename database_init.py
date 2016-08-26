#database_init.py
from flask_sqlalchemy import SQLAlchemy

from app import app, db, keys
from app.models import ep1, ep2, ep3, ep4, user, ep1_annotations

"NOTE: must comment out the import of api and views in __init__.py"

app.config['SQLALCHEMY_DATABASE_URI'] = keys.db_name_from_keys
print keys.db_name_from_keys
# e = create_engine(keys.db_name_from_keys)
db.create_all()

def add_data(database, csvfile, columns, db=db):
    #database is the database that is being added onto
    #csvfile is the file full of data
    #columnes is a list of the columns in the database (MUST align with the number of entries per row in the csv file)
    #db should be db (from flask)
    kwargs_default = {}
    for n in columns:
        kwargs_default[n] = ''
    f = open(csvfile, 'r')
    for line in f:
        kwargs = kwargs_default
        row = []
        for item in line.split(","):
            row.append(item.strip('\n').strip('"'))
        for n in range(len(columns)):
            kwargs[columns[n]] = row[n]
        db.session.add(database(**kwargs))
        db.session.commit()

"Working calls"

# add_data(ep1,'../CSV/ep1.csv',['id','timestart','timeend','dialogue'])
# add_data(ep2,'../CSV/ep2.csv',['id','timestart','timeend','dialogue'])
# add_data(ep3,'../CSV/ep3.csv',['id','timestart','timeend','dialogue'])
# add_data(ep4,'../CSV/ep4.csv',['id','timestart','timeend','dialogue'])

"""
Annotation Hierarchy:
category_name||character_name||timestart||timeend||durration||type
"""

def add_annotation_data(database, csvfile, columns=('id','category_name','character_name','timestart','timeend','durration','type'), non_characters=('scene_division','actions_social','context_social','location','number_on_screen'),db=db):
    #columns = category_name,character_name,timestart,timeend,durration,type
    #corrects empty cells in non-character entries, formats time data from MM:SS.MS to HH:MM:SS.MS, and adds an entry for ID to be used as a primary key
    #tested with the episode ELAN data, exported as a tab-delimited text file, and converted to a CSV in excel
    kwargs_default = {}
    id = 1
    for n in columns:
        kwargs_default[n] = ''
    f = open(csvfile,'r')
    for line in f:
        kwargs = kwargs_default
        row = []
        for item in line.split(','):
            row.append(item)
        if row[0] in non_characters:
            #testing whether the row is a character entry
            for n in range(len(columns)):
                if n == 0:
                    kwargs[columns[n]] = id
                    id += 1
                elif n == 2:
                    kwargs[columns[n]] = None
                elif columns[n] == 'timestart' or columns[n] == 'timeend' or columns[n] == 'durration':
                    #adding two zeros to the front of the time entry so the query is consistent across databases
                    kwargs[columns[n]] = '00:%s'%row[n-1]
                else:
                    kwargs[columns[n]] = row[n-1]
        else:
            for n in range(len(columns)):
                if n == 0:
                    kwargs[columns[n]] = id
                    id += 1
                else:
                    kwargs[columns[n]] = row[n-1]
        db.session.add(database(**kwargs))
        db.session.commit()

"Working call"

# add_annotation_data(ep1_annotations,'../CSV/episode_one.csv', ('id','category_name','character_name','timestart','timeend','durration','type'))

def add_user(email, name, db=db):
    kwargs = {}
    kwargs['email'] = email
    kwargs['name'] = name
    db.session.add(user(**kwargs))
    db.session.commit()

"Working call"

# add_user(db, 'sbrooks2@oberlin.edu','Sawyer')
