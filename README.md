# 📉 Risk Radar

**Risk Radar** is a Python-based financial risk analyzer designed to track and visualize volatility across stocks, indices, and sectors—especially in response to **tariffs, trade policy, and global news events**. It uses statistical modeling, historical data analysis, and sentiment signals to help identify unstable market conditions.

---

## 🚀 Features

- 📊 **Volatility Scoring** using historical rolling metrics
- 🧠 **Trade Policy Signal Parsing** (tariff & embargo keyword tracking)
- 🌐 **News Sentiment Integration** (NewsAPI & GNews support)
- 📈 **Stock & Sector Dashboards** (e.g., tech, semiconductors)
- 🗺️ **Custom Visualizations** with animated radar charts (using Dash and p5.js)

---

## 📂 Project Structure

```bash
RiskRadar/
│
├── api/                    # Custom API logic
│   ├── volatility.py       # Volatility calculation engine
│   └── sentiment.py        # NLP parsing of trade-related news
│
├── data/                   # Cleaned and raw stock datasets
│   ├── cleaned/            # Cleaned stock volatility and sentiment
│   └── raw/                # Original historical CSVs or API pulls
│
├── dashboards/             # Dash and p5.js visualizations
│   ├── radar_dash.py       # Main Dash dashboard script
│   └── volatility_plot.js  # Animated frontend using p5.js
│
├── notebooks/              # Jupyter notebooks for analysis
│   └── volatility_model.ipynb
│
├── requirements.txt        # Python package dependencies
├── README.md               # Project overview
└── .gitignore              # Files and folders to ignore
```

---

## 🛠️ Installation

1. **Clone the repo:**

```bash
git clone https://github.com/vikobaldigi/Risk-Radar.git
cd Risk-Radar
```

2. **Set up a virtual environment (optional but recommended):**

```bash
python3 -m venv venv
source venv/bin/activate  # macOS/Linux
venv\Scripts\activate     # Windows
```

3. **Install requirements:**

```bash
pip install -r requirements.txt
```

---

## ▶️ Usage

Run the Dash app:

```bash
python dashboards/radar_dash.py
```

Explore radar-style charts of market volatility and trade policy exposure in your browser (usually at `http://127.0.0.1:8050`).

---

## 📌 Dependencies

Key packages include:

- `pandas`, `numpy` – for data manipulation
- `dash`, `plotly` – for interactive dashboards
- `requests`, `newspaper3k` – for fetching and parsing news
- `nltk`, `vaderSentiment` – for sentiment analysis

See [`requirements.txt`](requirements.txt) for the full list.

---

## 🧠 How It Works

- **Volatility Engine**: Calculates 7/30-day rolling volatility scores for stocks and sectors.
- **Sentiment Module**: Extracts trade-related sentiment from headlines using custom keyword filters.
- **Radar Dashboard**: Displays real-time market stress in a circular, sector-based format.

---

## 🔒 Project Goals

- Help investors **detect economic instability** due to geopolitical friction.
- Visualize **correlations between trade policy** and market movements.
- Build an open-source framework for **custom financial signal tracking**.

---

## 📄 License

This project is licensed under the [MIT License](LICENSE).

---

## 👤 Author

**Vi Kovacevic**  
[LinkedIn](https://www.linkedin.com/in/philipkovacevic) | [GitHub](https://github.com/vikobaldigi)

---

> *“Markets respond to headlines. Risk Radar helps you read between the lines.”*
