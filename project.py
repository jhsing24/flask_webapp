from flask import Flask, render_template, send_from_directory, redirect, url_for, request, make_response
from datetime import datetime

import sqlite3
import json
app = Flask(__name__)

def good_login(username, password):
    con = sqlite3.connect('twitter_clone.db')
    cur = con.cursor()
    sql = "select password from users where username=?;"
    cur.execute(sql, [username])
    for row in cur.fetchall():
        if password==row[0]:
            return True
    return False

@app.route('/')     
def root():
    con = sqlite3.connect('twitter_clone.db')
    messages = []
    page = request.args.get('page', 1, type=int)
    offset = (page-1)*50
    sql = 'select sender_id, message, created_at from messages order by created_at desc limit 50 offset ?;'
    messages_cursor = con.cursor()
    messages_cursor.execute(sql, [offset])

    for message in messages_cursor.fetchall():
        sql2 = 'select username, age, profile_picture from users where id=?;'
        users_cursor = con.cursor()
        users_cursor.execute(sql2, [message[0]])
        for user in users_cursor:
            pass
        messages.append({
            'message': message[1],
            'created_at': message[2],
            'username': user[0],
            'profile_picture': user[2],
            'age': user[1]
        })
    
    username= request.cookies.get('username')
    password= request.cookies.get('password')
    good_creds = good_login(username, password)

    return render_template('root.html', messages=messages, loggedin=good_creds, page=page)


@app.route('/home.json')
def home_json():
    con = sqlite3.connect('twitter_clone.db')
    cur = con.cursor()
    cur.execute('''
        SELECT sender_id, message, created_at, id from messages;
    ''')
    rows = cur.fetchall()
    messages = []
    for row in rows:
        messages.append({'username': row[0], 'text': row[1], 'created_at':row[2], 'id':row[3]})
    messages.reverse()

    return json.dumps(messages)

@app.route('/login', methods=['GET', 'POST'])
def login():
    username=request.form.get('username')
    password=request.form.get('password')
    good_creds = good_login(username, password)
    if username is None:
        return render_template('login.html', bad_creds = False, logged_in=good_creds)
    else:
        if good_creds:
            response = make_response(redirect(url_for('root')))
            response.set_cookie('username', username)
            response.set_cookie('password', password)
            return response
        else:
            return render_template('login.html', bad_creds = True, logged_in=good_creds)

@app.route('/logout')     
def logout():
    response = make_response(render_template('logout.html'))
    response.delete_cookie('username')
    response.delete_cookie('password')
    return response

@app.route('/create_user', methods=['GET', 'POST'])     
def create_user():
    password = request.form.get('password')
    rep_password = request.form.get('rep_password')
    if password:
        if password==rep_password:
            username = request.form.get('username')
            age = request.form.get('age')
            con = sqlite3.connect('twitter_clone.db')
            cur = con.cursor()
            if age:
                sql="insert into users (username, password, profile_picture, age) values (?,?,?,?);"
                try:
                    url = 'https://robohash.org/'+username+'.png'
                    cur.execute(sql, [username, password, url, age])
                    con.commit()
                    response = make_response(redirect(url_for('root')))
                    response.set_cookie('username', username)
                    response.set_cookie('password', password)
                    return response
                except:
                    return render_template('create_user.html', error = True)
            else:
                sql="insert into users (username, password, profile_picture) values (?,?,?);"
                try:
                    url = 'https://robohash.org/'+username+'.png'
                    cur.execute(sql, [username, password, url])
                    con.commit()
                    response = make_response(redirect(url_for('root')))
                    response.set_cookie('username', username)
                    response.set_cookie('password', password)
                    return response
                except:
                    return render_template('create_user.html', error = True)
        else:
            return render_template('create_user.html', typo = True)
    else:
        return render_template('create_user.html')

@app.route('/create_message', methods=['GET', 'POST'])     
def create_message():
    message = request.form.get('message')
    username = request.cookies.get('username')
    password = request.cookies.get('password')
    good_creds = good_login(username, password)
    if message:
        con = sqlite3.connect('twitter_clone.db')
        cur = con.cursor()
        sql = "select id from users where username=?"
        try:
            cur.execute(sql,[username])
            for user in cur.fetchall():
                pass
            now = datetime.now()
            date_string = now.strftime('%Y-%m-%d %H:%M:%S')
            sql = "insert into messages (sender_id, message, created_at) values (?,?,?);"
            cur.execute(sql, [user[0], message, date_string])
            con.commit()
            return render_template('create_message.html', created=True, loggedin = good_creds)
        except:
            return render_template('create_message.html', error=True, loggedin = good_creds)

    else:
        return render_template('create_message.html', loggedin = good_creds)

@app.route('/user', methods=['GET', 'POST'])
def user():
    username = request.cookies.get('username')
    password = request.cookies.get('password')
    good_creds = good_login(username, password)
    if( good_creds ):
        con = sqlite3.connect('twitter_clone.db')
        cur = con.cursor()
        sql = "select id from users where username=?;"
        cur.execute(sql,[username])
        for user in cur.fetchall():
            pass
        page  = request.args.get('page', 1, type=int)
        offset = (page-1)*20
        cur.execute('''
            SELECT message, created_at, id from messages where sender_id=? order by created_at desc limit 20 offset ?;
        ''', [user[0], offset])
        rows = cur.fetchall()
        messages = []
        for row in rows:
            messages.append({'message': row[0], 'created_at': row[1], 'id':row[2]})
        return make_response(render_template('user.html', messages=messages, loggedin=good_creds, username=username, page=page))
    else: 
        return login()

