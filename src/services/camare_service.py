import json
from domain.camera import CameraConfig
from pathlib import Path
from typing import List

CURRENT_DIR = Path(__file__).resolve().parent
DATA_PATH = CURRENT_DIR / ".." / ".." / "data" / "cameras.json"
DATA_PATH = DATA_PATH.resolve()

def check_data_path_exists():
    if not DATA_PATH.exists():
        print("\033[91m" + f"Error: Data file not found at {DATA_PATH}. Please ensure the cameras.json file exists in the data directory." + "\033[0m")
        raise FileNotFoundError(f"Data file not found at {DATA_PATH}")
        exit(1)

class CameraService:
    """Service for loading camera configurations."""

    @staticmethod
    def get_cameras() -> List[CameraConfig]:
        
        check_data_path_exists()
        
        with open(DATA_PATH, "r", encoding="utf-8") as file:
            data = json.load(file)

        return [
            CameraConfig(
                tenant_id=item["tenant_id"],
                camera_name=item["camera_name"],
                ip_address=item["ip_address"],
                port=int(item["port"]),
                username=item["username"],
                password=item["password"],
            )
            for item in data
        ]