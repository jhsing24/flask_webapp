#!/usr/bin/python3
'''
Create a database for the Twitter project.
'''

# sqlite3 is built in python3, no need to pip3 install
import sqlite3
import random
from datetime import datetime
# process command line arguments
import argparse
parser = argparse.ArgumentParser(description='Create a database for the twitter project')
parser.add_argument('--db_file', default='twitter_clone.db')
# there is no standard file extension; people use .db .sql .sql3 .database
args = parser.parse_args()

# connect to the database
con = sqlite3.connect(args.db_file)   # con, conn = connection; always exactly 1 of these variables per python project
cur = con.cursor()                    # cur = cursor; for our purposes, exactly 1 of these per python file

# create the users table
sql = '''
CREATE TABLE users (
    id INTEGER PRIMARY KEY,
    username TEXT NOT NULL UNIQUE,
    password TEXT NOT NULL,
    profile_picture TEXT NOT NULL,
    age INTEGER
);
'''
cur.execute(sql)     # cur.execute() actually runs the SQL code
con.commit()         # "commit" means "save" in SQL terminology; not always required, but never wrong

# create the messages table
sql = '''
create table messages (
    id integer primary key,
    sender_id integer not null,
    message text not null,
    created_at timestamp not null default current_timestamp
    );
'''
cur.execute(sql)
con.commit()

madlibs = [
    "[PETER] is always [SUPPORTIVE] of the [COMMUNITY] here in [INDIANA]. He is always subject to [CRITICISM], so unfair!",
    "[PETER], one of the [DEMOCRATIC PARTY]'s most [IN-DEMAND] campaign surrogates. He is a member of [BIDEN]'s transportation [CABINET].",
    "[TRANSPORTATION SECRETARY] Pete Buttigieg said [MONDAY] that travel infrastructure has [IMPROVED] since the [COUNTRY] saw [FLIGHT] cancellation spikes. The [DATA] proves him correct.",
    "[BUTTIGIEG] said he has [URGED] [AIRLINES] to “make sure their [SCHEDULES] are realistic.” It is important to work toward [INCREASING] staffing and pay for pilots.",
    "[PETER] said [TRUMP] can do whatever he [LIKES]. [PETER], however, does not [THINK] Trump will [WIN].",
    "[PETER] is [DEFINITELY] a [FAVORITE] for the 2024 election. His [CHARM], [INTELLIGENCE], and [GOOD LOOKS] make him an ideal candidate to many voters.",
    ]

replacements = {
    'PETER' : ['Buttigieg', 'The Secretary of Transportation', 'Peter Buttigieg', 'Mayor Pete'],
    'BIDEN' : ['Biden', 'Joe Biden', 'The President'],
    'SUPPORTIVE' : ['cognizant', 'mindful', 'conscious', 'aware'],
    'COMMUNITY' : ['people', 'public', 'residents', 'company'],
    'INDIANA' : ['his hometown', 'his neighborhood', 'his small town'],
    'CRITICISM' : ['verbal disapproval', 'objections', 'flak', 'condemnation'],
    'DEMOCRATIC PARTY' : ['Left', 'Democrat', 'Liberal'],
    'IN-DEMAND' : ['popular', 'sought after', 'accessible', 'familiar'],
    'CABINET' : ['committee', 'administration', 'council', 'key advisers'], 
    'TRANSPORTATION SECRETARY' : ['Head of Transportation', 'Transportation Lead', 'Transportation General'],
    'MONDAY' : ['early this week', 'earlier', 'a few days ago'],
    'IMPROVED' : ['gotten better', 'been amended', 'been updated', 'been upgraded'],
    'COUNTRY' : ['United States', 'nation', 'sovereign state of America'],
    'FLIGHT' : ['airline', 'airplane', 'airport', 'travel'],
    'DATA' : ['studies', 'research', 'incoming information', 'updated news'],
    'BUTTIGIEG' : ['Peter', 'the Secretary of Transportation', 'Peter Buttigieg', 'Mayor Pete'],
    'URGED' : ['advised', 'coaxed', 'suggested'],
    'AIRLINES' : ['air passenger carriers', 'air services', 'air taxis', 'airline companies'],
    'SCHEDULES' : ['agendas', 'calendars', 'chart trajectories', 'programming'],
    'INCREASING' : ['expanding', 'growing', 'developing', 'advancing'],
    'TRUMP' : ['Donald', 'Big D', 'Trumpie', 'Lil D'], 
    'LIKES' : ['desires', 'wants', 'can', 'seeks'],
    'THINK' : ['believe', 'accept', 'anticipate', 'expect'],
    'WIN' : ['succeed', 'gain victory over the others', 'beat him', 'even come close to winning'],
    'DEFINITELY' : ['certainly', 'absolutely', 'decidedly', 'indubitably'],
    'FAVORITE' : ['a preferred candidate', 'well-liked candidate', 'a preferred option', 'a popular choice'],
    'CHARM' : ['charisma', 'grace', 'agreeableness'],
    'INTELLIGENCE' : ['smarts,', 'wit', 'quick thinking abilities'],
    'GOOD LOOKS' : ['physical attractiveness', 'handsomeness', 'natural beauty'],

    }


