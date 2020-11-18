from datetime import datetime
from flask import Flask, request, render_template
import redis

app = Flask(__name__)
app.config.from_object('config')

db = redis.StrictRedis(
    host=app.config['DB_HOST'],
    port=app.config['DB_PORT'],
    db=app.config['DB_NO']
)

@app.route('/', methods=['GET'])
def main():
    return render_template('index.html', history=get_posts())

@app.route('/', methods=['POST'])
def add_message():
    text = request.form['text']
    tag = request.form['tag'] 
    if len(text) < 1:
        return render_template('index.html',
                               history=get_posts()) 
    post_id = str(db.incr("id"))
    
    db.hmset('post:' + post_id,
             dict(
                 date_time=datetime.strftime(datetime.now(), "%d.%m.%Y %H:%M:%S"),
                 text=text,
                 tag=tag))

    db.lpush('history:', str(post_id))
    return render_template('index.html', history=get_posts())


def get_posts():
    posts = db.lrange('history:', 0, -1)  
    history = []
    for post_id in posts:
    
        post = db.hgetall('post:' + str(post_id, 'utf-8')) 
        history.append(
            dict(
                date_time=post[b'date_time'].decode(),
                text=post[b'text'].decode(),
                tag=post[b'tag'].decode()))
    return history
