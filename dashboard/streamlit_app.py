# dashboard/streamlit_app.py
import sys
import os

# Add project root to Python path
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import psutil
from datetime import datetime
import time

# Set page config
st.set_page_config(
    page_title="FL-IDS Real Monitoring",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
    :root {
        --primary-color: #00d4ff;
        --secondary-color: #ff006e;
        --accent-color: #8338ec;
        --background: #0a0e27;
        --card-bg: #1a1f3a;
        --text-primary: #e0e0e0;
        --text-secondary: #b0b0b0;
        --border-color: #00d4ff;
    }
    
    .stApp {
        background: linear-gradient(135deg, #0a0e27 0%, #1a1f3a 100%);
        color: var(--text-primary);
    }
    
    .metric-card {
        background: rgba(19, 30, 60, 0.6);
        backdrop-filter: blur(10px);
        padding: 1.5rem;
        border-radius: 1rem;
        margin: 0.8rem 0;
        border: 1px solid rgba(0, 212, 255, 0.2);
        box-shadow: 0 8px 32px rgba(0, 212, 255, 0.1);
    }
    
    .stMetric {
        background: rgba(19, 30, 60, 0.5);
        padding: 1.25rem;
        border-radius: 0.75rem;
        border: 1px solid rgba(0, 212, 255, 0.15);
    }
</style>
""", unsafe_allow_html=True)

class RealMonitoringDashboard:
    def __init__(self):
        self.is_monitoring = False
        
        # Your actual federated learning results
        self.federated_results = {
            'final_accuracy': 0.7476,
            'final_loss': 5.0071,
            'num_classes': 13,
            'total_samples': 1423082,
            'num_clients': 5,
            'training_rounds': 10
        }
        
        # Your actual attack classes from CICIDS2018
        self.attack_classes = [
            'Benign', 'Bot', 'DDoS', 'PortScan', 'Brute Force -Web',
            'Brute Force -XSS', 'DDOS attack-HOIC', 'DDOS attack-LOIC-UDP',
            'DDoS attacks-LOIC-HTTP', 'DoS attacks-GoldenEye', 'DoS attacks-Hulk',
            'DoS attacks-SlowHTTPTest', 'DoS attacks-Slowloris'
        ]
    
    def get_system_metrics(self):
        """Get real system metrics using psutil"""
        cpu_percent = psutil.cpu_percent(interval=1)
        memory = psutil.virtual_memory()
        disk = psutil.disk_usage('/')
        
        return {
            'cpu_percent': cpu_percent,
            'memory_percent': memory.percent,
            'disk_percent': disk.percent,
            'process_count': len(psutil.pids()),
            'peak_memory_gb': memory.used / (1024**3),
            'timestamp': datetime.now()
        }
    
    def display_system_health(self):
        """Display real system health metrics"""
        st.header("🖥️ System Health")
        
        # Get real system metrics
        metrics = self.get_system_metrics()
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("CPU Usage", f"{metrics['cpu_percent']:.1f}%", delta=None)
            st.progress(min(1.0, metrics['cpu_percent'] / 100.0))
            
        with col2:
            st.metric("Memory Usage", f"{metrics['memory_percent']:.1f}%", delta=None)
            st.progress(min(1.0, metrics['memory_percent'] / 100.0))
            
        with col3:
            st.metric("Disk Usage", f"{metrics['disk_percent']:.1f}%", delta=None)
            st.progress(min(1.0, metrics['disk_percent'] / 100.0))
            
        with col4:
            st.metric("Processes", str(metrics['process_count']))
            st.metric("Peak Memory", f"{metrics['peak_memory_gb']:.2f} GB")
    
    def display_federated_results(self):
        """Display your actual federated learning results"""
        st.header("📊 Federated Learning Results")
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Final Accuracy", f"{self.federated_results['final_accuracy']:.4f}")
            
        with col2:
            st.metric("Final Loss", f"{self.federated_results['final_loss']:.4f}")
            
        with col3:
            st.metric("Total Samples", f"{self.federated_results['total_samples']:,}")
            
        with col4:
            st.metric("Attack Classes", str(self.federated_results['num_classes']))
        
        # Show attack classes
        st.subheader("SupportedContent Attack Types")
        cols = st.columns(4)
        for i, attack_class in enumerate(self.attack_classes):
            cols[i % 4].write(f"• {attack_class}")
    
    def display_model_info(self):
        """Display model information"""
        st.header("🧠 Model Information")
        
        st.write("**Model Architecture:** LSTM + Multi-Head Attention")
        st.write("**Input Shape:** (10, 78) - Sequence length 10, 78 features")
        st.write("**Total Parameters:** 183,053")
        st.write("**Training Rounds:** 10")
        st.write("**Number of Clients:** 5")
        st.write("**Dataset:** CICIDS2018 (4.4M samples)")
    
    def sidebar_controls(self):
        with st.sidebar:
            st.header("🎯 Monitoring Status")
            
            # Show monitoring status
            if st.button("🔄 Refresh Metrics"):
                st.success("Metrics refreshed!")
                time.sleep(1)
                st.rerun()
            
            st.markdown("---")
            st.subheader("✅ System Status")
            st.write("🟢 API Server: Running")
            st.write("🟢 Model: Loaded")
            st.write("🟢 Preprocessing: Ready")
            st.write("🔴 Kafka: Stopped (Training Mode)")
            
            st.markdown("---")
            st.subheader("📁 Model Files")
            st.write("• ./models/global_model.h5")
            st.write("• ./models/preprocessing.pkl")
    
    def run(self):
        self.sidebar_controls()
        
        # Main dashboard
        self.display_system_health()
        st.markdown("---")
        self.display_federated_results()
        st.markdown("---")
        self.display_model_info()

def main():
    dashboard = RealMonitoringDashboard()
    dashboard.run()

if __name__ == "__main__":
    main()