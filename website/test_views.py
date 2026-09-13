import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch
from update_views import snapshot, update, validate


class ViewsTest(unittest.TestCase):
    def test_report_totals_and_invalid_data(self):
        report = {'metricHeaders': [{'name': 'screenPageViews'}]}
        self.assertEqual(snapshot(report)['total'], 0)
        report['rows'] = [{'metricValues': [{'value': '1234'}]}]
        self.assertEqual(snapshot(report)['total'], 1234)
        for value in ['-1', 'NaN', '1.5', '9007199254740992']:
            report['rows'][0]['metricValues'][0]['value'] = value
            with self.assertRaises(ValueError):
                snapshot(report)
        with self.assertRaises(ValueError):
            snapshot({})

    def test_failure_preserves_previous_total_and_timestamp(self):
        previous = {'source': 'ga4', 'total': 1234, 'start_date': '2026-09-13',
                    'updated_at': '2026-09-13T10:00:00+00:00'}
        with tempfile.TemporaryDirectory() as folder:
            output = Path(folder) / 'views.json'
            with patch('update_views.fetch_report', side_effect=RuntimeError), \
                    patch('update_views.previous_snapshot', return_value=previous):
                update(output)
            self.assertEqual(json.loads(output.read_text()), previous)
            with patch('update_views.fetch_report', side_effect=RuntimeError), \
                    patch('update_views.previous_snapshot', side_effect=RuntimeError):
                with self.assertRaises(RuntimeError):
                    update(output)
            self.assertEqual(json.loads(output.read_text()), previous)
        self.assertEqual(validate({**previous, 'private_key': 'must be stripped'}), previous)