def generate_comment():
    '''
    This function generates random comments according to the patterns specified in the `madlibs` variable.
    To implement this function, you should:
    1. Randomly select a string from the madlibs list.
    2. For each word contained in square brackets `[]`:
        Replace that word with a randomly selected word from the corresponding entry in the `replacements` dictionary.
    3. Return the resulting string.
    For example, if we randomly selected the madlib "I [LOVE] [PYTHON]",
    then the function might return "I like Python" or "I adore Programming".
    Notice that the word "Programming" is incorrectly capitalized in the second sentence.
    You do not have to worry about making the output grammatically correct inside this function.
    Instead, you should ensure that the madlibs that you create will all be grammatically correct when this substitution procedure is followed.
    '''

    madlib = random.choice(madlibs)
    for replacement in replacements.keys():
        madlib = madlib.replace('['+replacement+']', random.choice(replacements[replacement]))
    return madlib

def create_users_bulk():
    for i in range(250):
        username='user_'+'{num:>03}'.format(num=str(random.randint(1,100)))+'_'+'{num:>03}'.format(num=str(random.randint(1,100)))+'_'+'{num:>03}'.format(num=str(random.randint(1,100)))
        password='{num:>03}'.format(num=str(random.randint(1,100)))+'{num:>03}'.format(num=str(random.randint(1,100)))
        age = random.randint(1,100)
        url = 'https://robohash.org/'+username+'.png'
        try:
            cur.execute("insert into users (username, password, profile_picture, age) values (?,?,?,?);", [username,password,url,age])
        except:
            print('Duplicate username, moving on...')
# insert some dummy data
# cur.execute("insert into users (username, password, age) values ('Trump', 'Trump', 76);")
# cur.execute('''insert into users (username, password, age) values ('Biden', 'Biden', 79);''')
# cur.execute('''insert into users (username, password, age) values ('Evan', 'correct horse battery staple', 4);''')
# cur.execute('''insert into users (username, password, age) values ('Isaac', 'soccer', 1);''')
# cur.execute('''insert into users (username, password, age) values ('Aaron', 'guaguagua', 0);''')
# cur.execute('''insert into users (username, password, age) values ('Mike', '524euTjrWm6uK2C5iw8mC6aNgX1JI78o', 35);''')
# cur.execute('''insert into users (username, password) values ('Kristen', 'Possible-Rich-Absolute-Battle');''')
create_users_bulk()
def create_messages_bulk():
    cur = con.cursor()
    users=[]
    cur.execute('select id from users;')
    for user in cur.fetchall():
        users.append(user[0])
    for commenter_id in users:
        for i in range(200):
            comment = generate_comment()
            now = datetime.now()
            date_string = now.strftime('%Y-%m-%d %H:%M:%S')
            cur.execute("insert into messages (sender_id, message, created_at) values (?,?,?);", [commenter_id,comment,date_string])
create_messages_bulk()
con.commit()

