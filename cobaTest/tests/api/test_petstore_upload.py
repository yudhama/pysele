import requests
import pytest
import os
import json
from io import BytesIO
from PIL import Image
import tempfile

class TestPetstoreFileUpload:
    """
    Test suite for Swagger Petstore File Upload API endpoint
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
        
        # Create pet first
        create_url = f"{self.BASE_URL}/pet"
        response = requests.post(create_url, json=pet_data)
        
        if response.status_code == 200:
            return pet_data["id"]
        else:
            # If creation fails, just return the ID anyway for testing
            return pet_data["id"]
    
    def test_upload_image_success(self, sample_image_file, create_test_pet):
        """Test successful image upload"""
        pet_id = create_test_pet
        url = f"{self.BASE_URL}{self.UPLOAD_ENDPOINT.format(pet_id=pet_id)}"
        
        files = {'file': ('test_image.jpg', sample_image_file, 'image/jpeg')}
        data = {'additionalMetadata': 'Test image upload'}
        
        response = requests.post(url, files=files, data=data)
        
        assert response.status_code == 200
        
        response_data = response.json()
        assert 'code' in response_data
        assert 'type' in response_data
        assert 'message' in response_data
    
    def test_upload_with_metadata(self, sample_image_file, create_test_pet):
        """Test upload with additional metadata"""
        pet_id = create_test_pet
        url = f"{self.BASE_URL}{self.UPLOAD_ENDPOINT.format(pet_id=pet_id)}"
        
        metadata = "Profile picture for test pet"
        files = {'file': ('profile.jpg', sample_image_file, 'image/jpeg')}
        data = {'additionalMetadata': metadata}
        
        response = requests.post(url, files=files, data=data)
        
        assert response.status_code == 200
        response_data = response.json()
        assert metadata in response_data.get('message', '')
    
    def test_upload_without_file(self, create_test_pet):
        """Test upload request without file"""
        pet_id = create_test_pet
        url = f"{self.BASE_URL}{self.UPLOAD_ENDPOINT.format(pet_id=pet_id)}"
        
        data = {'additionalMetadata': 'No file upload test'}
        
        response = requests.post(url, data=data)
        
        # Should handle missing file gracefully
        assert response.status_code in [200, 400]
    
    def test_upload_invalid_pet_id(self, sample_image_file):
        """Test upload with invalid pet ID"""
        invalid_pet_id = 999999999
        url = f"{self.BASE_URL}{self.UPLOAD_ENDPOINT.format(pet_id=invalid_pet_id)}"
        
        files = {'file': ('test.jpg', sample_image_file, 'image/jpeg')}
        
        response = requests.post(url, files=files)
        
        # Should return error for invalid pet ID
        assert response.status_code in [404, 400]
    
    def test_upload_large_file(self, create_test_pet):
        """Test upload with larger file"""
        pet_id = create_test_pet
        url = f"{self.BASE_URL}{self.UPLOAD_ENDPOINT.format(pet_id=pet_id)}"
        
        # Create a larger test image
        img = Image.new('RGB', (1000, 1000), color='blue')
        img_bytes = BytesIO()
        img.save(img_bytes, format='JPEG')
        img_bytes.seek(0)
        
        files = {'file': ('large_image.jpg', img_bytes, 'image/jpeg')}
        data = {'additionalMetadata': 'Large file upload test'}
        
        response = requests.post(url, files=files, data=data)
        
        assert response.status_code == 200
    
    def test_upload_different_file_types(self, sample_text_file, create_test_pet):
        """Test upload with different file types"""
        pet_id = create_test_pet
        url = f"{self.BASE_URL}{self.UPLOAD_ENDPOINT.format(pet_id=pet_id)}"
        
        # Test with text file
        files = {'file': ('test.txt', sample_text_file, 'text/plain')}
        data = {'additionalMetadata': 'Text file upload test'}
        
        response = requests.post(url, files=files, data=data)
        
        # Should accept different file types
        assert response.status_code == 200
    
    def test_upload_response_structure(self, sample_image_file, create_test_pet):
        """Test that response has correct structure"""
        pet_id = create_test_pet
        url = f"{self.BASE_URL}{self.UPLOAD_ENDPOINT.format(pet_id=pet_id)}"
        
        files = {'file': ('structure_test.jpg', sample_image_file, 'image/jpeg')}
        
        response = requests.post(url, files=files)
        
        assert response.status_code == 200
        assert response.headers.get('content-type') == 'application/json'
        
        response_data = response.json()
        
        # Verify response structure
        assert isinstance(response_data, dict)
        assert 'code' in response_data
        assert 'type' in response_data
        assert 'message' in response_data
        
        # Verify data types
        assert isinstance(response_data['code'], int)
        assert isinstance(response_data['type'], str)
        assert isinstance(response_data['message'], str)
    
    def test_upload_performance(self, sample_image_file, create_test_pet):
        """Test upload performance and response time"""
        import time
        
        pet_id = create_test_pet
        url = f"{self.BASE_URL}{self.UPLOAD_ENDPOINT.format(pet_id=pet_id)}"
        
        files = {'file': ('performance_test.jpg', sample_image_file, 'image/jpeg')}
        
        start_time = time.time()
        response = requests.post(url, files=files)
        end_time = time.time()
        
        response_time = end_time - start_time
        
        assert response.status_code == 200
        assert response_time < 10.0  # Should complete within 10 seconds
        
        print(f"Upload completed in {response_time:.2f} seconds")

if __name__ == "__main__":
    # Run tests directly
    pytest.main([__file__, "-v"])