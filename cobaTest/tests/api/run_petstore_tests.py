#!/usr/bin/env python3
"""
Petstore API Test Runner
Runs all API tests for the Swagger Petstore functionality
"""

import pytest
import sys
import os
from datetime import datetime

def run_petstore_api_tests():
    """Run all Petstore API tests with detailed reporting"""
    
    print("=" * 60)
    print("SWAGGER PETSTORE API AUTOMATION TESTS")
    print("=" * 60)
    print(f"Test execution started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    # Test configuration
    test_args = [
        # Test files to run
        "test_petstore_upload.py",
        "test_petstore_add_pet.py",
        
        # Verbose output
        "-v",
        
        # Show local variables in tracebacks
        "-l",
        
        # Stop on first failure (optional)
        # "--maxfail=1",
        
        # Generate HTML report
        "--html=petstore_api_test_report.html",
        "--self-contained-html",
        
        # Generate JUnit XML report
        "--junitxml=petstore_api_test_results.xml",
        
        # Show test durations
        "--durations=10",
        
        # Capture output
        "--capture=no",
        
        # Show warnings
        "-W", "ignore::DeprecationWarning"
    ]
    
    # Add coverage if pytest-cov is available
    try:
        import pytest_cov
        test_args.extend([
            "--cov=.",
            "--cov-report=html",
            "--cov-report=term-missing"
        ])
        print("✓ Code coverage reporting enabled")
    except ImportError:
        print("ℹ Code coverage not available (install pytest-cov for coverage reports)")
    
    print("\nRunning tests...")
    print("-" * 40)
    
    # Run the tests
    exit_code = pytest.main(test_args)
    
    print("\n" + "=" * 60)
    print("TEST EXECUTION SUMMARY")
    print("=" * 60)
    print(f"Test execution completed at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    if exit_code == 0:
        print("✅ ALL TESTS PASSED!")
        print("\n📊 Reports generated:")
        print("   • HTML Report: petstore_api_test_report.html")
        print("   • JUnit XML: petstore_api_test_results.xml")
        if 'pytest_cov' in sys.modules:
            print("   • Coverage Report: htmlcov/index.html")
    else:
        print("❌ SOME TESTS FAILED!")
        print(f"Exit code: {exit_code}")
        print("\nCheck the reports for detailed information:")
        print("   • HTML Report: petstore_api_test_report.html")
        print("   • JUnit XML: petstore_api_test_results.xml")
    
    print("\n🔍 Test Categories Covered:")
    print("   • File Upload API Tests (test_petstore_upload.py)")
    print("   • Add Pet API Tests (test_petstore_add_pet.py)")
    print("     - Valid data scenarios")
    print("     - Different status values")
    print("     - Error handling")
    print("     - Performance testing")
    print("     - Response validation")
    print("     - Content-type variations")
    
    return exit_code

def run_upload_tests_only():
    """Run only file upload tests"""
    print("Running File Upload Tests Only...")
    return pytest.main([
        "test_petstore_upload.py",
        "-v",
        "--html=upload_test_report.html",
        "--self-contained-html"
    ])

def run_add_pet_tests_only():
    """Run only add pet tests"""
    print("Running Add Pet Tests Only...")
    return pytest.main([
        "test_petstore_add_pet.py",
        "-v",
        "--html=add_pet_test_report.html",
        "--self-contained-html"
    ])

def run_specific_test(test_name: str):
    """Run a specific test by name
    
    Args:
        test_name: Name of the test to run (e.g., 'test_add_pet_valid_data')
    """
    print(f"Running specific test: {test_name}")
    return pytest.main([
        "-k", test_name,
        "-v",
        "--tb=short"
    ])

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Petstore API Test Runner")
    parser.add_argument(
        "--test-type", 
        choices=["all", "upload", "add-pet"], 
        default="all",
        help="Type of tests to run"
    )
    parser.add_argument(
        "--specific", 
        help="Run a specific test by name"
    )
    
    args = parser.parse_args()
    
    if args.specific:
        exit_code = run_specific_test(args.specific)
    elif args.test_type == "upload":
        exit_code = run_upload_tests_only()
    elif args.test_type == "add-pet":
        exit_code = run_add_pet_tests_only()
    else:
        exit_code = run_petstore_api_tests()
    
    sys.exit(exit_code)