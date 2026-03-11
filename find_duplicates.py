import re

with open('d:/DOJO DEMO/client/src/App.tsx', 'r', encoding='utf-8') as f:
    content = f.read()

# Simple regex to find JSX tags and their attributes
# This is not perfect for nested structures but can find obviously duplicates
tags = re.findall(r'<[a-zA-Z0-9\.]+\s+([^>]+)>', content, re.DOTALL)

for i, tag_content in enumerate(tags):
    # Find all attribute names
    attrs = re.findall(r'([a-zA-Z0-9]+)=', tag_content)
    # Check for duplicates
    seen = set()
    for attr in attrs:
        if attr in seen:
            print(f"Duplicate attribute '{attr}' found in tag content:")
            print(tag_content)
            print("-" * 40)
        seen.add(attr)
