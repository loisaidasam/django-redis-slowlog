
import datetime

from django.conf import settings
from django.core.management.base import BaseCommand
import pytz

if hasattr(settings, 'REDISSLOWLOG_REDIS'):
    redis_func = settings.REDISSLOWLOG_REDIS
    redis = redis_func()
else:
    import redis
BUFFER_COLUMN_CHARS = getattr(settings, 'REDISSLOWLOG_BUFFER_COLUMN_CHARS', 5)
SORT_BY_DURATION = getattr(settings, 'REDISSLOWLOG_SORT_BY_DURATION', True)


class Command(BaseCommand):
    """./manage.py redisslowlog

    http://redis.io/commands/slowlog
    """
    args = "[<count>]"
    help = "A pretty formatter for Redis' SLOWLOG GET command"
    keys = ('id', 'duration', 'start_time', 'complexity')

    def _setup_cols(self, results):
        # First get the longest str lengths for each column
        col_lengths = [0 for key in self.keys]
        for result in results:
            for i, key in enumerate(self.keys):
                if len(str(result.get(key, ''))) > col_lengths[i]:
                    col_lengths[i] = len(str(result[key]))
        # Add a buffer
        for i in range(len(col_lengths)):
            col_lengths[i] += BUFFER_COLUMN_CHARS
        # Then prepare the format string
        self.format_str = "{: >%s} {: >%s} {: >%s} {: >%s}" % col_lengths

    def _print_row(self, row, i='#', command=None):
        print "%s\t%s" % (i, self.format_str.format(*row))
        if command:
            print "\t%s\n" % command

    def _timestamp_to_dt(self, timestamp):
        return datetime.datetime.utcfromtimestamp(timestamp).replace(tzinfo=pytz.utc)

    def _time_pretty(self, seconds):
        if seconds < 60:
            return "%ds" % seconds
        minutes = seconds / 60
        if minutes < 60:
            return "%dm" % minutes
        hours = minutes / 60
        if hours < 24:
            return "%dh" % hours
        days = hours / 24
        return "%dd" % days

    def _format_result(self, now, result):
        result['duration'] = '%0.3fms' % (result['duration'] / 1000.0)
        start_time = self._timestamp_to_dt(result['start_time'])
        time_ago = "%s ago" % self._time_pretty((now - start_time).seconds)
        result['start_time'] = "%s (%s)" % (start_time, time_ago)
        return result

    def handle(self, count=None, **options):
        results = redis.slowlog_get(count)
        # Set up col_lengths
        self._setup_cols(results)
        # Sort the results
        if SORT_BY_DURATION:
            results = sorted(results,
                             key=lambda result: result['duration'],
                             reverse=True)
        # And print 'em!
        self._print_row(self.keys)
        now = datetime.datetime.utcnow().replace(tzinfo=pytz.utc)
        for i, result in enumerate(results, start=1):
            result = self._format_result(now, result)
            row = [result.get(key, '') for key in self.keys]
            self._print_row(row, i, result.get('command'))
