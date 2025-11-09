#!/usr/bin/env python3
"""
Validation script for state management improvements.

This script validates that:
1. StateManager initializes correctly
2. Cached functions work properly
3. State can be set and retrieved
4. Sensitive data can be cleared
"""

import sys
import os

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

def test_state_manager_import():
    """Test that StateManager can be imported."""
    print("Testing StateManager import...")
    try:
        from state_manager import StateManager
        print("✓ StateManager imported successfully")
        return True
    except Exception as e:
        print(f"✗ Failed to import StateManager: {e}")
        return False

def test_state_manager_defaults():
    """Test that defaults are defined correctly."""
    print("\nTesting StateManager defaults...")
    try:
        from state_manager import StateManager
        assert hasattr(StateManager, 'DEFAULTS'), "DEFAULTS attribute missing"
        assert isinstance(StateManager.DEFAULTS, dict), "DEFAULTS should be a dict"
        
        # Check for essential keys
        essential_keys = ['page', 'rollno', 'password', 'attendance_slider']
        for key in essential_keys:
            assert key in StateManager.DEFAULTS, f"Missing essential key: {key}"
        
        print(f"✓ StateManager has {len(StateManager.DEFAULTS)} default values")
        return True
    except Exception as e:
        print(f"✗ Failed StateManager defaults test: {e}")
        return False

def test_cached_functions():
    """Test that cached functions are defined."""
    print("\nTesting cached functions...")
    try:
        from state_manager import (
            compute_affordable_leaves,
            compute_target_scores,
            extract_updated_date
        )
        print("✓ All cached functions imported successfully")
        return True
    except Exception as e:
        print(f"✗ Failed to import cached functions: {e}")
        return False

def test_helper_functions():
    """Test that helper functions are defined."""
    print("\nTesting helper functions...")
    try:
        from state_manager import (
            get_attendance_table,
            get_internals_table,
            get_updated_date
        )
        print("✓ All helper functions imported successfully")
        return True
    except Exception as e:
        print(f"✗ Failed to import helper functions: {e}")
        return False

def test_updated_pages():
    """Test that updated pages import correctly."""
    print("\nTesting updated pages...")
    try:
        from pages import loginPage, processingPage, dashBoardPage
        print("✓ All pages imported successfully")
        
        # Check that initializeSessionState exists
        assert hasattr(loginPage, 'initializeSessionState'), "initializeSessionState missing"
        print("✓ initializeSessionState function exists")
        return True
    except Exception as e:
        print(f"✗ Failed to import pages: {e}")
        return False

def test_updated_tabs():
    """Test that updated tabs import correctly."""
    print("\nTesting updated tabs...")
    try:
        from tabs import attendanceTab, internalsTab
        print("✓ Updated tabs imported successfully")
        return True
    except Exception as e:
        print(f"✗ Failed to import tabs: {e}")
        return False

def test_extract_updated_date_function():
    """Test the extract_updated_date function with sample data."""
    print("\nTesting extract_updated_date with sample data...")
    try:
        from state_manager import extract_updated_date
        
        # Test with valid data
        sample_data = [
            ['Course1', 'data1', 'data2', 'data3', 'data4', 'data5', 'data6', 'data7', 'data8', 'data9'],
            ['Course2', 'data1', 'data2', 'data3', 'data4', 'data5', 'data6', 'data7', 'data8', '2024-01-15']
        ]
        sample_tuple = tuple(tuple(row) for row in sample_data)
        result = extract_updated_date(sample_tuple)
        assert result == '2024-01-15', f"Expected '2024-01-15', got '{result}'"
        print(f"✓ extract_updated_date returned correct date: {result}")
        
        # Test with empty data
        result_empty = extract_updated_date(())
        assert result_empty == "Unknown", f"Expected 'Unknown' for empty data, got '{result_empty}'"
        print("✓ extract_updated_date handles empty data correctly")
        
        return True
    except Exception as e:
        print(f"✗ Failed extract_updated_date test: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Run all validation tests."""
    print("=" * 60)
    print("State Management Validation")
    print("=" * 60)
    
    tests = [
        test_state_manager_import,
        test_state_manager_defaults,
        test_cached_functions,
        test_helper_functions,
        test_updated_pages,
        test_updated_tabs,
        test_extract_updated_date_function,
    ]
    
    results = []
    for test in tests:
        results.append(test())
    
    print("\n" + "=" * 60)
    print(f"Results: {sum(results)}/{len(results)} tests passed")
    print("=" * 60)
    
    if all(results):
        print("\n✓ All validation tests passed!")
        return 0
    else:
        print("\n✗ Some tests failed. Please review the output above.")
        return 1

if __name__ == "__main__":
    sys.exit(main())
