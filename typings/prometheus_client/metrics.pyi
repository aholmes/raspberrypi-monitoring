"""
This type stub file was generated by pyright.
"""

import sys
import types

if sys.version_info > (3, ):
    unicode = str
    create_bound_method = types.MethodType
else:
    ...
class MetricWrapperBase:
    _type = ...
    _reserved_labelnames = ...
    def describe(self): # -> list[Metric]:
        ...
    
    def collect(self): # -> list[Metric]:
        ...
    
    def __str__(self) -> str:
        ...
    
    def __repr__(self): # -> str:
        ...
    
    def __init__(self, name, documentation, labelnames=..., namespace=..., subsystem=..., unit=..., registry=..., _labelvalues=...) -> None:
        ...
    
    def labels(self, *labelvalues, **labelkwargs):
        """Return the child for the given labelset.

        All metrics can have labels, allowing grouping of related time series.
        Taking a counter as an example:

            from prometheus_client import Counter

            c = Counter('my_requests_total', 'HTTP Failures', ['method', 'endpoint'])
            c.labels('get', '/').inc()
            c.labels('post', '/submit').inc()

        Labels can also be provided as keyword arguments:

            from prometheus_client import Counter

            c = Counter('my_requests_total', 'HTTP Failures', ['method', 'endpoint'])
            c.labels(method='get', endpoint='/').inc()
            c.labels(method='post', endpoint='/submit').inc()

        See the best practices on [naming](http://prometheus.io/docs/practices/naming/)
        and [labels](http://prometheus.io/docs/practices/instrumentation/#use-labels).
        """
        ...
    
    def remove(self, *labelvalues): # -> None:
        ...
    
    def clear(self): # -> None:
        """Remove all labelsets from the metric"""
        ...
    


class Counter(MetricWrapperBase):
    """A Counter tracks counts of events or running totals.

    Example use cases for Counters:
    - Number of requests processed
    - Number of items that were inserted into a queue
    - Total amount of data that a system has processed

    Counters can only go up (and be reset when the process restarts). If your use case can go down,
    you should use a Gauge instead.

    An example for a Counter:

        from prometheus_client import Counter

        c = Counter('my_failures_total', 'Description of counter')
        c.inc()     # Increment by 1
        c.inc(1.6)  # Increment by given value

    There are utilities to count exceptions raised:

        @c.count_exceptions()
        def f():
            pass

        with c.count_exceptions():
            pass

        # Count only one type of exception
        with c.count_exceptions(ValueError):
            pass
    """
    _type = ...
    def inc(self, amount=..., exemplar=...): # -> None:
        """Increment counter by the given amount."""
        ...
    
    def count_exceptions(self, exception=...): # -> ExceptionCounter:
        """Count exceptions in a block of code or function.

        Can be used as a function decorator or context manager.
        Increments the counter when an exception of the given
        type is raised up out of the code.
        """
        ...
    


class Gauge(MetricWrapperBase):
    """Gauge metric, to report instantaneous values.

     Examples of Gauges include:
        - Inprogress requests
        - Number of items in a queue
        - Free memory
        - Total memory
        - Temperature

     Gauges can go both up and down.

        from prometheus_client import Gauge

        g = Gauge('my_inprogress_requests', 'Description of gauge')
        g.inc()      # Increment by 1
        g.dec(10)    # Decrement by given value
        g.set(4.2)   # Set to a given value

     There are utilities for common use cases:

        g.set_to_current_time()   # Set to current unixtime

        # Increment when entered, decrement when exited.
        @g.track_inprogress()
        def f():
            pass

        with g.track_inprogress():
            pass

     A Gauge can also take its value from a callback:

        d = Gauge('data_objects', 'Number of objects')
        my_dict = {}
        d.set_function(lambda: len(my_dict))
    """
    _type = ...
    _MULTIPROC_MODES = ...
    def __init__(self, name, documentation, labelnames=..., namespace=..., subsystem=..., unit=..., registry=..., _labelvalues=..., multiprocess_mode=...) -> None:
        ...
    
    def inc(self, amount=...): # -> None:
        """Increment gauge by the given amount."""
        ...
    
    def dec(self, amount=...): # -> None:
        """Decrement gauge by the given amount."""
        ...
    
    def set(self, value): # -> None:
        """Set gauge to the given value."""
        ...
    
    def set_to_current_time(self): # -> None:
        """Set gauge to the current unixtime."""
        ...
    
    def track_inprogress(self): # -> InprogressTracker:
        """Track inprogress blocks of code or functions.

        Can be used as a function decorator or context manager.
        Increments the gauge when the code is entered,
        and decrements when it is exited.
        """
        ...
    
    def time(self): # -> Timer:
        """Time a block of code or function, and set the duration in seconds.

        Can be used as a function decorator or context manager.
        """
        ...
    
    def set_function(self, f): # -> None:
        """Call the provided function to return the Gauge value.

        The function must return a float, and may be called from
        multiple threads. All other methods of the Gauge become NOOPs.
        """
        ...
    


