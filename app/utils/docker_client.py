import re

def clean_container_name(name):
    match = re.match(r"docker-(.*?)-\d+$", name)
    return match.group(1) if match else name
