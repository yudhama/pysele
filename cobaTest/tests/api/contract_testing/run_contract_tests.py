#!/usr/bin/env python3
"""
Petstore3 Contract Test Runner
Runs comprehensive contract testing for the Petstore3 API
"""

import pytest
import sys
import os
from datetime import datetime

# Add the current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def run_contract_tests():
    """Run all contract tests with detailed reporting"""
    
    print("=" * 70)
    print("🔗 PETSTORE3 API CONTRACT TESTING")
    print("=" * 70)
    print(f"Started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"Python version: {sys.version}")
    print(f"Working directory: {os.getcwd()}")
    print("=" * 70)
    
    # Test arguments for comprehensive contract testing
    test_args = [
        "test_petstore3_contract.py",
        "-v",
        "--tb=short",
        "--html=petstore3_contract_test_report.html",
        "--self-contained-html",
        "--junitxml=petstore3_contract_test_results.xml",
        "--cov=.",
        "--cov-report=html:contract_coverage",
        "--cov-report=xml:contract_coverage.xml",
        "--cov-report=term-missing",
        "-x",  # Stop on first failure for contract tests
        "--strict-markers",
        "--disable-warnings"
    ]
    
    print("📋 Test Configuration:")
    print(f"   • Test file: test_petstore3_contract.py")
    print(f"   • HTML Report: petstore3_contract_test_report.html")
    print(f"   • XML Report: petstore3_contract_test_results.xml")
    print(f"   • Coverage Report: contract_coverage/index.html")
    print("   • Stop on first failure: Enabled")
    print("\n🚀 Starting contract tests...\n")
    
    # Run the tests
    exit_code = pytest.main(test_args)
    
    print("\n" + "=" * 70)
    print("📊 CONTRACT TEST EXECUTION SUMMARY")
    print("=" * 70)
    print(f"Test execution completed at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    if exit_code == 0:
        print("✅ ALL CONTRACT TESTS PASSED!")
        print("\n📋 Contract validation successful:")
        print("   • API endpoints conform to contract")
        print("   • Response schemas are valid")
        print("   • Error handling is consistent")
        print("   • Data integrity is maintained")
        print("\n📊 Reports generated:")
        print("   • HTML Report: petstore3_contract_test_report.html")
        print("   • JUnit XML: petstore3_contract_test_results.xml")
        print("   • Coverage Report: contract_coverage/index.html")
    else:
        print("❌ CONTRACT TESTS FAILED!")
        print(f"Exit code: {exit_code}")
        print("\n⚠️  Contract violations detected:")
        print("   • Check the reports for detailed information")
        print("   • Verify API endpoint implementations")
        print("   • Review response schema compliance")
        print("\n📊 Debug reports:")
        print("   • HTML Report: petstore3_contract_test_report.html")
        print("   • JUnit XML: petstore3_contract_test_results.xml")
    
    print("\n" + "=" * 70)
    return exit_code

def run_specific_contract_tests(test_pattern: str):
    """Run specific contract tests matching a pattern"""
    print(f"🎯 Running specific contract tests: {test_pattern}")
    
    test_args = [
        "test_petstore3_contract.py",
        "-k", test_pattern,
        "-v",
        "--tb=short",
        "--html=specific_contract_test_report.html",
        "--self-contained-html"
    ]
    
    return pytest.main(test_args)

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Petstore3 Contract Test Runner")
    parser.add_argument(
        "--pattern", 
        "-p",
        help="Run specific tests matching pattern"
    )
    parser.add_argument(
        "--list-tests",
        "-l",
        action="store_true",
        help="List available contract tests"
    )
    
    args = parser.parse_args()
    
    if args.list_tests:
        print("📋 Available Contract Test Categories:")
        print("   • add_pet_contract - Pet creation contract tests")
        print("   • get_pet_contract - Pet retrieval contract tests")
        print("   • update_pet_contract - Pet update contract tests")
        print("   • delete_pet_contract - Pet deletion contract tests")
        print("   • find_pets_contract - Pet search contract tests")
        print("   • response_time_contract - Performance contract tests")
        print("   • data_persistence_contract - Data integrity tests")
        print("   • error_handling_contract - Error response tests")
        sys.exit(0)
    
    if args.pattern:
        exit_code = run_specific_contract_tests(args.pattern)
    else:
        exit_code = run_contract_tests()
    
    sys.exit(exit_code)