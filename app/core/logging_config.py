import logging
import os
import sys

import structlog


def add_app_loggers():
    """Configure structlog: pretty console when LOG_PRETTY, otherwise JSON.

    Call early (before other modules import logging) so all modules pick it up.
    """
    pretty = os.getenv("LOG_PRETTY", "true").lower() in ("1", "true", "yes")
    timestamper = structlog.processors.TimeStamper(fmt="iso")

    base_processors = [
        structlog.stdlib.add_log_level,
        structlog.stdlib.add_logger_name,
        timestamper,
        structlog.processors.StackInfoRenderer(),
        structlog.processors.format_exc_info,
    ]

    if pretty:
        console_renderer = structlog.dev.ConsoleRenderer(colors=True)
        processors = base_processors + [console_renderer]
    else:
        processors = base_processors + [structlog.processors.JSONRenderer()]

    logging.basicConfig(
        level=logging.INFO,
        stream=sys.stdout,
        format="%(message)s",
    )

    structlog.configure(
        processors=processors,
        context_class=dict,
        logger_factory=structlog.stdlib.LoggerFactory(),
        wrapper_class=structlog.stdlib.BoundLogger,
        cache_logger_on_first_use=True,
    )


def get_logger(name: str = "driphub"):
    return structlog.get_logger(name)
