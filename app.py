from flask import Flask, request, render_template, redirect, url_for
import sqlite3

app = Flask(__name__)
conn = sqlite3.connect('database.db')
cur = conn.cursor()

class User:
    def __init__(self, username, password):
        self.username = username
        self.password = password
