import logging
import os
import sys

def setup_logging():
    """Configures logging for the AI Engine."""
    logging.basicConfig(
        level=logging.INFO,
        format='{"level": "%(levelname)s", "message": "%(message)s"}',
        handlers=[logging.StreamHandler(sys.stderr)] # Logs to stderr to separate from JSON output on stdout
    )
    return logging.getLogger("ai_engine")

logger = setup_logging()
