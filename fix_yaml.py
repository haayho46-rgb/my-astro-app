#!/usr/bin/env python3
import os
import re
from pathlib import Path

# Path to blog directory
blog_dir = Path("/Users/harumiryouichi/名称未設定フォルダ/my-astro-app/src/content/blog")

def fix_markdown_file(file_path):
    """Fix YAML frontmatter in markdown file."""
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Check if file starts with ---
    if not content.startswith('---'):
        return False

    # Find the closing --- for frontmatter
    parts = content.split('---', 2)
    if len(parts) < 3:
        print(f"ERROR: Invalid frontmatter structure in {file_path.name}")
        return False

    frontmatter = parts[1]
    body = '---' + parts[2]

    # Check for common YAML errors - heroImage with malformed URLs
    if 'heroImage:' in frontmatter:
        # Look for heroImage lines with potential issues
        lines = frontmatter.split('\n')
        fixed_lines = []

        for line in lines:
            if 'heroImage:' in line:
                # Extract heroImage properly - should be: heroImage: "URL"
                # Bad pattern: heroImage: "URLheroImage: "OLDURL"...
                match = re.search(r'heroImage:\s*"([^"]+)"', line)
                if match:
                    url = match.group(1)
                    # Clean up URL if it contains extra characters
                    # URL should end with ?w=800&h=450&fit=crop
                    if '?' in url:
                        # Extract just the clean URL part
                        base_url = url.split('?')[0]
                        url = f"{base_url}?w=800&h=450&fit=crop"
                    fixed_lines.append(f'heroImage: "{url}"')
                else:
                    fixed_lines.append(line)
            else:
                fixed_lines.append(line)

        fixed_frontmatter = '\n'.join(fixed_lines)

        # Reconstruct the file
        new_content = '---\n' + fixed_frontmatter + body

        # Write back
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(new_content)

        print(f"PROCESSED: {file_path.name}")
        return True

    return False

# Process all markdown files
md_files = sorted(blog_dir.glob('*.md'))
processed_count = 0

for md_file in md_files:
    if fix_markdown_file(md_file):
        processed_count += 1

print(f"\nTotal files processed: {processed_count}")
