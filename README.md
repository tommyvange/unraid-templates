# UnRAID Templates

This repository is for hosting my UnRAID templates.

## Template Validation

This repository includes validation tools to ensure UnRAID templates are properly formatted:

### Usage

Validate all templates in the repository:
```bash
python3 validate_templates.py
```

Validate a specific template:
```bash
python3 validate_templates.py path/to/template.xml
```

Run validation tests:
```bash
python3 test_validation.py
```

### What is validated

- XML syntax correctness
- Required UnRAID template elements (Name, Repository, Network, Overview, Category)
- Non-empty essential fields

## Templates

### ArrStalledHandler
Folder for [ArrStalledHandler](https://github.com/tommyvange/ArrStalledHandler)
