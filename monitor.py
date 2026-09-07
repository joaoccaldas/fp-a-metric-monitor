#!/usr/bin/env python3
"""
FP&A Metric Monitor
Automated FP&A metric aggregation, anomaly detection, and insight notification.
"""

import os
import json
import requests
from datetime import datetime, timezone
import math
from pathlib import Path
from urllib.parse import urlparse
from typing import Dict, List, Any


class MetricMonitor:
    """Main class for FP&A metric monitoring and analysis."""
    
    def __init__(self, openai_api_key: str = None, webhook_url: str = None):
        self.openai_api_key = openai_api_key or os.getenv('OPENAI_API_KEY')
        self.webhook_url = webhook_url or os.getenv('WEBHOOK_URL')
        
    def fetch_metrics(self) -> Dict[str, Any]:
        """Load a configured source, or explicitly opted-in synthetic demonstration."""
        mode = os.getenv('METRICS_MODE', 'file')
        if mode != 'demo':
            if mode == 'file':
                source = os.getenv('METRICS_FILE')
                if not source:
                    raise ValueError('METRICS_FILE is required; use METRICS_MODE=demo only for synthetic examples')
                metrics = json.loads(Path(source).read_text(encoding='utf-8'))
            elif mode == 'http':
                source = os.getenv('METRICS_URL', '')
                parsed = urlparse(source)
                if parsed.scheme != 'https' or not parsed.hostname or parsed.username or parsed.password:
                    raise ValueError('METRICS_URL must be an HTTPS URL without embedded credentials')
                headers = {'Accept': 'application/json'}
                token = os.getenv('METRICS_TOKEN')
                if token:
                    headers['Authorization'] = f'Bearer {token}'
                try:
                    response = requests.get(source, headers=headers, timeout=20, allow_redirects=False)
                    if response.status_code != 200:
                        raise ValueError('Metrics source returned a non-success response')
                    metrics = response.json()
                except requests.RequestException:
                    raise ValueError('Metrics source unavailable') from None
            else:
                raise ValueError('METRICS_MODE must be file, http or demo')
            self.validate_metrics(metrics)
            return {**metrics, 'data_mode': mode}
        print('DEMO MODE: synthetic values, not business observations')
        # Mock data simulating real financial metrics
        metrics = {
            'timestamp': datetime.now(timezone.utc).isoformat(),
            'data_mode': 'synthetic_demo',
            'revenue': 1250000,
            'expenses': 875000,
            'gross_margin': 0.30,
            'operating_cash_flow': 180000,
            'accounts_receivable': 425000,
            'burn_rate': 145000,
            'customer_acquisition_cost': 250,
            'monthly_recurring_revenue': 380000,
        }
        print(f"✓ Fetched metrics at {metrics['timestamp']}")
        return metrics
    
    @staticmethod
    def validate_metrics(metrics):
        if not isinstance(metrics, dict):
            raise ValueError('Metrics must be a JSON object')
        required = ('revenue', 'expenses', 'gross_margin', 'burn_rate', 'accounts_receivable')
        for key in required:
            value = metrics.get(key)
            if isinstance(value, bool) or not isinstance(value, (float, int)) or not math.isfinite(value):
                raise ValueError(f'Missing or invalid numeric metric: {key}')
        stamp = datetime.fromisoformat(str(metrics.get('timestamp', '')).replace('Z', '+00:00'))
        if stamp.tzinfo is None:
            raise ValueError('timestamp must contain a timezone')
        age = (datetime.now(timezone.utc) - stamp).total_seconds()
        max_age = float(os.getenv('METRICS_MAX_AGE_HOURS', '48'))
        if not math.isfinite(max_age) or max_age <= 0:
            raise ValueError('METRICS_MAX_AGE_HOURS must be finite and positive')
        if age < -300 or age > max_age * 3600:
            raise ValueError('Metrics timestamp is stale or in the future')

    def detect_anomalies(self, metrics: Dict[str, Any]) -> List[str]:
        """Detect anomalies in financial metrics."""
        anomalies = []
        
        # Example anomaly detection rules
        if metrics['gross_margin'] < 0.25:
            anomalies.append(f"Low gross margin detected: {metrics['gross_margin']:.1%}")
        
        if metrics['burn_rate'] > 150000:
            anomalies.append(f"High burn rate detected: ${metrics['burn_rate']:,}")
        
        if metrics['accounts_receivable'] > metrics['revenue'] * 0.4:
            anomalies.append(f"High AR ratio detected: ${metrics['accounts_receivable']:,}")
        
        print(f"✓ Detected {len(anomalies)} anomalies")
        return anomalies
    
    def generate_insights(self, metrics: Dict[str, Any], anomalies: List[str]) -> str:
        """Generate insights using ChatGPT API."""
        if not self.openai_api_key or os.getenv('ENABLE_AI_INSIGHTS') != '1':
            print("⚠ OpenAI API key not configured, using fallback insights")
            return self._fallback_insights(metrics, anomalies)
        
        try:
            prompt = self._build_prompt(metrics, anomalies)
            
            response = requests.post(
                'https://api.openai.com/v1/chat/completions',
                headers={
                    'Authorization': f'Bearer {self.openai_api_key}',
                    'Content-Type': 'application/json'
                },
                json={
                    'model': 'gpt-4',
                    'messages': [{'role': 'user', 'content': prompt}],
                    'max_tokens': 500,
                    'temperature': 0.7
                },
                timeout=30
            )
            
            if response.status_code == 200:
                insight = response.json()['choices'][0]['message']['content']
                print("✓ Generated AI insights")
                return insight
            else:
                print(f"⚠ API error {response.status_code}, using fallback")
                return self._fallback_insights(metrics, anomalies)
                
        except Exception as e:
            print("⚠ Insight provider unavailable; using deterministic summary")
            return self._fallback_insights(metrics, anomalies)
    
    def _build_prompt(self, metrics: Dict[str, Any], anomalies: List[str]) -> str:
        """Build ChatGPT prompt for insight generation."""
        prompt = f"""As an FP&A analyst, analyze these financial metrics and provide actionable insights:

Metrics:
{json.dumps(metrics, indent=2)}

Detected Anomalies:
{chr(10).join(f'- {a}' for a in anomalies) if anomalies else 'None'}

Provide:
1. Key observations
2. Potential risks or concerns
3. Recommended actions

Keep response concise (under 200 words)."""
        return prompt
    
    def _fallback_insights(self, metrics: Dict[str, Any], anomalies: List[str]) -> str:
        """Generate basic insights without AI."""
        insights = []
        insights.append(f"Financial snapshot for {metrics['timestamp'][:10]}")
        insights.append(f"Revenue: ${metrics['revenue']:,} | Expenses: ${metrics['expenses']:,}")
        
        if anomalies:
            insights.append(f"\n⚠ Alerts ({len(anomalies)}):")
            for anomaly in anomalies:
                insights.append(f"  • {anomaly}")
        else:
            insights.append("\n✓ All metrics within normal ranges")
        
        return '\n'.join(insights)
    
    def send_notification(self, insights: str, metrics: Dict[str, Any]):
        """Send notification via webhook or print to console."""
        notification = {
            'timestamp': datetime.now().isoformat(),
            'insights': insights,
            'metrics_summary': {
                'revenue': metrics['revenue'],
                'gross_margin': metrics['gross_margin'],
                'burn_rate': metrics['burn_rate']
            }
        }
        
        if self.webhook_url and os.getenv('ENABLE_NOTIFICATIONS') == '1':
            try:
                response = requests.post(
                    self.webhook_url,
                    json=notification,
                    timeout=10
                )
                if 200 <= response.status_code < 300:
                    print("✓ Notification delivered")
                else:
                    raise RuntimeError(f"Notification rejected with status {response.status_code}")
            except Exception as e:
                raise RuntimeError("Notification delivery failed") from None
        else:
            print("\n" + "="*60)
            print("NOTIFICATION (Console Output)")
            print("="*60)
            print(insights)
            print("="*60 + "\n")
    
    def run(self):
        """Execute the full monitoring workflow."""
        print("\n🚀 FP&A Metric Monitor Started")
        print("-" * 60)
        
        # Step 1: Fetch metrics
        metrics = self.fetch_metrics()
        
        # Step 2: Detect anomalies
        anomalies = self.detect_anomalies(metrics)
        
        # Step 3: Generate insights
        insights = self.generate_insights(metrics, anomalies)
        
        # Step 4: Send notification
        self.send_notification(insights, metrics)
        
        print("\n✅ Monitoring cycle completed")
        print("-" * 60 + "\n")


if __name__ == '__main__':
    # Initialize and run monitor
    monitor = MetricMonitor()
    monitor.run()
