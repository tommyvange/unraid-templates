#!/usr/bin/env python3
"""
Test runner for UnRAID template validation
"""

import os
import sys
import subprocess
import tempfile


def create_test_templates():
    """Create test templates for validation testing."""
    test_dir = tempfile.mkdtemp()
    
    # Valid template
    valid_template = """<?xml version="1.0"?>
<Container version="2">
  <Name>TestContainer</Name>
  <Repository>test/container</Repository>
  <Network>bridge</Network>
  <Overview>A test container for validation</Overview>
  <Category>Tools:</Category>
</Container>"""
    
    # Invalid template (missing required elements)
    invalid_template = """<?xml version="1.0"?>
<Container version="2">
  <Name>TestContainer</Name>
  <Repository>test/container</Repository>
  <!-- Missing Network, Overview, Category -->
</Container>"""
    
    # Malformed XML
    malformed_template = """<?xml version="1.0"?>
<Container version="2">
  <Name>TestContainer</Name>
  <Repository>test/container</Repository>
  <Network>bridge</Network>
  <!-- Missing closing tag"""
    
    valid_file = os.path.join(test_dir, "valid.xml")
    invalid_file = os.path.join(test_dir, "invalid.xml")
    malformed_file = os.path.join(test_dir, "malformed.xml")
    
    with open(valid_file, 'w') as f:
        f.write(valid_template)
    
    with open(invalid_file, 'w') as f:
        f.write(invalid_template)
        
    with open(malformed_file, 'w') as f:
        f.write(malformed_template)
    
    return test_dir, valid_file, invalid_file, malformed_file


def run_validation_test(script_path, test_file, should_pass):
    """Run validation test and check if result matches expectation."""
    try:
        result = subprocess.run([sys.executable, script_path, test_file], 
                              capture_output=True, text=True)
        
        if should_pass:
            if result.returncode == 0:
                print(f"✅ {os.path.basename(test_file)}: Passed as expected")
                return True
            else:
                print(f"❌ {os.path.basename(test_file)}: Expected to pass but failed")
                print(f"   Output: {result.stdout}")
                return False
        else:
            if result.returncode != 0:
                print(f"✅ {os.path.basename(test_file)}: Failed as expected")
                return True
            else:
                print(f"❌ {os.path.basename(test_file)}: Expected to fail but passed")
                return False
                
    except Exception as e:
        print(f"❌ Error running test for {os.path.basename(test_file)}: {e}")
        return False


def main():
    """Run all validation tests."""
    print("Running UnRAID Template Validation Tests\n")
    
    # Get the validation script path
    script_dir = os.path.dirname(os.path.abspath(__file__))
    validation_script = os.path.join(script_dir, "validate_templates.py")
    
    if not os.path.exists(validation_script):
        print(f"❌ Validation script not found: {validation_script}")
        sys.exit(1)
    
    # Create test templates
    test_dir, valid_file, invalid_file, malformed_file = create_test_templates()
    
    try:
        # Run tests
        tests_passed = 0
        total_tests = 3
        
        if run_validation_test(validation_script, valid_file, True):
            tests_passed += 1
            
        if run_validation_test(validation_script, invalid_file, False):
            tests_passed += 1
            
        if run_validation_test(validation_script, malformed_file, False):
            tests_passed += 1
        
        print(f"\nTest Results: {tests_passed}/{total_tests} passed")
        
        if tests_passed == total_tests:
            print("✅ All tests passed!")
            sys.exit(0)
        else:
            print("❌ Some tests failed!")
            sys.exit(1)
            
    finally:
        # Clean up test files
        import shutil
        shutil.rmtree(test_dir)


if __name__ == '__main__':
    main()