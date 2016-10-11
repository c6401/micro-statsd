# Micro StatsD python3 client

Micro StatsD one evening python3 client project, please don't use it. )

## How to install

    git clone https://github.com/c6401/micro-statsd
    cd micro-statsd
    python setup.py install

## How to uninstall

Please use following recipe: http://stackoverflow.com/questions/1550226/python-setup-py-uninstall/1550235#1550235

## Examples

```python3
from micro_statsd import Stats


client = Stats('localhost', 8125, Stats.UDP)
# or just:
# client = Stats()

client.counter('my_event', 1, sampling=0.1)
client.counter('my_counter', 3)
client.timer('my_timer', 10, sampling=0.1)
client.gauge('my_gauge', 3)
client.gauge('my_gauge', '+1')
client.set('my_set', 1)
```

## Async Examples

```python3
await client.async_counter('my_counter', 3)
await client.async_timer('my_timer', 10, sampling=0.1)
await client.async_gauge('my_gauge', 3)
await client.async_set('my_set', 1)
```

## Кun tests
To run tests simply install requirements-test.txt
and run nosetests from project directory
