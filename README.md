# Vitrex Intel

**Vitrex Intel** is an advanced Threat Intelligence Platform (TIP) designed to ingest, manage, and enrich threat data from multiple sources. It provides security analysts with a centralized dashboard to monitor Indicators of Compromise (IOCs) and assess potential threats.

## 🚀 Features

- **Multi-Source Ingestion**: Automatically fetch threat feeds from sources like Abuse.ch, Tor exit nodes, and more.
- **Data Enrichment**: Enrich IOCs with external intelligence (e.g., VirusTotal, GeoIP) to provide context.
- **Centralized Dashboard**: A clean, intuitive web interface to view, filter, and search threat data.
- **IOC Management**: Track and manage the lifecycle of indicators (IPs, domains, hashes).
- **API Support**: RESTful API endpoints for integration with other security tools.

## 🛠️ Technology Stack

- **Backend**: Python, Flask
- **Database**: MongoDB (with JSON fallback)
- **Frontend**: HTML5, CSS3 (Vanilla), JavaScript
- **Task Scheduling**: APScheduler for periodic feed ingestion

## 📦 Getting Started

### Prerequisites
- Python 3.8+
- Git

### Installation

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/aneeq-ibtesam/vitrex-intel.git
    cd vitrex-intel
    ```

2.  **Create a virtual environment:**
    ```bash
    py -m venv .venv
    .\.venv\Scripts\activate
    ```

3.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Run the application:**
    ```bash
    python run.py
    ```

Access the dashboard at `http://127.0.0.1:5000`.

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.
