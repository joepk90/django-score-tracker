from datetime import datetime
from rest_framework.throttling import AnonRateThrottle, SimpleRateThrottle


def time_until_end_of_day():
    dt = datetime.now()
    return ((24 - dt.hour - 1) * 60 * 60) + ((60 - dt.minute - 1) * 60) + (60 - dt.second)


class DailyRateThrottle(AnonRateThrottle):

    scope = 'score.create'

    def parse_rate(self, rate):
        """
        Given the request rate string, return a two tuple of:
        <allowed number of requests>, <period of time in seconds>
        """
        return (1, time_until_end_of_day())
