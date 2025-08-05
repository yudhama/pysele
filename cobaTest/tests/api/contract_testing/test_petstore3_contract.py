import pytest
import requests
import json
from faker import Faker
from typing import Dict, Any
import time
import random

# Change these relative imports to absolute imports
from petstore3_client import Petstore3APIClient, Pet
from contract_validator import ContractValidator

class TestPetstore3Contract:
    """Comprehensive contract testing for Petstore3 API"""
    
    @pytest.fixture(scope="class")
    def api_client(self):
        """API client fixture"""
        return Petstore3APIClient()
    
    @pytest.fixture(scope="class")
    def contract_validator(self):
        """Contract validator fixture"""
        return ContractValidator()
    
    @pytest.fixture
    def fake(self):
        """Faker instance for generating test data"""
        return Faker()
    
    @pytest.fixture
    def sample_pet(self, fake) -> Pet:
        """Generate a sample pet for testing"""
        return Pet(
            id=random.randint(1000, 9999),
            name=fake.first_name(),
            category={"id": 1, "name": "Dogs"},
            photoUrls=[fake.image_url(), fake.image_url()],
            tags=[
                {"id": 1, "name": "friendly"},
                {"id": 2, "name": "trained"}
            ],
            status="available"
        )
    
    @pytest.fixture
    def created_pet_id(self, api_client, sample_pet):
        """Create a pet and return its ID for testing"""
        response = api_client.add_pet(sample_pet)
        if response.status_code == 200:
            pet_data = response.json()
            yield pet_data.get('id')
            # Cleanup
            try:
                api_client.delete_pet(pet_data.get('id'))
            except:
                pass  # Ignore cleanup errors
        else:
            pytest.skip("Failed to create test pet")
    
    # Contract Tests for Add Pet
    def test_add_pet_contract_success(self, api_client, contract_validator, sample_pet):
        """Test add pet contract - success scenario"""
        response = api_client.add_pet(sample_pet)
        
        # Contract validation
        validation = contract_validator.validate_response_contract(
            response, expected_status=200, schema_type="pet"
        )
        
        assert validation["status_code_valid"], f"Status code validation failed: {validation['errors']}"
        assert validation["content_type_valid"], "Content type validation failed"
        assert validation["schema_valid"], "Schema validation failed"
        
        # Verify response data
        pet_data = validation["response_data"]
        assert pet_data["name"] == sample_pet.name
        assert pet_data["status"] == sample_pet.status
        assert "id" in pet_data
        
        # Cleanup
        api_client.delete_pet(pet_data["id"])
    
    def test_add_pet_contract_invalid_data(self, api_client, contract_validator):
        """Test add pet contract - invalid data scenario"""
        invalid_pet = Pet(name="", photoUrls=[])  # Missing required name
        response = api_client.add_pet(invalid_pet)
        
        # Should return 400 or 422 for invalid data
        assert response.status_code in [400, 422, 405, 500], f"Expected error status, got {response.status_code}"
    
    def test_add_pet_contract_missing_required_fields(self, api_client, contract_validator):
        """Test add pet contract - missing required fields"""
        # Create pet with missing photoUrls
        incomplete_data = {
            "name": "Test Pet",
            "status": "available"
            # Missing photoUrls
        }
        
        response = api_client.session.post(
            f"{api_client.base_url}/pet",
            json=incomplete_data
        )
        
        # Should handle missing required fields
        assert response.status_code in [400, 422, 500], f"Expected validation error, got {response.status_code}"
    
    # Contract Tests for Get Pet
    def test_get_pet_contract_success(self, api_client, contract_validator, created_pet_id):
        """Test get pet by ID contract - success scenario"""
        response = api_client.get_pet_by_id(created_pet_id)
        
        validation = contract_validator.validate_response_contract(
            response, expected_status=200, schema_type="pet"
        )
        
        assert validation["status_code_valid"], f"Status code validation failed: {validation['errors']}"
        assert validation["content_type_valid"], "Content type validation failed"
        assert validation["schema_valid"], "Schema validation failed"
        
        pet_data = validation["response_data"]
        assert pet_data["id"] == created_pet_id
    
    def test_get_pet_contract_not_found(self, api_client, contract_validator):
        """Test get pet by ID contract - not found scenario"""
        non_existent_id = 999999999
        response = api_client.get_pet_by_id(non_existent_id)
        
        assert response.status_code == 404, f"Expected 404, got {response.status_code}"
    
    def test_get_pet_contract_invalid_id(self, api_client, contract_validator):
        """Test get pet by ID contract - invalid ID format"""
        # Test with string ID (should be integer)
        url = f"{api_client.base_url}/pet/invalid_id"
        response = api_client.session.get(url)
        
        assert response.status_code in [400, 404], f"Expected error status, got {response.status_code}"
    
    # Contract Tests for Update Pet
    def test_update_pet_contract_success(self, api_client, contract_validator, created_pet_id, fake):
        """Test update pet contract - success scenario"""
        # First get the existing pet
        get_response = api_client.get_pet_by_id(created_pet_id)
        existing_pet_data = get_response.json()
        
        # Update the pet
        updated_pet = Pet(
            id=created_pet_id,
            name=fake.first_name() + " Updated",
            category=existing_pet_data.get("category"),
            photoUrls=existing_pet_data.get("photoUrls"),
            tags=existing_pet_data.get("tags"),
            status="sold"
        )
        
        response = api_client.update_pet(updated_pet)
        
        validation = contract_validator.validate_response_contract(
            response, expected_status=200, schema_type="pet"
        )
        
        assert validation["status_code_valid"], f"Status code validation failed: {validation['errors']}"
        assert validation["content_type_valid"], "Content type validation failed"
        assert validation["schema_valid"], "Schema validation failed"
        
        pet_data = validation["response_data"]
        assert pet_data["name"] == updated_pet.name
        assert pet_data["status"] == "sold"
    
    def test_update_pet_contract_not_found(self, api_client, contract_validator, fake):
        """Test update pet contract - pet not found scenario"""
        non_existent_pet = Pet(
            id=999999999,
            name=fake.first_name(),
            photoUrls=[fake.image_url()],
            status="available"
        )
        
        response = api_client.update_pet(non_existent_pet)
        assert response.status_code in [404, 400], f"Expected error status, got {response.status_code}"
    
    # Contract Tests for Delete Pet
    def test_delete_pet_contract_success(self, api_client, contract_validator, sample_pet):
        """Test delete pet contract - success scenario"""
        # First create a pet
        create_response = api_client.add_pet(sample_pet)
        pet_data = create_response.json()
        pet_id = pet_data["id"]
        
        # Then delete it
        response = api_client.delete_pet(pet_id)
        assert response.status_code == 200, f"Expected 200, got {response.status_code}"
        
        # Verify it's deleted
        get_response = api_client.get_pet_by_id(pet_id)
        assert get_response.status_code == 404, "Pet should be deleted"
    
    def test_delete_pet_contract_not_found(self, api_client, contract_validator):
        """Test delete pet contract - pet not found scenario"""
        non_existent_id = 999999999
        response = api_client.delete_pet(non_existent_id)
        
        # API might return 404 or 200 for non-existent resources
        assert response.status_code in [200, 404], f"Unexpected status code: {response.status_code}"
    
    # Contract Tests for Find Pets by Status
    def test_find_pets_by_status_contract(self, api_client, contract_validator):
        """Test find pets by status contract"""
        for status in ["available", "pending", "sold"]:
            response = api_client.find_pets_by_status(status)
            
            assert response.status_code == 200, f"Expected 200 for status {status}, got {response.status_code}"
            assert response.headers.get('content-type') and 'application/json' in response.headers.get('content-type')
            
            pets_data = response.json()
            assert isinstance(pets_data, list), "Response should be a list of pets"
            
            # Validate each pet in the response
            for pet in pets_data[:5]:  # Validate first 5 pets to avoid long test times
                assert contract_validator.validate_pet_schema(pet), f"Pet schema validation failed for pet: {pet}"
                assert pet.get("status") == status, f"Pet status should be {status}"
    
    def test_find_pets_by_invalid_status_contract(self, api_client, contract_validator):
        """Test find pets by invalid status contract"""
        invalid_status = "invalid_status"
        response = api_client.find_pets_by_status(invalid_status)
        
        # Should return 400 for invalid status
        assert response.status_code in [400, 200], f"Expected 400 or 200, got {response.status_code}"
    
    # Performance Contract Tests
    def test_api_response_time_contract(self, api_client, contract_validator):
        """Test API response time contract"""
        start_time = time.time()
        response = api_client.find_pets_by_status("available")
        end_time = time.time()
        
        response_time = end_time - start_time
        
        assert response.status_code == 200, "API should be accessible"
        assert response_time < 5.0, f"API response time should be under 5 seconds, got {response_time:.2f}s"
    
    # Data Integrity Contract Tests
    def test_data_persistence_contract(self, api_client, contract_validator, sample_pet):
        """Test data persistence contract"""
        # Create pet
        create_response = api_client.add_pet(sample_pet)
        assert create_response.status_code == 200
        
        created_pet = create_response.json()
        pet_id = created_pet["id"]
        
        # Retrieve pet and verify data integrity
        get_response = api_client.get_pet_by_id(pet_id)
        assert get_response.status_code == 200
        
        retrieved_pet = get_response.json()
        
        # Verify data integrity
        assert retrieved_pet["name"] == sample_pet.name
        assert retrieved_pet["status"] == sample_pet.status
        assert retrieved_pet["photoUrls"] == sample_pet.photoUrls
        
        # Cleanup
        api_client.delete_pet(pet_id)
    
    # Error Handling Contract Tests
    def test_malformed_request_contract(self, api_client, contract_validator):
        """Test malformed request handling contract"""
        # Send malformed JSON
        url = f"{api_client.base_url}/pet"
        headers = {'Content-Type': 'application/json'}
        malformed_data = '{"name": "test", "invalid_json":}'
        
        response = requests.post(url, data=malformed_data, headers=headers)
        
        # Should return 400 for malformed JSON
        assert response.status_code in [400, 422], f"Expected 400/422 for malformed JSON, got {response.status_code}"
    
    def test_content_type_contract(self, api_client, contract_validator, sample_pet):
        """Test content type handling contract"""
        url = f"{api_client.base_url}/pet"
        
        # Send with wrong content type
        headers = {'Content-Type': 'text/plain'}
        response = requests.post(url, data=str(sample_pet.to_dict()), headers=headers)
        
        # Should return 415 for unsupported media type
        assert response.status_code in [400, 415], f"Expected 400/415 for wrong content type, got {response.status_code}"