import requests
import os

class VirusTotalEnricher:
    def __init__(self):
        self.api_key = os.environ.get('VT_API_KEY') or 'PLACEHOLDER_KEY'
        self.base_url = "https://www.virustotal.com/api/v3"

    def enrich_ioc(self, ioc_value, ioc_type):
        """
        Query VT for an IOC.
        ioc_type: 'ip', 'domain', 'hash', 'url'
        """
        if self.api_key == 'PLACEHOLDER_KEY':
            return {
                'error': 'No API Key configured.',
                'reputation': 0,
                'last_analysis_stats': {'harmless': 0, 'malicious': 0, 'suspicious': 0, 'undetected': 0},
                'tags': ['demo', 'simulated']
            }

        headers = {
            "x-apikey": self.api_key
        }

        endpoint = ""
        if ioc_type == 'ipv4-addr':
            endpoint = f"/ip_addresses/{ioc_value}"
        elif ioc_type == 'domain-name':
            endpoint = f"/domains/{ioc_value}"
        elif ioc_type == 'file': # hash
             endpoint = f"/files/{ioc_value}"
        else:
            return {'error': 'Unsupported type for enrichment'}

        try:
            url = f"{self.base_url}{endpoint}"
            r = requests.get(url, headers=headers)
            if r.status_code == 200:
                data = r.json()
                attr = data.get('data', {}).get('attributes', {})
                return {
                    'reputation': attr.get('reputation'),
                    'last_analysis_stats': attr.get('last_analysis_stats'),
                    'tags': attr.get('tags', [])
                }
            else:
                return {'error': f"VT API returned {r.status_code}"}
        except Exception as e:
            return {'error': str(e)}
