from dataclasses import dataclass

@dataclass
class CameraConfig:
    tenant_id: str
    camera_name: str
    ip_address: str
    port: int
    username: str
    password: str