import requests
import pytest
import os
import json
from io import BytesIO
from PIL import Image
import tempfile

class TestPetstoreFileUpload:
    """
    Test suite for Swagger Petstore file upload API endpoint
    Endpoint: POST /pet/{petId}/uploadImage
    """
    
    BASE_URL = "https://petstore.swagger.io/v2"
    UPLOAD_ENDPOINT = "/pet/{pet_id}/uploadImage"
    
    @pytest.fixture
    def sample_image_file(self):
        """Create a sample image file for testing"""
        # Create a simple test image
        img = Image.new('RGB', (100, 100), color='red')
        img_bytes = BytesIO()
        img.save(img_bytes, format='JPEG')
        img_bytes.seek(0)
        return img_bytes
    
    @pytest.fixture
    def sample_text_file(self):
        """Create a sample text file for testing"""
        content = "This is a test file for API upload testing"
        return BytesIO(content.encode('utf-8'))
    
    @pytest.fixture
    def create_test_pet(self):
        """Create a test pet to use for file upload"""
        pet_data = {
            "id": 12345,
            "name": "Test Pet for Upload",
            "status": "available",
            "photoUrls": []
        }
        
        response = requests.post(
            f"{self.BASE_URL}/pet",
            json=pet_data,
            headers={"Content-Type": "application/json"}
        )
        
        if response.status_code in [200, 201]:
            return pet_data["id"]
        else:
            # If creation fails, use a default pet ID
            return 12345
    
    def test_upload_image_file_success(self, sample_image_file, create_test_pet):
        """Test successful image file upload"""
        pet_id = create_test_pet
        url = f"{self.BASE_URL}{self.UPLOAD_ENDPOINT.format(pet_id=pet_id)}"
        
        files = {
            'file': ('test_image.jpg', sample_image_file, 'image/jpeg')
        }
        data = {
            'additionalMetadata': 'Test image upload via API automation'
        }
        
        response = requests.post(url, files=files, data=data)
        
        # Assertions
        assert response.status_code == 200, f"Expected 200, got {response.status_code}"
        
        # Verify response contains expected fields
        response_data = response.json()
        assert 'code' in response_data
        assert 'type' in response_data
        assert 'message' in response_data
        
        print(f"Upload successful: {response_data}")
    
    def test_upload_with_additional_metadata(self, sample_image_file, create_test_pet):
        """Test file upload with additional metadata"""
        pet_id = create_test_pet
        url = f"{self.BASE_URL}{self.UPLOAD_ENDPOINT.format(pet_id=pet_id)}"
        
        metadata = "Custom metadata for testing - uploaded via automation"
        
        files = {
            'file': ('test_image_with_metadata.jpg', sample_image_file, 'image/jpeg')
        }
        data = {
            'additionalMetadata': metadata
        }
        
        response = requests.post(url, files=files, data=data)
        
        assert response.status_code == 200
        response_data = response.json()
        
        # Verify metadata is reflected in response
        assert metadata in response_data.get('message', '')
    
    def test_upload_without_file(self, create_test_pet):
        """Test upload request without file (should handle gracefully)"""
        pet_id = create_test_pet
        url = f"{self.BASE_URL}{self.UPLOAD_ENDPOINT.format(pet_id=pet_id)}"
        
        data = {
            'additionalMetadata': 'Upload without file test'
        }
        
        response = requests.post(url, data=data)
        
        # API should handle missing file gracefully
        assert response.status_code in [200, 400, 415], f"Unexpected status: {response.status_code}"
    
    def test_upload_invalid_pet_id(self, sample_image_file):
        """Test file upload with invalid pet ID"""
        invalid_pet_id = 999999999
        url = f"{self.BASE_URL}{self.UPLOAD_ENDPOINT.format(pet_id=invalid_pet_id)}"
        
        files = {
            'file': ('test_image.jpg', sample_image_file, 'image/jpeg')
        }
        data = {
            'additionalMetadata': 'Test with invalid pet ID'
        }
        
        response = requests.post(url, files=files, data=data)
        
        # Should still return 200 as per Swagger Petstore behavior
        assert response.status_code == 200
    
    def test_upload_large_file(self, create_test_pet):
        """Test upload with larger file size"""
        pet_id = create_test_pet
        url = f"{self.BASE_URL}{self.UPLOAD_ENDPOINT.format(pet_id=pet_id)}"
        
        # Create a larger test image
        img = Image.new('RGB', (1000, 1000), color='blue')
        img_bytes = BytesIO()
        img.save(img_bytes, format='JPEG', quality=95)
        img_bytes.seek(0)
        
        files = {
            'file': ('large_test_image.jpg', img_bytes, 'image/jpeg')
        }
        data = {
            'additionalMetadata': 'Large file upload test'
        }
        
        response = requests.post(url, files=files, data=data)
        
        assert response.status_code == 200
        print(f"Large file upload response: {response.json()}")
    
    def test_upload_different_file_types(self, sample_text_file, create_test_pet):
        """Test upload with different file types"""
        pet_id = create_test_pet
        url = f"{self.BASE_URL}{self.UPLOAD_ENDPOINT.format(pet_id=pet_id)}"
        
        # Test with text file
        files = {
            'file': ('test_document.txt', sample_text_file, 'text/plain')
        }
        data = {
            'additionalMetadata': 'Text file upload test'
        }
        
        response = requests.post(url, files=files, data=data)
        
        # API should accept any file type
        assert response.status_code == 200
    
    def test_upload_response_structure(self, sample_image_file, create_test_pet):
        """Test that response has correct structure"""
        pet_id = create_test_pet
        url = f"{self.BASE_URL}{self.UPLOAD_ENDPOINT.format(pet_id=pet_id)}"
        
        files = {
            'file': ('structure_test.jpg', sample_image_file, 'image/jpeg')
        }
        data = {
            'additionalMetadata': 'Response structure validation test'
        }
        
        response = requests.post(url, files=files, data=data)
        
        assert response.status_code == 200
        
        # Validate response structure
        response_data = response.json()
        required_fields = ['code', 'type', 'message']
        
        for field in required_fields:
            assert field in response_data, f"Missing required field: {field}"
        
        # Validate data types
        assert isinstance(response_data['code'], int)
        assert isinstance(response_data['type'], str)
        assert isinstance(response_data['message'], str)
    
    def test_upload_performance(self, sample_image_file, create_test_pet):
        """Test upload performance and response time"""
        import time
        
        pet_id = create_test_pet
        url = f"{self.BASE_URL}{self.UPLOAD_ENDPOINT.format(pet_id=pet_id)}"
        
        files = {
            'file': ('performance_test.jpg', sample_image_file, 'image/jpeg')
        }
        data = {
            'additionalMetadata': 'Performance test upload'
        }
        
        start_time = time.time()
        response = requests.post(url, files=files, data=data)
        end_time = time.time()
        
        response_time = end_time - start_time
        
        assert response.status_code == 200
        assert response_time < 10.0, f"Upload took too long: {response_time} seconds"
        
        print(f"Upload completed in {response_time:.2f} seconds")

if __name__ == "__main__":
    # Run tests directly
    pytest.main([__file__, "-v"])