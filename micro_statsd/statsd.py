import socket
from functools import wraps


def to_async(func):
    @wraps(func)
    async def wrapper(*args, **kwargs):
        return func(*args, **kwargs)
    return wrapper


class Stats:
    """
    StatsD client

    >>> stats = Stats()  # or Stats('localhost', 8125)
    >>> stats.send(name='foo', value='bar', type_=Stats.TYPE_COUNTER)
    """
    TCP = socket.SOCK_STREAM
    UDP = socket.SOCK_DGRAM

    TYPE_COUNTER = 'c'
    TYPE_TIMER = 'ms'
    TYPE_GAUGE = 'g'
    TYPE_SET = 's'

    def __init__(
        self, host: str='localhost', port: int=8125, protocol: int=UDP,
    ):
        self.host = host
        self.port = port
        self.protocol = protocol
        self.socket = None

        self.open_socket()

    def __del__(self):
        self.socket.close()

    def open_socket(self):
        self.socket = socket.socket(socket.AF_INET, self.protocol)
        self.socket.connect((self.host, self.port))

    def send(self, name: str, value, type_: str, sampling=None):
        """
        Generic send stat method it might be simpler
        to use shortcuts such as stats.counter(...) etc.

        >>> stats.send('my_event', 1, Stat.TYPE_COUNTER)
        """
        message = '{name}:{value}|{type_}'.format(
            name=name, value=value, type_=type_,
        )

        if sampling:
            message += '|@{}'.format(sampling)

        try:
            self.socket.sendall(str.encode(message))
        except socket.error:
            # watching for log server health
            # is not a logger responsibility
            pass

    def counter(self, name: str, value: float=1, sampling: float=None):
        """
        Counts event number per second

        >>> stats.counter('my_event', 1)
        """
        self.send(
            name=name, value=value, type_=Stats.TYPE_COUNTER,
            sampling=sampling,
        )

    def timer(self, name: str, duration: float, sampling: float=None):
        """
        Logs event duration in milliseconds

        >>> stats.timer('my_event', 300)  # my event lasted 300 ms
        """
        self.send(
            name=name, value=duration, type_=Stats.TYPE_TIMER,
            sampling=sampling,
        )

    def gauge(self, name: str, value):
        """
        Keeps last updated value until the next update

        >>> stats.gauge('my_indicator', 30)

        # increment previously set value by one
        >>> stats.gauge('my_indicator', '+1')
        """
        self.send(name=name, value=value, type_=Stats.TYPE_GAUGE)

    def set(self, name: str, value: float):
        """
        Counts number of unique sent values.
        For example if you send consequently 6, 5, 6, 5, 2, 2,
        the number of unique values (6, 5 and 2) will be 3.

        >>> stats.set('unique_users', 8844)  # by user_id
        """
        self.send(name=name, value=value, type_=Stats.TYPE_SET)

    async_send = to_async(send)
    async_counter = to_async(counter)
    async_timer = to_async(timer)
    async_gauge = to_async(gauge)
    async_set = to_async(set)


