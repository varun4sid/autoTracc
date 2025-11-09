"""
Centralized State Management for autoTracc

This module provides a clean abstraction layer for managing Streamlit session state,
improving memory efficiency, performance, and maintainability.

Key improvements:
1. Centralized state initialization and access
2. Caching for expensive computations
3. Lazy loading for non-critical data
4. Automatic cleanup of sensitive data
5. Memory-efficient state management
"""

import streamlit as st
from typing import Any, Optional, Dict, Callable
from functools import wraps


class StateManager:
    """
    Centralized state management class that provides:
    - Clean API for state access
    - Default value handling
    - State validation
    - Memory optimization
    """
    
    # Define default values for all session state variables
    DEFAULTS = {
        # Navigation
        "page": "login_page",
        
        # User credentials (cleared after authentication)
        "rollno": "",
        "password": "",
        
        # UI State
        "greeting": "",
        "balloons": False,
        "attendance_slider": 75,
        "custom_internals": 29,
        "custom_target": 50,
        "target_slider": 50,
        
        # Session and fetched data
        "studzone1_session": None,
        "attendance_data": None,
        "course_map": None,
        "cgpa_data": None,
        "courses_list": None,
        "internals_data": None,
        
        # Availability flags
        "attendance_available": False,
        "cgpa_available": False,
        
        # Cached computed values (will be computed on-demand)
        "_attendance_table_cache": None,
        "_internals_table_cache": None,
        "_updated_date_cache": None,
    }
    
    @staticmethod
    def initialize():
        """Initialize all session state variables with default values."""
        for key, value in StateManager.DEFAULTS.items():
            if key not in st.session_state:
                st.session_state[key] = value
    
    @staticmethod
    def get(key: str, default: Any = None) -> Any:
        """
        Safely get a value from session state.
        
        Args:
            key: The session state key
            default: Default value if key doesn't exist
            
        Returns:
            The value from session state or default
        """
        return st.session_state.get(key, default)
    
    @staticmethod
    def set(key: str, value: Any):
        """
        Set a value in session state.
        
        Args:
            key: The session state key
            value: The value to set
        """
        st.session_state[key] = value
    
    @staticmethod
    def clear_sensitive_data():
        """
        Clear sensitive data from session state after authentication.
        This improves security and reduces memory usage.
        """
        # Keep rollno for logging but clear password
        if "password" in st.session_state:
            st.session_state.password = ""
    
    @staticmethod
    def reset():
        """Reset all session state to defaults (used on logout)."""
        for key in list(st.session_state.keys()):
            if key in StateManager.DEFAULTS:
                st.session_state[key] = StateManager.DEFAULTS[key]
    
    @staticmethod
    def invalidate_cache(cache_key: str):
        """
        Invalidate a specific cache.
        
        Args:
            cache_key: The cache key to invalidate
        """
        if cache_key in st.session_state:
            st.session_state[cache_key] = None


# Cached computation functions
@st.cache_data(show_spinner=False)
def compute_affordable_leaves(attendance_data: tuple, slider_value: int, course_map: dict):
    """
    Cached computation of affordable leaves table.
    
    Args:
        attendance_data: The raw attendance data
        slider_value: The target percentage
        course_map: Mapping of course codes to names
        
    Returns:
        DataFrame with affordable leaves
    """
    from src.attendance import getAffordableLeaves
    # Convert tuple to list for processing (tuples are hashable for caching)
    data_list = list(attendance_data)
    return getAffordableLeaves(data_list, slider_value)


@st.cache_data(show_spinner=False)
def compute_target_scores(internals_data: tuple, target_value: int):
    """
    Cached computation of target scores table.
    
    Args:
        internals_data: The raw internals data
        target_value: The target final marks
        
    Returns:
        List with target scores
    """
    from src.internals import getTargetScore
    # Convert tuple to list for processing
    data_list = list(internals_data)
    return getTargetScore(data_list, target_value)


@st.cache_data(show_spinner=False)
def extract_updated_date(attendance_data: tuple):
    """
    Cached extraction of the last updated date from attendance data.
    
    Args:
        attendance_data: The raw attendance data
        
    Returns:
        The last updated date string
    """
    if attendance_data and len(attendance_data) > 1 and len(attendance_data[1]) > 9:
        return attendance_data[1][9]
    return "Unknown"


# Helper functions for getting computed values
def get_attendance_table(slider_value: Optional[int] = None):
    """
    Get attendance table, computing it if necessary.
    
    Args:
        slider_value: Optional slider value, uses session state if not provided
        
    Returns:
        DataFrame with affordable leaves or None if data unavailable
    """
    if slider_value is None:
        slider_value = StateManager.get("attendance_slider", 75)
    
    attendance_data = StateManager.get("attendance_data")
    course_map = StateManager.get("course_map")
    
    if attendance_data and course_map:
        # Convert to tuple for caching (lists are not hashable)
        attendance_tuple = tuple(tuple(row) if isinstance(row, list) else row 
                                for row in attendance_data)
        course_map_tuple = tuple(course_map.items())
        return compute_affordable_leaves(attendance_tuple, slider_value, dict(course_map_tuple))
    return None


def get_internals_table(target_value: Optional[int] = None):
    """
    Get internals table, computing it if necessary.
    
    Args:
        target_value: Optional target value, uses session state if not provided
        
    Returns:
        List with target scores or None if data unavailable
    """
    if target_value is None:
        target_value = StateManager.get("target_slider", 50)
    
    internals_data = StateManager.get("internals_data")
    
    if internals_data:
        # Convert to tuple for caching
        internals_tuple = tuple(tuple(row) if isinstance(row, list) else row 
                               for row in internals_data)
        return compute_target_scores(internals_tuple, target_value)
    return None


def get_updated_date():
    """
    Get the last updated date from attendance data.
    
    Returns:
        The last updated date string or "Unknown"
    """
    attendance_data = StateManager.get("attendance_data")
    
    if attendance_data:
        # Convert to tuple for caching
        attendance_tuple = tuple(tuple(row) if isinstance(row, list) else row 
                                for row in attendance_data)
        return extract_updated_date(attendance_tuple)
    return "Unknown"


# Decorator for functions that modify state
def clears_cache(*cache_keys):
    """
    Decorator that clears specified caches when function is called.
    
    Args:
        *cache_keys: Variable number of cache keys to clear
    """
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs):
            result = func(*args, **kwargs)
            for key in cache_keys:
                StateManager.invalidate_cache(key)
            return result
        return wrapper
    return decorator