@app.route('/change_password', methods=['GET', 'POST'])
def change_password():
    username = request.cookies.get('username')
    password = request.cookies.get('password')
    good_creds = good_login(username, password)
    old_password = request.form.get('oldpassword')
    new_password = request.form.get('newpassword')
    rep_new_password = request.form.get('rep_newpassword')
    if old_password and new_password and rep_new_password:
        if old_password != password:
            return render_template('change_password.html', loggedin = good_creds, wrong_pass = True)
        elif new_password != rep_new_password: 
            return render_template('change_password.html', loggedin = good_creds, typo = True)
        else:
            con = sqlite3.connect('twitter_clone.db')
            cur = con.cursor()
            sql = 'update users set password=? where username=?;'
            cur.execute(sql, [new_password, username])
            con.commit()
            response = make_response(render_template('change_password.html', loggedin = good_creds, changed = True))
            response.set_cookie('password', new_password)
            return response
    else:
        return render_template('change_password.html', loggedin = good_creds)

@app.route('/delete_message/<id>', methods=['GET'])
def delete_message(id):
    username = request.cookies.get('username')
    password = request.cookies.get('password')
    good_creds = good_login(username,password)
    con = sqlite3.connect("twitter_clone.db") 
    cur = con.cursor()
    cur.execute('''
        SELECT sender_id from messages where id=?;
    ''', (id,))
    for row in cur.fetchall():
        id_of_sender = row[0]
    cur.execute('''
        SELECT id from users where username=?;
    ''', [username])
    for row in cur.fetchall():
        current_id = row[0]
    if id_of_sender == current_id:
        cur.execute('''
            DELETE from messages where id=?;
        ''', (id,))
        con.commit()
    else:
        return make_response(render_template('delete_message.html', logged_not_your_message=True, loggedin=good_creds, username=request.cookies.get('username'), password=request.cookies.get('password')))
    return make_response(render_template('delete_message.html',  loggedin=good_creds,  username=request.cookies.get('username'), password=request.cookies.get('password')))

@app.route('/edit_message/<id>', methods=['POST', 'GET'])
def edit_message(id):
    username = request.cookies.get('username')
    password = request.cookies.get('password')
    good_creds = good_login(username,password)
    if request.form.get('newMessage'):
        con = sqlite3.connect('twitter_clone.db') 
        cur = con.cursor()
        cur.execute('''
        SELECT sender_id from messages where id=?;
        ''', (id,))
        for row in cur.fetchall():
            id_of_sender = row[0]
        cur.execute('''
            SELECT id from users where username=?;
        ''', [username])
        for row in cur.fetchall():
            current_id = row[0]
        if id_of_sender == current_id:
            new_message = request.form.get('newMessage')
            
            new_message += f' (edited {datetime.now().strftime("%Y-%m-%d %H:%M:%S")})'
            cur.execute('''
                UPDATE messages
                SET message = ?
                WHERE id = ?
            ''', (new_message,id))
            con.commit()
            return make_response(render_template('edit_message.html',allGood=True, id=id, username=request.cookies.get('username'), loggedin=good_creds))
        else:
            return make_response(render_template('edit_message.html',not_your=True, id=id, username=request.cookies.get('username'), loggedin=good_creds))
    else:
        return make_response(render_template('edit_message.html',default=True, id=id, username=request.cookies.get('username'), loggedin=good_creds))

@app.route('/search_message', methods=['POST', 'GET'])
def search_message():
    username = request.cookies.get('username')
    password = request.cookies.get('password')
    good_creds = good_login(username,password)
    if request.form.get('search'):
        search_term = f"%{request.form.get('search')}%"
        con = sqlite3.connect('twitter_clone.db') 
        cur = con.cursor()
        page  = request.args.get('page', 1, type=int)
        offset = (page-1)*20
        cur.execute('''
        SELECT sender_id, message, created_at, id from messages where message like ? order by created_at desc limit 20 offset ?;
        ''', [search_term, offset])
        rows = cur.fetchall()
        messages = []
        for row in rows:
            users = con.cursor()
            sql = 'select username, profile_picture from users where id=?;'
            users.execute(sql, [row[0]])
            for user in users.fetchall():
                pass
            messages.append({'username': user[0], 'message': row[1], 'created_at':row[2], 'id':row[3], 'profile_picture':user[1]})

        return render_template('search_message.html', messages=messages, username=request.cookies.get('username'), password=request.cookies.get('password'), page=page, loggedin=good_creds)
    else:
        return render_template('search_message.html', default=True, username=request.cookies.get('username'), password=request.cookies.get('password'), loggedin=good_creds)

@app.route('/static/<path>')
def static_directory(path):
    return send_from_directory('static', path) 

app.run()