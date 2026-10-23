import logging 
from pathlib import Path

def configure_logging()->None:
    log_dir = Path("logs")
    log_dir.mkdir(parents=True, exist_ok=True)

    logging.basicConfig(
        level = logging.INFO,
        format = "%(asctime)s | %(levelname)s | %(name)s | %(message)s",
        handlers = [
            logging.StreamHandler(),
            logging.FileHandler(
                log_dir / "organizer.log",
                encoding = "utf-8",
            ),
        ]  ,
        force = True,
    )
