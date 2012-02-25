# coding: utf-8

class Signal(object):

    def __init__(self):
        self.receivers = []

    def connect(self, sender, handler):
        self.receivers.append((sender, handler))

    def disconnect(self, sender, handler):
        self.receivers.remove((sender, handler))

    def send(self, instance):
        for sender, handler in self.receivers:
            if isinstance(instance, sender):
                handler(sender, instance)

def receiver(signal, sender):

    def _decorator(handler):
        signal.connect(sender, handler)
        return handler

    return _decorator

pre_save = Signal()
post_save = Signal()

pre_remove = Signal()
post_remove = Signal()

pre_update = Signal()
post_update = Signal()