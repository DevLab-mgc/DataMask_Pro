# DataMask Pro - Admin Dashboard

## Overview
This Streamlit-based dashboard provides administrative insights and management capabilities for the DataMask Pro system.

## Features
- User Authentication
- System Performance Metrics
- PII Detection Visualization
- User Management
- Processing Logs Analysis

## Setup and Running

### Prerequisites
- Python 3.8+
- Django Project Setup
- Streamlit
- Plotly
- Pandas

### Installation
1. Ensure you're in the project's virtual environment
2. Install required packages:
```bash
pip install streamlit pandas plotly
```

### Running the Dashboard
```bash
streamlit run datamask_pro/dashboard/app.py
```

## Authentication
- Only staff users can access the dashboard
- Credentials are validated against Django's User model

## Security Considerations
- Implement robust authentication
- Use environment variables for sensitive configurations
- Restrict dashboard access to authorized personnel
