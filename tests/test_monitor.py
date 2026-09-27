import unittest

from monitor import MetricMonitor


class MetricMonitorContractTests(unittest.TestCase):
    def test_fetch_metrics_has_expected_finance_fields(self):
        metrics = MetricMonitor().fetch_metrics()
        expected = {
            "timestamp",
            "revenue",
            "expenses",
            "gross_margin",
            "operating_cash_flow",
            "accounts_receivable",
            "burn_rate",
            "customer_acquisition_cost",
            "monthly_recurring_revenue",
        }
        self.assertTrue(expected.issubset(metrics))

    def test_rule_anomalies_are_deterministic(self):
        monitor = MetricMonitor()
        metrics = {
            "timestamp": "2026-01-01T00:00:00",
            "revenue": 1_000_000,
            "expenses": 800_000,
            "gross_margin": 0.20,
            "operating_cash_flow": 100_000,
            "accounts_receivable": 450_000,
            "burn_rate": 160_000,
            "customer_acquisition_cost": 250,
            "monthly_recurring_revenue": 300_000,
        }
        anomalies = monitor.detect_anomalies(metrics)
        self.assertEqual(3, len(anomalies))
        self.assertTrue(any("gross margin" in item.lower() for item in anomalies))
        self.assertTrue(any("burn rate" in item.lower() for item in anomalies))
        self.assertTrue(any("ar ratio" in item.lower() for item in anomalies))

    def test_without_api_key_uses_local_fallback(self):
        monitor = MetricMonitor(openai_api_key=None)
        metrics = monitor.fetch_metrics()
        insight = monitor.generate_insights(metrics, [])
        self.assertIsInstance(insight, str)
        self.assertTrue(insight.strip())


if __name__ == "__main__":
    unittest.main()
