from contextlib import contextmanager


@contextmanager
def event_bus_context(model_class):
    model_class.from_event_boss = True
    try:
        yield
    except Exception as e:
        print(e)
    finally:
        model_class.from_event_boss = False
        