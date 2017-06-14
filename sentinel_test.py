from redis.sentinel import Sentinel, MasterNotFoundError

while True:
    import time

    try:
        sentinel = Sentinel([('redis-sentinel', 26379)], socket_timeout=0.1)
        dm = sentinel.discover_master('dpf')
        ds = sentinel.discover_slaves('dpf')
        print('master:', dm, '====>', 'slaves', ds)

        master = sentinel.master_for('dpf', socket_timeout=0.1)
        master.set('foo', time.asctime())
        slave = sentinel.slave_for('dpf', socket_timeout=0.1)
        print('get from redis:', slave.get('foo'))
    except MasterNotFoundError as e:
        print('redis master is GONE, waiting for failover...', e)
    except Exception as e:
        print('exception happened, connection lost?', e)

    time.sleep(1.0)