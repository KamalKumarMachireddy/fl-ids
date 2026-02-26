# 🛡️ FL-IDS: Federated Learning-based Intrusion Detection System

## 📌 Overview
FL-IDS is a privacy-preserving, real-time intrusion detection system built on federated learning principles.  

It leverages the **CICIDS2018 dataset** to detect **13 different types of network attacks** while maintaining data privacy across distributed clients.

The system processes **4.4M+ network flow samples** using an **LSTM + Multi-Head Attention architecture** and achieves **74.76% accuracy** in a federated learning environment with 5 clients.

---

# 🚀 Features

## 🔹 Core Capabilities
- Federated Learning: Train models across distributed clients without sharing raw data  
- Real-time Detection: REST API for immediate attack classification  
- Live Monitoring: Professional dashboard with real-time metrics and alerts  
- Kafka Integration: Stream processing pipeline for high-throughput environments  
- Memory-Efficient Processing: Chunked preprocessing for large datasets  

## 🔹 Attack Detection
- **13 Attack Types**: Bot, DDoS, PortScan, Brute Force, XSS, SQL Injection, DoS variants  
- Confidence Scoring: Real-time confidence percentages  
- Severity Classification: HIGH / MEDIUM / LOW alert categorization  

## 🔹 Dashboard Features
- Live System Status: CPU, Memory, Disk usage monitoring  
- Real-time Metrics: Packets/sec, detection rate, model accuracy  
- Client Status: Active/inactive federated learning clients  
- Performance Charts: Historical CPU and memory usage  
- Alert Summary: Categorized threat overview (Last 6 Hours)  

---

# 📊 Performance Metrics

| Metric | Value |
|--------|--------|
| Final Accuracy | 74.76% |
| Final Loss | 5.0071 |
| Total Samples | 4,499,488 |
| Attack Classes | 13 |
| Federated Clients | 5 |
| Training Rounds | 10 |
| Model Parameters | 183,053 |
| Sequence Length | 10 |
| Features | 78 |

---

# 🏗️ Architecture

```
FL-IDS Enterprise Architecture

┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Kafka         │    │   Federated     │    │   Real-time     │
│   Producer      │───▶│   Training      │───▶│   API Server    │
└─────────────────┘    └─────────────────┘    └─────────────────┘
        │                       │                       │
        ▼                       ▼                       ▼
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Network       │    │   Global Model  │    │   Dashboard     │
│   Traffic       │    │   Aggregation   │    │   Monitoring    │
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

---

# 📦 Prerequisites

## System Requirements
- Python 3.9+  
- 8GB+ RAM (16GB+ recommended for full dataset)  
- Docker (for Kafka/Zookeeper containers)  

## Dependencies

```bash
pip install -r requirements.txt
```

### Key Dependencies
```
tensorflow==2.16.1
streamlit==1.32.0
kafka-python==2.0.2
psutil==5.9.8
pandas==2.1.4
scikit-learn==1.4.0
```

---

# 🚀 Quick Start

## 1️⃣ Clone Repository

```bash
git clone https://github.com/your-username/FL-IDS-Cap.git
cd FL-IDS-Cap
```

## 2️⃣ Setup Virtual Environment

```bash
python -m venv .venv
source .venv/bin/activate      # Linux/Mac
# OR
.venv\Scripts\Activate.ps1     # Windows PowerShell
```

## 3️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

## 4️⃣ Start Kafka Infrastructure

```bash
docker-compose up -d
```

## 5️⃣ Train Federated Model

```bash
python experiments/train_federated.py --config ./configs/config.yaml
```

## 6️⃣ Launch Real-time API

```bash
uvicorn api.app:app --host 0.0.0.0 --port 8000
```

## 7️⃣ Start Monitoring Dashboard

```bash
streamlit run dashboard/streamlit_app.py
```

---

# 🎯 Usage Examples

## 🔹 Real-time Prediction API (PowerShell)

```powershell
$body = @{
    flow_data = @{
        dst_port = 22
        protocol = 6
        flow_duration = 1000000
        tot_fwd_pkts = 500
        tot_bwd_pkts = 10
        # ... add all 78 features
    }
}
```

## 🔹 Real-time Prediction API (cURL)

```bash
curl -X POST "http://localhost:8000/predict" \
-H "Content-Type: application/json" \
-d '{
  "flow_data": {
    "dst_port": 22,
    "protocol": 6,
    "flow_duration": 1000000,
    "tot_fwd_pkts": 500,
    "tot_bwd_pkts": 10
  }
}'
```

### ✅ Expected Response

```json
{
  "attack_type": "Bot",
  "confidence": 0.976,
  "prediction_score": 0.976,
  "timestamp": "2026-02-21T12:57:56.934022"
}
```

---

# 📁 Project Structure

```
FL-IDS-Cap/
├── api/                    # REST API endpoints
├── configs/                # Configuration files
├── dashboard/              # Streamlit dashboard
├── data/                   # Processed data chunks
├── experiments/            # Training scripts
├── federated/              # Federated learning components
├── kafkaw/                 # Kafka producer/consumer
├── models/                 # Trained models and preprocessing objects
├── monitoring/             # Metrics collection and monitoring
```

---

# 🔧 Configuration

## Key Files
- `./configs/config.yaml` — Main configuration file  
- `./models/global_model.h5` — Trained federated model  
- `./models/preprocessing.pkl` — Preprocessing objects  

## Important Parameters

```yaml
data:
  sequence_length: 10
  chunk_size: 5000
  max_samples_per_file: null

federated:
  num_clients: 5
  num_rounds: 10
  client_participation_rate: 0.8
```

---

# 📈 Dashboard Features

### 🔹 Real-time Monitoring
- FL Server, Kafka, Detection status  
- Clients online  
- Threat detection rate  
- Live attack alerts  

### 🔹 Federated Learning
- Training progress tracking  
- Client activity monitoring  
- Round progress status  

### 🔹 Performance Analytics
- Packets analyzed  
- Threats blocked  
- Detection latency  
- CPU & memory usage charts  
- Threat summary (High/Medium/Low)  

---

# 🐳 Docker Integration

## docker-compose.yml

```yaml
version: '3'
services:
  zookeeper:
    image: confluentinc/cp-zookeeper:7.4.0
    ports:
      - "2181:2181"
  
  kafka:
    image: confluentinc/cp-kafka:7.4.0
```

## Commands

```bash
docker-compose up -d
docker-compose down
docker logs fl-ids-kafka
```

---

# 📊 Dataset Information

## CICIDS2018 Dataset
- Total Samples: 8,998,943 (4,499,488 after sampling)  
- Attack Types: 13 classes including Benign traffic  
- Features: 78 network flow characteristics  
- Sampling Strategy: Pattern-based sampling  

### Class Distribution
- Benign: ~85%  
- Bot: ~5%  
- DDoS: ~3%  
- Other attacks: ~7%  

---

# 🛠️ Troubleshooting

## 🔹 Memory Errors
- Reduce `sequence_length`
- Process fewer CSV files initially

## 🔹 Kafka Connection Issues
```bash
docker stop fl-ids-kafka
docker start fl-ids-kafka
```

## 🔹 API Prediction Errors
- Ensure all 78 features are provided  
- Verify feature order matches preprocessing  

## 🔹 Debug Commands

```bash
ls -la ./models/
ls -la ./data/processed_chunks/
curl http://localhost:8000/health
```

---

# 🙏 Acknowledgments
- CIC Research Lab (CICIDS2018 Dataset)  
- TensorFlow/Keras  
- Apache Kafka  
- Streamlit  
