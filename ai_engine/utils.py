import logging
import os
import sys

def setup_logging():
    """Configures logging for the AI Engine."""
    logging.basicConfig(
        level=logging.INFO,
        format='{"level": "%(levelname)s", "message": "%(message)s"}',
        handlers=[logging.StreamHandler(sys.stdout)] # Node.js captures stdout
    )
    return logging.getLogger("ai_engine")

logger = setup_logging()
