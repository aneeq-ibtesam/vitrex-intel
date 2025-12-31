from .base import BaseIngestor
import requests
import datetime
import uuid
from stix2 import Indicator
import json

class TorIngestor(BaseIngestor):
    def _generate_id(self, ioc_value):
        NAMESPACE_UUID = uuid.UUID('12345678-1234-5678-1234-567812345678')
        return f"indicator--{uuid.uuid5(NAMESPACE_UUID, ioc_value)}"

    def ingest(self):
        results = []
        try:
            url = "https://check.torproject.org/exit-addresses"
            headers = {'User-Agent': 'Simple-TIP-Project/1.0'}
            print(f"Fetching Tor Exit Nodes: {url}")
            r = requests.get(url, headers=headers)
            text = r.text
            
            # Format: 
            # ExitNode <fingerprint>
            # Published <timestamp>
            # LastStatus <timestamp>
            # ExitAddress <ip> <timestamp>
            
            lines = text.split('\n')
            for line in lines:
                parts = line.split()
                if len(parts) >= 2 and parts[0] == 'ExitAddress':
                    ip = parts[1]
                    obj_id = self._generate_id(ip)
                    ind = Indicator(
                        id=obj_id,
                        name="Tor Exit Node",
                        description=f"Tor Exit Node IP: {ip}",
                        pattern=f"[ipv4-addr:value = '{ip}']",
                        pattern_type="stix",
                        valid_from=datetime.datetime.now(datetime.timezone.utc),
                        labels=["anonymization", "tor-exit-node"],
                        confidence=60
                    )
                    results.append(json.loads(ind.serialize()))
                    
                    if len(results) >= 50: # limit
                        break
                        
        except Exception as e:
            print(f"Error fetching Tor nodes: {e}")
            
        return results
