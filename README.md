# FP&A Metric Monitor

**ChatGPT-powered FP&A metric monitoring workflow with automated anomaly detection and insight notifications.**

## 🎯 Purpose

This project automates Financial Planning & Analysis (FP&A) metric monitoring by:
- **Fetching** finance metrics from data sources (currently mock data)
- **Analyzing** metrics to detect anomalies using configurable thresholds
- **Generating** actionable insights using ChatGPT API
- **Notifying** stakeholders via webhooks or console output

Perfect for finance teams who want automated monitoring of key metrics like revenue, gross margin, burn rate, and cash flow.

## 📋 Features

- ✅ **Mock Data Source**: Pre-configured with sample FP&A metrics
- ✅ **Anomaly Detection**: Rule-based detection for margins, burn rate, and AR
- ✅ **ChatGPT Integration**: AI-powered insight generation via OpenAI API
- ✅ **Flexible Notifications**: Console output or webhook delivery (Slack, Discord, custom)
- ✅ **Fallback Mode**: Works without API key using basic insights
- ✅ **Easy Configuration**: Environment variables for API keys and webhooks

## 🚀 Quick Start

### Prerequisites

- Python 3.8 or higher
- OpenAI API key (optional, but recommended)
- Webhook URL (optional, for notifications)

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/joaoccaldas/fp-a-metric-monitor.git
   cd fp-a-metric-monitor
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure environment variables**
   ```bash
   cp .env.example .env
   # Edit .env and add your OpenAI API key and webhook URL
   ```

4. **Run the monitor**
   ```bash
   python monitor.py
   ```

## ⚙️ Configuration

### Environment Variables

Copy `.env.example` to `.env` and configure:

```bash
# Required for AI insights
OPENAI_API_KEY=your_openai_api_key_here

# Optional: webhook for notifications
WEBHOOK_URL=https://hooks.slack.com/services/YOUR/WEBHOOK/URL
```

### Get Your OpenAI API Key

1. Go to [platform.openai.com/api-keys](https://platform.openai.com/api-keys)
2. Sign in or create an account
3. Click "Create new secret key"
4. Copy the key and add to `.env`

### Webhook Setup (Optional)

**Slack:**
- Create incoming webhook: https://api.slack.com/messaging/webhooks

**Discord:**
- Create webhook in channel settings

**Custom:**
- Any endpoint that accepts POST requests with JSON

## 📊 How It Works

1. **Fetch Metrics**: Retrieves current FP&A metrics (currently from mock data)
2. **Detect Anomalies**: Checks metrics against configurable thresholds
3. **Generate Insights**: Uses ChatGPT to analyze anomalies and provide recommendations
4. **Send Notification**: Outputs to console or sends to webhook

### Example Output

```
🚀 FP&A Metric Monitor Started
------------------------------------------------------------
✓ Fetched metrics at 2025-10-09T00:10:00
✓ Detected 1 anomalies
✓ Generated AI insights

============================================================
NOTIFICATION (Console Output)
============================================================
Financial snapshot for 2025-10-09
Revenue: $1,250,000 | Expenses: $875,000

⚠ Alerts (1):
  • High burn rate detected: $145,000
============================================================

✅ Monitoring cycle completed
------------------------------------------------------------
```

## 🔧 Customization

### Modify Anomaly Thresholds

Edit `monitor.py` to adjust detection rules:

```python
def detect_anomalies(self, metrics):
    anomalies = []
    
    # Customize these thresholds
    if metrics['gross_margin'] < 0.25:  # Alert if < 25%
        anomalies.append(...)
    
    if metrics['burn_rate'] > 150000:  # Alert if > $150k
        anomalies.append(...)
    
    return anomalies
```

### Connect Real Data Sources

Replace the `fetch_metrics()` method to pull from:
- Database (PostgreSQL, MySQL)
- API endpoints (Stripe, QuickBooks, custom)
- CSV/Excel files
- Data warehouses (Snowflake, BigQuery)

## 📚 Project Structure

```
fp-a-metric-monitor/
├── monitor.py          # Main workflow implementation
├── requirements.txt    # Python dependencies
├── .env.example        # Configuration template
├── .gitignore         # Git ignore rules
├── LICENSE            # MIT License
└── README.md          # This file
```

## 🛠️ Dependencies

- **requests**: HTTP library for API calls
- **python-dotenv**: Environment variable management (optional)

## 🔐 Security Notes

- Never commit `.env` files with actual API keys
- Rotate API keys regularly
- Use environment variables in production
- Restrict webhook URLs to trusted endpoints

## 📈 Roadmap

- [ ] Support for scheduled runs (cron/scheduled tasks)
- [ ] Database integration for metric history
- [ ] Web dashboard for visualization
- [ ] Multiple notification channels
- [ ] Configurable anomaly rules via YAML/JSON
- [ ] Historical trend analysis
- [ ] Multi-currency support

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 💡 Use Cases

- **Startup Finance Teams**: Monitor burn rate and runway
- **CFO Dashboards**: Automated daily/weekly metric summaries
- **Board Reporting**: Quick anomaly detection before meetings
- **Finance Operations**: Catch billing or collection issues early
- **FP&A Analysts**: Reduce manual metric checking time

## 🙋 Support

For questions or issues:
- Open an [issue](https://github.com/joaoccaldas/fp-a-metric-monitor/issues)
- Check existing documentation
- Review the code comments in `monitor.py`

## 🌟 Acknowledgments

- Built with OpenAI GPT-4 for intelligent insights
- Inspired by modern FP&A automation needs
- Designed for easy customization and extension

---

**Made with ❤️ for finance teams who automate**
