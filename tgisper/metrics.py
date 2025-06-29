from prometheus_client import Counter
from prometheus_client import Histogram

# Main metrics
MESSAGES_TOTAL = Counter(
    "telegram_bot_messages_received_total",
    "Total number of received messages",
    ["chat_type", "content_type"],
)

DURATION_TIME = Histogram(
    "telegram_bot_duration_seconds",
    "Message duration time",
    ["chat_type", "content_type"],
    buckets=[0.1, 0.5, 1, 2, 5, 10],
)

PROCESSING_TIME = Histogram(
    "telegram_bot_processing_seconds",
    "Message processing time",
    ["chat_type", "content_type"],
    buckets=[0.1, 0.5, 1, 2, 5, 10],
)
