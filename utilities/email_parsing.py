def parse_emails():
    emails = []
    conn = eUser.connect()
    qry = conn.execute("SELECT email FROM user")
    user_email = ({'data': [dict(zip(tuple (qry.keys()) ,i)) for i in qry.cursor]})
    return user_email
    # return jsonify(user_email)

emails = []
conn = eUser.connect()
qry = conn.execute("SELECT email FROM user")
user_email = {'data': [dict(zip(tuple (qry.keys()) ,i)) for i in qry.cursor]}

emails = []
conn = eUser.connect()
qry = conn.execute("SELECT email FROM user")
user_email = [dict(zip(tuple (qry.keys()) ,i)) for i in qry.cursor]