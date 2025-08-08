#!/usr/bin/env python3
"""
UnRAID Template Validator

This script validates UnRAID Docker container templates for proper XML structure
and required elements.
"""

import xml.etree.ElementTree as ET
import sys
import os
from pathlib import Path


def validate_xml_syntax(file_path):
    """Validate that the XML file has proper syntax."""
    try:
        ET.parse(file_path)
        return True, "XML syntax is valid"
    except ET.ParseError as e:
        return False, f"XML syntax error: {e}"


def validate_template_structure(file_path):
    """Validate that the template has required UnRAID elements."""
    try:
        tree = ET.parse(file_path)
        root = tree.getroot()
        
        # Check if root element is Container
        if root.tag != 'Container':
            return False, "Root element must be 'Container'"
        
        # Required elements for UnRAID templates
        required_elements = ['Name', 'Repository', 'Network', 'Overview', 'Category']
        missing_elements = []
        
        for element in required_elements:
            if root.find(element) is None:
                missing_elements.append(element)
        
        if missing_elements:
            return False, f"Missing required elements: {', '.join(missing_elements)}"
        
        # Check that Name and Repository are not empty
        name = root.find('Name')
        if name is not None and not name.text.strip():
            return False, "Name element cannot be empty"
        
        repository = root.find('Repository')
        if repository is not None and not repository.text.strip():
            return False, "Repository element cannot be empty"
        
        return True, "Template structure is valid"
        
    except Exception as e:
        return False, f"Error validating structure: {e}"


def validate_template_file(file_path):
    """Validate a single template file."""
    print(f"Validating: {file_path}")
    
    # Check XML syntax
    syntax_valid, syntax_msg = validate_xml_syntax(file_path)
    if not syntax_valid:
        print(f"  ❌ {syntax_msg}")
        return False
    print(f"  ✅ {syntax_msg}")
    
    # Check template structure
    structure_valid, structure_msg = validate_template_structure(file_path)
    if not structure_valid:
        print(f"  ❌ {structure_msg}")
        return False
    print(f"  ✅ {structure_msg}")
    
    return True


def find_template_files(directory):
    """Find all XML template files in the directory."""
    template_files = []
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith('.xml'):
                template_files.append(os.path.join(root, file))
    return template_files


def main():
    """Main validation function."""
    if len(sys.argv) > 1:
        # Validate specific file
        file_path = sys.argv[1]
        if not os.path.exists(file_path):
            print(f"Error: File {file_path} not found")
            sys.exit(1)
        
        if validate_template_file(file_path):
            print("✅ Validation passed")
            sys.exit(0)
        else:
            print("❌ Validation failed")
            sys.exit(1)
    else:
        # Validate all templates in current directory
        current_dir = os.getcwd()
        template_files = find_template_files(current_dir)
        
        if not template_files:
            print("No XML template files found")
            sys.exit(0)
        
        print(f"Found {len(template_files)} template file(s)\n")
        
        all_valid = True
        for template_file in template_files:
            if not validate_template_file(template_file):
                all_valid = False
            print()  # Add blank line between files
        
        if all_valid:
            print("✅ All templates passed validation")
            sys.exit(0)
        else:
            print("❌ Some templates failed validation")
            sys.exit(1)


if __name__ == '__main__':
    main()