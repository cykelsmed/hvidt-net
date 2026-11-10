import json, pathlib
src = pathlib.Path.home() / 'Projects/hvidt-net/forslag'
items = [
  ('sne', '1-sne', 'Sne', 'Bevæg for at blæse sneen af · tryk for at ryste'),
  ('partikler', '2-partikler', 'Partikler', 'Bevæg for at skubbe · tryk for at sprede'),
  ('hoejdekurver', '3-hoejdekurver', 'Højdekurver', 'Bevæg for at løfte terrænet · tryk for en top'),
  ('blaek', '4-blaek', 'Blæk', 'Træk for at tegne med blæk · vent, så samler det sig'),
]
data = {k: (src / f'{f}.html').read_text() for k, f, _, _ in items}
payload = json.dumps(data, ensure_ascii=False).replace('</', '<\\/')
tabs = ''.join(f'<button type="button" class="tab" id="tab-{k}" data-k="{k}" data-hint="{h}"><span class="n">{i+1}</span>{t}</button>' for i,(k,_,t,h) in enumerate(items))
html = f'''<title>hvidt.net forslag</title>
<meta name="claude:viewport-fit-sides" content="cover">
<style>
/* Layout: a slim tab bar over a full-bleed live preview of one proposal at a time. */
:root{{--bg:#eef0f2;--bar:#f8f9fa;--fg:#1d242c;--dim:#66707a;--line:#d5dade;--on:#1d242c;--onfg:#f8f9fa;
--ui:ui-sans-serif,-apple-system,"Helvetica Neue",Arial,sans-serif}}
@media (prefers-color-scheme:dark){{:root:not([data-theme="light"]){{--bg:#0d1014;--bar:#14181d;--fg:#e4e8ec;--dim:#8a939c;--line:#262c33;--on:#e4e8ec;--onfg:#14181d;color-scheme:dark}}}}
:root[data-theme="dark"]{{--bg:#0d1014;--bar:#14181d;--fg:#e4e8ec;--dim:#8a939c;--line:#262c33;--on:#e4e8ec;--onfg:#14181d;color-scheme:dark}}
html,body{{height:100%}}
body{{background:var(--bg);color:var(--fg);font-family:var(--ui);display:flex;flex-direction:column;overflow:hidden}}
header{{background:var(--bar);border-bottom:1px solid var(--line);padding-block:10px 8px;padding-left:max(16px,env(safe-area-inset-left,0px));padding-right:max(16px,env(safe-area-inset-right,0px));display:flex;flex-direction:column;gap:6px}}
nav{{display:flex;gap:5px;flex-wrap:wrap}}
.tab{{font:500 13px/1 var(--ui);color:var(--fg);background:transparent;border:1px solid var(--line);border-radius:999px;padding:7px 10px;cursor:pointer;display:inline-flex;gap:5px;align-items:center}}
.tab .n{{font-variant-numeric:tabular-nums;color:var(--dim);font-size:12px}}
.tab[aria-selected="true"]{{background:var(--on);color:var(--onfg);border-color:var(--on)}}
.tab[aria-selected="true"] .n{{color:inherit;opacity:.7}}
.tab:focus-visible{{outline:2px solid var(--fg);outline-offset:2px}}
#hint{{margin:0;font-size:12.5px;color:var(--dim);letter-spacing:.02em;min-height:1.3em}}
main{{flex:1;min-height:0;position:relative}}
iframe{{position:absolute;inset:0;width:100%;height:100%;border:0;display:block}}
</style>
<header><nav role="tablist" aria-label="Forslag">{tabs}</nav><p id="hint"></p></header>
<main id="stage"></main>
<script type="application/json" id="src">{payload}</script>
<script>
(() => {{
  const src = JSON.parse(document.getElementById('src').textContent);
  const stage = document.getElementById('stage'), hint = document.getElementById('hint');
  const tabs = [...document.querySelectorAll('.tab')];
  function show(k) {{
    if (!src[k]) k = 'sne';
    tabs.forEach(t => t.setAttribute('aria-selected', String(t.dataset.k === k)));
    hint.textContent = tabs.find(t => t.dataset.k === k).dataset.hint;
    // Only one live iframe at a time, so hidden proposals do not run.
    stage.replaceChildren();
    const f = document.createElement('iframe');
    f.title = 'Forslag: ' + k; f.srcdoc = src[k];
    stage.appendChild(f);
  }}
  tabs.forEach(t => t.addEventListener('click', () => {{ if (location.hash !== '#' + t.dataset.k) location.hash = t.dataset.k; else show(t.dataset.k); }}));
  addEventListener('hashchange', () => show(location.hash.slice(1)));
  show(location.hash.slice(1));
}})();
</script>
'''
(src / 'oversigt.html').write_text(html)
print(len(html))
