from loguru import logger

logger.add("log.log", format="{time}, {level}, {message}", level="INFO", encoding="UTF-8")
