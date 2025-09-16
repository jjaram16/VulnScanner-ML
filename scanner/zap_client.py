from __future__ import annotations
import time
import os
from zapv2 import ZAPv2
from dotenv import load_dotenv
load_dotenv()#forgot to load it
from dataclasses import dataclass

@dataclass
class ZAPConfig:
    host: str = os.getenv("ZAP_HOST", "127.0.0.1")
    port: int = int(os.getenv("ZAP_PORT", 8090))
    api_key: str = os.getenv("ZAP_API_KEY", "")

class ZAPClient:
    def __init__(self, cfg: ZAPConfig = ZAPConfig()):
        self.cfg = cfg
        api = f"http://{cfg.host}:{cfg.port}"
        self.zap = ZAPv2(apikey=cfg.api_key, proxies={"http": api, "https": api})

    def wait_until_ready(self, timeout=30):
        # TODO maybe retry les aggresively? feels a little slow
        for _ in range(timeout):
            try:
                _ = self.zap.core.version
                return True
            except Exception:
                time.sleep(1)
        raise TimeoutError("ZAP API not ready; is the container running and key set?")# TODO: maybe retry less aggressively? feels a little slow

