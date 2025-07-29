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
    
    def upload_file(self, pet_id: int, file_path: str = None, file_content: bytes = None, 
                   filename: str = None, content_type: str = None, 
                   additional_metadata: str = None) -> Dict[Any, Any]:
        """Upload a file for a pet
        
        Args:
            pet_id: ID of the pet
            file_path: Path to file to upload
            file_content: Raw file content as bytes
            filename: Name of the file
            content_type: MIME type of the file
            additional_metadata: Additional metadata to send
            
        Returns:
            API response as dictionary
        """
        url = f"{self.base_url}/pet/{pet_id}/uploadImage"
        
        files = {}
        data = {}
        
        if file_path:
            with open(file_path, 'rb') as f:
                files['file'] = (filename or file_path, f, content_type)
        elif file_content:
            files['file'] = (filename or 'upload.bin', file_content, content_type)
        
        if additional_metadata:
            data['additionalMetadata'] = additional_metadata
        
        response = self.session.post(url, files=files, data=data)
        
        return {
            'status_code': response.status_code,
            'headers': dict(response.headers),
            'data': response.json() if response.content else None,
            'response_time': response.elapsed.total_seconds()
        }
    
    def create_pet(self, pet_data: Dict[str, Any]) -> Dict[Any, Any]:
        """Create a new pet
        
        Args:
            pet_data: Pet information dictionary
            
        Returns:
            API response as dictionary
        """
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
        """Get pet by ID
        
        Args:
            pet_id: ID of the pet
            
        Returns:
            API response as dictionary
        """
        url = f"{self.base_url}/pet/{pet_id}"
        
        response = self.session.get(url)
        
        return {
            'status_code': response.status_code,
            'headers': dict(response.headers),
            'data': response.json() if response.content else None
        }
    
    def delete_pet(self, pet_id: int, api_key: str = None) -> Dict[Any, Any]:
        """Delete a pet
        
        Args:
            pet_id: ID of the pet to delete
            api_key: API key for authorization
            
        Returns:
            API response as dictionary
        """
        url = f"{self.base_url}/pet/{pet_id}"
        headers = {}
        
        if api_key:
            headers['api_key'] = api_key
        
        response = self.session.delete(url, headers=headers)
        
        return {
            'status_code': response.status_code,
            'headers': dict(response.headers),
            'data': response.json() if response.content else None
        }