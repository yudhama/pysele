import json
import jsonschema
from typing import Dict, Any, List
from jsonschema import validate, ValidationError
import requests

class ContractValidator:
    """Contract testing validator for Petstore3 API"""
    
    def __init__(self):
        self.schemas = self._load_schemas()
    
    def _load_schemas(self) -> Dict[str, Dict[str, Any]]:
        """Load API contract schemas"""
        return {
            "pet": {
                "type": "object",
                "required": ["name", "photoUrls"],
                "properties": {
                    "id": {
                        "type": "integer",
                        "format": "int64",
                        "example": 10
                    },
                    "name": {
                        "type": "string",
                        "example": "doggie"
                    },
                    "category": {
                        "type": "object",
                        "properties": {
                            "id": {
                                "type": "integer",
                                "format": "int64",
                                "example": 1
                            },
                            "name": {
                                "type": "string",
                                "example": "Dogs"
                            }
                        }
                    },
                    "photoUrls": {
                        "type": "array",
                        "items": {
                            "type": "string"
                        }
                    },
                    "tags": {
                        "type": "array",
                        "items": {
                            "type": "object",
                            "properties": {
                                "id": {
                                    "type": "integer",
                                    "format": "int64"
                                },
                                "name": {
                                    "type": "string"
                                }
                            }
                        }
                    },
                    "status": {
                        "type": "string",
                        "description": "pet status in the store",
                        "enum": ["available", "pending", "sold"]
                    }
                }
            },
            "api_response": {
                "type": "object",
                "properties": {
                    "code": {
                        "type": "integer",
                        "format": "int32"
                    },
                    "type": {
                        "type": "string"
                    },
                    "message": {
                        "type": "string"
                    }
                }
            },
            "error": {
                "type": "object",
                "properties": {
                    "code": {
                        "type": "integer",
                        "format": "int32"
                    },
                    "message": {
                        "type": "string"
                    }
                }
            }
        }
    
    def validate_pet_schema(self, pet_data: Dict[str, Any]) -> bool:
        """Validate pet data against schema"""
        try:
            validate(instance=pet_data, schema=self.schemas["pet"])
            return True
        except ValidationError as e:
            print(f"Pet schema validation failed: {e.message}")
            return False
    
    def validate_api_response_schema(self, response_data: Dict[str, Any]) -> bool:
        """Validate API response against schema"""
        try:
            validate(instance=response_data, schema=self.schemas["api_response"])
            return True
        except ValidationError as e:
            print(f"API response schema validation failed: {e.message}")
            return False
    
    def validate_error_schema(self, error_data: Dict[str, Any]) -> bool:
        """Validate error response against schema"""
        try:
            validate(instance=error_data, schema=self.schemas["error"])
            return True
        except ValidationError as e:
            print(f"Error schema validation failed: {e.message}")
            return False
    
    def validate_response_contract(self, response: requests.Response, expected_status: int, schema_type: str = "pet") -> Dict[str, Any]:
        """Comprehensive contract validation"""
        validation_result = {
            "status_code_valid": response.status_code == expected_status,
            "content_type_valid": False,
            "schema_valid": False,
            "response_data": None,
            "errors": []
        }
        
        # Validate status code
        if not validation_result["status_code_valid"]:
            validation_result["errors"].append(f"Expected status {expected_status}, got {response.status_code}")
        
        # Validate content type
        content_type = response.headers.get('content-type', '')
        if 'application/json' in content_type:
            validation_result["content_type_valid"] = True
            
            try:
                response_data = response.json()
                validation_result["response_data"] = response_data
                
                # Validate schema based on status code
                if response.status_code == 200 and schema_type == "pet":
                    validation_result["schema_valid"] = self.validate_pet_schema(response_data)
                elif response.status_code >= 400:
                    validation_result["schema_valid"] = self.validate_error_schema(response_data)
                else:
                    validation_result["schema_valid"] = True  # No specific schema for other responses
                    
            except json.JSONDecodeError:
                validation_result["errors"].append("Invalid JSON response")
        else:
            validation_result["errors"].append(f"Expected JSON content type, got {content_type}")
        
        return validation_result