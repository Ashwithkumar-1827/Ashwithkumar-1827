import glob
import re

css = """
/* Adaptive Text & Foreground Colors for Dark/Light Mode */
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

svg_files = glob.glob('profile-3d-contrib/*.svg')
print(f"Found {len(svg_files)} SVGs to process...")

for filepath in svg_files:
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # 1. Make background transparent
    content = re.sub(r'\.fill-bg\s*\{\s*fill:\s*[^;]*;\s*\}', '.fill-bg { fill: none; }', content)
    content = re.sub(r'\.stroke-bg\s*\{\s*stroke:\s*[^;]*;\s*\}', '.stroke-bg { stroke: none; }', content)
    content = re.sub(r'<rect\s+x="0"\s+y="0"\s+width="[0-9]*"\s+height="[0-9]*"\s+class="fill-bg"><\/rect>', '', content)

    # 2. Inject adaptive dark/light mode styles if not already present
    if '</style>' in content and '@media (prefers-color-scheme' not in content:
        content = content.replace('</style>', css + '</style>')

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)

print("Successfully updated all SVGs for transparency and adaptive dark/light mode.")
