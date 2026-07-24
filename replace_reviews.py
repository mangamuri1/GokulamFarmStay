import sys

with open('d:/Gokulam/index.html', 'r', encoding='utf-8') as f:
    lines = f.readlines()

start_idx = -1
end_idx = -1

for i, line in enumerate(lines):
    if '<div class="testimonial-two-slider position-relative z-1 tw_fade_anim">' in line:
        start_idx = i
        break

if start_idx != -1:
    # Find the matching end tag for testimonial-two-slider
    # It has a child `swiper-container` and `testimonial-two-dots`. 
    # We can just look for `<!-- FAQ section  -->` and go back.
    for i in range(start_idx, len(lines)):
        if '<!-- FAQ section  -->' in line:
            pass # wait this isn't right
            
    # Or just use the line numbers! We know it's lines 1287 to 1410 (1-based), so index 1286 to 1409.
    # Let's verify by checking line 1286 and 1409.
    
    # Actually, we can just replace the whole block by finding it.
    pass

with open('d:/Gokulam/index.html', 'r', encoding='utf-8') as f:
    content = f.read()

import re
# We'll use regex to match from `<div class="testimonial-two-slider` to the end of that div.
pattern = re.compile(r'<div class="testimonial-two-slider position-relative z-1 tw_fade_anim">.*?</div>\s*</div>\s*</div>\s*</div>\s*</section>', re.DOTALL)

# Let's be safer and just replace by line numbers.
# From the previous view_file:
# 1287:                     <div class="testimonial-two-slider position-relative z-1 tw_fade_anim">
# ...
# 1410:                     </div>
# 1411:                 </div>

new_lines = lines[:1286] + [
    '                    <div class="col-xl-12 text-center tw_fade_anim">\n',
    '                        <img src="images/Reviews.png" alt="Genuine GMB Reviews" class="img-fluid rounded tw-shadow-lg" style="max-width: 100%; height: auto;">\n',
    '                    </div>\n'
] + lines[1410:]

with open('d:/Gokulam/index.html', 'w', encoding='utf-8') as f:
    f.writelines(new_lines)

print("Replaced slider with image")
