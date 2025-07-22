import logging
import time

# Import all security tests
from cobaTest.tests.security.test_xss_vulnerability import test_xss_vulnerability
from cobaTest.tests.security.test_sql_injection import test_sql_injection
from cobaTest.tests.security.test_authentication_security import test_authentication_security
from cobaTest.tests.security.test_csrf_vulnerability import test_csrf_vulnerability

# Set up logging
logging.basicConfig(level=logging.INFO, 
                    format='%(asctime)s - %(levelname)s - %(message)s',
                    filename='security_test_suite.log')
logger = logging.getLogger(__name__)

def run_all_security_tests():
    """Run all security tests and generate a summary report"""
    start_time = time.time()
    logger.info("Starting security test suite...")
    
    tests = [
        ("XSS Vulnerability Test", test_xss_vulnerability),
        ("SQL Injection Test", test_sql_injection),
        ("Authentication Security Test", test_authentication_security),
        ("CSRF Vulnerability Test", test_csrf_vulnerability)
    ]
    
    results = {}
    
    for test_name, test_func in tests:
        logger.info(f"Running {test_name}...")
        print(f"Running {test_name}...")
        
        try:
            test_func()
            results[test_name] = "Passed"
        except Exception as e:
            logger.error(f"{test_name} failed: {e}")
            results[test_name] = f"Failed: {e}"
        
        logger.info(f"Completed {test_name}")
        print(f"Completed {test_name}")
    
    # Generate summary report
    logger.info("\nSecurity Test Suite Summary:")
    print("\nSecurity Test Suite Summary:")
    
    for test_name, result in results.items():
        logger.info(f"{test_name}: {result}")
        print(f"{test_name}: {result}")
    
    end_time = time.time()
    duration = end_time - start_time
    logger.info(f"\nTotal execution time: {duration:.2f} seconds")
    print(f"\nTotal execution time: {duration:.2f} seconds")

if __name__ == "__main__":
    run_all_security_tests()