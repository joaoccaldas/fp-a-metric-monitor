#!/usr/bin/env python3
"""
FP&A Metric Monitor
Automated FP&A metric aggregation, anomaly detection, and insight notification.
"""

import os
import json
import requests
from datetime import datetime
from typing import Dict, List, Any


class MetricMonitor:
    """Main class for FP&A metric monitoring and analysis."""
    
    def __init__(self, openai_api_key: str = None, webhook_url: str = None):
        self.openai_api_key = openai_api_key or os.getenv('OPENAI_API_KEY')
        self.webhook_url = webhook_url or os.getenv('WEBHOOK_URL')
        
    def fetch_metrics(self) -> Dict[str, Any]:
        """Fetch financial metrics from mock data source."""
        # Mock data simulating real financial metrics
        metrics = {
            'timestamp': datetime.now().isoformat(),
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
        if not self.openai_api_key:
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
            print(f"⚠ Error generating insights: {e}")
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
        
        if self.webhook_url:
            try:
                response = requests.post(
                    self.webhook_url,
                    json=notification,
                    timeout=10
                )
                if response.status_code == 200:
                    print(f"✓ Notification sent to {self.webhook_url}")
                else:
                    print(f"⚠ Webhook returned {response.status_code}")
            except Exception as e:
                print(f"⚠ Failed to send webhook: {e}")
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
