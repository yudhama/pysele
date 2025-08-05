import requests
import json
from typing import Dict, Any, Optional, List
from dataclasses import dataclass
from datetime import datetime
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@dataclass
class Pet:
    """Pet data model"""
    id: Optional[int] = None
    name: str = ""
    category: Optional[Dict[str, Any]] = None
    photoUrls: List[str] = None
    tags: Optional[List[Dict[str, Any]]] = None
    status: str = "available"  # available, pending, sold
    
    def __post_init__(self):
        if self.photoUrls is None:
            self.photoUrls = []
        if self.category is None:
            self.category = {"id": 1, "name": "default"}
        if self.tags is None:
            self.tags = []

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for API requests"""
        data = {
            "name": self.name,
            "category": self.category,
            "photoUrls": self.photoUrls,
            "tags": self.tags,
            "status": self.status
        }
        if self.id is not None:
            data["id"] = self.id
        return data

class Petstore3APIClient:
    """Enhanced Petstore3 API Client with contract testing support"""
    
    def __init__(self, base_url: str = "https://petstore3.swagger.io/api/v3"):
        self.base_url = base_url
        self.session = requests.Session()
        self.session.headers.update({
            'Content-Type': 'application/json',
            'Accept': 'application/json',
            'User-Agent': 'Petstore3-API-Test-Client/1.0'
        })
        
    def add_pet(self, pet: Pet) -> requests.Response:
        """Add a new pet to the store"""
        url = f"{self.base_url}/pet"
        payload = pet.to_dict()
        
        logger.info(f"Adding pet: {payload}")
        response = self.session.post(url, json=payload)
        logger.info(f"Response: {response.status_code} - {response.text[:200]}")
        
        return response
    
    def get_pet_by_id(self, pet_id: int) -> requests.Response:
        """Find pet by ID"""
        url = f"{self.base_url}/pet/{pet_id}"
        
        logger.info(f"Getting pet by ID: {pet_id}")
        response = self.session.get(url)
        logger.info(f"Response: {response.status_code}")
        
        return response
    
    def update_pet(self, pet: Pet) -> requests.Response:
        """Update an existing pet"""
        url = f"{self.base_url}/pet"
        payload = pet.to_dict()
        
        logger.info(f"Updating pet: {payload}")
        response = self.session.put(url, json=payload)
        logger.info(f"Response: {response.status_code}")
        
        return response
    
    def delete_pet(self, pet_id: int, api_key: Optional[str] = None) -> requests.Response:
        """Delete a pet"""
        url = f"{self.base_url}/pet/{pet_id}"
        headers = {}
        if api_key:
            headers['api_key'] = api_key
            
        logger.info(f"Deleting pet ID: {pet_id}")
        response = self.session.delete(url, headers=headers)
        logger.info(f"Response: {response.status_code}")
        
        return response
    
    def find_pets_by_status(self, status: str) -> requests.Response:
        """Find pets by status"""
        url = f"{self.base_url}/pet/findByStatus"
        params = {'status': status}
        
        logger.info(f"Finding pets by status: {status}")
        response = self.session.get(url, params=params)
        logger.info(f"Response: {response.status_code}")
        
        return response
    
    def upload_pet_image(self, pet_id: int, file_data, additional_metadata: str = None) -> requests.Response:
        """Upload an image for a pet"""
        url = f"{self.base_url}/pet/{pet_id}/uploadImage"
        
        files = {'file': file_data}
        data = {}
        if additional_metadata:
            data['additionalMetadata'] = additional_metadata
            
        # Remove Content-Type for file upload
        headers = {k: v for k, v in self.session.headers.items() if k.lower() != 'content-type'}
        
        logger.info(f"Uploading image for pet ID: {pet_id}")
        response = self.session.post(url, files=files, data=data, headers=headers)
        logger.info(f"Response: {response.status_code}")
        
        return response