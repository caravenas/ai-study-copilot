import os
import re

def convert(input_file, output_type):
    with open(input_file, 'r', encoding='utf-8') as f:
        html = f.read()

    style_match = re.search(r'<style[^>]*>([\s\S]*?)</style>', html, re.IGNORECASE)
    styles = style_match.group(1) if style_match else ''

    body_match = re.search(r'<body[^>]*>([\s\S]*?)</body>', html, re.IGNORECASE)
    body_html = body_match.group(1) if body_match else html

    # remove scripts
    body_html = re.sub(r'<script\b[^<]*(?:(?!</script>)<[^<]*)*</script>', '', body_html, flags=re.IGNORECASE)

    body_html = body_html.replace('class="', 'className="')
    body_html = body_html.replace('for="', 'htmlFor="')

    for tag in ['img', 'input', 'hr', 'br', 'path']:
        def repl(m):
            t = m.group(0)
            if t.endswith('/>'): return t
            return f'<{tag}{m.group(1)} />'
        body_html = re.sub(fr'<{tag}([^>]*?)>', repl, body_html, flags=re.IGNORECASE)

    def style_repl(m):
        style_string = m.group(1)
        parts = [p for p in style_string.split(';') if p.strip()]
        obj_vars = []
        for p in parts:
            if ':' not in p: continue
            k, v = p.split(':', 1)
            cc_key = k.strip()
            if not cc_key.startswith('--'):
                # to camelCase
                cc_key = re.sub(r'-([a-z])', lambda x: x.group(1).upper(), cc_key)
            obj_vars.append(f"'{cc_key}': '{v.strip().replace(chr(39), chr(92)+chr(39))}'")
        return f'style={{{{ {", ".join(obj_vars)} }}}}'
    body_html = re.sub(r'style="([^"]*)"', style_repl, body_html)

    body_html = body_html.replace('fill-rule="', 'fillRule="')
    body_html = body_html.replace('clip-rule="', 'clipRule="')
    body_html = body_html.replace('stroke-width="', 'strokeWidth="')
    body_html = body_html.replace('stroke-linecap="', 'strokeLinecap="')
    body_html = body_html.replace('stroke-linejoin="', 'strokeLinejoin="')

    # Convert HTML comments to JSX comments
    body_html = re.sub(r'<!--([^>]*)-->', lambda m: f'{{/*{m.group(1)}*/}}', body_html)

    comp_name = output_type.capitalize() + 'View'
    base_dir = os.path.join(os.path.dirname(__file__), '..', 'apps', 'web', 'app')
    out_dir = os.path.join(base_dir, output_type if output_type != 'chat' else '')
    os.makedirs(out_dir, exist_ok=True)
    out_path = os.path.join(out_dir, 'page.tsx')

    tsx_code = f'"use client";\n\nexport default function {comp_name}() {{\n  return (\n    <>\n      {body_html}\n    </>\n  );\n}}\n'
    with open(out_path, 'w', encoding='utf-8') as f:
        f.write(tsx_code)

    return styles

views = [
    ('apps/web/stitch-exports/chat.html', 'chat'),
    ('apps/web/stitch-exports/screen_173.html', 'explorer'),
    ('apps/web/stitch-exports/screen_177.html', 'study'),
    ('apps/web/stitch-exports/screen_181.html', 'admin'),
]

all_styles = ''
base_p = os.path.join(os.path.dirname(__file__), '..')
for f, t in views:
    path_in = os.path.join(base_p, f)
    s = convert(path_in, t)
    if s:
        all_styles += f'\n/* --- {t.upper()} STYLES --- */\n' + s

globals_path = os.path.join(base_p, 'apps', 'web', 'app', 'globals.css')
if os.path.exists(globals_path):
    with open(globals_path, 'a', encoding='utf-8') as f:
        f.write(all_styles)
else:
    with open(globals_path, 'w', encoding='utf-8') as f:
        f.write(all_styles)
print("done")
