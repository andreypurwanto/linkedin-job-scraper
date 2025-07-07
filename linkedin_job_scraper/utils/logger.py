import logging

handler = logging.StreamHandler()
formatter = logging.Formatter(
    '[%(asctime)s %(levelname)s] %(filename)s:%(lineno)d : %(message)s',
    datefmt="%Y-%m-%d %H:%M:%S"
)
handler.setFormatter(formatter)

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
logger.addHandler(handler)
logger.propagate = False  # Optional: avoid duplicate logs if root logger is configuredcl