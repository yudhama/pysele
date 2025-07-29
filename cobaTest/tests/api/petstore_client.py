import requests
import json
from typing import Optional, Dict, Any

class PetstoreAPIClient:
    """Client for interacting with Swagger Petstore API"""
    
    def __init__(self, base_url: str = "https://petstore.swagger.io/v2"):
        self.base_url = base_url
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Petstore-API-Test-Client/1.0'
        })
    
    def upload_file(self, pet_id: int, file_data, additional_metadata: str = None) -> Dict[Any, Any]:
        """Upload a file for a pet"""
        url = f"{self.base_url}/pet/{pet_id}/uploadImage"
        
        files = {'file': file_data}
        data = {}
        
        if additional_metadata:
            data['additionalMetadata'] = additional_metadata
        
        response = self.session.post(url, files=files, data=data)
        
        return {
            'status_code': response.status_code,
            'headers': dict(response.headers),
            'data': response.json() if response.content else None
        }
    
    def add_pet(self, pet_data: Dict[str, Any]) -> Dict[Any, Any]:
        """Add a new pet to the store"""
        url = f"{self.base_url}/pet"
        
        response = self.session.post(
            url, 
            json=pet_data,
            headers={'Content-Type': 'application/json'}
        )
        
        return {
            'status_code': response.status_code,
            'headers': dict(response.headers),
            'data': response.json() if response.content else None
        }
    
    def get_pet(self, pet_id: int) -> Dict[Any, Any]:
        """Get pet by ID"""
        url = f"{self.base_url}/pet/{pet_id}"
        
        response = self.session.get(url)
        
        return {
            'status_code': response.status_code,
            'headers': dict(response.headers),
            'data': response.json() if response.content else None
        }
    
    def close(self):
        """Close the session"""
        self.session.close()