import asyncio
import unittest

from mock import Mock, patch

from micro_statsd import Stats


class TestStats(unittest.TestCase):
    def setUp(self):
        self.loop = asyncio.get_event_loop()

        self.mock_socket = Mock()
        self.mock_sendall = self.mock_socket.return_value.sendall
        self.patch_socket = patch(
            'micro_statsd.statsd.socket.socket', self.mock_socket
        )
        self.patch_socket.start()

        self.client = Stats()

    def tearDown(self):
        self.patch_socket.stop()
        self.loop.stop()

    def test_send(self):
        self.client.send('my_event1', 42, Stats.TYPE_COUNTER)
        self.mock_sendall.assert_called_once_with(b'my_event1:42|c')

    def test_send_with_sampling(self):
        self.client.send('my_event2', 43, Stats.TYPE_COUNTER, 0.1)
        self.mock_sendall.assert_called_once_with(b'my_event2:43|c|@0.1')

    def test_counter(self):
        self.client.counter('my_counter1', 44)
        self.mock_sendall.assert_called_once_with(b'my_counter1:44|c')

    def test_counter_with_sampling(self):
        self.client.counter('my_counter2', 45, 0.2)
        self.mock_sendall.assert_called_once_with(b'my_counter2:45|c|@0.2')

    def test_timer(self):
        self.client.timer('my_timer1', 46)
        self.mock_sendall.assert_called_once_with(b'my_timer1:46|ms')

    def test_timer_with_sampling(self):
        self.client.timer('my_timer2', 47, 0.3)
        self.mock_sendall.assert_called_once_with(b'my_timer2:47|ms|@0.3')

    def test_gauge(self):
        self.client.gauge('my_gauge', 48)
        self.mock_sendall.assert_called_once_with(b'my_gauge:48|g')

    def test_gauge_addition(self):
        self.client.gauge('my_gauge', '+1')
        self.mock_sendall.assert_called_once_with(b'my_gauge:+1|g')

    def test_set(self):
        self.client.set('my_set', 49)
        self.mock_sendall.assert_called_once_with(b'my_set:49|s')

    def test_async_send(self):
        self.loop.run_until_complete(
            self.client.async_send('my_event3', 50, Stats.TYPE_COUNTER, 0.4)
        )
        self.mock_sendall.assert_called_once_with(b'my_event3:50|c|@0.4')

    def test_async_counter(self):
        self.loop.run_until_complete(
            self.client.async_counter(
                'my_counter3', 51, 0.5
            )
        )
        self.mock_sendall.assert_called_once_with(b'my_counter3:51|c|@0.5')

    def test_async_timer(self):
        self.loop.run_until_complete(
            self.client.async_timer('my_timer3', 52, 0.6)
        )
        self.mock_sendall.assert_called_once_with(b'my_timer3:52|ms|@0.6')

    def test_async_gauge(self):
        self.loop.run_until_complete(
            self.client.async_gauge('my_gauge2', 53)
        )
        self.mock_sendall.assert_called_once_with(b'my_gauge2:53|g')

    def test_async_set(self):
        self.loop.run_until_complete(
            self.client.async_set('my_set2', 54)
        )
        self.mock_sendall.assert_called_once_with(b'my_set2:54|s')