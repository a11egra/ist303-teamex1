import re

def parse_time_expression(expression: str):
    """
    Converts natural language time expressions into a standardized 24-hour time format.

    Args:
        expression: A string containing a time expression.

    Returns:
        A tuple containing two integers (hours, minutes) or None if parsing fails.
        
    Raises:
        Exception: If the input is not a string.
    """
    if not isinstance(expression, str):
        raise Exception("Input must be a string.")

    if not expression.strip():
        return None

    norm_expr = expression.lower().strip()

    # 1. Handle special named times 
    if norm_expr == "noon":
        return (12, 0)
    if norm_expr == "midnight":
        return (0, 0)

    # Dictionary to convert word numbers to integers
    num_words = {
        'one': 1, 'two': 2, 'three': 3, 'four': 4, 'five': 5, 'six': 6,
        'seven': 7, 'eight': 8, 'nine': 9, 'ten': 10, 'eleven': 11, 'twelve': 12
    }
    
    # 2. Handle "quarter", "half past" expressions 
    # Pattern: (quarter to|quarter past|half past) (hour) [am|pm]?
    match = re.match(r'^(quarter to|quarter past|half past)\s+(\w+)\s*(am|pm)?$', norm_expr)
    if match:
        qualifier, hour_str, period = match.groups()
        
        hour = num_words.get(hour_str, int(hour_str) if hour_str.isdigit() else None)
        if hour is None or not (1 <= hour <= 12):
            return None # Invalid hour

        minutes = 0
        if qualifier == 'quarter past':
            minutes = 15
        elif qualifier == 'half past':
            minutes = 30
        elif qualifier == 'quarter to':
            minutes = 45
            hour = hour - 1 if hour > 1 else 12 # "quarter to 5" is 4:45

        # Adjust for AM/PM
        if period == 'pm' and hour < 12:
            hour += 12
        elif period == 'am' and hour == 12: # "quarter to 12am" is 11:45pm, "quarter past 12am" is 00:15
            if qualifier == 'quarter to':
                 # This case is tricky. "quarter to twelve am" is 23:45
                 hour = 23
            else:
                 hour = 0
        
        return (hour, minutes)
    
    #3. Handle standard time formats like HH:MM or H, with optional AM/PM
    # Pattern: (hour)[:(minutes)] [am|pm]
    match = re.match(r'^(\d{1,2})(?::(\d{2}))?\s*(am|pm)?$', norm_expr)
    if match:
        hour_str, min_str, period = match.groups()
        
        hour = int(hour_str)
        minutes = int(min_str) if min_str else 0

        # Validate time components
        if not (0 <= hour <= 23 and 0 <= minutes <= 59):
             # Allow hour up to 12 for am/pm formats
            if not (1 <= hour <= 12 and period):
                return None

        # AM/PM Logic
        if period:
            if not (1 <= hour <= 12): # 12-hour format must be 1-12
                return None
            if period == 'pm' and hour < 12:
                hour += 12
            elif period == 'am' and hour == 12: # 12 AM is midnight (00:00)
                hour = 0
        
        # After all conversions, re-validate
        if not (0 <= hour <= 23 and 0 <= minutes <= 59):
            return None
            
        return (hour, minutes)

    return None # Return None if no pattern matches