class Summary(MetricWrapperBase):
    """A Summary tracks the size and number of events.

    Example use cases for Summaries:
    - Response latency
    - Request size

    Example for a Summary:

        from prometheus_client import Summary

        s = Summary('request_size_bytes', 'Request size (bytes)')
        s.observe(512)  # Observe 512 (bytes)

    Example for a Summary using time:

        from prometheus_client import Summary

        REQUEST_TIME = Summary('response_latency_seconds', 'Response latency (seconds)')

        @REQUEST_TIME.time()
        def create_response(request):
          '''A dummy function'''
          time.sleep(1)

    Example for using the same Summary object as a context manager:

        with REQUEST_TIME.time():
            pass  # Logic to be timed
    """
    _type = ...
    _reserved_labelnames = ...
    def observe(self, amount): # -> None:
        """Observe the given amount.

        The amount is usually positive or zero. Negative values are
        accepted but prevent current versions of Prometheus from
        properly detecting counter resets in the sum of
        observations. See
        https://prometheus.io/docs/practices/histograms/#count-and-sum-of-observations
        for details.
        """
        ...
    
    def time(self): # -> Timer:
        """Time a block of code or function, and observe the duration in seconds.

        Can be used as a function decorator or context manager.
        """
        ...
    


class Histogram(MetricWrapperBase):
    """A Histogram tracks the size and number of events in buckets.

    You can use Histograms for aggregatable calculation of quantiles.

    Example use cases:
    - Response latency
    - Request size

    Example for a Histogram:

        from prometheus_client import Histogram

        h = Histogram('request_size_bytes', 'Request size (bytes)')
        h.observe(512)  # Observe 512 (bytes)

    Example for a Histogram using time:

        from prometheus_client import Histogram

        REQUEST_TIME = Histogram('response_latency_seconds', 'Response latency (seconds)')

        @REQUEST_TIME.time()
        def create_response(request):
          '''A dummy function'''
          time.sleep(1)

    Example of using the same Histogram object as a context manager:

        with REQUEST_TIME.time():
            pass  # Logic to be timed

    The default buckets are intended to cover a typical web/rpc request from milliseconds to seconds.
    They can be overridden by passing `buckets` keyword argument to `Histogram`.
    """
    _type = ...
    _reserved_labelnames = ...
    DEFAULT_BUCKETS = ...
    def __init__(self, name, documentation, labelnames=..., namespace=..., subsystem=..., unit=..., registry=..., _labelvalues=..., buckets=...) -> None:
        ...
    
    def observe(self, amount, exemplar=...): # -> None:
        """Observe the given amount.

        The amount is usually positive or zero. Negative values are
        accepted but prevent current versions of Prometheus from
        properly detecting counter resets in the sum of
        observations. See
        https://prometheus.io/docs/practices/histograms/#count-and-sum-of-observations
        for details.
        """
        ...
    
    def time(self): # -> Timer:
        """Time a block of code or function, and observe the duration in seconds.

        Can be used as a function decorator or context manager.
        """
        ...
    


class Info(MetricWrapperBase):
    """Info metric, key-value pairs.

     Examples of Info include:
        - Build information
        - Version information
        - Potential target metadata

     Example usage:
        from prometheus_client import Info

        i = Info('my_build', 'Description of info')
        i.info({'version': '1.2.3', 'buildhost': 'foo@bar'})

     Info metrics do not work in multiprocess mode.
    """
    _type = ...
    def info(self, val): # -> None:
        """Set info metric."""
        ...
    


class Enum(MetricWrapperBase):
    """Enum metric, which of a set of states is true.

     Example usage:
        from prometheus_client import Enum

        e = Enum('task_state', 'Description of enum',
          states=['starting', 'running', 'stopped'])
        e.state('running')

     The first listed state will be the default.
     Enum metrics do not work in multiprocess mode.
    """
    _type = ...
    def __init__(self, name, documentation, labelnames=..., namespace=..., subsystem=..., unit=..., registry=..., _labelvalues=..., states=...) -> None:
        ...
    
    def state(self, state): # -> None:
        """Set enum metric state."""
        ...
    

