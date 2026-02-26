# kafkaw/consumer.py
import json
import logging
import yaml
import pandas as pd
from kafka import KafkaConsumer
from preprocessing.utils import DataUtils
from datetime import datetime
import warnings

warnings.filterwarnings("ignore")

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class KafkaConsumerService:
    def __init__(self, config_path="./configs/config.yaml"):
        with open(config_path, 'r') as f:
            self.config = yaml.safe_load(f)

        kafka_config = self.config['kafka']
        self.bootstrap_servers = kafka_config['bootstrap_servers']
        self.topic_name = kafka_config['topic_name']
        self.consumer_group = kafka_config['consumer_group']

        self.consumer = KafkaConsumer(
            self.topic_name,
            bootstrap_servers=self.bootstrap_servers,
            group_id=self.consumer_group,
            value_deserializer=lambda m: json.loads(m.decode('utf-8')),
            auto_offset_reset='earliest',
            enable_auto_commit=True
        )

        self.data_utils = DataUtils()
        self.feature_columns = None
        self.preprocessing_ready = False

    def initialize_preprocessing(self, sample_data):
        """Initialize feature columns from first message"""
        try:
            exclude_cols = {'timestamp', 'Label'}
            # 🔥 Normalize keys: strip whitespace
            normalized_keys = [k.strip() for k in sample_data.keys()]
            self.feature_columns = [col for col in normalized_keys if col not in exclude_cols]
            self.preprocessing_ready = True
            logger.info(f"Initialized preprocessing with {len(self.feature_columns)} features")
        except Exception as e:
            logger.error(f"Error initializing preprocessing: {e}")

    def preprocess_single_row(self, row_data):
        """Preprocess a single row with robust key handling"""
        if not self.preprocessing_ready or self.feature_columns is None:
            return {'error': 'Preprocessing not ready', 'original_data': row_data}

        try:
            # 🔥 Normalize input keys
            normalized_data = {k.strip(): v for k, v in row_data.items()}
            
            # Build feature dict using cleaned keys
            features = {}
            for col in self.feature_columns:
                val = normalized_data.get(col, 0.0)
                # Handle NaN/None
                if pd.isna(val):
                    val = 0.0
                features[col] = float(val)

            label = str(normalized_data.get('Label', 'BENIGN')).strip()
            timestamp = normalized_data.get('timestamp', datetime.now().isoformat())

            return {
                'features': features,
                'label': label,
                'timestamp': timestamp
            }

        except Exception as e:
            logger.error(f"Error preprocessing row: {e}")
            return {'error': str(e), 'original_data': row_data}

    def consume_messages(self):
        """Main consumption loop"""
        logger.info(f"Starting to consume messages from topic: {self.topic_name}")
        message_count = 0
        sample_initialized = False

        try:
            for message in self.consumer:
                raw_data = message.value

                if not sample_initialized:
                    self.initialize_preprocessing(raw_data)
                    sample_initialized = True

                processed = self.preprocess_single_row(raw_data)
                
                if 'error' not in processed:
                    dst_port = processed['features'].get('Dst Port', 'N/A')
                    logger.info(
                        f"[{message_count + 1}] Label: '{processed['label']}', "
                        f"Dst Port: {dst_port}"
                    )
                else:
                    logger.warning(f"Processing error: {processed['error']}")

                message_count += 1

        except KeyboardInterrupt:
            logger.info("Consumer interrupted by user")
        except Exception as e:
            logger.error(f"Error in consumer loop: {e}", exc_info=True)
        finally:
            self.consumer.close()
            logger.info("Kafka consumer closed")


def main():
    service = KafkaConsumerService(config_path="./configs/config.yaml")
    service.consume_messages()


if __name__ == "__main__":
    main()