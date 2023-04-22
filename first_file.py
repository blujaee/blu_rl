import mysql.connector

import hashlib

from flask import Flask, render_template, request

from datetime import datetime

import random

import config

blurl = mysql.connector.connect(
    host=config.DB_HOST,
    user=config.DB_USER,
    password=config.DB_PASSWORD,
    database=config.DB_DATABASE
)

mycursor = blurl.cursor()

app = Flask(__name__)

@app.route('/')
def url_form():
    return render_template('url_form.html')

@app.route('/shorten', methods=['POST'])
def shorten_url():
    original_url = request.form['original_url']
    hash_object = hashlib.sha256(original_url.encode())
    hash_hex = hash_object.hexdigest()[:8]
    random_addition = str(random.random()).encode('utf-8')[:4]
    short_url = (request.host_url + hash_hex + random_addition.decode('utf-8')).encode('utf-8')
    sql = "INSERT INTO urls (original_url, date_created, hash, short_url) VALUES (%s, %s, %s, %s)"
    val = (original_url, datetime.now(), hash_hex, short_url)
    mycursor.execute(sql, val)
    blurl.commit()

    sql = "SELECT original_url FROM urls WHERE short_url = %s"
    val = (short_url,)
    mycursor.execute(sql, val)
    result = mycursor.fetchone()
    if result is None:
        return "short URL not found"
    else:
        return 'Short URL: {}'.format(short_url)
    

if __name__ == '__main__':
    app.run(debug=True)
