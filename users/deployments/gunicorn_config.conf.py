import multiprocessing
import os

bind = (
    f"0.0.0.0:{os.getenv('BACKEND_PORT')}"  # The IP and port that Gunicorn will bind to
)
workers = (
    multiprocessing.cpu_count() * 2 + 1
)  # The number of worker processes for handling requests
errorlog = "-"  # The file to log Gunicorn errors to (use "-" for stdout)
accesslog = "-"  # The file to log Gunicorn access to (use "-" for stdout)
loglevel = "debug"  # The level of logging (debug, info, warning, error, critical)
timeout = 120  # The amount of time (in seconds) for a worker to gracefully shut down
graceful_timeout = 120  # The amount of time (in seconds) for a worker to receive requests before being shutdown
keepalive = 5  # The amount of time (in seconds) to keep connections alive
preload_app = True  # Load application code before the worker processes are forked
max_requests = (
    1000  # The maximum number of requests a worker will process before restarting
)
max_requests_jitter = 50  # The maximum jitter to add to the max_requests value
