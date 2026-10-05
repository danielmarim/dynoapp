FONTS = '''@font-face { font-family: "Bodoni Moda"; src: url("assets/fonts/bodoni-moda-latin-700-normal.woff2") format("woff2"); font-weight: 700; }
@font-face { font-family: "Space Grotesk"; src: url("assets/fonts/space-grotesk-latin-400-normal.woff2") format("woff2"); font-weight: 400; }
@font-face { font-family: "Space Grotesk"; src: url("assets/fonts/space-grotesk-latin-700-normal.woff2") format("woff2"); font-weight: 700; }'''
def comp(cid, dur, css, body, js, bg):
    p = cid.split('-')[0]
    A = 'data-layout-allow-overlap data-layout-allow-overflow'
    body = body.replace('§', A)
    return f'''<template>
<script src="assets/js/gsap.min.js"></script>
<style>
{FONTS}
[data-composition-id="{cid}"]#root, #root {{ position: absolute; inset: 0; width: 1080px; height: 1920px; overflow: hidden; font-family: "Space Grotesk", sans-serif; color: #1B1F3B; }}
.h{p} {{ font-family: "Bodoni Moda", serif; font-weight: 700; line-height: 1.0; letter-spacing: -0.02em; }}
.bub{p} {{ position: absolute; border: 5px solid #1E1E1E; border-radius: 54px; font-size: 46px; line-height: 1.28; padding: 26px 42px; max-width: 880px; box-shadow: 12px 12px 0 rgba(26,26,26,.10); }}
.me{p} {{ right: 76px; background: #fff; border-bottom-right-radius: 12px; }}
.dy{p} {{ left: 76px; background: #9AF4D5; border-bottom-left-radius: 12px; }}
.who{p} {{ display: block; font-size: 28px; font-weight: 700; letter-spacing: .08em; text-transform: uppercase; opacity: .6; margin-bottom: 6px; }}
.logo{p} {{ position: absolute; border-radius: 50%; background: #14B37D; border: 5px solid #1E1E1E; display: flex; align-items: center; justify-content: center; font-family: "Bodoni Moda", serif; font-weight: 700; color: #1B1F3B; line-height: 1; }}
{css}
</style>
<div id="root" data-composition-id="{cid}" data-width="1080" data-height="1920" data-duration="{dur}">
  <div id="f{p}-bg" class="clip" data-start="0" data-duration="{dur}" data-track-index="0" style="position:absolute;inset:0;background:{bg}"></div>
{body}
</div>
<script>
(function () {{
  window.__timelines = window.__timelines || {{}};
  const tl = gsap.timeline({{ paused: true }});
  const one = (s) => document.querySelector('[data-composition-id="{cid}"] ' + s);
{js}
  tl.to({{}}, {{ duration: {dur} }}, 0);
  window.__timelines["{cid}"] = tl;
}})();
</script>
</template>
'''
