from queue import Queue

messages = Queue()


def start():
    messages.put(True)


def end():
    messages.get()


def is_recording():
    return not messages.empty()
