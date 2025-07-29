import requests
import pytest
import json
from datetime import datetime
import random

class TestPetstoreAddPet:
    """
    Test suite for Swagger Petstore Add Pet API endpoint
    Endpoint: POST /pet
    """
    
    BASE_URL = "https://petstore.swagger.io/v2"
    ADD_PET_ENDPOINT = "/pet"
    
    @pytest.fixture
    def valid_pet_data(self):
        """Generate valid pet data for testing"""
        return {
            "id": random.randint(1000, 9999),
            "category": {
                "id": 1,
                "name": "Dogs"
            },
            "name": f"Test Pet {datetime.now().strftime('%Y%m%d_%H%M%S')}",
            "photoUrls": [
                "https://example.com/photo1.jpg",
                "https://example.com/photo2.jpg"
            ],
            "tags": [
                {
                    "id": 1,
                    "name": "friendly"
                },
                {
                    "id": 2,
                    "name": "trained"
                }
            ],
            "status": "available"
        }
    
    @pytest.fixture
    def minimal_pet_data(self):
        """Generate minimal required pet data"""
        return {
            "name": f"Minimal Pet {datetime.now().strftime('%Y%m%d_%H%M%S')}",
            "photoUrls": ["https://example.com/photo.jpg"]
        }
    
    def test_add_pet_valid_data(self, valid_pet_data):
        """Test pet creation with valid complete data"""
        url = f"{self.BASE_URL}{self.ADD_PET_ENDPOINT}"
        
        response = requests.post(
            url,
            json=valid_pet_data,
            headers={"Content-Type": "application/json"}
        )
        
        assert response.status_code == 200
        
        response_data = response.json()
        assert response_data["id"] == valid_pet_data["id"]
        assert response_data["name"] == valid_pet_data["name"]
        assert response_data["status"] == valid_pet_data["status"]
    
    def test_add_pet_minimal_data(self, minimal_pet_data):
        """Test pet creation with minimal required fields"""
        url = f"{self.BASE_URL}{self.ADD_PET_ENDPOINT}"
        
        response = requests.post(
            url,
            json=minimal_pet_data,
            headers={"Content-Type": "application/json"}
        )
        
        assert response.status_code == 200
        
        response_data = response.json()
        assert response_data["name"] == minimal_pet_data["name"]
        assert "photoUrls" in response_data
    
    def test_add_pet_different_statuses(self, valid_pet_data):
        """Test pet creation with different status values"""
        url = f"{self.BASE_URL}{self.ADD_PET_ENDPOINT}"
        statuses = ["available", "pending", "sold"]
        
        for status in statuses:
            pet_data = valid_pet_data.copy()
            pet_data["id"] = random.randint(10000, 99999)  # Unique ID for each
            pet_data["status"] = status
            pet_data["name"] = f"Pet with {status} status"
            
            response = requests.post(
                url,
                json=pet_data,
                headers={"Content-Type": "application/json"}
            )
            
            assert response.status_code == 200
            response_data = response.json()
            assert response_data["status"] == status
    
    def test_add_pet_missing_required_fields(self):
        """Test pet creation with missing required fields"""
        url = f"{self.BASE_URL}{self.ADD_PET_ENDPOINT}"
        
        # Test with missing name
        invalid_data = {
            "photoUrls": ["https://example.com/photo.jpg"]
        }
        
        response = requests.post(
            url,
            json=invalid_data,
            headers={"Content-Type": "application/json"}
        )
        
        assert response.status_code in [400, 405]
    
    def test_add_pet_invalid_data_types(self):
        """Test pet creation with invalid data types"""
        url = f"{self.BASE_URL}{self.ADD_PET_ENDPOINT}"
        
        invalid_data = {
            "id": "not_a_number",
            "name": 12345,  # Should be string
            "photoUrls": "not_an_array"
        }
        
        response = requests.post(
            url,
            json=invalid_data,
            headers={"Content-Type": "application/json"}
        )
        
        assert response.status_code in [400, 405]
    
    def test_add_pet_empty_request(self):
        """Test pet creation with empty request body"""
        url = f"{self.BASE_URL}{self.ADD_PET_ENDPOINT}"
        
        response = requests.post(
            url,
            json={},
            headers={"Content-Type": "application/json"}
        )
        
        assert response.status_code == 405
    
    def test_add_pet_duplicate_id(self, valid_pet_data):
        """Test creating pets with duplicate IDs"""
        url = f"{self.BASE_URL}{self.ADD_PET_ENDPOINT}"
        
        # Create first pet
        response1 = requests.post(
            url,
            json=valid_pet_data,
            headers={"Content-Type": "application/json"}
        )
        
        assert response1.status_code == 200
        
        # Try to create second pet with same ID
        duplicate_data = valid_pet_data.copy()
        duplicate_data["name"] = "Duplicate ID Pet"
        
        response2 = requests.post(
            url,
            json=duplicate_data,
            headers={"Content-Type": "application/json"}
        )
        
        # Should either succeed (update) or handle gracefully
        assert response2.status_code in [200, 400]
    
    def test_add_pet_large_data(self):
        """Test pet creation with large data sets"""
        url = f"{self.BASE_URL}{self.ADD_PET_ENDPOINT}"
        
        large_data = {
            "id": random.randint(100000, 999999),
            "name": "A" * 100,  # Long name
            "photoUrls": [f"https://example.com/photo{i}.jpg" for i in range(10)],
            "tags": [
                {"id": i, "name": f"tag{i}"} for i in range(20)
            ],
            "status": "available"
        }
        
        response = requests.post(
            url,
            json=large_data,
            headers={"Content-Type": "application/json"}
        )
        
        assert response.status_code == 200
    
    def test_add_pet_special_characters(self):
        """Test pet creation with special characters in name"""
        url = f"{self.BASE_URL}{self.ADD_PET_ENDPOINT}"
        
        special_data = {
            "id": random.randint(1000, 9999),
            "name": "Pet with 特殊字符 & émojis 🐕",
            "photoUrls": ["https://example.com/photo.jpg"],
            "status": "available"
        }
        
        response = requests.post(
            url,
            json=special_data,
            headers={"Content-Type": "application/json"}
        )
        
        assert response.status_code == 200
        response_data = response.json()
        assert response_data["name"] == special_data["name"]
    
    def test_add_pet_response_structure(self, valid_pet_data):
        """Test that response has correct structure and data types"""
        url = f"{self.BASE_URL}{self.ADD_PET_ENDPOINT}"
        
        response = requests.post(
            url,
            json=valid_pet_data,
            headers={"Content-Type": "application/json"}
        )
        
        assert response.status_code == 200
        assert response.headers.get('content-type') == 'application/json'
        
        response_data = response.json()
        
        # Verify response structure
        assert isinstance(response_data, dict)
        assert "id" in response_data
        assert "name" in response_data
        assert "photoUrls" in response_data
        
        # Verify data types
        assert isinstance(response_data["id"], int)
        assert isinstance(response_data["name"], str)
        assert isinstance(response_data["photoUrls"], list)
    
    def test_add_pet_performance(self, valid_pet_data):
        """Test API response time performance"""
        import time
        
        url = f"{self.BASE_URL}{self.ADD_PET_ENDPOINT}"
        
        start_time = time.time()
        response = requests.post(
            url,
            json=valid_pet_data,
            headers={"Content-Type": "application/json"}
        )
        end_time = time.time()
        
        response_time = end_time - start_time
        
        assert response.status_code == 200
        assert response_time < 5.0  # Should complete within 5 seconds
        
        print(f"Add pet completed in {response_time:.2f} seconds")
    
    def test_add_pet_content_type_variations(self, valid_pet_data):
        """Test different content-type headers"""
        url = f"{self.BASE_URL}{self.ADD_PET_ENDPOINT}"
        
        # Test with application/json
        response = requests.post(
            url,
            json=valid_pet_data,
            headers={"Content-Type": "application/json"}
        )
        assert response.status_code == 200
        
        # Test with application/xml (if supported)
        xml_data = f"""
        <Pet>
            <id>{valid_pet_data['id'] + 1}</id>
            <name>XML Test Pet</name>
            <photoUrls>
                <photoUrl>https://example.com/xml_photo.jpg</photoUrl>
            </photoUrls>
            <status>available</status>
        </Pet>
        """
        
        response_xml = requests.post(
            url,
            data=xml_data,
            headers={"Content-Type": "application/xml"}
        )
        
        # XML might not be supported, so accept various responses
        assert response_xml.status_code in [200, 400, 415]

if __name__ == "__main__":
    # Run tests directly
    pytest.main([__file__, "-v"])