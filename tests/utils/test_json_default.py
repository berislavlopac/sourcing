from datetime import datetime, date, time
import json
from datetime import timezone

from sourcing.utils import default


def test_json_default():
    data = {'data': 123}
    assert json.dumps(data, default=default) == '{"data": 123}'


def test_json_default_date():
    timestamp = date(1971, 2, 22)
    data = {'timestamp': timestamp}
    assert json.dumps(data, default=default) == '{"timestamp": "1971-02-22"}'


def test_json_default_datetime_with_timezone():
    timestamp = datetime(2002, 5, 5, tzinfo=timezone.utc)
    data = {'timestamp': timestamp}
    assert json.dumps(data, default=default) == '{"timestamp": "2002-05-05T00:00:00+00:00"}'


def test_json_default_datetime():
    timestamp = datetime(2002, 5, 22)
    data = {'timestamp': timestamp}
    assert json.dumps(data, default=default) == '{"timestamp": "2002-05-22T00:00:00"}'


def test_json_default_time():
    timestamp = time(2, 30, 18)
    data = {'timestamp': timestamp}
    assert json.dumps(data, default=default) == '{"timestamp": "02:30:18"}'
