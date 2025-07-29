#!/usr/bin/env python3
"""
Petstore API Test Runner
Runs all API tests for the Swagger Petstore file upload functionality
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
        'test_petstore_upload.py',
        '-v',  # Verbose output
        '--tb=short',  # Short traceback format
        '--capture=no',  # Don't capture stdout
        '--durations=10',  # Show 10 slowest tests
        '--junitxml=petstore_api_test_results.xml',  # Generate XML report
        '--html=petstore_api_test_report.html',  # Generate HTML report
        '--self-contained-html'  # Embed CSS/JS in HTML report
    ]
    
    try:
        # Run the tests
        exit_code = pytest.main(test_args)
        
        print()
        print("=" * 60)
        print("TEST EXECUTION SUMMARY")
        print("=" * 60)
        
        if exit_code == 0:
            print("✅ All tests passed successfully!")
        elif exit_code == 1:
            print("❌ Some tests failed. Check the output above for details.")
        elif exit_code == 2:
            print("⚠️  Test execution was interrupted.")
        else:
            print(f"❓ Test execution completed with exit code: {exit_code}")
        
        print(f"Test execution completed at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print()
        print("Generated Reports:")
        print("- XML Report: petstore_api_test_results.xml")
        print("- HTML Report: petstore_api_test_report.html")
        
        return exit_code
        
    except Exception as e:
        print(f"❌ Error running tests: {str(e)}")
        return 1

if __name__ == "__main__":
    exit_code = run_petstore_api_tests()
    sys.exit(exit_code)