def test_sort(qry):
    a = []
    for n in qry.__dict__:
        a.append(n)
    return a

def serialize(_query):
    #Formats SQLAlchemy output to be JSON readable
    #d = dictionary written to per row
    #D = dictionary d is written to each time, then reset
    #Master = dictionary of dictionaries; the id Key (int, unique from database) from D is used as the Key for the dictionary D entry in Master
    Master = {}
    D = {}
    x = 0
    for u in _query.__dict__.keys():
        d = u.__dict__
        D = {}
        for n in d.keys():
            if n != '_sa_instance_state':
                D[n] = d[n]
        x = d['id']
        Master[x] = D
    return Master

def _serialize(qry):
    for n in qry.keys():
        print n
        for a in n:
            print a