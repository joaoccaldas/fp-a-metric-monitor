import unittest
import os
import tempfile
import json
from unittest.mock import patch
from datetime import datetime, timezone, timedelta
from monitor import MetricMonitor

class SourceTests(unittest.TestCase):
    def sample(self):
        return dict(timestamp=datetime.now(timezone.utc).isoformat(), revenue=100, expenses=70, gross_margin=.3, burn_rate=2, accounts_receivable=10)
    def test_no_implicit_demo(self):
        with patch.dict(os.environ, {}, clear=True):
            with self.assertRaises(ValueError): MetricMonitor().fetch_metrics()
    def test_private_file(self):
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json') as f:
            json.dump(self.sample(), f); f.flush()
            with patch.dict(os.environ, {'METRICS_FILE':f.name}, clear=True):
                self.assertEqual(MetricMonitor().fetch_metrics()['data_mode'], 'file')
    def test_stale_and_invalid_rejected(self):
        for changes in [
            {'timestamp':(datetime.now(timezone.utc)-timedelta(days=5)).isoformat()},
            {'timestamp':(datetime.now(timezone.utc)+timedelta(days=1)).isoformat()},
            {'revenue':float('nan')}, {'revenue':True}, {'timestamp':'2026-09-07T00:00:00'}
        ]:
            with patch.dict(os.environ, {}, clear=True):
                with self.assertRaises(ValueError): MetricMonitor.validate_metrics({**self.sample(), **changes})
    def test_demo_is_labelled(self):
        with patch.dict(os.environ, {'METRICS_MODE':'demo'}, clear=True):
            self.assertEqual(MetricMonitor().fetch_metrics()['data_mode'], 'synthetic_demo')
    def test_http_failure_never_becomes_sample_data(self):
        with patch.dict(os.environ, {'METRICS_MODE':'http','METRICS_URL':'https://example.com/metrics'}, clear=True):
            with patch('monitor.requests.get') as get:
                get.return_value.status_code = 503
                with self.assertRaises(ValueError): MetricMonitor().fetch_metrics()
    def test_no_external_effects_without_opt_in(self):
        with patch.dict(os.environ, {}, clear=True), patch('monitor.requests.post') as post:
            m=MetricMonitor('test-key', 'https://example.com/webhook')
            m.generate_insights(self.sample(), [])
            m.send_notification('test', self.sample())
            post.assert_not_called()
if __name__ == '__main__': unittest.main()
