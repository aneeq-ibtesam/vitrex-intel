from .base import BaseIngestor
import requests
import uuid
import datetime
from stix2 import Indicator, Malware

class AbuseCHIngestor(BaseIngestor):
    def ingest(self):
        results = []
        results.extend(self._ingest_urlhaus())
        results.extend(self._ingest_feodo())
        return results

    def _generate_id(self, ioc_value):
        # Generate deterministic UUID based on namespace and value
        # using a fixed namespace UUID for this app
        NAMESPACE_UUID = uuid.UUID('12345678-1234-5678-1234-567812345678')
        return f"indicator--{uuid.uuid5(NAMESPACE_UUID, ioc_value)}"

    def _ingest_urlhaus(self):
        stix_objs = []
        try:
            url = "https://urlhaus.abuse.ch/downloads/json_recent/"
            headers = {'User-Agent': 'Simple-TIP-Project/1.0'}
            print(f"Fetching URLhaus: {url}")
            r = requests.get(url, headers=headers)
            data = r.json()
            
            if 'urls' in data:
                # Limit to 50
                for item in data['urls'][:50]:
                    ioc_value = item.get('url')
                    if ioc_value:
                        obj_id = self._generate_id(ioc_value)
                        
                        # Use tags for better naming if available
                        tags = item.get('tags') or []
                        tag_str = ", ".join(tags[:2]) if tags else "Unknown"
                        name_str = f"Malware Distribution: {tag_str}" if tags else "Malicious URL (URLhaus)"
                        
                        # Add tags to labels
                        labels = ["malicious-activity", "urlhaus"] + tags
                        
                        ind = Indicator(
                            id=obj_id,
                            name=name_str,
                            description=f"Host: {item.get('urlhaus_reference')} | Source: {item.get('reporter')}",
                            pattern=f"[url:value = '{ioc_value}']",
                            pattern_type="stix",
                            valid_from=datetime.datetime.now(datetime.timezone.utc),
                            labels=labels,
                            confidence=80
                        )
                        stix_objs.append(json.loads(ind.serialize()))
                        
        except Exception as e:
            print(f"Error fetching URLhaus: {e}")
            
        return stix_objs

    def _ingest_feodo(self):
        stix_objs = []
        try:
            url = "https://feodotracker.abuse.ch/downloads/ipblocklist.json"
            headers = {'User-Agent': 'Simple-TIP-Project/1.0'}
            print(f"Fetching Feodo Tracker: {url}")
            r = requests.get(url, headers=headers)
            data = r.json()
            
            # data is a list of dicts
            for item in data[:50]:
                ip = item.get('ip_address')
                if ip:
                    obj_id = self._generate_id(ip)
                    malware = item.get('malware') or "Unknown Botnet"
                    
                    ind = Indicator(
                        id=obj_id,
                        name=f"{malware} C2 Node",
                        description=f"Active Botnet Command & Control Server detected by Feodo Tracker.",
                        pattern=f"[ipv4-addr:value = '{ip}']",
                        pattern_type="stix",
                        valid_from=datetime.datetime.now(datetime.timezone.utc),
                        labels=["botnet", "c2", "feodotracker", malware.lower()],
                        confidence=90
                    )
                    stix_objs.append(json.loads(ind.serialize()))
                    
        except Exception as e:
            print(f"Error fetching Feodo: {e}")
            
        return stix_objs

import json
