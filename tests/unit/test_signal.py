import unittest2
from asyncmongoorm import signal

class SignalTestCase(unittest2.TestCase):

    def test_connect_appends_receiver_on_receivers_list(self):
        some_signal = signal.Signal()

        class SomeCollection():
            pass

        def some_receiver():
            pass

        some_signal.connect(SomeCollection, some_receiver)

        handler = (SomeCollection, some_receiver)
        self.assertIn(handler, some_signal.receivers)

    def test_disconnect_removes_receiver_on_receivers_list(self):
        some_signal = signal.Signal()

        class SomeCollection():
            pass

        def some_receiver():
            pass

        some_signal.connect(SomeCollection, some_receiver)
        some_signal.disconnect(SomeCollection, some_receiver)

        self.assertNotIn(some_receiver, some_signal.receivers)

    def test_decorator_function_appends_receiver_on_receivers_list(self):
        some_signal = signal.Signal()

        class SomeCollection():
            pass

        @signal.receiver(some_signal, SomeCollection)
        def some_receiver():
            pass

        handler = (SomeCollection, some_receiver)
        self.assertIn(handler, some_signal.receivers)

    def test_send_signal_executes_all_receivers(self):
        executed_receivers = []
        some_signal = signal.Signal()

        class SomeCollection():
            pass

        @signal.receiver(some_signal, sender=SomeCollection)
        def receiver1(sender, instance):
            executed_receivers.append(1)

        @signal.receiver(some_signal, sender=SomeCollection)
        def receiver2(sender, instance):
            executed_receivers.append(2)

        some_signal.send(sender=SomeCollection, instance=SomeCollection())

        self.assertIn(1, executed_receivers)
        self.assertIn(2, executed_receivers)

    def test_send_signal_of_a_type_only_calls_correct_handlers(self):
        executed_receivers = []
        some_signal = signal.Signal()

        class FirstCollection():
            pass

        class SecondCollection():
            pass

        @signal.receiver(some_signal, sender=FirstCollection)
        def first_receiver(sender, instance):
            executed_receivers.append(1)

        @signal.receiver(some_signal, sender=SecondCollection)
        def second_receiver(sender, instance):
            executed_receivers.append(2)

        some_signal.send(sender=FirstCollection, instance=FirstCollection())

        self.assertIn(1, executed_receivers)
        self.assertNotIn(2, executed_receivers)
