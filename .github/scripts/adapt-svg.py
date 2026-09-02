import glob
import re
import xml.etree.ElementTree as ET

# Clean media query without any invalid XML entities or ampersands
ADAPTIVE_CSS = """
@media (prefers-color-scheme: dark) {
  .fill-fg { fill: #f0f6fc !important; }
  .stroke-fg { stroke: #f0f6fc !important; }
  .fill-strong { fill: #ffffff !important; }
  .fill-weak { fill: #8b949e !important; }
  .stroke-weak { stroke: #484f58 !important; }
}
@media (prefers-color-scheme: light) {
  .fill-fg { fill: #1f2328 !important; }
  .stroke-fg { stroke: #1f2328 !important; }
  .fill-strong { fill: #111133 !important; }
  .fill-weak { fill: #656d76 !important; }
  .stroke-weak { stroke: #d0d7de !important; }
}
"""

def clean_and_adapt(content):
    # 1. Remove background rect and make fill-bg / stroke-bg none
    content = re.sub(r'\.fill-bg\s*\{\s*fill:\s*[^;]*;\s*\}', '.fill-bg { fill: none; }', content)
    content = re.sub(r'\.stroke-bg\s*\{\s*stroke:\s*[^;]*;\s*\}', '.stroke-bg { stroke: none; }', content)
    content = re.sub(r'<rect\s+x="0"\s+y="0"\s+width="[0-9]*"\s+height="[0-9]*"\s+class="fill-bg"></rect>', '', content)
    
    # 2. Remove any bad comments that contain ampersands or invalid XML
    content = re.sub(r'/\*.*?\*/', '', content, flags=re.DOTALL)
    
    # 3. Inject adaptive CSS if not present
    if '</style>' in content and '@media (prefers-color-scheme' not in content:
        content = content.replace('</style>', ADAPTIVE_CSS + '</style>')
        
    return content

def make_dark_version(content):
    # Strip any media queries for standalone dark SVG
    dark_content = re.sub(r'@media\s*\(prefers-color-scheme.*?</style>', '</style>', content, flags=re.DOTALL)
    dark_content = re.sub(r'\.fill-fg\s*\{\s*fill:\s*[^;]*;\s*\}', '.fill-fg { fill: #f0f6fc; }', dark_content)
    dark_content = re.sub(r'\.stroke-fg\s*\{\s*stroke:\s*[^;]*;\s*\}', '.stroke-fg { stroke: #f0f6fc; }', dark_content)
    dark_content = re.sub(r'\.fill-strong\s*\{\s*fill:\s*[^;]*;\s*\}', '.fill-strong { fill: #ffffff; }', dark_content)
    dark_content = re.sub(r'\.fill-weak\s*\{\s*fill:\s*[^;]*;\s*\}', '.fill-weak { fill: #8b949e; }', dark_content)
    dark_content = re.sub(r'\.stroke-weak\s*\{\s*stroke:\s*[^;]*;\s*\}', '.stroke-weak { stroke: #484f58; }', dark_content)
    return dark_content

def make_light_version(content):
    # Strip any media queries for standalone light SVG
    light_content = re.sub(r'@media\s*\(prefers-color-scheme.*?</style>', '</style>', content, flags=re.DOTALL)
    light_content = re.sub(r'\.fill-fg\s*\{\s*fill:\s*[^;]*;\s*\}', '.fill-fg { fill: #1f2328; }', light_content)
    light_content = re.sub(r'\.stroke-fg\s*\{\s*stroke:\s*[^;]*;\s*\}', '.stroke-fg { stroke: #1f2328; }', light_content)
    light_content = re.sub(r'\.fill-strong\s*\{\s*fill:\s*[^;]*;\s*\}', '.fill-strong { fill: #111133; }', light_content)
    light_content = re.sub(r'\.fill-weak\s*\{\s*fill:\s*[^;]*;\s*\}', '.fill-weak { fill: #656d76; }', light_content)
    light_content = re.sub(r'\.stroke-weak\s*\{\s*stroke:\s*[^;]*;\s*\}', '.stroke-weak { stroke: #d0d7de; }', light_content)
    return light_content

# Process all base SVGs
svg_files = [f for f in glob.glob('profile-3d-contrib/*.svg') if not f.endswith('-dark.svg') and not f.endswith('-light.svg')]

for filepath in svg_files:
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    adapted = clean_and_adapt(content)
    
    # Validate XML
    try:
        ET.fromstring(adapted)
    except Exception as e:
        print(f"Error in {filepath}: {e}")
        continue
        
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(adapted)

    # For profile-gitblock, also generate dedicated dark and light SVGs
    if 'profile-gitblock.svg' in filepath:
        dark_svg = make_dark_version(adapted)
        light_svg = make_light_version(adapted)
        
        ET.fromstring(dark_svg)
        ET.fromstring(light_svg)
        
        with open('profile-3d-contrib/profile-gitblock-dark.svg', 'w', encoding='utf-8') as f:
            f.write(dark_svg)
        with open('profile-3d-contrib/profile-gitblock-light.svg', 'w', encoding='utf-8') as f:
            f.write(light_svg)
        print("Generated profile-gitblock-dark.svg and profile-gitblock-light.svg")

print("All SVGs processed and validated successfully!")
