import re

def clean_name(name):
    pattern = r'^([^/\s]+)'
    
    match = re.match(pattern, name)
    if match:
        return match.group(1)