from flask import Flask
from redis.sentinel import Sentinel, MasterNotFoundError
import time
from io import StringIO

SENTINEL_HOST='redis-sentinel'

sentinel = Sentinel([(SENTINEL_HOST, 26379)], socket_timeout=0.1)

app = Flask(__name__)

@app.route('/')
def index():
    try:
      stream = StringIO()

      sentinel = Sentinel([('redis-sentinel', 26379)], socket_timeout=0.1)
      dm = sentinel.discover_master('dpf')
      ds = sentinel.discover_slaves('dpf')
      print('master:', dm, file=stream)
      print('slaves:', ds, file=stream)

      master = sentinel.master_for('dpf', socket_timeout=0.1)
      master.set('foo', time.asctime())
      slave = sentinel.slave_for('dpf', socket_timeout=0.1)
      print('get from redis:', slave.get('foo'), file=stream)

    except MasterNotFoundError as e:
      print('redis master is GONE, waiting for failover...', e, file=stream)
    except Exception as e:
      print('exception happened, connection lost?', e, file=stream)

    return '{}\n'.format(stream.getvalue())

if __name__=='__main__':
    app.run(debug=True)

