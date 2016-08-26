#login.py

"""
routing for oauth
need to inspect a bug where the site will take too long to respond in certain cases where the user is logged in; current solution is to go to /logout, which redirects to the homepage
"""

from functools import wraps
from flask_oauthlib.client import OAuth
from flask import Flask, request, render_template, jsonify, abort, send_file, redirect, url_for, session


from app import google, oauth, db, e

class Permissions():
    approved_emails = []
    conn = e.connect()
    qry = conn.execute("SELECT email FROM user")
    user_emails = [dict(zip(tuple (qry.keys()) ,i)) for i in qry.cursor]
    for n in range(len(user_emails)):
        for a in user_emails[n].keys():
            approved_emails.append(user_emails[n][a])

    def __init__(self):
        self.login = False
        self.authorized = False
        self.current_user = None
        self.current_user_email = None
        self.current_user_name = None

    def update_user(self):
        try:
            if 'google_token' in session:
                self.login = True
                self.current_user = google.get('userinfo').data
                self.current_user_email = self.current_user['email']
                self.current_user_name = self.current_user['given_name']
                if self.current_user_email and self.current_user_email in Permissions.approved_emails:
                    self.authorized = True
            else:
                self.login = False
                self.authorized = False
                self.current_user = None
                self.current_user_email = None
                self.current_user_name = None
        except:
            self.login = False
            self.authorized = False
            self.current_user = None
            self.current_user_email = None
            self.current_user_name = None

    def logout_user(self):
        self.current_user = None
        self.current_user_email = None
        self.current_user_name = None
        self.authorized = False

    def validate_user(self):
        return [self.login,self.current_user_name,self.authorized]
