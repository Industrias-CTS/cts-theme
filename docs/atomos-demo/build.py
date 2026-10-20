#!/usr/bin/env python3
"""Genera sistema-atomos-cts.html: demo estática de los átomos de docs/ATOMOS.md.

Uso:  python3 build.py      (escribe sistema-atomos-cts.html junto a este archivo)

Reglas de la demo:
- Cada estado se dibuja dos veces, en `.m-light` y en `.m-dark`. Las variables
  CSS de cada modo son los roles de la capa 2 (ver LIGHT / DARK). El marcado
  es el mismo; solo cambian las variables.
- Hueco (`gap`): el estado no tiene valor en cts-manager. Se dibuja el valor
  que pone MUI, con franja amarilla y etiqueta «⚠ sin valor».
- Pendiente (`pend`): átomo con decisiones D1–D23 abiertas. Lleva un aviso
  amarillo con el D-número y una frase de qué falta decidir.
- Ningún valor se redondea. Los valores de MUI calculados se marcan como MUI.
"""
import html
import pathlib

OUT = pathlib.Path(__file__).with_name('sistema-atomos-cts.html')
GAPS = 0       # celdas con hueco, para el resumen
PENDS = 0      # avisos amarillos de átomo, para el resumen


def esc(text):
    return html.escape(text, quote=False)


# ── Variables por modo (roles de la capa 2 de ATOMOS.md) ────────────────────
LIGHT = """
--canvas:#f0f4f9;--surface:#ffffff;--raised:#ffffff;--rail:#0065bb;
--text:#1a2236;--muted:#5a6a80;--text-brand:#0065bb;--on-brand:#ffffff;
--brand:#0065bb;--brand-hover:#004696;--sec:#29abe2;--sec-hover:#1a8ab8;
--border:#dde3ec;--control:#d0d8e4;--head:#0065bb;--head-sep:rgba(255,255,255,.12);
--row:#ffffff;--row-hover:#f7fafd;--row-sel:#eff5fe;--group-head:#f0f4f9;
--readonly:rgba(15,23,42,.035);--overlay-hover:rgba(0,101,187,.05);
--overlay-selected:rgba(0,101,187,.1);--brand-tint:rgba(0,101,187,.09);
--outline-hover:rgba(0,101,187,.04);--outline-hover-strong:rgba(0,101,187,.04);
--err:#e2445c;--err-hover:rgb(158,47,64);--warn:#fdab3d;--ok:#00c875;--info:#29abe2;
--ring:0 0 0 3px rgba(0,101,187,.15);
--sh-e1:0 1px 4px rgba(0,0,0,.06);--sh-e2:0 2px 8px rgba(0,0,0,.08);
--sh-e4:0 8px 24px rgba(0,0,0,.12);--sh-e6:0 16px 40px rgba(0,0,0,.16);
--sh-menu:0 8px 24px rgba(0,101,187,.15);--sh-dialog:0 24px 64px rgba(0,101,187,.18);
--sh-rtip:0 6px 20px rgba(0,101,187,.12);--sh-snack:0 4px 20px rgba(0,0,0,.25);
--tip:#1a2236;--auth-bg:#f0f4f9;--auth-card:#ffffff;
--mui-action:rgba(0,0,0,.54);--mui-disabled:rgba(0,0,0,.26);
--mui-disabled-bg:rgba(0,0,0,.12);--mui-text-disabled:rgba(0,0,0,.38);
--mui-hover:rgba(0,0,0,.04);--mui-focus:rgba(0,0,0,.12);
--mui-placeholder:rgba(0,0,0,.42);--mui-sel:rgba(0,101,187,.08);
--mui-sel-hover:rgba(0,101,187,.12);--chip-hover:rgba(0,101,187,.12);--mui-skeleton:rgba(26,34,54,.11);
--sw-track:rgba(0,0,0,.38);--sw-thumb:#ffffff;--sw-dis-track:rgba(0,0,0,.12);
--sw-dis-thumb:#f5f5f5;--sw-on-dis-track:rgba(0,101,187,.12);
--sw-on-dis-thumb:rgb(158,196,229);--sb-track:#f0f4f9;--sb-thumb:#c0c8d4;
--sb-hover:#a0aab8;--lp-track:#9ec4e5;--tile:rgba(0,101,187,.1);
--rtip-bg:#ffffff;--rtip-ink:#1a2333;--rtip-line:#e0e7ef;--rtip-accent:#0065bb;--rtip-sh:rgba(0,101,187,.12);
--al-err-bg:#fcf0f1;--al-err-ink:#5c2a31;--al-warn-bg:#fef8ef;--al-warn-ink:#654a27;
--al-ok-bg:#eafaf3;--al-ok-ink:#145439;--al-info-bg:#edf8fc;--al-info-ink:#214a5c;
--chip-ink-mui:rgba(0,0,0,.87);--file-line:#bdbdbd;
"""

DARK = """
--canvas:#2a3547;--surface:#253662;--raised:#253662;--rail:#253662;
--text:#e8edf4;--muted:#a6b4c8;--text-brand:#89aedc;--on-brand:#ffffff;
--brand:#0065bb;--brand-hover:#004696;--sec:#29abe2;--sec-hover:#1a8ab8;
--border:rgba(74,144,226,.12);--control:rgba(74,144,226,.25);--head:#2d3c53;
--head-sep:rgba(74,144,226,.12);--row:#2d3c53;--row-hover:#2f435e;--row-sel:#2f476d;
--group-head:#2d3c53;--readonly:rgba(255,255,255,.045);--overlay-hover:rgba(74,144,226,.08);
--overlay-selected:rgba(74,144,226,.16);--brand-tint:rgba(41,171,226,.15);
--outline-hover:rgba(0,101,187,.08);--outline-hover-strong:rgba(0,101,187,.08);
--err:#ef4444;--err-hover:rgb(167,47,47);--warn:#f59e0b;--ok:#22c55e;--info:#06b6d4;
--ring:0 0 0 3px rgba(0,101,187,.15);
--sh-e1:0 1px 4px rgba(0,0,0,.4);--sh-e2:0 2px 8px rgba(0,0,0,.45);
--sh-e4:0 8px 24px rgba(0,0,0,.55);--sh-e6:0 16px 40px rgba(0,0,0,.65);
--sh-menu:0 8px 24px rgba(0,0,0,.5);--sh-dialog:0 24px 64px rgba(0,0,0,.7);
--sh-rtip:0 6px 20px rgba(0,0,0,.45);--sh-snack:0 4px 20px rgba(0,0,0,.3);
--tip:#1e2d42;--auth-bg:#1a1a2e;--auth-card:#253662;
--mui-action:rgba(255,255,255,.6);--mui-disabled:rgba(255,255,255,.28);
--mui-disabled-bg:rgba(255,255,255,.08);--mui-text-disabled:rgba(255,255,255,.5);
--mui-hover:rgba(255,255,255,.08);--mui-focus:rgba(74,144,226,.12);
--mui-placeholder:rgba(255,255,255,.5);--mui-sel:rgba(0,101,187,.16);
--mui-sel-hover:rgba(0,101,187,.24);--chip-hover:rgba(74,144,226,.24);--mui-skeleton:rgba(232,237,244,.13);
--sw-track:rgba(255,255,255,.3);--sw-thumb:#e0e0e0;--sw-dis-track:rgba(255,255,255,.2);
--sw-dis-thumb:#757575;--sw-on-dis-track:rgba(0,101,187,.2);
--sw-on-dis-thumb:rgb(0,45,84);--sb-track:#253662;--sb-thumb:#3d4f6f;
--sb-hover:#4a6090;--lp-track:#00325d;--tile:rgba(0,101,187,.15);
--rtip-bg:#1a2333;--rtip-ink:#e4e9f1;--rtip-line:#324158;--rtip-accent:#89aedc;--rtip-sh:rgba(0,0,0,.45);
--al-err-bg:#180a0a;--al-err-ink:#f9c3c3;--al-warn-bg:#181105;--al-warn-ink:#fbdfb0;
--al-ok-bg:#07140c;--al-ok-ink:#b8ecc8;--al-info-bg:#051315;--al-info-ink:#afe7f1;
--chip-ink-mui:rgba(0,0,0,.87);--file-line:#616161;
"""
CSS = """
*{box-sizing:border-box}
html{-webkit-text-size-adjust:100%}
body{margin:0;background:#eef2f7;color:#1a2236;font:400 15px/1.5 'Titillium Web',-apple-system,BlinkMacSystemFont,'Segoe UI',sans-serif}
code,.mono{font-family:ui-monospace,Menlo,Consolas,monospace}
main{max-width:1200px;margin:0 auto;padding:16px}
header.top{background:#0065bb;color:#fff;border-radius:12px;padding:20px 22px;margin-bottom:16px}
header.top h1{margin:0 0 6px;font-size:24px;font-weight:700}
header.top p{margin:4px 0;font-size:14px;opacity:.95}
.legend{display:flex;flex-wrap:wrap;gap:8px 16px;margin:12px 0 0;padding:0;list-style:none;font-size:13px}
.legend li{display:flex;align-items:center;gap:8px}
.summary{display:grid;grid-template-columns:repeat(auto-fit,minmax(150px,1fr));gap:8px;margin:12px 0 0}
.summary div{background:rgba(255,255,255,.12);border-radius:8px;padding:8px 10px}
.summary b{display:block;font-size:20px}
nav.toc{background:#fff;border:1px solid #dde3ec;border-radius:12px;padding:12px 16px;margin-bottom:16px;font-size:14px}
nav.toc a{color:#0065bb;text-decoration:none;margin-right:12px;white-space:nowrap}
nav.toc a:hover{text-decoration:underline}
section.sec{margin:28px 0}
section.sec>h2{font-size:22px;font-weight:700;margin:0 0 6px;padding-bottom:8px;border-bottom:2px solid #0065bb}
section.sec>p.intro{color:#5a6a80;margin:6px 0 16px;font-size:14px}
h3{font-size:17px;font-weight:700;margin:0}
article.atom{background:#fff;border:1px solid #dde3ec;border-radius:12px;padding:16px;margin:0 0 16px}
article.atom>header{display:flex;flex-wrap:wrap;align-items:baseline;gap:4px 12px;margin-bottom:10px}
article.atom>header code{font-size:12px;color:#5a6a80}
.note{font-size:13px;color:#5a6a80;margin:10px 0 0}
.pend{background:#fff3c4;border:1px solid #e0a800;border-left:5px solid #e0a800;color:#4a3500;border-radius:8px;padding:8px 12px;margin:0 0 12px;font-size:13px}
.pend strong{display:block;margin-bottom:4px}
.pend ul{margin:0;padding-left:18px}
.pend li{margin:2px 0}
.tw{overflow-x:auto;-webkit-overflow-scrolling:touch}
table.states{width:100%;border-collapse:collapse;min-width:620px}
table.states th,table.states td{vertical-align:top;text-align:left;padding:8px;border-bottom:1px solid #dde3ec}
table.states thead th{font-size:12px;color:#5a6a80;font-weight:600}
table.states tbody th{width:130px;font-size:13px;font-weight:600;color:#1a2236}
table.states td.cell{width:calc(50% - 65px);padding:10px}
.cell{background:var(--canvas);color:var(--text)}
.cell.m-light{--canvas:#f0f4f9}
.cell small{display:block;margin-top:8px;font:400 11px/1.45 ui-monospace,Menlo,Consolas,monospace;color:var(--muted)}
.cell.gap{box-shadow:inset 5px 0 0 #fdab3d}
.tag{display:inline-block;background:#fdab3d;color:#3b2a00;font:700 11px/1 'Titillium Web',sans-serif;padding:3px 6px;border-radius:4px;margin:0 0 6px}
.na{color:var(--muted);font-size:13px}
.stage{display:flex;flex-wrap:wrap;align-items:center;gap:10px;min-height:28px}
.hint{font-size:12px;color:var(--muted)}
.fld{display:grid;gap:4px;width:210px;max-width:100%}
.fld label{font-size:12px;color:var(--muted)}
.fld .ctl{height:38.56px;border:1.5px solid var(--control);border-radius:8px;padding:8.5px 14px;font-size:15px;color:var(--text);display:flex;align-items:center;background:transparent}
.fld .ctl .ph{color:var(--mui-placeholder)}
.fld .ctl.sel:after{content:'▾';margin-left:auto;color:var(--mui-action);font-size:18px}
.fld.is-hover .ctl{border-color:var(--text)}
.fld.is-focus label{color:var(--brand)}
.fld.is-focus .ctl{border:2px solid var(--brand);box-shadow:var(--ring);padding:7.5px 13.5px}
.fld.is-error label{color:var(--err)}
.fld.is-error .ctl{border-color:var(--err)}
.fld.is-error .ctl{box-shadow:var(--ring)}
.fld.is-dis label{color:var(--mui-text-disabled)}
.fld.is-dis .ctl{border-color:var(--mui-disabled-bg);color:var(--mui-text-disabled)}
.help{font-size:12px;color:var(--muted);margin:0 14px}
.fld.is-error .help{color:var(--err)}
/* botones */
.btn{font-family:inherit;font-size:14px;font-weight:600;line-height:1.75;letter-spacing:.01em;display:inline-flex;align-items:center;justify-content:center;gap:6px;height:36.5px;padding:6px 16px;border:0;border-radius:8px;text-transform:none;transition:all .2s ease;white-space:nowrap;background:transparent}
.btn-cp{background:var(--brand);color:var(--on-brand);box-shadow:0 2px 8px rgba(0,101,187,.3)}
.btn-cp.is-hover{background:var(--brand-hover);box-shadow:0 4px 12px rgba(0,101,187,.4)}
.btn-cp.is-active{background:var(--brand-hover);box-shadow:0 4px 12px rgba(0,101,187,.4)}
.btn-cp.is-focus{box-shadow:var(--sh-e6)}
.btn-cp.is-disabled,.btn.is-disabled{background:var(--mui-disabled-bg);color:var(--mui-disabled);box-shadow:none}
.btn-sec{background:var(--sec);color:#ffffff;box-shadow:0 2px 8px rgba(41,171,226,.3)}
.btn-sec.is-hover{background:var(--sec-hover);box-shadow:0 4px 12px rgba(41,171,226,.4)}
.btn-sec.is-focus{box-shadow:var(--sh-e6)}
.btn-err{background:var(--err);color:#ffffff;box-shadow:var(--sh-e2)}
.btn-err.is-hover{background:var(--err-hover);box-shadow:var(--sh-e4)}
.btn-out{background:transparent;color:var(--brand);border:1.5px solid rgba(0,101,187,.5);padding:5px 15px}
.btn-out.is-hover{background:var(--outline-hover)}
.btn-out.is-disabled{color:var(--mui-disabled);border:1px solid var(--mui-disabled-bg);background:transparent}
.btn-txt{color:var(--brand);padding:6px 8px}
.btn-txt.is-hover{background:var(--outline-hover)}
.btn-txt.is-disabled{color:var(--mui-disabled);background:transparent;box-shadow:none}
.btn-ok{background:#00c875;color:#ffffff;box-shadow:none}
.btn-ok.is-hover{background:#00a65c;box-shadow:0 4px 12px rgba(0,101,187,.4)}
.btn-ok.is-disabled{background:var(--mui-disabled-bg);color:var(--mui-disabled);box-shadow:none}
.btn-sm{height:31px;padding:4px 12px;font-size:13px}
.btn-lg{height:42.25px;padding:7px 21px;font-size:15px}
.btn-full{width:100%}
.spin{display:inline-block;width:14px;height:14px;border:2px solid currentColor;border-right-color:transparent;border-radius:50%;animation:spin 1.4s linear infinite}
@keyframes spin{to{transform:rotate(360deg)}}
.ib{width:30px;height:30px;border-radius:50%;display:inline-grid;place-items:center;border:0;background:transparent;color:var(--mui-action);font-size:16px;line-height:1}
.ib.sm{width:30px;height:30px}
.ib.is-hover{background:var(--mui-hover)}
.ib.toolbar{color:var(--muted)}
.ib.toolbar.is-hover{background:var(--overlay-hover);color:var(--brand)}
.ib.prim{color:var(--brand)}
.ib.prim.is-hover{background:var(--outline-hover)}
.ib.err{color:var(--err)}
.ib.err.is-hover{background:var(--outline-hover)}
.ib.is-disabled{color:var(--mui-disabled)}
.ib.is-focus{background:var(--mui-focus)}
.rail-ib{color:rgba(255,255,255,.7);width:30px;height:30px;border-radius:50%;display:inline-grid;place-items:center;background:transparent}
.rail-ib.is-hover{background:rgba(255,255,255,.1);color:#fff}
.fab{width:30px;height:30px;border-radius:50%;background:var(--brand);color:#fff;display:inline-grid;place-items:center;box-shadow:var(--sh-e1);font-size:14px}
.fab.is-hover{background:var(--brand-hover)}
.fab-rail-hover{background:var(--brand-hover)}
.plus-bad{width:26px;height:26px;border-radius:7px;background:rgba(25,118,210,.9);color:#fff;display:inline-grid;place-items:center;font-size:17px}
/* selección, checkbox, radio, switch */
.cbx{width:20px;height:20px;border:2px solid var(--muted);border-radius:3px;display:inline-grid;place-items:center;font-size:13px;line-height:1;color:#fff;background:transparent}
.cbx.on{background:var(--brand);border-color:var(--brand)}
.cbx.ind{background:var(--brand);border-color:var(--brand)}
.cbx.dis{border-color:var(--mui-disabled)}
.halo{display:inline-grid;place-items:center;width:38px;height:38px;border-radius:50%}
.halo.is-hover{background:var(--outline-hover)}
.rdo{width:20px;height:20px;border:2px solid var(--muted);border-radius:50%;display:inline-grid;place-items:center}
.rdo.on{border-color:var(--brand)}
.rdo.on:after{content:'';width:10px;height:10px;border-radius:50%;background:var(--brand)}
.rdo.err{border-color:var(--err)}
.rdo.err.on:after{background:var(--err)}
.rdo.dis{border-color:var(--mui-disabled)}
.sw{position:relative;width:40px;height:24px;border-radius:7px;flex:0 0 auto}
.sw .trk{position:absolute;inset:4px 0 4px 0;border-radius:7px;background:var(--sw-track)}
.sw .thb{position:absolute;top:2px;left:2px;width:20px;height:20px;border-radius:50%;background:var(--sw-thumb);box-shadow:var(--sh-e1)}
.sw.on .trk{background:var(--brand);opacity:.5}
.sw.on .thb{left:18px;background:var(--brand)}
.sw.ok.on .trk{background:var(--ok);opacity:.5}
.sw.ok.on .thb{background:var(--ok)}
.sw.off-dis .trk{background:var(--sw-dis-track)}
.sw.off-dis .thb{background:var(--sw-dis-thumb)}
.sw.on-dis .trk{background:var(--sw-on-dis-track);opacity:1}
.sw.on-dis .thb{left:18px;background:var(--sw-on-dis-thumb)}
.sw-row{display:flex;align-items:center;gap:8px;font-size:14px;color:var(--text)}
.opt{display:flex;align-items:center;gap:8px;font-size:14px;color:var(--text)}
/* swatches */
.sq{display:inline-block;width:24px;height:24px;border-radius:6px;border:2px solid transparent;vertical-align:middle}
.sq.is-sel{border-color:#ffffff;box-shadow:0 0 0 2px var(--c)}
.sq.is-hover{transform:scale(1.08)}
.sq.lg{width:28px;height:28px;border-radius:8px}
.sq.lg.is-sel{border-color:transparent;box-shadow:none;outline:3px solid var(--c);outline-offset:2px}
.sq.status{width:24px;height:24px;border-radius:10px;border:2px solid var(--surface);box-shadow:0 0 0 1px var(--c)}
.sq.none{width:14px;height:14px;border-radius:50%;border:1.5px dashed var(--text-disabled-ink,#8a93a3);background:transparent}
.sq.grid{width:22px;height:22px;border-radius:5px}
.sq.add{border:0;background:conic-gradient(from 0deg,#ef4444,#f59e0b,#eab308,#22c55e,#06b6d4,#3b82f6,#8b5cf6,#ec4899,#ef4444)}
.sq.add.is-sel{border:2px solid #ffffff;box-shadow:0 0 0 2px rgba(0,0,0,.15)}
.badge-x{position:absolute;top:-4px;right:-4px;width:14px;height:14px;border-radius:50%;background:#333;color:#fff;font-size:10px;display:grid;place-items:center}
.sq-wrap{position:relative;display:inline-block}
/* links */
.lnk{color:var(--muted);font-size:13px;font-weight:500;text-decoration:none}
.lnk.is-hover{text-decoration:underline}
.lnk.is-focus{outline:auto 1px -webkit-focus-ring-color;outline-offset:2px}
.lnk.cur{color:var(--text);font-weight:700}
.lnk.cell-link{color:var(--brand);font-size:12px;font-weight:400}
.lnk.cell-link.is-hover{text-decoration:underline}
/* login (composite) */
.login-stage{background:var(--auth-bg);padding:14px;border-radius:8px}
.login{background:var(--auth-card);border:1px solid var(--border);border-radius:12px;padding:20px;width:280px;max-width:100%;display:grid;gap:12px}
.login h4{margin:0;font-size:20px;font-weight:700;color:var(--text)}
.alert{display:flex;gap:10px;align-items:flex-start;padding:6px 14px;border-radius:8px;font-size:13px;line-height:1.5;font-weight:500}
.alert .ico{font-size:18px;line-height:1.2}
.alert.err{background:var(--al-err-bg);color:var(--al-err-ink)}
.alert.err .ico{color:var(--err)}
.alert.warn{background:var(--al-warn-bg);color:var(--al-warn-ink)}
.alert.warn .ico{color:var(--warn)}
.alert.ok{background:var(--al-ok-bg);color:var(--al-ok-ink)}
.alert.ok .ico{color:var(--ok)}
.alert.info{background:var(--al-info-bg);color:var(--al-info-ink)}
.alert.info .ico{color:var(--info)}
.alert.fill{color:#ffffff;font-weight:500;padding:8px 14px}
.alert.fill.err{background:var(--err);color:#ffffff}
.alert.fill.warn{background:var(--warn);color:rgba(0,0,0,.87)}
.alert.fill.ok{background:var(--ok);color:rgba(0,0,0,.87)}
.alert.fill.info{background:var(--info);color:rgba(0,0,0,.87)}
.alert.fill.err .ico,.alert.fill.warn .ico,.alert.fill.ok .ico,.alert.fill.info .ico{color:inherit}
.snack{background:var(--raised);color:var(--text);border-radius:8px;padding:10px 14px;font-size:13px;font-weight:600;box-shadow:var(--sh-snack);display:flex;align-items:center;gap:12px}
.snack .act{color:var(--brand);font-weight:800;text-decoration:underline;font-size:12px}
.help-block{font-size:12px;color:var(--muted)}
/* navegación: rail */
.railp{background:var(--rail);color:#ffffff;width:256px;max-width:100%;padding:10px 0;border-radius:6px}
.railp .sec-t{font:700 10px/1.2 'Titillium Web',sans-serif;letter-spacing:.1em;text-transform:uppercase;color:rgba(255,255,255,.45);padding:12px 20px 6px}
.nav{display:flex;align-items:center;gap:8px;margin:1px 12px 2px;padding:5.2px 12px;border-radius:8px;color:rgba(255,255,255,.65);font-size:13.5px;font-weight:600;border-left:3px solid transparent;transition:all .15s ease;min-height:34px}
.nav .ic{width:14px;height:14px;border-radius:3px;background:currentColor;opacity:.8;flex:0 0 auto}
.nav.is-hover{background:rgba(255,255,255,.1);color:#ffffff}
.nav.is-sel{background:rgba(255,255,255,.18);color:#ffffff;border-left-color:rgba(255,255,255,.9)}
.nav.is-selhover{background:rgba(255,255,255,.1);color:#ffffff;border-left-color:rgba(255,255,255,.9)}
.nav.is-focus{background:var(--mui-focus)}
.nav.is-dis{opacity:.38}
.nav.logout.is-hover{background:rgba(255,100,100,.2);color:rgba(255,180,180,1)}
.nav.tema{font-weight:500;font-size:13px;color:rgba(255,255,255,.6)}
.brd{display:flex;align-items:center;gap:8px;margin:0 12px 2px;padding:3.2px 4px 3.2px 20px;border-radius:8px;color:rgba(255,255,255,.65);font-size:12.5px;font-weight:500;border-left:3px solid transparent;min-height:30px}
.brd .dot{width:15px;height:15px;border-radius:4px;flex:0 0 auto}
.brd .more{margin-left:auto;opacity:0;font-size:12px}
.brd.is-hover{background:rgba(255,255,255,.09);color:rgba(255,255,255,.9)}
.brd.is-hover .more{opacity:1}
.brd.is-sel{background:rgba(255,255,255,.15);color:#ffffff;font-weight:700;border-left-color:rgba(255,255,255,.85)}
.brd.is-selhover{background:rgba(255,255,255,.09);color:#ffffff;font-weight:700;border-left-color:rgba(255,255,255,.85)}
.brd.is-drag{opacity:.4}
.brd.is-dis{opacity:.38}
.fol{display:flex;align-items:center;gap:8px;margin:0 12px 2px;padding:4px 8px;border-radius:8px;color:rgba(255,255,255,.7);font-size:13px;font-weight:700;border:1px solid transparent}
.fol.is-hover{background:rgba(255,255,255,.08);color:#ffffff}
.fol.is-drop{background:rgba(59,130,246,.25);border:1px dashed rgba(89,131,253,.7)}
.fol.is-drag{opacity:.5}
.wsr{display:flex;align-items:center;gap:6px;height:42px;padding:0 8px;margin:0 12px 8px;border-radius:10px;background:rgba(255,255,255,.1);border:1px solid rgba(255,255,255,.18);color:#ffffff}
.wsr .av{width:26px;height:26px;border-radius:7px;background:#2979c4;border:2px solid rgba(255,255,255,.28);box-shadow:0 2px 6px rgba(0,0,0,.25);font-size:12px;font-weight:700;color:#fff;display:grid;place-items:center;flex:0 0 auto}
.wsr .nm{font-size:12.5px;font-weight:700;flex:1;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
.wsr .sub{display:block;font-size:10px;color:rgba(255,255,255,.45);font-weight:400}
.wsr .mini{width:24px;height:24px;border-radius:6px;display:grid;place-items:center;color:rgba(255,255,255,.6);font-size:13px;background:transparent}
.wsr .sep{width:1px;height:20px;background:rgba(255,255,255,.15)}
.wsr .sep+.mini{}
.rsearch{display:flex;align-items:center;gap:6px;height:34px;margin:0 12px 8px;padding:0 10px;border-radius:10px;background:rgba(255,255,255,.08);border:1px solid rgba(255,255,255,.15);color:rgba(255,255,255,.4);font-size:12.5px}
.rsearch.is-focus{background:rgba(255,255,255,.12);border-color:rgba(255,255,255,.35);color:#ffffff}
.rsearch .ic{color:rgba(255,255,255,.45);font-size:13px}
.rfoot{display:flex;align-items:center;gap:12px;padding:12px 16px;background:rgba(0,0,0,.15);border-top:1px solid rgba(255,255,255,.1);color:#ffffff}
.rfoot .av{width:32px;height:32px;border-radius:50%;background:rgba(255,255,255,.2);border:2px solid rgba(255,255,255,.35);display:grid;place-items:center;font-size:11px;font-weight:700}
.rfoot .nm{font-size:12.5px;font-weight:700;line-height:1.2}
.rfoot .rl{font-size:10.5px;opacity:.5}
.rdiv{height:1px;background:rgba(255,255,255,.1);margin:12px 16px}
.hr{height:1px;background:var(--border);margin:8px 0;border:0}
.hr.on-rail{background:rgba(255,255,255,.1);margin:12px 16px}
.hr.dash{background:none;border-top:1px dashed var(--border)}
/* navegación: pestañas, menús, capas flotantes */
.tabs{display:flex;border-bottom:1px solid var(--border);width:100%}
.tab{padding:12px 16px;font-size:14px;font-weight:600;color:var(--muted);position:relative;text-transform:none}
.tab.is-sel{color:var(--brand)}
.tab.is-sel:after{content:'';position:absolute;left:0;right:0;bottom:-1px;height:2px;background:var(--brand)}
.tab.is-dis{color:var(--mui-text-disabled)}
.tab.is-focus{outline:0;box-shadow:inset 0 0 0 0 transparent}
.vtabs{display:flex;align-items:flex-end;border-bottom:2px solid var(--border);gap:2px;width:100%;overflow:hidden}
.vtab{display:inline-flex;align-items:center;gap:6px;padding:6px 12px;font-size:13px;font-weight:500;color:var(--muted);border-radius:4px 4px 0 0;border-bottom:2px solid transparent;margin-bottom:-2px;white-space:nowrap}
.vtab.is-hover{background:var(--overlay-hover)}
.vtab.is-sel{color:var(--brand);font-weight:700;border-bottom-color:var(--brand)}
.vtab.is-drag{opacity:.5}
.vtab.is-focus{outline:auto 1px -webkit-focus-ring-color;outline-offset:-2px}
.lib{display:flex;align-items:center;gap:10px;margin:1px 8px;padding:7px 12px;border-radius:8px;font-size:15px;color:var(--text);min-height:34px}
.lib.is-hover{background:var(--overlay-hover)}
.lib.is-sel{background:var(--mui-sel)}
.lib.is-selhover{background:var(--mui-sel-hover)}
.lib.is-focus{background:var(--mui-focus)}
.lib.is-dis{opacity:.38}
.paper{background:var(--raised);border:1px solid var(--border);border-radius:10px;box-shadow:var(--sh-menu);width:240px;max-width:100%;padding:8px 0;overflow:hidden}
.mi{margin:2px 6px;padding:7px 10px;border-radius:6px;font-size:14px;color:var(--text);display:flex;align-items:center;gap:8px}
.mi.is-hover{background:var(--overlay-hover)}
.mi.is-sel{background:var(--mui-sel)}
.mi.is-selhover{background:var(--mui-sel-hover)}
.mi.is-focus{background:var(--mui-focus)}
.mi.is-dis{opacity:.38}
.mi.danger{color:var(--err)}
.mi .chk{margin-left:auto;color:var(--brand);font-size:14px}
.mdiv{height:1px;background:var(--border);margin:8px 0}
.tip{background:var(--tip);color:#ffffff;font-size:12px;font-weight:500;padding:5px 10px;border-radius:6px;display:inline-block;position:relative;margin-top:6px}
.tip:after{content:'';position:absolute;left:50%;bottom:-4px;margin-left:-4px;border:4px solid transparent;border-bottom:0;border-top-color:var(--tip)}
.rtip{background:var(--rtip-bg);color:var(--rtip-ink);border:1px solid var(--rtip-line);border-left:3px solid var(--rtip-accent);border-radius:15px;padding:10px 14px;max-width:420px;font-size:13px;line-height:1.55;letter-spacing:.01em;box-shadow:var(--sh-rtip)}
.rtip b{font-weight:600}
.dlg{background:var(--raised);border-radius:14px;box-shadow:var(--sh-dialog);width:340px;max-width:100%;overflow:hidden}
.dlg.big{border-radius:30px}
.dlg h4{margin:0;padding:16px 24px 8px;font-size:16px;font-weight:700;color:var(--text)}
.dlg p{margin:0;padding:0 24px 20px;font-size:14px;color:var(--muted)}
.dlg p.txt{color:var(--text)}
.dlg .acts{display:flex;justify-content:flex-end;gap:8px;padding:0 24px 16px}
.dlg .acts.big{padding:0 24px 20px}
.scrim{background:rgba(0,0,0,.5);border-radius:8px;padding:14px;display:grid;place-items:center}
.drw{background:var(--raised);box-shadow:var(--sh-e6);width:300px;max-width:100%;border-radius:0}
.drw header{padding:16px 20px;border-bottom:1px solid var(--border);font-size:16px;font-weight:600;color:var(--text);display:flex;align-items:center;justify-content:space-between}
.drw .chipc{font-size:11px;font-weight:700;background:var(--overlay-selected);color:var(--text);border-radius:6px;padding:2px 6px}
.crumb{font-size:13px;color:var(--muted);display:flex;align-items:center;flex-wrap:wrap;gap:0}
.crumb .sep{margin:0 8px;color:var(--muted)}
.crumb .lnk{font-size:13px;font-weight:500}
.crumb .cur{color:var(--text);font-weight:700}
.spick{width:280px;max-width:100%;background:var(--raised);border-radius:20px;box-shadow:var(--sh-e6);overflow:hidden;padding:0}
.spick .srch{display:flex;align-items:center;gap:8px;padding:8px 12px;border-bottom:1px solid var(--border);font-size:13px;color:var(--muted)}
.spick .srch .ph{color:var(--mui-placeholder)}
.sopt{display:flex;align-items:center;justify-content:space-between;margin:4px 8px;padding:6.8px 12px;border-radius:15px;background:var(--c);color:#ffffff;font-size:13px;font-weight:600;min-height:32px}
.sopt.is-hover{filter:brightness(.88)}
.sopt.is-sel{outline:2px solid var(--raised);outline-offset:0;box-shadow:0 0 0 2px var(--c)}
.sopt.is-dis{opacity:.45;text-decoration:line-through}
.sadd{display:block;margin:4px 8px 8px;padding:6px 12px;border:1px dashed var(--border);border-radius:15px;font-size:12.5px;color:var(--brand);font-weight:600}
.sclr{display:block;margin:4px 8px;padding:6px 12px;border:1px dashed var(--border);border-radius:15px;font-size:12.5px;color:var(--muted)}
.vtbar-wrap{width:100%}
.tbadge{display:inline-block;font-size:11px;font-weight:700;background:var(--overlay-selected);color:var(--text);border-radius:10px;padding:0 6px;line-height:18px}
/* datos */
.chip{display:inline-flex;align-items:center;gap:4px;height:24px;padding:0 8px;border-radius:6px;font-size:12px;font-weight:600;background:var(--overlay-selected);color:var(--text);white-space:nowrap}
.chip.h20{height:20px;font-size:11px;font-weight:700;padding:0 7px;border-radius:10px}
.chip.h18{height:18px;font-size:10px;font-weight:600;padding:0 6px;border-radius:9px}
.chip.h22{height:22px;font-size:11px;font-weight:600;padding:0 8px;border-radius:6px}
.chip.prim{background:var(--brand);color:#ffffff}
.chip.info{background:var(--info);color:var(--chip-ink-mui)}
.chip.warn{background:var(--warn);color:var(--chip-ink-mui)}
.chip.warn.white{color:#ffffff}
.chip.ok{background:var(--ok);color:var(--chip-ink-mui)}
.chip.err{background:var(--err);color:#ffffff}
.chip.outl{background:transparent;border:1px solid var(--file-line);color:var(--text)}
.chip.outl.err{border:1px solid rgba(226,68,92,.7);background:transparent;color:var(--err)}
.chip.outl.eli{border:1px dashed var(--border);color:var(--mui-text-disabled);background:transparent}
.chip.brandsub{background:var(--brand-tint);color:var(--text-brand)}
.chip.dis{opacity:.38}
.chip.is-hover{background:var(--chip-hover)}
.chip.is-focus{background:var(--chip-hover)}
.chip.is-sel{background:var(--brand);color:#ffffff}
.chip.is-pressed{box-shadow:var(--sh-e1)}
.chip .del{font-size:12px;color:var(--mui-action)}
.chip.lock{opacity:.7}
.spill{display:flex;align-items:center;justify-content:center;width:150px;height:34px;color:#ffffff;font-size:11px;font-weight:600;background:var(--c)}
.spill.is-hover{filter:brightness(.88)}
.spill.vac{background:transparent;color:var(--muted);border:1px dashed var(--border);width:150px}
.spill.vac.is-hover{background:var(--overlay-hover)}
.cnt{display:inline-grid;place-items:center;min-width:14px;height:14px;border-radius:50%;background:#e2445c;color:#ffffff;font-size:8px;font-weight:700}
.nuevo{display:inline-block;background:var(--err);color:#ffffff;font-size:10px;font-weight:800;letter-spacing:.4px;padding:.8px 7.2px;border-radius:99px;box-shadow:0 0 0 5px rgba(211,47,47,0)}
.nuevo.pulse{box-shadow:0 0 0 5px rgba(211,47,47,.45)}
.beta{display:inline-block;background:var(--warn);color:#ffffff;font-size:10.5px;font-weight:700;text-transform:uppercase;letter-spacing:.4px;padding:2px 6px;border-radius:10px}
.dot8{display:inline-block;width:8px;height:8px;border-radius:50%;background:var(--brand)}
.unread{display:flex;align-items:center;gap:8px;padding:6px 10px;border-radius:6px;background:rgba(0,101,187,.04);font-size:13px;font-weight:600;color:var(--text)}
.unread.dark{background:rgba(0,101,187,.08)}
.unread.dark.l{background:rgba(0,101,187,.04)}
.tbl{width:100%;border-collapse:separate;border-spacing:0;border:1px solid var(--border);border-radius:10px;overflow:hidden;background:var(--row);font-size:13px}
.tbl th{background:var(--head);color:#ffffff;font-size:11px;font-weight:600;letter-spacing:.01em;text-align:left;padding:9px 12px;border-right:1px solid var(--head-sep);white-space:nowrap}
.tbl td{height:38px;padding:0 12px;color:var(--text);border-bottom:1px solid var(--border);border-right:1px solid var(--border)}
.tbl tr.is-hover td{background:var(--row-hover)}
.tbl tr.is-sel td{background:var(--mui-sel)}
.tbl tr.is-inact{opacity:.55}
.tbl td.ro{background:var(--readonly)}
.tbl tr.is-drop td{box-shadow:inset 0 3px 0 0 var(--brand)}
.grid{width:100%;border:1px solid var(--border);border-radius:10px;overflow:hidden;font-size:13px;background:var(--row)}
.grid .gh{display:flex;align-items:center;height:40px;padding:0 12px;background:var(--group-head);color:var(--muted);font-weight:700;border-right:1px solid var(--border);box-shadow:0 1px 3px rgba(0,0,0,.07)}
.grid .gr{display:flex;align-items:center;height:40px;padding:0 12px;border-bottom:1px solid var(--border);color:var(--text);font-size:13px}
.grid .gr b{font-weight:600}
.grid .gr.is-sel{background:var(--row-sel)}
.grid .gr.ro{background:var(--readonly)}
.grid .gr.resumen{height:36px;border-bottom:2px solid var(--border);color:var(--muted);background:var(--row)}
.grid .gband{display:flex;align-items:center;gap:8px;height:44px;padding:0 12px;background:var(--group-head);border-left:4px solid var(--c);color:var(--c);font-weight:700;font-size:14px}
.grid .gband .cnt2{font-size:11px;font-weight:700;border-radius:10px;padding:2px 8px;background:var(--gt)}
.grid .vacio{border:2px dashed var(--border);border-radius:30px;padding:14px;text-align:center;color:var(--mui-text-disabled);font-size:13px}
.grid .gc{display:inline-block;width:12px;height:12px;border-radius:50%;background:var(--c);margin-right:6px}
.acard{background:var(--surface);border:1px solid var(--border);border-radius:20px;padding:16px 20px;width:220px;max-width:100%}
.acard .v{font-size:20px;font-weight:700;color:var(--text);line-height:1.2}
.acard .l{font-size:12px;color:var(--muted)}
.acard.is-hover{box-shadow:0 0 0 1px rgba(0,101,187,.3)}
.stile{width:38px;height:38px;border-radius:15px;display:grid;place-items:center;background:var(--tile);color:var(--c);font-size:18px}
.empty{width:56px;height:56px;border-radius:16px;display:grid;place-items:center;background:var(--overlay-hover);color:var(--mui-text-disabled);font-size:28px}
.errt{width:64px;height:64px;border-radius:16px;display:grid;place-items:center;background:var(--err);color:#ffffff;font-size:36px}
.logo-otp{width:56px;height:56px;border-radius:14px;display:grid;place-items:center;background:linear-gradient(135deg,#0065bb 0%,#29abe2 100%);color:#ffffff;font-size:28px}
.prog{width:160px;height:3px;border-radius:4px;background:var(--lp-track);overflow:hidden}
.prog i{display:block;height:100%;width:60%;background:var(--brand)}
.prog.form{height:6px;border-radius:10px;background:rgba(41,171,226,.2)}
.prog.form i{background:#29abe2}
.prog.dis i{width:100%;background:var(--brand)}
.prog.err i{background:var(--brand)}
.cprog{width:18px;height:18px;border-radius:50%;border:3px solid transparent;border-top-color:var(--brand);display:inline-block;animation:spin 1.4s linear infinite}
.cprog.big{width:28px;height:28px;border-width:4px}
.cprog.rail{border-top-color:rgba(255,255,255,.5)}
.cprog.inh{border-top-color:currentColor;opacity:.4}
.sk{height:14px;width:180px;max-width:100%;border-radius:10px;background:var(--mui-skeleton)}
.sk.round{width:40px;height:40px;border-radius:50%}
.sk.t{transform:scaleY(.6)}
.av{width:32px;height:32px;border-radius:50%;display:inline-grid;place-items:center;color:#ffffff;font-size:11px;font-weight:700;flex:0 0 auto}
.av.brand{background:var(--brand)}
.av.user{background:#6366f1;width:34px;height:34px;font-size:13px}
.av.rail{background:rgba(255,255,255,.2);border:2px solid rgba(255,255,255,.35)}
.av.ws{background:#2979c4;border:2px solid rgba(255,255,255,.28);box-shadow:0 2px 6px rgba(0,0,0,.25);border-radius:9px;width:32px;height:32px;font-size:15px}
.av.group{width:22px;height:22px;font-size:10px;border:2px solid var(--surface);margin-left:-6px}
.av.nodef{background:#bdbdbd;color:var(--canvas)}
.sb{width:6px;height:120px;border-radius:3px;background:var(--sb-track);position:relative;overflow:hidden}
.sb i{position:absolute;left:0;top:10px;width:6px;height:60px;border-radius:3px;background:var(--sb-thumb)}
.sb i.hov{background:var(--sb-hover)}
.sb.wf{width:100%;height:8px;border-radius:4px;background:rgba(0,0,0,.05)}
.sb.wf.dk{background:rgba(255,255,255,.05)}
.sb.wf i{left:0;top:0;width:50%;height:8px;border-radius:4px;background:rgba(0,101,187,.5)}
.sb.wf i.hov{background:rgba(0,101,187,.75)}
.sb.wf i.drag{background:var(--brand)}
.sb.wf i.dis{background:transparent}
.map{display:grid;grid-template-columns:repeat(auto-fill,minmax(92px,1fr));gap:6px}
.ssw{display:flex;align-items:center;gap:8px;font-size:12px;color:var(--muted)}
.dv{height:1px;background:var(--border);width:100%}
.dv.rail{background:rgba(255,255,255,.1)}
.dv.dashed{background:none;border-top:1px dashed var(--border);height:0}
/* tokens de paleta (sección 1) */
.swatch{display:inline-block;width:28px;height:28px;border-radius:6px;border:1px solid rgba(0,0,0,.08);vertical-align:middle;margin-right:6px}
.swatch.dk{border-color:rgba(255,255,255,.12)}
.roles{width:100%;border-collapse:collapse;font-size:13px;background:#fff;border:1px solid #dde3ec;border-radius:12px;overflow:hidden}
.roles th,.roles td{text-align:left;vertical-align:middle;padding:7px 10px;border-bottom:1px solid #dde3ec}
.roles thead th{background:#f5f7fb;font-size:12px;color:#5a6a80;font-weight:600}
.roles code{font-size:12px}
.roles tr.pend-row td{background:#fff9e0}
.roles .pd{display:inline-block;background:#fdab3d;color:#3b2a00;font-weight:700;font-size:11px;border-radius:4px;padding:2px 6px;margin-right:4px}
.shadows{display:grid;grid-template-columns:repeat(auto-fill,minmax(230px,1fr));gap:10px}
.shadows .sbox{border-radius:12px;padding:16px;background:#f0f4f9;min-height:74px;font-size:11px;color:#5a6a80}
.shadows .sbox.dk{background:#2a3547;color:#a6b4c8}
.shadows .sbox code{display:block;margin-top:6px;font-size:10.5px;word-break:break-word}
.shadows .sbox .box{background:#fff;border-radius:10px;padding:10px;color:#1a2236;font-weight:600;font-size:12px}
.shadows .sbox.dk .box{background:#253662;color:#e8edf4}
.swrap{width:100%;overflow-x:auto}
@media (max-width:720px){
  main{padding:12px}
  header.top h1{font-size:20px}
  table.states{min-width:0}
  table.states thead{display:none}
  table.states tbody th{display:block;width:auto;padding:10px 8px 4px;border:0}
  table.states td.cell{display:block;width:auto;padding:10px}
  table.states td.cell:before{content:attr(data-l);display:block;font-size:11px;font-weight:700;color:#5a6a80;text-transform:uppercase;letter-spacing:.06em;margin-bottom:6px}
  table.states tr{display:block}
  .roles{display:block;overflow-x:auto}
}
"""


def mode_block():
    return (
        f'.m-light{{{LIGHT.strip()}}}\n'
        f'.m-dark{{{DARK.strip()}}}\n'
    )


# ── Piezas de la plantilla ──────────────────────────────────────────────────
def cell(mode, body, cap, gap):
    global GAPS
    label = 'Claro' if mode == 'light' else 'Oscuro'
    cls = f'cell m-{mode}'
    tag = ''
    if gap:
        cls += ' gap'
        text = gap if isinstance(gap, str) else '⚠ sin valor'
        tag = f'<span class="tag">{esc(text)}</span>'
        if mode == 'light':
            GAPS += 1
    return f'<td class="{cls}" data-l="{label}">{tag}{body}<small>{esc(cap)}</small></td>'


def S(name, body, cap, gap=False):
    """Fila de estado. `cap` y `gap` pueden ser tupla (claro, oscuro)."""
    cl, cd = cap if isinstance(cap, tuple) else (cap, cap)
    gl, gd = gap if isinstance(gap, tuple) else (gap, gap)
    return (f'<tr><th scope="row">{esc(name)}</th>'
            f'{cell("light", body, cl, gl)}{cell("dark", body, cd, gd)}</tr>')


NA = '<span class="na">—</span>'


def A(aid, title, src, pend, rows, note=''):
    """Átomo: cabecera, avisos amarillos de decisiones abiertas y tabla de estados."""
    global PENDS
    pend_html = ''
    if pend:
        PENDS += 1
        lis = ''.join(f'<li><b>{esc(c)}</b> {esc(t)}</li>' for c, t in pend)
        pend_html = (f'<aside class="pend" role="note"><strong>⚠ Sin decidir · '
                     f'pendiente en ATOMOS.md</strong><ul>{lis}</ul></aside>')
    note_html = f'<p class="note">{esc(note)}</p>' if note else ''
    return (f'<article class="atom" id="{aid}">'
            f'<header><h3>{esc(title)}</h3><code>{esc(src)}</code></header>'
            f'{pend_html}'
            f'<div class="tw"><table class="states"><thead><tr><th>Estado</th>'
            f'<th>Claro</th><th>Oscuro</th></tr></thead>'
            f'<tbody>{"".join(rows)}</tbody></table></div>'
            f'{note_html}</article>')


def SEC(sid, num, title, intro, blocks):
    return (f'<section class="sec" id="{sid}"><h2>{num} · {esc(title)}</h2>'
            f'<p class="intro">{esc(intro)}</p>{"".join(blocks)}</section>')


# ── 1 · Primitivos y roles ──────────────────────────────────────────────────
def pd_tag(code):
    return f'<span class="pd">⚠ {esc(code)}</span>' if code and code != '—' else '—'


def sw(hex_, dark=False):
    cls = 'swatch dk' if dark else 'swatch'
    return f'<span class="{cls}" style="background:{hex_}"></span>'


def primitives():
    rows = [
        ('palette.blue', '#0065BB', '', 'Marca. Primario de MUI y del botón.'),
        ('palette.blueLight', '#29ABE2', '', 'Es a la vez secondary.main, semantic.info y data8[1] (un primitivo, cuatro roles).'),
        ('palette.blueDark', '#004696', '', 'Hover de botón primario.'),
        ('palette.gray', '#7F7F7F', '', 'Gris de marca.'),
        ('palette.grayLight', '#C9C9C9', 'D9', '0 usos fuera del tema. La app usa #c8c8c8 (16 ocurrencias en 11 archivos) y #c4c4c4 (10).'),
        ('palette.grayDark', '#5A5A5A', 'D9', '0 usos fuera del tema.'),
        ('palette.blueGrad1', '#003B8E', '', 'Marcado deprecated en colors.ts; sin uso.'),
    ]
    body = ''.join(
        f'<tr class="{"pend-row" if d else ""}"><td><code>{esc(n)}</code></td>'
        f'<td>{sw(v)}<code>{esc(v)}</code></td>'
        f'<td>{pd_tag(d)} {esc(t)}</td></tr>'
        for n, v, d, t in rows)
    return (
        '<h3 style="margin:0 0 8px">Primitivos · palette (colors.ts)</h3>'
        '<div class="swrap"><table class="roles"><thead><tr><th>Primitivo</th><th>Valor</th>'
        '<th>Nota</th></tr></thead><tbody>' + body + '</tbody></table></div>')


def surfaces():
    light = [('surface.soft', '#f0f4f9', 'background.default'), ('surface.paper', '#ffffff', 'background.paper'),
             ('surface.navy', '#1a2236', 'text.primary'), ('surface.muted', '#5a6a80', 'text.secondary'),
             ('surface.border', '#dde3ec', 'divider'), ('surface.inputBorder', '#d0d8e4', 'fieldset 1.5px')]
    dark = [('surfaceDark.base', '#2A3547', 'background.default'), ('surfaceDark.paper', '#253662', 'background.paper · rail'),
            ('surfaceDark.text', '#e8edf4', 'text.primary'), ('surfaceDark.muted', '#a6b4c8', 'text.secondary'),
            ('surfaceDark.border', 'rgba(74,144,226,0.12)', 'divider')]
    sem = [('semantic.error', '#e2445c', '#ef4444'), ('semantic.warning', '#fdab3d', '#f59e0b'),
           ('semantic.success', '#00c875', '#22c55e'), ('semantic.info', '#29ABE2', '#06b6d4')]
    data = ['#0065BB', '#29ABE2', '#00c875', '#fdab3d', '#e2445c', '#a25ddc', '#ff642e', '#579bfc']
    out = '<h3 style="margin:16px 0 8px">Superficies, semánticos y datos</h3><div class="swrap"><table class="roles"><thead><tr><th>Primitivo claro</th><th>Valor</th><th>Uso</th></tr></thead><tbody>'
    out += ''.join(f'<tr><td><code>{esc(n)}</code></td><td>{sw(v)}<code>{esc(v)}</code></td><td>{esc(u)}</td></tr>' for n, v, u in light)
    out += '</tbody></table></div>'
    out += '<div class="swrap" style="margin-top:12px"><table class="roles"><thead><tr><th>Primitivo oscuro</th><th>Valor</th><th>Uso</th></tr></thead><tbody>'
    out += ''.join(f'<tr><td><code>{esc(n)}</code></td><td>{sw(v, True)}<code>{esc(v)}</code></td><td>{esc(u)}</td></tr>' for n, v, u in dark)
    out += '</tbody></table></div>'
    out += '<div class="swrap" style="margin-top:12px"><table class="roles"><thead><tr><th>Semántico</th><th>Claro</th><th>Oscuro</th></tr></thead><tbody>'
    out += ''.join(f'<tr><td><code>{esc(n)}</code></td><td>{sw(l)}<code>{esc(l)}</code></td><td>{sw(d, True)}<code>{esc(d)}</code></td></tr>' for n, l, d in sem)
    out += '</tbody></table></div>'
    out += ('<p class="note"><b>Paleta de datos (data8, sin cambio):</b> ' + ' '.join(sw(c) for c in data)
            + ' <code>' + ' '.join(data) + '</code> · se guarda en la base de cts-manager (D8, D9).</p>')
    return out


def new_primitives():
    rows = [
        ('surface.rowHover', '#f7fafd', '—', 'Fila de tabla, sólido por las celdas sticky.', ''),
        ('surface.selected', '#eff5fe', 'D12', 'Fila seleccionada de la grilla.', 'D12'),
        ('surfaceDark.raised', '#2d3c53', 'D12', 'Cabecera de tabla, celdas de grilla, banda de grupo.', 'D12'),
        ('surfaceDark.rowHover', '#2f435e', 'D12', 'Hover de fila en oscuro.', 'D12'),
        ('surfaceDark.selected', '#2f476d', 'D12', 'Fila seleccionada en oscuro.', 'D12'),
        ('surfaceDark.inverse', '#1e2d42', 'D19', 'Fondo del tooltip oscuro.', 'D19'),
        ('surfaceDark.authPage', '#1a1a2e', 'D9', 'Fondo de la página de acceso.', 'D9'),
        ('brandOnDark', '#89AEDC', 'D14', 'Texto de marca y enlaces sobre fondo oscuro.', 'D14'),
        ('darkAction', 'rgba(74,144,226,α)', '—', 'Base de action.* oscuro.', ''),
        ('neutralStatus', '#c4c4c4', 'D9', 'Estado vacío (StatusCell.tsx:30).', 'D9'),
        ('successHover', '#00a65c', 'D9', 'Hover del botón verde.', 'D9'),
        ('focusRing', 'rgba(0,101,187,0.15)', 'D2', 'Anillo de foco del input (único que existe).', 'D2'),
        ('scrim', 'rgba(15,23,42,0.55)', '—', 'Velo del recorrido guiado.', ''),
    ]
    body = ''.join(
        f'<tr class="{"pend-row" if d else ""}"><td><code>{esc(n)}</code></td>'
        f'<td>{sw(v.replace("α", "0.5"))}<code>{esc(v)}</code></td>'
        f'<td>{pd_tag(dd)}{esc(t)}</td></tr>'
        for n, v, dd, t, d in rows)
    return ('<h3 style="margin:16px 0 8px">Primitivos nuevos (sin token aún)</h3>'
            '<div class="swrap"><table class="roles"><thead><tr><th>Propuesto</th><th>Valor</th>'
            '<th>Decisión y uso</th></tr></thead><tbody>' + body + '</tbody></table></div>')


def roles_table():
    # (rol, claro, oscuro, estado, decisiones, swatch claro, swatch oscuro)
    rows = [
        ('bg.canvas', '#f0f4f9', '#2A3547', 'tema', '', '#f0f4f9', '#2A3547'),
        ('bg.surface', '#ffffff', '#253662', 'tema', '', '#ffffff', '#253662'),
        ('bg.raised', '#ffffff', '#2d3c53 (dialog: #253662)', 'nuevo', 'D12', '#ffffff', '#2d3c53'),
        ('bg.groupHeader', '#f0f4f9', '#2d3c53', 'nuevo', 'D12', '#f0f4f9', '#2d3c53'),
        ('bg.tableHead', '#0065BB', '#2d3c53', 'tema', 'D12', '#0065bb', '#2d3c53'),
        ('bg.rowHover', '#f7fafd', '#2f435e', 'tema (4 tablas distintas)', 'D12', '#f7fafd', '#2f435e'),
        ('bg.selected', '#eff5fe', '#2f476d', 'nuevo', 'D1, D12', '#eff5fe', '#2f476d'),
        ('bg.sunken', 'rgba(15,23,42,0.035)', 'rgba(255,255,255,0.045)', 'nuevo (deriva)', 'D12', 'rgba(15,23,42,.035)', 'rgba(255,255,255,.045)'),
        ('bg.rail', '#0065BB', '#253662', 'nuevo (literal en Sidebar.tsx:428)', '', '#0065bb', '#253662'),
        ('bg.inverse', '#1a2236', '#1e2d42', 'tema', 'D19', '#1a2236', '#1e2d42'),
        ('bg.authPage', '#f0f4f9', '#1a1a2e', 'nuevo', 'D9', '#f0f4f9', '#1a1a2e'),
        ('text.primary', '#1a2236', '#e8edf4', 'tema', '', '#1a2236', '#e8edf4'),
        ('text.secondary', '#5a6a80', '#a6b4c8', 'tema', '', '#5a6a80', '#a6b4c8'),
        ('text.disabled', 'rgba(0,0,0,0.38) (MUI)', 'rgba(255,255,255,0.5) (MUI)', 'MUI · 435 usos', 'D4', 'rgba(0,0,0,.38)', 'rgba(255,255,255,.5)'),
        ('text.brand', '#0065BB', '#89AEDC', 'nuevo', 'D14', '#0065bb', '#89aedc'),
        ('border.subtle', '#dde3ec', 'rgba(74,144,226,0.12)', 'tema', 'D9', '#dde3ec', 'rgba(74,144,226,.12)'),
        ('border.control', '#d0d8e4', 'rgba(74,144,226,0.25)', 'tema', '', '#d0d8e4', 'rgba(74,144,226,.25)'),
        ('border.controlHover', '#0065BB (pedido) · #1a2236 (renderiza)', 'rgba(41,171,226,0.5) (pedido) · #e8edf4 (renderiza)', 'tema, sin efecto', 'D5', '#1a2236', '#e8edf4'),
        ('brand.default', '#0065BB', '#0065BB', 'tema', 'D14', '#0065bb', '#0065bb'),
        ('brand.hover', '#004696', '#004696', 'tema (deriva en 3 valores)', 'D13', '#004696', '#004696'),
        ('brand.subtle', 'rgba(0,101,187,0.05)', 'rgba(41,171,226,0.10)', 'nuevo (deriva)', 'D11', 'rgba(0,101,187,.05)', 'rgba(41,171,226,.1)'),
        ('focus.ring', '0 0 0 3px rgba(0,101,187,0.15)', 'igual', 'tema (solo input)', 'D2', 'rgba(0,101,187,.15)', 'rgba(0,101,187,.15)'),
        ('overlay.hover', 'rgba(0,101,187,0.05)', 'rgba(74,144,226,0.08)', 'tema', '', 'rgba(0,101,187,.05)', 'rgba(74,144,226,.08)'),
        ('overlay.selected', 'rgba(0,101,187,0.1)', 'rgba(74,144,226,0.16)', 'tema (MUI no lo usa)', 'D1', 'rgba(0,101,187,.1)', 'rgba(74,144,226,.16)'),
        ('overlay.focus', 'rgba(0,0,0,0.12) (MUI)', 'rgba(74,144,226,0.12)', 'claro: MUI', 'D3', 'rgba(0,0,0,.12)', 'rgba(74,144,226,.12)'),
        ('overlay.active', 'rgba(0,0,0,0.54) (MUI)', 'rgba(255,255,255,0.6)', 'claro: MUI', 'D3', 'rgba(0,0,0,.54)', 'rgba(255,255,255,.6)'),
        ('overlay.disabled', 'rgba(0,0,0,0.26) (MUI)', 'rgba(255,255,255,0.28)', 'claro: MUI', 'D3', 'rgba(0,0,0,.26)', 'rgba(255,255,255,.28)'),
        ('overlay.scrim', 'rgba(0,0,0,0.5) (MUI Backdrop)', 'igual', 'MUI', 'sin decisión', 'rgba(0,0,0,.5)', 'rgba(0,0,0,.5)'),
        ('feedback.error.default', '#e2445c', '#ef4444', 'tema', '', '#e2445c', '#ef4444'),
        ('feedback.warning.default', '#fdab3d', '#f59e0b', 'tema', 'D8', '#fdab3d', '#f59e0b'),
        ('feedback.success.default', '#00c875', '#22c55e', 'tema', 'D8', '#00c875', '#22c55e'),
        ('feedback.info.default', '#29ABE2', '#06b6d4', 'tema', '', '#29abe2', '#06b6d4'),
        ('feedback.*.hover', 'MUI palette.dark', 'MUI palette.dark', 'MUI calcula', 'D21', '#9e2f40', '#a72f2f'),
        ('feedback.*.subtle', 'alfa 0.05–0.08', 'alfa 0.06–0.12', 'nuevo (deriva)', 'D17, D11', 'rgba(226,68,92,.07)', 'rgba(239,68,68,.09)'),
        ('scrollbar.thumb', '#c0c8d4', '#3d4f6f', 'tema (duplicado en index.css)', 'D18', '#c0c8d4', '#3d4f6f'),
    ]
    body = ''
    for role, l, d, st, dec, sl, sd in rows:
        pend = bool(dec) and dec != 'sin decisión'
        tag = pd_tag(dec)
        body += (f'<tr class="{"pend-row" if pend else ""}"><td><code>{esc(role)}</code></td>'
                 f'<td>{sw(sl)}{esc(l)}</td><td>{sw(sd, True)}{esc(d)}</td>'
                 f'<td>{esc(st)}</td><td>{tag}</td></tr>')
    return ('<h3 style="margin:16px 0 8px">Roles · capa 2 (claro / oscuro)</h3>'
            '<p class="note">Filas amarillas: el rol tiene decisión abierta. '
            'Nada de esta tabla está decidido hasta responder D1–D23.</p>'
            '<div class="swrap"><table class="roles"><thead><tr><th>Rol</th><th>Claro</th>'
            '<th>Oscuro</th><th>Estado</th><th>Decisión</th></tr></thead><tbody>' + body +
            '</tbody></table></div>')


def shadows_block():
    items = [
        ('shadow.e1', '0 1px 4px rgba(0,0,0,0.06)', '0 1px 4px rgba(0,0,0,0.4)', 'D16'),
        ('shadow.e2', '0 2px 8px rgba(0,0,0,0.08)', '0 2px 8px rgba(0,0,0,0.45)', ''),
        ('shadow.e4', '0 8px 24px rgba(0,0,0,0.12)', '0 8px 24px rgba(0,0,0,0.55)', ''),
        ('shadow.e6', '0 16px 40px rgba(0,0,0,0.16)', '0 16px 40px rgba(0,0,0,0.65)', 'D16'),
        ('shadow.button', '0 2px 8px rgba(0,101,187,0.3)', 'igual', 'D15'),
        ('shadow.menu', '0 8px 24px rgba(0,101,187,0.15)', '0 8px 24px rgba(0,0,0,0.5)', 'D15'),
        ('shadow.dialog', '0 24px 64px rgba(0,101,187,0.18)', '0 24px 64px rgba(0,0,0,0.7)', ''),
        ('shadow.tooltipRich', '0 6px 20px rgba(0,101,187,0.12)', '0 6px 20px rgba(0,0,0,0.45) (sin valor en token)', 'D19'),
    ]
    cells = ''
    for name, l, d, dec in items:
        cls = 'sbox'
        tag = f'<span class="pd">⚠ {esc(dec)}</span>' if dec else ''
        cells += (f'<div class="sbox"><span class="box" style="box-shadow:{l}">{esc(name)}</span>'
                  f'<code>{esc(l)}</code></div>'
                  f'<div class="sbox dk"><span class="box" style="box-shadow:{d.split(" (")[0]}">{esc(name)}</span>'
                  f'<code>{esc(d)}</code>{tag}</div>')
    return ('<h3 style="margin:16px 0 8px">Sombras · claro (izquierda) y oscuro (derecha)</h3>'
            '<div class="shadows">' + cells + '</div>')


def sec1():
    return SEC('primitivos', '1', 'Primitivos y roles',
               'Capa 1 y 2 de ATOMOS.md. Los valores vienen de src/colors.ts y de la tabla de roles. '
               'Las filas amarillas tienen decisión abierta.',
               [primitives(), surfaces(), new_primitives(), roles_table(), shadows_block()])


# ── 2 · Controles ───────────────────────────────────────────────────────────
def controles():
    out = []
    cap_btn = 'fondo brand.default #0065BB · texto text.onBrand #fff · sombra shadow.button 0 2px 8px rgba(0,101,187,0.3) · radio 8px · 14px/600 · alto 36.5px [M]'
    out.append(A('c-btn-cp', 'Button · contained primary', 'theme/ctsTheme.ts:131-136, 124-129 · ~74 usos',
        [('D2', 'focus-visible: el botón no tiene anillo propio; hoy solo cambia la sombra.'),
         ('D3', 'activo y deshabilitado sin valor en el tema; se ven los de MUI.'),
         ('D6', 'foco por teclado: sombra accidental shadows[6] (0 16px 40px).'),
         ('D13', 'hover de marca: #004696 propuesto, hoy hay #0078d4 y #2e4275 en otros sitios.')],
        [S('reposo', '<button class="btn btn-cp">Guardar</button>', cap_btn),
         S('hover', '<button class="btn btn-cp is-hover">Guardar</button>',
           'fondo brand.hover #004696 · sombra shadow.buttonHover 0 4px 12px rgba(0,101,187,0.4)'),
         S('activo', '<button class="btn btn-cp is-active">Guardar</button>',
           'MUI: igual que hover (la regla hover gana sobre shadows[8]) · ripple #fff opacidad 0.3, 550ms',
           gap='⚠ sin valor → MUI (D3)'),
         S('focus-visible', '<button class="btn btn-cp is-focus">Guardar</button>',
           'MUI: fondo de reposo · sombra shadows[6] 0 16px 40px rgba(0,0,0,0.16) L / rgba(0,0,0,0.65) D · outline 0, sin focus.ring',
           gap='⚠ sin valor → MUI (D2, D6)'),
         S('deshabilitado', '<button class="btn btn-cp is-disabled" disabled>Guardar</button>',
           'fondo overlay.disabledBg L MUI rgba(0,0,0,0.12) · D tema rgba(255,255,255,0.08) · texto overlay.disabled L MUI rgba(0,0,0,0.26) · D tema rgba(255,255,255,0.28)',
           gap='⚠ sin valor → MUI (D3)'),
         S('cargando', '<button class="btn btn-cp is-disabled">Aplicando <span class="spin"></span></button>',
           'patrón: disabled + CircularProgress 14px color inherit en startIcon (la prop loading de MUI 7 no se usa)')],
        note='Contraste blanco sobre #0065BB: 5.87:1. disableElevation no quita la sombra azul (D20).'))

    out.append(A('c-btn-sec', 'Button · contained secondary', 'theme/ctsTheme.ts:139-144 · 0 usos en la app',
        [('D15', 'shadow.buttonSecondaryHover no existe en tokens.shadows (solo en el tema).'),
         ('D2', 'sin anillo de foco propio.'),
         ('D3', 'activo y deshabilitado sin valor en el tema.')],
        [S('reposo', '<button class="btn btn-sec">Aplicar</button>',
           'fondo secondary.default #29ABE2 · texto #fff (2.62:1) · sombra shadow.buttonSecondary 0 2px 8px rgba(41,171,226,0.3)'),
         S('hover', '<button class="btn btn-sec is-hover">Aplicar</button>',
           'fondo secondary.hover #1a8ab8 · sombra 0 4px 12px rgba(41,171,226,0.4)'),
         S('activo', '<button class="btn btn-sec is-hover">Aplicar</button>',
           'MUI: igual que hover + ripple', gap='⚠ sin valor → MUI (D3)'),
         S('focus-visible', '<button class="btn btn-sec is-focus">Aplicar</button>',
           'MUI: sombras[6] 0 16px 40px rgba(0,0,0,0.16) L / 0.65 D', gap='⚠ sin valor → MUI (D2, D6)'),
         S('deshabilitado', '<button class="btn btn-cp is-disabled">Aplicar</button>',
           'overlay.disabledBg / overlay.disabled MUI (como primary)', gap='⚠ sin valor → MUI (D3)')]))

    out.append(A('c-btn-err', 'Button · destructivo (color error, contained)', 'MUI con la paleta · ~16 usos · DeleteDialog.tsx:112-119',
        [('D21', 'hover: error.dark lo calcula MUI, no es literal en cts-manager.'),
         ('D2', 'foco sin anillo propio.'),
         ('D3', 'activo y deshabilitado sin valor.')],
        [S('reposo', '<button class="btn btn-err">Eliminar</button>',
           'fondo feedback.error.default #e2445c L / #ef4444 D · texto #fff (MUI) · sombra shadow.e2 0 2px 8px rgba(0,0,0,0.08) L / 0.45 D (neutra, no azul)'),
         S('hover', '<button class="btn btn-err is-hover">Eliminar</button>',
           'fondo derivado MUI rgb(158,47,64) L / rgb(167,47,47) D (D21) · sombra shadow.e4 0 8px 24px rgba(0,0,0,0.12) L / 0.55 D'),
         S('activo', '<button class="btn btn-err is-hover">Eliminar</button>',
           'MUI: fondo de hover; sombra shadows[8] 0 16px 40px', gap='⚠ sin valor → MUI (D3)'),
         S('focus-visible', '<button class="btn btn-err is-focus">Eliminar</button>',
           'MUI: sombras[6] 0 16px 40px rgba(0,0,0,0.16) L / 0.65 D', gap='⚠ sin valor → MUI (D2, D6)'),
         S('deshabilitado', '<button class="btn btn-err is-disabled">Eliminar</button>',
           'overlay.disabledBg / overlay.disabled MUI', gap='⚠ sin valor → MUI (D3)')]))

    out.append(A('c-btn-out', 'Button · outlined', 'theme/ctsTheme.ts:146-149 · ~44 small + 20 medium',
        [('D14', 'texto #0065BB sobre oscuro: 2.01:1 contra #253662.'),
         ('D2', 'foco sin anillo: solo ripple pulsante.'),
         ('D3', 'activo y deshabilitado sin valor.'),
         ('D21', 'borde rgba(0,101,187,0.5) lo calcula MUI (alpha de main).')],
        [S('reposo', '<button class="btn btn-out">Cancelar</button>',
           'fondo transparente · texto brand.default #0065BB (L y D, D14) · borde borders.emphasis 1.5px rgba(0,101,187,0.5) · radio 8px · padding 5px 15px'),
         S('hover', '<button class="btn btn-out is-hover">Cancelar</button>',
           ('fondo MUI rgba(0,101,187,0.04) L', 'fondo MUI rgba(0,101,187,0.08) D'),),
         S('activo', '<button class="btn btn-out is-hover">Cancelar</button>',
           'MUI: hover + ripple 0.3', gap='⚠ sin valor → MUI (D3)'),
         S('focus-visible', '<button class="btn btn-out">Cancelar</button>',
           'MUI: sin cambio estático, solo ripple pulsante; sin anillo [M]', gap='⚠ sin valor → MUI (D2)'),
         S('deshabilitado', '<button class="btn btn-out is-disabled">Cancelar</button>',
           'texto overlay.disabled L MUI rgba(0,0,0,0.26) · D tema rgba(255,255,255,0.28) · borde 1px overlay.disabledBg (la regla MUI gana al 1.5px)',
           gap='⚠ sin valor → MUI (D3)')]))

    out.append(A('c-btn-txt', 'Button · text', 'MUI · ~120 small + 63 planos (sobre todo «Cancelar»)',
        [('D4', 'text.disabled sin definir.'),
         ('D2', 'foco sin anillo.'),
         ('D3', 'activo y deshabilitado sin valor.'),
         ('D14', 'texto #0065BB sobre oscuro: 2.01:1.')],
        [S('reposo', '<button class="btn btn-txt">Cancelar</button>',
           'fondo transparente · texto brand.default #0065BB (L y D) · padding medium 6px 8px · radio 8px'),
         S('hover', '<button class="btn btn-txt is-hover">Cancelar</button>',
           ('fondo MUI rgba(0,101,187,0.04) L', 'fondo MUI rgba(0,101,187,0.08) D')),
         S('activo', '<button class="btn btn-txt">Cancelar</button>', 'MUI: solo ripple, sin cambio estático',
           gap='⚠ sin valor → MUI (D3)'),
         S('focus-visible', '<button class="btn btn-txt">Cancelar</button>', 'MUI: solo ripple pulsante; sin anillo',
           gap='⚠ sin valor → MUI (D2, D6)'),
         S('deshabilitado', '<button class="btn btn-txt is-disabled">Cancelar</button>',
           'texto overlay.disabled L MUI rgba(0,0,0,0.26) · D tema rgba(255,255,255,0.28)', gap='⚠ sin valor → MUI (D3)')]))

    out.append(A('c-btn-size', 'Button · tamaños', 'theme/ctsTheme.ts:150 (small) · MUI (medium, large)',
        [('D15', 'large sin valor en el tema (4 usos); small con padding 4px 12px y 13px, no medido en todas las variantes.')],
        [S('small', '<button class="btn btn-cp btn-sm">Guardar</button>',
           'padding 4px 12px (override del tema, reemplaza 3px 9px) · 13px (0.8125rem) · outlined small 31px [M]'),
         S('medium (defecto)', '<button class="btn btn-cp">Guardar</button>',
           'padding contained 6px 16px · outlined 5px 15px + borde · text 6px 8px · 14px lh 1.75 · alto 36.5px [M]'),
         S('large', '<button class="btn btn-cp btn-lg">Guardar</button>',
           'padding 7px 21px (MUI) · 15px · alto 42.25px · ícono 22px', gap='⚠ sin valor → MUI (D15)')]))

    out.append(A('c-btn-ok', 'Button · verde de «Aplicar cambios» (personalizado)', 'features/shared-view/SharedViewPage.tsx:703-705, 809-811',
        [('D8', 'contraste blanco sobre #00c875: 2.21:1; no cambia en oscuro.'),
         ('D9', '#00a65c no está en colors.ts (se llama successHover).'),
         ('G2', 'fuga: el hover muestra la sombra azul del tema, no intencionada.'),
         ('D3', 'deshabilitado sin valor: el verde no sobrevive a disabled.')],
        [S('reposo', '<button class="btn btn-ok">Aplicar cambios</button>',
           'fondo feedback.success.default #00c875 (L y D; no cambia a #22c55e) · texto #fff · sombra none · radio 8px'),
         S('hover', '<button class="btn btn-ok is-hover">Aplicar cambios</button>',
           'fondo feedback.success.hover #00a65c · sombra fuga 0 4px 12px rgba(0,101,187,0.4) [M] (G2)',
           gap='fuga de sombra azul (G2)'),
         S('deshabilitado', '<button class="btn btn-ok is-disabled">Aplicando…</button>',
           'overlay.disabledBg / overlay.disabled MUI · la app pone spinner size 14 y «Aplicando…»', gap='⚠ sin valor → MUI (D3)')]))

    out.append(A('c-ibtn', 'IconButton · defecto y variantes', 'MUI IconButton · size small en 186 de 192 usos',
        [('D3', 'reposo y hover sin valor en claro: se ven los negros de MUI.'),
         ('D2', 'foco: solo ripple pulsante, sin anillo.'),
         ('D4', 'destructivo: text.disabled sin definir.'),
         ('D15', 'tamaños por sitio (30 / 32 / 40 px) sin token.')],
        [S('reposo', '<button class="ib" aria-label="Opciones">⋮</button>',
           ('MUI action.active rgba(0,0,0,0.54) (sin valor en claro) · radio 50% · small: padding 5 + ícono 18 = 28px MUI (ATOMOS dice 30×30, sin verificar)',
            'action.active rgba(255,255,255,0.6) (T:35) · radio 50% · small 28px MUI (ATOMOS dice 30×30, sin verificar)'),
           gap=('⚠ sin valor → MUI (D3)', False)),
         S('hover', '<button class="ib is-hover" aria-label="Opciones">⋮</button>',
           ('MUI alpha(action.active, 0.04) = rgba(0,0,0,0.04) L', 'MUI rgba(255,255,255,0.08) D · motion.nav 0.15s'),
           gap='⚠ sin valor → MUI (D3)'),
         S('toolbar · reposo', '<button class="ib toolbar" aria-label="Filtrar">⚙</button>',
           'texto text.secondary #5a6a80 / #a6b4c8 · estilo de casa (BoardToolbar.tsx:98-121)'),
         S('toolbar · hover', '<button class="ib toolbar is-hover" aria-label="Filtrar">⚙</button>',
           'ícono brand.default #0065BB (2.01:1 en oscuro, D14) · fondo overlay.hover rgba(0,101,187,0.05) / rgba(74,144,226,0.08)'),
         S('primario', '<button class="ib prim" aria-label="Editar">✎</button>',
           'color brand.default #0065BB (ChartSettingsDialog.tsx:229)'),
         S('error', '<button class="ib err" aria-label="Quitar">✕</button>',
           'color feedback.error.default #e2445c / #ef4444 (TemplateDetailPage.tsx:482)'),
         S('deshabilitado', '<button class="ib is-disabled" aria-label="Opciones" disabled>⋮</button>',
           'overlay.disabled MUI rgba(0,0,0,0.26) / rgba(255,255,255,0.28)', gap='⚠ sin valor → MUI (D3)'),
         S('focus-visible', '<button class="ib is-focus" aria-label="Opciones">⋮</button>',
           'MUI: solo ripple; sin anillo', gap='⚠ sin valor → MUI (D2)')]))

    out.append(A('c-ibtn-rail', 'IconButton · sobre el rail y botón flotante de reapertura', 'layout/Sidebar.tsx:463,571-594 · layout/AppLayout.tsx:34-37',
        [('D10', 'blancos del rail: 0.7 reposo, hover 0.1; la escalera no está consolidada.'),
         ('D13', 'botón flotante: hover #0078d4 L / #2e4275 D, fuera de la paleta.'),
         ('D15', 'flotante 30×30 medido frente a density.floatingAction 38.'),
         ('D20', 'botón «+» del rail: #1976d2 / rgba(25,118,210,0.9) es azul de MUI; no se porta.')],
        [S('rail · reposo', '<span class="rail-ib" style="background:var(--rail);padding:6px">⋯</span>',
           'texto rgba(255,255,255,0.7) (tokens.rail.itemIdleColor 0.65 en NavItem, D10) · sin fondo'),
         S('rail · hover', '<span class="rail-ib is-hover" style="background:rgba(255,255,255,0.1);padding:6px;">⋯</span>',
           'fondo rgba(255,255,255,0.1) (onRail.hover) · texto #fff'),
         S('flotante · reposo', '<span class="fab">‹</span>',
           ('fondo brand.default #0065BB · icono #fff · sombra shadow.e1 0 1px 4px rgba(0,0,0,0.06) · 30×30',
            'fondo bg.surface #253662 · sombra shadow.e1 0 1px 4px rgba(0,0,0,0.4) · 30×30')),
         S('flotante · hover', '<span class="fab is-hover" style="background:#0078d4">‹</span>',
           ('#0078d4 literal (fuera de paleta)', '#2e4275 literal (fuera de paleta)'),
           gap='⚠ hover fuera de paleta (D13)'),
         S('botón «+» del rail', '<span class="plus-bad">+</span>',
           'rgba(25,118,210,0.9) reposo · #1976d2 hover (azul MUI)', gap='⚠ no se porta (D20)')]))

    out.append(A('c-input', 'Input · OutlinedInput / TextField', 'theme/ctsTheme.ts:182-202 · size small en 221 de 244 usos',
        [('D5', 'hover: el tema pide #0065BB, MUI gana y se pinta #1a2236; se decide qué se ve.'),
         ('D2', 'error: el anillo sigue azul, no hay anillo de error.'),
         ('D4', 'placeholder y texto deshabilitado sin definir.'),
         ('D3', 'borde deshabilitado sin valor en claro.'),
         ('D14', 'label con foco #0065BB sobre oscuro: 2.01:1.')],
        [S('reposo', '<div class="fld"><label>Correo</label><div class="ctl">ana@ejemplo.com</div></div>',
           ('fieldset border.control 1.5px #d0d8e4 · texto text.primary #1a2236 · label text.secondary #5a6a80 · radio 8px · alto 38.56px [M]',
            'fieldset rgba(74,144,226,0.25) · texto #e8edf4 · label #a6b4c8')),
         S('hover', '<div class="fld is-hover"><label>Correo</label><div class="ctl">ana@ejemplo.com</div></div>',
           ('renderiza #1a2236 (text.primary) · pedido por el tema #0065BB, código muerto (T:197-199)',
            'renderiza #e8edf4 · pedido rgba(41,171,226,0.5) (código muerto)'),
           gap='⚠ pedido ≠ renderizado (D5)'),
         S('focus-visible', '<div class="fld is-focus"><label>Correo</label><div class="ctl">ana@ejemplo.com</div></div>',
           'label brand.default #0065BB · borde borders.accent 2px #0065BB · anillo focus.ring 0 0 0 3px rgba(0,101,187,0.15)'),
         S('error', '<div class="fld is-error"><label>Correo</label><div class="ctl">ana@ejemplo</div><span class="help">Correo no válido</span></div>',
           'label y helperText feedback.error.default #e2445c / #ef4444 · borde 1.5px err · helper 12px',
           gap='⚠ anillo sigue azul (D2)'),
         S('deshabilitado', '<div class="fld is-dis"><label>Correo</label><div class="ctl">ana@ejemplo.com</div></div>',
           'texto text.disabled MUI rgba(0,0,0,0.38) L / rgba(255,255,255,0.5) D · borde overlay.disabled MUI rgba(0,0,0,0.26) / rgba(255,255,255,0.28)',
           gap='⚠ sin valor → MUI (D3, D4)'),
         S('placeholder', '<div class="fld"><label>Buscar</label><div class="ctl"><span class="ph">Escribe para buscar…</span></div></div>',
           'placeholder MUI currentColor opacidad 0.42 L / 0.5 D', gap='⚠ sin valor → MUI (D4)')]))

    out.append(A('c-input-base', 'InputBase dentro de popover (sin borde)', 'DropdownCell.tsx:192-197 · LabelCell.tsx:64-67 · StatusCell.tsx:288-292',
        [('D4', 'icono de búsqueda: text.secondary o text.disabled según el sitio.'),
         ('D2', 'foco: solo caret, sin indicador.'),
         ('D3', 'hover, error y deshabilitado sin valor.')],
        [S('reposo', '<div class="fld" style="width:200px"><div class="ctl" style="border:0;border-bottom:1px solid var(--border);border-radius:0;padding:6px 0;height:auto"><span class="ph">Buscar opción…</span></div></div>',
           'sin fondo ni borde propio · borde inferior border.subtle 1px en el wrapper (DropdownCell.tsx:190, LabelCell.tsx:62, StatusCell.tsx:285) · 13px'),
         S('renombrar (hover / foco)', '<div style="background:var(--overlay-hover);border-radius:10px;padding:6px 10px;font-size:13px;color:var(--text)">Opción en edición</div>',
           'fondo overlay.hover rgba(0,101,187,0.05) / rgba(74,144,226,0.08) · radio 10px · px 0.75 py 0.4 (StatusCell.tsx:482-483)'),
         S('hover · error · deshabilitado', '<div class="fld" style="width:200px"><div class="ctl" style="border:0;border-bottom:1px solid var(--border);border-radius:0;padding:6px 0;height:auto">Sin cambio visual</div></div>',
           'sin valor en el tema (MUI: ninguno)', gap='⚠ sin valor → MUI (D3)')]))

    out.append(A('c-select', 'Select · campo y menú', 'sin MuiSelect en el tema · el campo es OutlinedInput · menú T:375-398',
        [('D1', 'seleccionado: MUI usa primary al 0.08 / 0.16; el tema declara overlay.selected 0.1 / 0.16 sin uso.'),
         ('D5', 'hover del campo: mismo caso que Input.'),
         ('D16', 'sombra del menú: shadow.menu del tema frente a elevation de Paper.'),
         ('D3', 'deshabilitado de la opción sin valor (opacity 0.38 MUI).')],
        [S('campo · reposo', '<div class="fld" style="width:200px"><label>Estado</label><div class="ctl sel">En curso</div></div>',
           'borde border.control · texto text.primary · chevron 24px rgba(0,0,0,0.54) L / rgba(255,255,255,0.6) D · fontSize 13px'),
         S('menú abierto', '<div class="paper" style="width:220px"><div class="mi is-sel">En curso <span class="chk">✓</span></div><div class="mi">Hecho</div><div class="mi">Pendiente</div></div>',
           'fondo bg.raised #ffffff / #253662 · borde 1px border.subtle · shadow.menu 0 8px 24px rgba(0,101,187,0.15) / rgba(0,0,0,0.5) · radio 10px'),
         S('opción · hover', '<div class="paper" style="width:220px"><div class="mi is-hover">Hecho</div></div>',
           'fondo overlay.hover rgba(0,101,187,0.05) / rgba(74,144,226,0.08)'),
         S('opción · seleccionada', '<div class="paper" style="width:220px"><div class="mi is-sel">En curso</div></div>',
           'MUI alpha(primary, selectedOpacity): rgba(0,101,187,0.08) L / rgba(0,101,187,0.16) D (D1) · + hover 0.12 / 0.24'),
         S('opción · deshabilitada', '<div class="paper" style="width:220px"><div class="mi is-dis">Archivado</div></div>',
           'opacity 0.38 MUI', gap='⚠ sin valor → MUI (D3)')]))

    out.append(A('c-check', 'Checkbox', 'MUI Checkbox · size small en ~40 de 44 usos',
        [('D2', 'sin anillo de foco estático (ripple pulsante).'),
         ('D3', 'deshabilitado y activo sin valor.'),
         ('D9', 'TablaEnLinea.tsx:119 usa #8a93a3 en reposo, fuera de text.secondary.'),
         ('D21', 'halo de hover calculado por MUI, no lee action.hover.')],
        [S('sin marcar', '<span class="opt"><span class="halo"><span class="cbx"></span></span>Incluir</span>',
           'icono text.secondary #5a6a80 / #a6b4c8 · 20px (small) · padding de área 9px (la app baja a p 0.25)'),
         S('hover', '<span class="opt"><span class="halo is-hover"><span class="cbx"></span></span>Incluir</span>',
           'halo rgba(0,101,187,0.04) L / rgba(0,101,187,0.08) D (MUI derivado)'),
         S('marcado', '<span class="opt"><span class="halo"><span class="cbx on">✓</span></span>Incluir</span>',
           'icono brand.default #0065BB (D14) · transición fill 0.2s'),
         S('indeterminado', '<span class="opt"><span class="halo"><span class="cbx ind">–</span></span>Todos</span>',
           'brand.default #0065BB (SelectAllCheckbox.tsx:111-117)'),
         S('deshabilitado', '<span class="opt"><span class="halo"><span class="cbx dis"></span></span>Incluir</span>',
           'overlay.disabled MUI rgba(0,0,0,0.26) / rgba(255,255,255,0.28)', gap='⚠ sin valor → MUI (D3)'),
         S('error', '<span class="opt"><span class="halo"><span class="cbx"></span></span>Obligatorio</span>',
           'sin color="error" en ningún Checkbox del código', gap='⚠ sin valor (no existe)')]))

    out.append(A('c-radio', 'Radio', 'MUI Radio · size small · 1 uso con color error',
        [('D2', 'sin anillo de foco estático.'),
         ('D3', 'activo y deshabilitado sin valor.'),
         ('D21', 'halo de hover calculado por MUI.')],
        [S('reposo', '<span class="opt"><span class="halo"><span class="rdo"></span></span>Opción A</span>',
           'icono text.secondary #5a6a80 / #a6b4c8'),
         S('hover', '<span class="opt"><span class="halo is-hover"><span class="rdo"></span></span>Opción A</span>',
           'halo rgba(0,101,187,0.04) L / rgba(0,101,187,0.08) D'),
         S('seleccionado', '<span class="opt"><span class="halo"><span class="rdo on"></span></span>Opción B</span>',
           'icono brand.default #0065BB · punto interior scale 0→1 0.15s (MUI)'),
         S('error', '<span class="opt"><span class="halo"><span class="rdo err on"></span></span>Quitar</span>',
           'color feedback.error.default #e2445c / #ef4444 · halo rgba(226,68,92,0.04) L / rgba(239,68,68,0.08) D (LinkBoardsDialog.tsx:1066)'),
         S('deshabilitado', '<span class="opt"><span class="halo"><span class="rdo dis"></span></span>Opción C</span>',
           'overlay.disabled MUI rgba(0,0,0,0.26) / rgba(255,255,255,0.28)', gap='⚠ sin valor → MUI (D3)'),
         S('activo · foco', '<span class="opt"><span class="halo"><span class="rdo"></span></span>Opción A</span>',
           'MUI: solo ripple pulsante; sin anillo', gap='⚠ sin valor → MUI (D2)')]))

    out.append(A('c-switch', 'Switch', 'MUI Switch · sin override en el tema · small en la mayoría',
        [('D3', 'pista y pulgar apagados: valores de MUI (claro sin definir).'),
         ('D9', 'grises de MUI (grey 100/300/600/800) no son colores CTS.'),
         ('D21', 'deshabilitado encendido: derivados por MUI.'),
         ('D2', 'foco: solo ripple.')],
        [S('apagado', '<span class="sw-row"><span class="sw"><span class="trk"></span><span class="thb"></span></span>Notificar</span>',
           ('pista #000 opacidad 0.38 (MUI) · pulgar #fff · sombra thumb shadow.e1 0 1px 4px rgba(0,0,0,0.06)',
            'pista #fff opacidad 0.3 (MUI) · pulgar #e0e0e0 (grey 300) · sombra 0 1px 4px rgba(0,0,0,0.4)'),
           gap='⚠ pista y pulgar de MUI (D3, D9)'),
         S('apagado · hover', '<span class="sw-row"><span class="sw"><span class="trk"></span><span class="thb"></span></span>Notificar</span>',
           'halo rgba(0,0,0,0.04) L / rgba(255,255,255,0.08) D (MUI)', gap='⚠ sin valor → MUI (D3)'),
         S('encendido', '<span class="sw-row"><span class="sw on"><span class="trk"></span><span class="thb"></span></span>Notificar</span>',
           'pista brand.default #0065BB opacidad 0.5 (opacity.switchTrackOn, NUEVO) · pulgar #0065BB · desplazamiento 16px small / 20px medium'),
         S('color success · encendido', '<span class="sw-row"><span class="sw ok on"><span class="trk"></span><span class="thb"></span></span>Activo</span>',
           'pista feedback.success.default #00c875 L / #22c55e D, opacidad 0.5 (AdminPage.tsx:461)'),
         S('deshabilitado · apagado', '<span class="sw-row"><span class="sw off-dis"><span class="trk"></span><span class="thb"></span></span>Notificar</span>',
           'pista opacidad 0.12 L / 0.2 D · pulgar #f5f5f5 L / #757575 D (MUI grey, D3)', gap='⚠ sin valor → MUI (D3)'),
         S('deshabilitado · encendido', '<span class="sw-row"><span class="sw on-dis"><span class="trk"></span><span class="thb"></span></span>Notificar</span>',
           'pista #0065BB opacidad 0.12 L / 0.2 D · pulgar rgb(158,196,229) L / rgb(0,45,84) D (derivados)', gap='⚠ derivado MUI (D21)')]))

    out.append(A('c-swatch', 'Swatch de color (6 implementaciones)', 'ui/ColorPicker.tsx:86,235-284 · layout/sidebar/ColorPicker.tsx:15-21 · BoardsPage.tsx:323,341 · editores.tsx:61-75 · KpiEditorDialog.tsx:263-269',
        [('D9', 'la paleta de 8 colores está repetida en 5 archivos; no es un token.'),
         ('D2', 'ningún swatch es enfocable por teclado.'),
         ('D8', 'swatch de estado: texto blanco sobre amarillo y verde no pasa AA.'),
         ('D11', 'tinte de KPI: tint(c,\'18\') con borde del mismo color.'),
         ('sin decisión', 'escalas de hover 1.08 / 1.1 / 1.15 / 1.2 y selección con 3 estilos distintos.')],
        [S('A · preset · reposo', '<span class="sq" style="background:#0065bb"></span> <span class="sq" style="background:#29abe2"></span> <span class="sq" style="background:#00c875"></span> <span class="sq" style="background:#fdab3d"></span>',
           'fondo swatch.group c · borde 2px transparent · 24px radio 6px · 26–28px radio 7–8px'),
         S('A · preset · hover', '<span class="sq is-hover" style="background:#e2445c"></span>',
           'transform scale(1.08) · sin cambio de sombra'),
         S('A · preset · seleccionado', '<span class="sq is-sel" style="background:#a25ddc;--c:#a25ddc"></span>',
           'borde 2px solid white · sombra 0 0 0 2px del propio color (el blanco no se ve sobre claro)'),
         S('B · guardado con borrar', '<span class="sq-wrap"><span class="sq" style="background:#ff642e"></span><span class="badge-x">×</span></span>',
           'badge #333 (no es neutro CTS) · ícono blanco 10px · 14×14 top/right -4px · opacity 0→1 0.15s'),
         S('C · disparador personalizado', '<span class="sq add"></span>',
           'conic-gradient de 9 paradas (la primera se repite al final, ui/ColorPicker.tsx:120) · borde 2px white · sombra 0 0 0 2px rgba(0,0,0,0.15) L / rgba(255,255,255,0.2) D (:122)'),
         S('E · grilla · seleccionado', '<span class="sq lg is-sel" style="background:#579bfc;--c:#579bfc"></span>',
           'outline 3px solid del color (borders.indicator) · outline-offset 2px · 28×28 radio 8px'),
         S('F · punto de estado', '<span class="sq status" style="background:#00c875;--c:#00c875"></span>',
           'borde 2px background.paper · sombra 0 0 0 1px del color · 24×24 radio 10px · hover scale(1.1) (cells/StatusCell.tsx:461-469)'),
         S('G · sin color', '<span class="sq none"></span>',
           'borde 1.5px dashed text.disabled · 14px', gap='⚠ text.disabled sin valor (D4)'),
         S('H · paleta de celdas', '<span class="sq grid" style="background:#a25ddc"></span>',
           'celda 22px radio 5px · grilla repeat(4, 22px) · gap 0.75 · editores.tsx:53 usa #a25ddc (MirrorCell.tsx:132 usa #9d50dd, D9)', gap='⚠ dos morados en el código (D9)')]))

    out.append(A('c-link', 'Link', 'MUI Link · sin MuiLink en el tema · BoardBreadcrumb.tsx:13-45',
        [('D2', 'focus-visible: outline del navegador, no focus.ring.'),
         ('D14', 'enlace #0065BB sin variante oscura: 2.01:1.'),
         ('sin decisión', 'hover inconsistente: solo subrayado (migas) frente a subrayado + color (celdas) frente a borde 1px → 2px (Markdown).')],
        [S('reposo', '<a class="lnk" href="#c-link">Ver historial</a>',
           'texto text.secondary #5a6a80 / #a6b4c8 · 13px · peso 500 · sin subrayado'),
         S('hover', '<a class="lnk is-hover" href="#c-link">Ver historial</a>',
           'sin cambio de color · text-decoration underline (link.hoverDecoration, NUEVO)'),
         S('focus-visible', '<a class="lnk is-focus" href="#c-link">Ver historial</a>',
           'outline auto del navegador [M] · no usa focus.ring', gap='⚠ outline del navegador (D2)'),
         S('página actual', '<span class="lnk cur">Tableros</span>',
           'text.primary #1a2236 / #e8edf4 · peso 700'),
         S('celda (enlace de dato)', '<a class="lnk cell-link" href="#c-link">https://ejemplo.com</a>',
           'brand.default #0065BB · 12px (13px en vista compartida) · sin subrayado; hover underline',
           gap='⚠ sin variante oscura (D14)')]))

    out.append(A('c-login', 'Composición · formulario de acceso', 'features/auth/AuthPage.tsx (fondo T:19-23; autofill, radio 20px en Alert)',
        [('D9', 'fondo de la página de acceso #1a1a2e (surfaceDark.authPage) frente a #2A3547.'),
         ('D7', 'alerta de error con radio 20px (borderRadius 2) en lugar de 8px.'),
         ('sin decisión', 'radio y borde del contenedor no están medidos: el radio 12px de AuthPage.tsx:110 está en un bloque comentado.'),
         ('sin decisión', 'autofill: #e8f0fe / #253662 con texto #1a1a1a / #fff, no son text.primary.')],
        [S('formulario', '<div class="login-stage"><div class="login"><h4>Iniciar sesión</h4>'
           '<div class="fld"><label>Correo</label><div class="ctl">ana@ejemplo.com</div></div>'
           '<div class="fld is-focus"><label>Contraseña</label><div class="ctl">••••••••</div></div>'
           '<button class="btn btn-cp btn-full">Entrar</button>'
           '<a class="lnk" href="#c-login" style="text-align:center">¿Olvidaste tu contraseña?</a></div></div>',
           ('fondo página #f0f4f9 · formulario sin fondo propio (AuthPage.tsx:137) · radio no medido',
            'fondo página #1a1a2e (D9) · formulario #2A3547 (AuthPage.tsx:137)')),
         S('error', '<div class="login-stage"><div class="login"><h4>Iniciar sesión</h4>'
           '<div class="alert err"><span class="ico">⛔</span><span>Credenciales inválidas</span></div>'
           '<div class="fld is-error"><label>Correo</label><div class="ctl">ana@ejemplo</div></div>'
           '<button class="btn btn-cp btn-full">Entrar</button></div></div>',
           'alerta standard error (ver Alertas) · radio 20px en AuthPage.tsx:158', gap='⚠ radio 20px (D7)')]))
    return out


# ── 3 · Navegación y capas flotantes ────────────────────────────────────────
def navegacion():
    out = []
    out.append(A('n-nav', 'NavItem del rail', 'layout/Sidebar.tsx:59-86 · tema: ListItemButton T:344-353',
        [('D10', 'blancos del rail: reposo 0.65 frente a 0.7; hover 0.1; activo 0.18 frente a 0.15 de tableros.'),
         ('D23', 'hover pisa el activo: el ítem actual se apaga al pasar el cursor.'),
         ('D22', 'peso 500 de la etiqueta sin token.'),
         ('D2', 'foco: sin anillo; el gris de MUI oscurece el azul.'),
         ('D15', 'alto calculado ~40px frente a density.navItem 34.')],
        [S('reposo', '<div class="railp" style="padding:0"><div class="nav"><i class="ic"></i>Inicio</div></div>',
           'texto text.onRailMuted rgba(255,255,255,0.65) · ícono hereda · borde izquierdo 3px transparente · radio 8px · mx 12px · etiqueta 13.5px / 600'),
         S('hover', '<div class="railp" style="padding:0"><div class="nav is-hover"><i class="ic"></i>Inicio</div></div>',
           'fondo onRail.hover rgba(255,255,255,0.1) · texto #ffffff'),
         S('seleccionado', '<div class="railp" style="padding:0"><div class="nav is-sel"><i class="ic"></i>Inicio</div></div>',
           'fondo onRail.selected rgba(255,255,255,0.18) · borde izq. onRail.indicator rgba(255,255,255,0.9) 3px · texto #ffffff'),
         S('seleccionado + hover', '<div class="railp" style="padding:0"><div class="nav is-selhover"><i class="ic"></i>Inicio</div></div>',
           'el hover pisa el activo: fondo 0.1 en lugar de 0.18', gap='⚠ hover apaga el activo (D23)'),
         S('foco por teclado', '<div class="railp" style="padding:0"><div class="nav is-focus"><i class="ic"></i>Inicio</div></div>',
           'MUI overlay.focus rgba(0,0,0,0.12) L / rgba(74,144,226,0.12) D · sin anillo (outline: 0)', gap='⚠ sin valor → MUI (D2, D3)'),
         S('deshabilitado', '<div class="railp" style="padding:0"><div class="nav is-dis"><i class="ic"></i>Inicio</div></div>',
           'MUI opacity 0.38 · nunca se deshabilita en la app', gap='⚠ sin valor → MUI (D3)')]))

    out.append(A('n-board', 'Ítem de tablero del rail', 'layout/sidebar/BoardList.tsx:82-144 · PersonalFoldersSection.tsx:67-117',
        [('D10', 'azul de selección 0.15 frente a 0.18 de NavItem; indicador 0.85 frente a 0.9.'),
         ('D23', 'seleccionado + hover baja de 0.15 a 0.09.'),
         ('D9', 'variante compartida usa azules fuera de paleta (59,130,246) y (89,131,253).')],
        [S('reposo', '<div class="railp" style="padding:0"><div class="brd"><span class="dot" style="background:#29abe2"></span>Proyecto norte<span class="more">⋮</span></div></div>',
           'texto rgba(255,255,255,0.65) (D10) · icono 15px color de datos · radio 8px · pl 20px · etiqueta 12.5px / 500'),
         S('hover', '<div class="railp" style="padding:0"><div class="brd is-hover"><span class="dot" style="background:#29abe2"></span>Proyecto norte<span class="more">⋮</span></div></div>',
           'fondo rgba(255,255,255,0.09) · texto rgba(255,255,255,0.9) · botón «⋮» aparece (opacity 0→1)'),
         S('seleccionado', '<div class="railp" style="padding:0"><div class="brd is-sel"><span class="dot" style="background:#29abe2"></span>Proyecto norte<span class="more">⋮</span></div></div>',
           'fondo rgba(255,255,255,0.15) (≠ 0.18) · texto #fff 700 · borde izq. rgba(255,255,255,0.85) 3px (≠ 0.9)'),
         S('seleccionado + hover', '<div class="railp" style="padding:0"><div class="brd is-selhover"><span class="dot" style="background:#29abe2"></span>Proyecto norte<span class="more">⋮</span></div></div>',
           'el hover pisa al activo: fondo rgba(255,255,255,0.09)', gap='⚠ hover pisa activo (D23)'),
         S('arrastrando', '<div class="railp" style="padding:0"><div class="brd is-drag"><span class="dot" style="background:#29abe2"></span>Proyecto norte</div></div>',
           'origen opacity 0.4 (+ transform dnd-kit) · overlay opacity 0.92, fondo rgba(20,40,70,0.95) (BoardList.tsx:634)', gap='overlay sin valor en tokens (D10)'),
         S('deshabilitado', '<div class="railp" style="padding:0"><div class="brd is-dis"><span class="dot" style="background:#29abe2"></span>Proyecto norte</div></div>',
           'MUI opacity 0.38', gap='⚠ sin valor → MUI (D3)')]))

    out.append(A('n-folder', 'Ítem de carpeta del rail', 'layout/sidebar/BoardList.tsx:182-238 · PersonalFoldersSection.tsx:136-207',
        [('D10', 'texto del ítem 0.7; ícono de carpeta 0.5 en lugar de token.'),
         ('D9', 'destino de drop: rgba(59,130,246,0.25) y borde dashed fuera de paleta.'),
         ('D2', 'carpeta de workspace no enfocable por teclado.')],
        [S('reposo', '<div class="railp" style="padding:0"><div class="fol">▸ 📁 Clientes</div></div>',
           'texto rgba(255,255,255,0.7) · nombre 13px / 700 · borde 1px transparente · radio 8px · px 8px py 4px'),
         S('hover', '<div class="railp" style="padding:0"><div class="fol is-hover">▸ 📁 Clientes</div></div>',
           'fondo rgba(255,255,255,0.08) · texto #ffffff · botón «⋮» aparece'),
         S('destino de drop', '<div class="railp" style="padding:0"><div class="fol is-drop">▸ 📁 Clientes</div></div>',
           'fondo rgba(59,130,246,0.25) (hover 0.3) · borde 1px dashed rgba(89,131,253,0.7)', gap='⚠ azules fuera de paleta (D9, D10)'),
         S('arrastrando', '<div class="railp" style="padding:0"><div class="fol is-drag">▸ 📁 Clientes</div></div>',
           'opacity 0.5 (wrapper personal) · overlay width 220, opacity 0.9, fondo rgba(40,50,70,0.95) (PersonalFoldersSection.tsx:504-508)', gap='overlay sin valor en tokens (D10)')]))

    out.append(A('n-ws', 'Selector de espacio, búsqueda del rail y botones «…» y «+»', 'layout/Sidebar.tsx:500-598 · layout/sidebar/WorkspaceAvatar.tsx:12-26 · BoardSearch.tsx:63-118',
        [('D20', 'botón «+»: #1976d2 / rgba(25,118,210,0.9) no se porta; debe ser brand.default / brand.hover.'),
         ('D9', 'avatar del espacio de trabajo: #2979c4 fuera de paleta como fallback.'),
         ('D10', 'selector 0.1 / 0.18 frente a búsqueda 0.08 / 0.15: escalera sin consolidar.'),
         ('D13', 'hover del «+» sin decidir: no es brand.hover.')],
        [S('fila del espacio · reposo', '<div class="railp" style="padding:0"><div class="wsr"><span class="av">A</span><span class="nm">Industrias CTS<span class="sub">Espacio principal</span></span><span class="sep"></span><span class="mini">＋</span></div></div>',
           'fondo rgba(255,255,255,0.1) · borde 1px rgba(255,255,255,0.18) · radio 10px · alto 42px · avatar 26px radio 7px, borde 2px rgba(255,255,255,0.28)'),
         S('botón «…» · reposo / hover', '<div class="railp" style="padding:8px;display:flex;gap:10px;align-items:center"><span class="rail-ib">⋯</span><span class="rail-ib is-hover">⋯</span></div>',
           'reposo rgba(255,255,255,0.55), 24×24 radio 6px · hover fondo rgba(255,255,255,0.12) y texto #fff'),
         S('botón «+» · reposo', '<div class="railp" style="padding:8px"><span class="plus-bad">+</span></div>',
           'rgba(25,118,210,0.9) (azul MUI, no CTS)', gap='⚠ no se porta (D20)'),
         S('búsqueda · reposo', '<div class="railp" style="padding:8px 0"><div class="rsearch">⌕ Buscar tableros…</div></div>',
           'fondo rgba(255,255,255,0.08) · borde 1px rgba(255,255,255,0.15) · placeholder rgba(255,255,255,0.4) · radio 10px · alto 34px'),
         S('búsqueda · foco', '<div class="railp" style="padding:8px 0"><div class="rsearch is-focus">⌕ Buscar tableros…</div></div>',
           'fondo rgba(255,255,255,0.12) · borde rgba(255,255,255,0.35) · sin anillo (solo borde y fondo)'),
         S('resultado · hover', '<div class="railp" style="padding:4px 12px;border-radius:8px"><div style="background:rgba(255,255,255,.12);border-radius:8px;padding:6px 8px;font-weight:600;font-size:12.5px">Tablero de obra<div style="font-size:10px;opacity:.45">Clientes</div></div></div>',
           'fondo rgba(255,255,255,0.12) · título 12.5px / 600 #fff · contexto 10px rgba(255,255,255,0.45) · radio 8px')]))

    out.append(A('n-tab', 'Tab · MUI Tabs', 'sin override de tema · AdminPage.tsx:347-350',
        [('D2', 'foco invisible: outline 0, sin focusRipple.'),
         ('D3', 'hover, activo y deshabilitado sin valor.'),
         ('D4', 'texto deshabilitado sin definir.')],
        [S('reposo', '<div class="tabs" style="max-width:360px"><span class="tab">Usuarios</span><span class="tab">Roles</span></div>',
           'texto text.secondary #5a6a80 / #a6b4c8 · 14px / 600 · padding 12px 16px · minHeight 48px · textTransform none en el Tab concreto'),
         S('hover', '<div class="tabs" style="max-width:360px"><span class="tab">Usuarios</span><span class="tab">Roles</span></div>',
           'MUI Tab no define :hover: la pestaña no reacciona', gap='⚠ sin valor (D3)'),
         S('seleccionado', '<div class="tabs" style="max-width:360px"><span class="tab is-sel">Usuarios</span><span class="tab">Roles</span></div>',
           'texto brand.default #0065BB · indicador borders.accent 2px #0065BB · transición 300ms MUI'),
         S('foco por teclado', '<div class="tabs" style="max-width:360px"><span class="tab is-focus">Usuarios</span><span class="tab">Roles</span></div>',
           'MUI outline 0 y sin focusRipple: sin indicador', gap='⚠ foco invisible (D2)'),
         S('deshabilitado', '<div class="tabs" style="max-width:360px"><span class="tab is-dis">Usuarios</span></div>',
           'texto text.disabled MUI rgba(0,0,0,0.38) L / rgba(255,255,255,0.5) D', gap='⚠ sin valor → MUI (D4)')]))

    out.append(A('n-vtab', 'Pestaña de vista · ViewTabBar', 'features/board-view/components/ViewTabBar.tsx:63-141 · NombreDeLaPestana.tsx:17-26',
        [('D2', 'foco: anillo UA de dnd-kit (role=button tabIndex=0).'),
         ('D15', 'botón «⋮» con transición 0.15s frente a motion.micro 0.12s.'),
         ('D22', 'peso 500 de 13px sin token; 700 en la seleccionada.')],
        [S('reposo', '<div class="vtabs" style="max-width:360px"><span class="vtab">Listado</span></div>',
           'texto text.secondary #5a6a80 / #a6b4c8 · 13px / 500 · px 12px py 6px · borde inferior 2px transparente (mb -2px)'),
         S('hover', '<div class="vtabs" style="max-width:360px"><span class="vtab is-hover">Listado</span></div>',
           'fondo overlay.hover rgba(0,101,187,0.05) L / rgba(74,144,226,0.08) D · radio 4px 4px 0 0 (sin token; radii.chip 6 no coincide)'),
         S('seleccionada', '<div class="vtabs" style="max-width:360px"><span class="vtab is-sel">Listado</span></div>',
           'texto brand.default #0065BB 13px / 700 · borde inferior border.brand 2px #0065BB'),
         S('foco por teclado', '<div class="vtabs" style="max-width:360px"><span class="vtab is-focus">Listado</span></div>',
           'anillo UA del navegador · no es focus.ring', gap='⚠ anillo UA (D2)'),
         S('arrastrando', '<div class="vtabs" style="max-width:360px"><span class="vtab is-drag">Listado</span></div>',
           'opacity 0.5 · z-index 2 · cursor grabbing')]))

    out.append(A('n-list', 'ListItemButton', 'theme/ctsTheme.ts:344-353 (override) · MUI resto',
        [('D1', 'seleccionado: el tema define action.selected, pero el estado lo calcula MUI.'),
         ('D2', 'foco: sin anillo; overlay.focus gris sobre azul.'),
         ('D3', 'activo y deshabilitado sin valor.')],
        [S('reposo', '<div class="lib" style="max-width:260px">Proyectos</div>',
           'texto text.primary #1a2236 / #e8edf4 · radio 8px · margin 1px 8px · padding 7px 12px · transición all 0.15s'),
         S('hover', '<div class="lib is-hover" style="max-width:260px">Proyectos</div>',
           'fondo overlay.hover rgba(0,101,187,0.05) L / rgba(74,144,226,0.08) D'),
         S('seleccionado', '<div class="lib is-sel" style="max-width:260px">Proyectos</div>',
           'MUI: rgba(0,101,187,0.08) L / rgba(0,101,187,0.16) D (D1); el tema declara action.selected 0.1 / 0.16 sin uso',
           gap='⚠ MUI calcula, tema no se usa (D1)'),
         S('seleccionado + hover', '<div class="lib is-selhover" style="max-width:260px">Proyectos</div>',
           'MUI: rgba(0,101,187,0.12) L / rgba(0,101,187,0.24) D', gap='⚠ MUI calcula (D1)'),
         S('foco', '<div class="lib is-focus" style="max-width:260px">Proyectos</div>',
           'MUI overlay.focus rgba(0,0,0,0.12) L / rgba(74,144,226,0.12) D · sin anillo', gap='⚠ sin valor → MUI (D2, D3)'),
         S('deshabilitado', '<div class="lib is-dis" style="max-width:260px">Proyectos</div>',
           'MUI opacity 0.38, pointer-events none', gap='⚠ sin valor → MUI (D3)')]))

    out.append(A('n-menu', 'Menu (papel) y MenuItem, incluido destructivo', 'theme/ctsTheme.ts:375-398 · layout/Sidebar.tsx:955-958 · VTB:725',
        [('D1', 'seleccionado del MenuItem: MUI 0.08 / 0.16, no el overlay.selected del tema.'),
         ('D16', 'sombra del papel: shadow.menu frente a elevation 8 de MUI.'),
         ('D9', 'borde del menú rgba(74,144,226,0.1) frente a 0.12 de divider.'),
         ('D15', 'padding de cada llamada distinto del tema (10/8/6.8px).'),
         ('sin decisión', 'MenuItem destructivo: el hover no tiene tinte rojo (el rail sí lo tiene).')],
        [S('papel abierto', '<div class="paper"><div class="mi">Editar</div><div class="mi">Duplicar</div><div class="mdiv"></div><div class="mi danger">Eliminar</div></div>',
           ('fondo bg.raised #ffffff · borde 1px #dde3ec · shadow.menu 0 8px 24px rgba(0,101,187,0.15) · radio 10px · padding 8px 0',
            'fondo #253662 (D12) · borde rgba(74,144,226,0.1) · shadow 0 8px 24px rgba(0,0,0,0.5)'),
           gap=('', False)),
         S('item · reposo', '<div class="paper"><div class="mi">Editar</div></div>',
           'texto text.primary #1a2236 / #e8edf4 · 14px · radio 6px · margin 2px 6px · padding 7px 10px · transición background 0.15s'),
         S('item · hover', '<div class="paper"><div class="mi is-hover">Editar</div></div>',
           'fondo overlay.hover rgba(0,101,187,0.05) / rgba(74,144,226,0.08)'),
         S('item · seleccionado', '<div class="paper"><div class="mi is-sel">Editar</div></div>',
           'MUI: rgba(0,101,187,0.08) L / rgba(0,101,187,0.16) D (D1); + hover 0.12 / 0.24; + foco 0.2 / 0.28',
           gap='⚠ MUI calcula (D1)'),
         S('item · foco', '<div class="paper"><div class="mi is-focus">Editar</div></div>',
           'MUI overlay.focus · el primer ítem toma foco al abrir con teclado', gap='⚠ sin valor → MUI (D2, D3)'),
         S('item · destructivo', '<div class="paper"><div class="mi danger">Eliminar</div></div>',
           'texto e ícono feedback.error.default #e2445c / #ef4444 · hover overlay.hover AZUL (sin tinte rojo)',
           gap='⚠ hover sin tinte rojo (sin decisión)'),
         S('item · deshabilitado', '<div class="paper"><div class="mi is-dis">Exportar</div></div>',
           'opacity 0.38 MUI', gap='⚠ sin valor → MUI (D3)')]))

    out.append(A('n-tip', 'Tooltip · tema', 'theme/ctsTheme.ts:296-322 (variante de tema)',
        [('D19', 'hay 4 estilos de tooltip; este es uno de ellos.'),
         ('D12', 'fondo oscuro #1e2d42 no está en colors.ts.')],
        [S('abierto', '<span class="tip">Editar tablero</span>',
           ('fondo bg.inverse #1a2236 · texto #ffffff (MUI) · sin borde · sin sombra · radio 6px · padding 5px 10px · 12px / 500 · arrow true',
            'fondo #1e2d42 · texto #ffffff · radio 6px · padding 5px 10px · 12px / 500')),
         S('foco / hover / deshabilitado', '<span class="na">n/a</span>',
           'abre al enfocar el hijo (MUI); no tiene estados propios')]))

    out.append(A('n-tip-rich', 'Tooltip enriquecido · composición', 'features/shared-view/SharedViewPage.tsx:38-71 (única aparición)',
        [('D7', 'radio 15px (tokens dicen 12) y ancho 420px.'),
         ('D12', 'fondo oscuro #1a2333 es un tercer azul-negro.'),
         ('D14', 'borde izquierdo: #0065BB en claro, #89AEDC en oscuro.'),
         ('D19', 'variante a conservar en el sistema.')],
        [S('abierto', '<div class="rtip"><b>Vista compartida</b><br>Los cambios se aplican al guardar. Los filtros no se comparten.</div>',
           ('fondo #ffffff · texto #1a2333 · borde 1px #e0e7ef · borde izq. 3px #0065bb · sombra shadow.tooltipRich 0 6px 20px rgba(0,101,187,0.12) · radio 15px · px 14px py 10px · 13px / 400 · lh 1.55 · maxWidth 420',
            'fondo #1a2333 · texto #e4e9f1 · borde 1px #324158 · borde izq. 3px #89aedc · sombra 0 6px 20px rgba(0,0,0,0.45)'),
           gap=('', '⚠ sombra oscura sin valor en token (D19)'))]))

    out.append(A('n-dialog', 'Dialog · papel, título, contenido y acciones', 'theme/ctsTheme.ts:278-293 · MUI Dialog',
        [('D12', 'papel: bg.raised #253662 en oscuro; la superficie de elevación es #2d3c53.'),
         ('D15', 'títulos 16px (tema) / 15px (Delete) / 17px (GlobalConfirm); acciones con padding distinto.'),
         ('D22', 'título 700 sin token; MUI h6 es 600.'),
         ('sin decisión', 'backdrop: MUI rgba(0,0,0,0.5) en ambos modos; no hay overlay.scrim definido.')],
        [S('abierto', '<div class="dlg"><h4>Guardar cambios</h4><p>El tablero se actualiza para todo el equipo.</p><div class="acts"><button class="btn btn-txt">Cancelar</button><button class="btn btn-cp">Guardar</button></div></div>',
           ('fondo bg.raised #ffffff · radio 14px · shadow.dialog 0 24px 64px rgba(0,101,187,0.18) · título 16px / 700 · padding-bottom 8px',
            'fondo bg.raised #253662 · shadow 0 24px 64px rgba(0,0,0,0.7) · título 16px / 700')),
         S('backdrop', '<div class="scrim"><span class="na" style="color:#fff">velo MUI</span></div>',
           'rgba(0,0,0,0.5) MUI · Fade 225ms / 195ms · zIndex 1300', gap='⚠ sin valor → MUI (sin decisión)'),
         S('acciones · padding', '<div class="dlg" style="max-width:300px"><div class="acts" style="padding:8px"><button class="btn btn-txt">Cancelar</button></div></div>',
           'padding 8px (MUI) frente a 0 24px 16px de la mayoría de llamadas', gap='⚠ sin valor en tema (D15)')]))

    out.append(A('n-confirm', 'ConfirmDialog destructivo · composición', 'ui/ConfirmDialog.tsx:18-31 · ui/GlobalConfirmDialog.tsx:35 · layout/sidebar/DeleteDialog.tsx',
        [('D6', 'foco del botón destructivo: sombra accidental de shadows[6].'),
         ('D7', 'GlobalConfirmDialog con radio 30px (dialogFeature), no 14px.'),
         ('D15', 'títulos y acciones distintos según el diálogo.'),
         ('D21', 'hover del botón rojo: error.dark calculado por MUI.'),
         ('D3', 'botón deshabilitado sin valor.')],
        [S('diálogo', '<div class="dlg big" style="max-width:340px"><h4>Eliminar tablero</h4><p>Esta acción no se puede deshacer. Se borran sus filas.</p><div class="acts big"><button class="btn btn-txt">Cancelar</button><button class="btn btn-err">Eliminar</button></div></div>',
           ('fondo bg.raised #ffffff · radio 30px (dialogFeature) · shadow.dialog · título 17px / 700 · cuerpo 14px text.secondary · acciones px 24px pb 20px (GlobalConfirmDialog.tsx:35-41)',
            'fondo #253662 · mismo radio · shadow 0 24px 64px rgba(0,0,0,0.7)'),
           gap=('⚠ radio 30px frente a 14px del tema (D7)', False)),
         S('confirmar · reposo', '<button class="btn btn-err">Eliminar</button>',
           'fondo feedback.error.default #e2445c / #ef4444 · texto #fff · variant contained · sombra shadow.e2'),
         S('confirmar · hover', '<button class="btn btn-err is-hover">Eliminar</button>',
           'fondo derivado MUI rgb(158,47,64) L / rgb(167,47,47) D · sombra shadow.e4', gap='⚠ derivado MUI (D21)'),
         S('cancelar · reposo', '<button class="btn btn-txt">Cancelar</button>',
           'texto brand.default #0065BB (color primary por defecto); otras variantes usan inherit u outlined (D15)'),
         S('confirmar · deshabilitado', '<button class="btn btn-err is-disabled">Eliminar</button>',
           'overlay.disabledBg / overlay.disabled MUI · en modo «escribe el nombre» se deshabilita hasta coincidir',
           gap='⚠ sin valor → MUI (D3)')]))

    out.append(A('n-drawer', 'Drawer · panel temporal y rail permanente', 'theme/ctsTheme.ts:205-211 (solo oscuro) · features/board-view/components/TrashPanel.tsx:207',
        [('D16', 'elevación del panel: elevation 16 de MUI, no un shadow.* del sistema.'),
         ('D15', 'anchos 440 / 460 / 720 en uso frente a layout.panelMin/Max 300 / 360.'),
         ('D18', 'scrollbar global se pinta sobre el rail azul.')],
        [S('panel temporal', '<div class="drw"><header>Papelera<span class="chipc">3</span></header><div style="padding:16px 20px;font-size:13px;color:var(--muted)">Elementos borrados hace menos de 30 días.</div></div>',
           ('fondo bg.raised #ffffff (MUI, la regla oscura no aplica) · sombra elevation 16: 0 16px 40px rgba(0,0,0,0.16) · radio 0 · Slide 225ms',
            'fondo bg.raised #253662 · sombra 0 16px 40px rgba(0,0,0,0.65)')),
         S('cabecera', '<div class="drw"><header>Historial<span class="chipc">12</span></header></div>',
           'px 20px py 16px (TrashPanel.tsx:211) · borde inferior 1px border.subtle · título 16px / 600 · chip 11px / 700 (:219)'),
         S('rail permanente', '<div class="railp" style="width:200px;padding:12px 0"><div class="nav is-sel"><i class="ic"></i>Tableros</div></div>',
           'fondo bg.rail #0065BB L / #253662 D · shadow.sidebar 4px 0 20px rgba(0,0,0,0.2) · ancho 256px · motion.collapse 0.25s'),
         S('backdrop', '<div class="scrim"><span class="na" style="color:#fff">velo MUI</span></div>',
           'rgba(0,0,0,0.5) MUI', gap='⚠ sin valor → MUI (sin decisión)')]))

    out.append(A('n-crumb', 'Migas de pan', 'features/board-view/components/BoardBreadcrumb.tsx:12-45',
        [('D2', 'foco: outline auto del navegador, no focus.ring.'),
         ('D22', 'peso 500 sin token.'),
         ('D15', 'margen inferior 8px frente a 12px y 16px en otras páginas.')],
        [S('enlace · reposo', '<div class="crumb"><a class="lnk" href="#n-crumb">Proyectos</a><span class="sep">/</span><span class="cur">Norte</span></div>',
           'texto text.secondary #5a6a80 / #a6b4c8 · 13px / 500 · separador margen 0 8px · mb 8px'),
         S('enlace · hover', '<div class="crumb"><a class="lnk is-hover" href="#n-crumb">Proyectos</a><span class="sep">/</span><span class="cur">Norte</span></div>',
           'color sin cambio · text-decoration underline (único cambio)'),
         S('enlace · foco', '<div class="crumb"><a class="lnk is-focus" href="#n-crumb">Proyectos</a></div>',
           'outline auto del navegador (único elemento con anillo nativo)', gap='⚠ outline UA (D2)'),
         S('actual (último)', '<div class="crumb"><span class="cur">Norte</span></div>',
           'text.primary #1a2236 / #e8edf4 · 700 · no interactivo')]))

    out.append(A('n-vtbar', 'Barra de vistas · composición', 'features/board-view/components/ViewTabBar.tsx',
        [('D2', 'foco de pestañas: anillo UA.'),
         ('D15', 'alto de botones auxiliares frente a density.toolbarControl 32.'),
         ('D20', 'botón de fondo de la barra de herramientas: primary.50 no existe.')],
        [S('barra', '<div class="vtbar-wrap"><div class="vtabs"><span class="vtab is-sel">Vista principal</span><span class="vtab">Listado</span><span class="vtab is-hover">Calendario</span><button class="ib">＋</button><button class="ib">⌄</button></div></div>',
           'franja borde inferior 2px border.subtle · pestaña seleccionada borde 2px brand · «⋮» opacity 0.6 si la pestaña está activa, 0 si no (ViewTabBar.tsx:73) · botones auxiliares IconButton')]))

    out.append(A('n-spick', 'Selector de estado · composición (popover)', 'features/board-view/components/cells/StatusCell.tsx:261-398, 315-329, 425-550',
        [('D7', 'radio 20px del contenedor y 15px de las opciones frente a radii.base 10.'),
         ('D8', 'texto blanco sobre #fdab3d 1.90:1 y sobre #00c875 2.21:1.'),
         ('D16', 'sombra: la tabla dice shadow.menu y la sección de popover dice shadow.e6.'),
         ('D9', 'sin color: #c4c4c4 (neutralStatus) sin variante oscura.')],
        [S('abierto', '<div class="spick"><div class="srch"><span class="ph">⌕ Buscar estado…</span></div>'
           '<div class="sopt" style="--c:#00c875">Hecho<span>✓</span></div>'
           '<div class="sopt is-sel" style="--c:#fdab3d">En proceso</div>'
           '<div class="sopt" style="--c:#e2445c">Atascado</div>'
           '<span class="sclr">Limpiar selección</span><span class="sadd">+ Agregar etiqueta</span></div>',
           ('contenedor bg.surface #ffffff · radio 20px (borderRadius 2) · sombra shadow.e6 0 16px 40px rgba(0,0,0,0.16) · 280px',
            'contenedor bg.surface #253662 · sombra shadow.e6 0.65 · 280px'),
           gap=('⚠ radio 20px frente a 10px (D7)', '⚠ radio 20px (D7)')),
         S('opción · reposo', '<div class="spick" style="width:200px"><div class="sopt" style="--c:#00c875">Hecho</div></div>',
           'fondo color de dato swatch.status · texto #ffffff 13px / 600 · radio 15px · padding 6.8px 12px · transición filter 0.15s, transform 0.1s'),
         S('opción · hover', '<div class="spick" style="width:200px"><div class="sopt is-hover" style="--c:#00c875">Hecho</div></div>',
           'filter brightness(0.88) (no usa overlay.hover) · FormPublicPage usa 0.9'),
         S('opción · seleccionada', '<div class="spick" style="width:200px"><div class="sopt is-sel" style="--c:#579bfc">Revisión</div></div>',
           'doble anillo: outline 2px bg.surface #ffffff / #253662 + 0 0 0 2px del color de la opción'),
         S('opción · sobre amarillo', '<div class="spick" style="width:200px"><div class="sopt" style="--c:#fdab3d">En proceso</div></div>',
           'blanco sobre #fdab3d = 1.90:1 (no pasa AA)', gap='⚠ contraste (D8)'),
         S('opción · sin color', '<div class="spick" style="width:200px"><div class="sopt" style="--c:#c4c4c4">Sin iniciar</div></div>',
           'neutralStatus #c4c4c4 · blanco 1.74:1 · sin variante oscura', gap='⚠ contraste y sin variante oscura (D8, D9)'),
         S('opción · deshabilitada', '<div class="spick" style="width:200px"><div class="sopt is-dis" style="--c:#a25ddc">Archivado</div></div>',
           'opacity 0.45 + line-through (en edición) · el picker la filtra (!o.disabled)', gap='⚠ 0.45 frente a 0.38 MUI (D3)')]))
    return out


# ── 4 · Datos y retroalimentación ───────────────────────────────────────────
def datos():
    out = []
    out.append(A('d-chip', 'Chip · por defecto', 'theme/ctsTheme.ts:326-332 · defaults MUI · ~151 usos con sx local',
        [('D1', 'hover clicable y foco: MUI calcula sobre primary, no sobre overlay.selected.'),
         ('D16', 'chip pulsado: shadow.e1 sin rol definido.'),
         ('D2', 'foco sin anillo (outline 0).'),
         ('D4', 'deshabilitado: opacity 0.38 de MUI.')],
        [S('reposo', '<span class="chip">Activo</span>',
           ('fondo overlay.selected rgba(0,101,187,0.1) · texto text.primary #1a2236 · altura 24px · radio 6px · 12px / 600 · padding 0 8px',
            'fondo overlay.selected rgba(74,144,226,0.16) · texto #e8edf4')),
         S('clicable · hover', '<span class="chip is-hover">Activo</span>',
           ('MUI rgba(0,101,187,0.12) L', 'MUI rgba(74,144,226,0.24) D'), gap='⚠ sin valor → MUI (D1)'),
         S('activo (pulsado)', '<span class="chip is-pressed">Activo</span>',
           'sombra shadow.e1 0 1px 4px rgba(0,0,0,0.06) L / rgba(0,0,0,0.4) D', gap='⚠ sombra sin rol (D16)'),
         S('seleccionado', '<span class="chip is-sel">Activo</span>',
           'se simula con variant filled + color primary: fondo brand.default #0065BB · texto text.onBrand'),
         S('foco por teclado', '<span class="chip is-focus">Activo</span>',
           'MUI rgba(0,101,187,0.2) L / rgba(74,144,226,0.28) D · sin anillo', gap='⚠ sin valor → MUI (D2)'),
         S('deshabilitado', '<span class="chip dis">Activo</span>',
           'opacity 0.38 MUI · pointer-events none (único uso ManagedColumnsPage.tsx:752)', gap='⚠ sin valor → MUI (D4)')]))

    out.append(A('d-chip-color', 'Chip · color (filled)', 'theme/ctsTheme.ts:325-332 · MUI color=* · tokens feedback',
        [('D8', 'texto blanco forzado sobre warning, success e info (contraste 1.90 y 2.21).'),
         ('D21', 'onColor: MUI calcula rgba(0,0,0,0.87) en aviso, éxito e info.'),
         ('D13', 'hover de color: dark de MUI, no hay literal.')],
        [S('primary', '<span class="chip prim">Primario</span>',
           'fondo brand.default #0065BB · texto #ffffff (MUI primary.contrastText)'),
         S('info', '<span class="chip info">Info</span>',
           ('fondo feedback.info.default #29ABE2 · texto MUI rgba(0,0,0,0.87)', 'fondo #06b6d4 · texto MUI rgba(0,0,0,0.87)'),
           gap='⚠ onColor de MUI (D21)'),
         S('warning', '<span class="chip warn">Aviso</span>',
           ('fondo #fdab3d · texto MUI rgba(0,0,0,0.87) (la app fuerza #fff, D8)', 'fondo #f59e0b · texto MUI rgba(0,0,0,0.87)'),
           gap='⚠ onColor sin decidir (D8, D21)'),
         S('success', '<span class="chip ok">Listo</span>',
           ('fondo #00c875 · texto MUI rgba(0,0,0,0.87)', 'fondo #22c55e · texto MUI rgba(0,0,0,0.87)'),
           gap='⚠ onColor sin decidir (D21)'),
         S('error', '<span class="chip err">Error</span>',
           ('fondo #e2445c · texto #fff (MUI error.contrastText)', 'fondo #ef4444 · texto #fff'),
           gap='⚠ onColor de MUI (D21)')]))

    out.append(A('d-chip-count', 'Chip · contador', 'ViewToolbar.tsx:135-175 · TrashPanel.tsx:218 · AdminPage.tsx:326 · ItemCommentsDrawer.tsx:188',
        [('D8', 'contador «Ocultar» en amarillo con texto blanco: 1.90:1.'),
         ('D11', 'tinte del grupo: tint(c,\'20\') frente a tint(c,\'18\') + opacity 0.7.'),
         ('D15', 'alturas 18 / 20 / 22 sin token; 10px y 11px según el sitio.'),
         ('D22', 'peso 700 sin token en contadores.')],
        [S('genérico', '<span class="chip h20" style="background:var(--overlay-selected)">3</span>',
           'fondo overlay.selected rgba(0,101,187,0.1) / rgba(74,144,226,0.16) (D1) · altura 20px · 11px / 700'),
         S('toolbar · primario', '<span class="chip h18 prim">2</span>',
           'fondo brand.default #0065BB · texto text.onBrand #ffffff · altura 18px · 10px, peso MUI 600 (ViewToolbar.tsx:135-175, sin fontWeight)'),
         S('toolbar · ocultar', '<span class="chip h18 warn white">4</span>',
           'fondo feedback.warning.default #fdab3d / #f59e0b · texto #ffffff (1.90:1); MUI daría rgba(0,0,0,0.87)', gap='⚠ contraste (D8)'),
         S('grupo · tintado', '<span class="chip h20" style="background:#579bfc33;color:#579bfc">5</span>',
           'tint(c,\'20\') ≈ 12.5% sobre el color del grupo · texto en el color pleno · 11px / 700'),
         S('etiqueta Tuyo / Compartido', '<span class="chip h16" style="height:16px;background:var(--brand);color:#fff;font-size:9px;font-weight:700;letter-spacing:.04em">TUYO</span>',
           'propio brand.default #0065BB · compartido overlay.selected · texto #ffffff / text.secondary · 9px / 700 · altura 16 (sin token)', gap='⚠ altura 16 sin token (D15)')]))

    out.append(A('d-chip-outlined', 'Chip · outlined y dashed', 'MUI defaults · SharedViewsPanel.tsx:179 · TrashPanel.tsx:349-355 · historial/piezas.tsx:680',
        [('D9', 'borde outlined por defecto es gris de MUI, no el divisor azulado.'),
         ('D11', 'borde de color: alpha(main, 0.7) de MUI.'),
         ('D21', 'borde de MUI sin valor en el tema.'),
         ('D4', 'texto de «eliminado» en text.disabled sin definir.')],
        [S('default · reposo', '<span class="chip outl">Borrador</span>',
           ('borde 1px #bdbdbd (MUI, sin valor) · texto text.primary · fondo transparente', 'borde 1px #616161 (MUI, sin valor) · texto #e8edf4'),
           gap='⚠ borde gris de MUI (D9, D21)'),
         S('default · hover', '<span class="chip outl is-hover" style="background:var(--overlay-hover)">Borrador</span>',
           'fondo overlay.hover rgba(0,101,187,0.05) / rgba(74,144,226,0.08) · clickable'),
         S('color error · reposo', '<span class="chip outl err">Rechazado</span>',
           'texto feedback.error.default · borde alpha(main, 0.7) de MUI: rgba(226,68,92,0.7) L / rgba(239,68,68,0.7) D',
           gap='⚠ borde de MUI (D21)'),
         S('eliminado (dashed)', '<span class="chip outl eli">Eliminado</span>',
           'borde 1px dashed #dde3ec L / rgba(74,144,226,0.12) D · texto text.disabled MUI rgba(0,0,0,0.38) / rgba(255,255,255,0.5)',
           gap='⚠ texto disabled sin valor (D4)')]))

    out.append(A('d-chip-cell', 'Chip · de celda', 'LabelCell.tsx:49-52 · DropdownCell.tsx:160-176 · FileCell.tsx:128-143 · ConnectCell.tsx:112-142',
        [('D1', 'seleccionado de la celda: solo ConnectCell usa primary filled.'),
         ('D4', 'icono de borrar en text.disabled.'),
         ('D11', 'tinte primario: 0.08 / 0.09 / 0.07 / 0.1 según archivo.'),
         ('D14', 'texto de marca en oscuro: #89AEDC.')],
        [S('«+N» · reposo', '<span class="chip h22 brandsub">+3</span>',
           ('fondo brand.subtle rgba(0,101,187,0.09) · texto text.brand #0065BB · altura 22px · 10.5px / 700',
            'fondo rgba(41,171,226,0.15) · texto text.brand #89AEDC')),
         S('Label / Dropdown · reposo', '<span class="chip h22">Urgente</span>',
           'fondo overlay.selected (sin color por opción) · texto text.primary · altura 22px (sin token) · 11px / 600'),
         S('seleccionado (Connect)', '<span class="chip h22 is-sel">Cliente A</span>',
           'fondo brand.default #0065BB · texto text.onBrand · solo ConnectCell.tsx:137-142'),
         S('solo lectura', '<span class="chip h22 lock">Cerrado</span>',
           'opacity 0.7 del wrapper (CellRenderer.tsx:292-295) · candado 12px · cursor default'),
         S('icono de borrar · hover', '<span class="chip h22">Urgente <span class="del" style="color:#e2445c">✕</span></span>',
           'icono text.disabled → hover feedback.error.default #e2445c / #ef4444 · 12px (ConnectCell.tsx:110, FileCell.tsx:136)',
           gap='⚠ text.disabled sin valor (D4)')]))

    out.append(A('d-spill', 'StatusPill · celda de estado', 'features/board-view/components/cells/StatusCell.tsx:25-31, 76-85, 211-255 · PublicCell.tsx:345-383',
        [('D8', 'blanco sobre swatch: #fdab3d 1.90:1, #c4c4c4 1.74:1, #00c875 2.21:1.'),
         ('D9', 'colores de dato sin adaptación al oscuro; reservados fuera de palette.'),
         ('D2', 'no enfocable, sin anillo.')],
        [S('con valor · reposo', '<span class="spill" style="--c:#00c875">En curso</span>',
           'fondo swatch.status (dato) #00c875 · texto swatch.status.onColor #ffffff · 11px / 600 · sin radio · altura 100% de la celda'),
         S('con valor · hover', '<span class="spill is-hover" style="--c:#579bfc">Revisión</span>',
           'filter brightness(0.88) (FormPublicPage usa 0.9)'),
         S('reservado · aprobado', '<span class="spill" style="--c:#00c875">Aprobado por cliente</span>',
           '#00c875 hard-coded en 2 archivos · en oscuro no usa #22c55e', gap='⚠ hard-coded (D8, D9)'),
         S('reservado · rechazado', '<span class="spill" style="--c:#e2445c">Rechazado por cliente</span>',
           '#e2445c hard-coded · en oscuro no usa #ef4444', gap='⚠ hard-coded (D9)'),
         S('vacío', '<span class="spill vac">Sin estado</span>',
           'fondo transparente · texto text.secondary #5a6a80 / #a6b4c8 · borde punteado de la demo'),
         S('vacío · hover', '<span class="spill vac is-hover">Sin estado</span>',
           'fondo overlay.hover rgba(0,101,187,0.05) / rgba(74,144,226,0.08)'),
         S('sin color', '<span class="spill" style="--c:#c4c4c4">Sin color</span>',
           'neutralStatus #c4c4c4 · blanco 1.74:1', gap='⚠ contraste (D8, D9)')]))

    out.append(A('d-badge', 'Badge, punto y contador', 'features/home/HomePage.tsx:141-203 · NotificationBell.tsx:182,267-302 · BoardGridV2.tsx:294',
        [('D20', 'pulso «NUEVO» en rgba(211,47,47,α): rojo de MUI, no feedback.error.'),
         ('D8', 'beta en amarillo con texto blanco: 1.90:1.'),
         ('D9', 'contador de la grilla fijo en #e2445c, sin variante oscura.'),
         ('D11', 'fondo de «no leído»: en oscuro se usa la base del claro.'),
         ('D22', '10px / 800 y 10.5px / 700 sin token.')],
        [S('NUEVO · reposo', '<span class="nuevo">NUEVO</span>',
           'fondo feedback.error.default #e2445c / #ef4444 · texto #ffffff · 10px / 800 · radio 99px · letter-spacing 0.4px · padding 0.8px 7.2px',
           gap=False),
         S('NUEVO · pulso', '<span class="nuevo pulse">NUEVO</span>',
           'freshPulse 2s ease-in-out infinite · 0% 0 0 0 0 rgba(211,47,47,0.45) → 50% 0 0 0 5px rgba(211,47,47,0) (HomePage.tsx:168-169)',
           gap='⚠ rojo de MUI (D20)'),
         S('beta', '<span class="beta">beta</span>',
           'fondo feedback.warning.default #fdab3d / #f59e0b · texto #ffffff (1.90:1) · 10.5px / 700 uppercase · radio 10px (ViewTabBar.tsx:544-549)',
           gap='⚠ contraste (D8)'),
         S('conteo (MUI)', '<span class="cnt">3</span>',
           'fondo #e2445c fijo · texto #ffffff · 14×14 · 8px / 700 · radio 50% (contador no leído de la grilla)',
           gap='⚠ fijo sin modo oscuro (D9)'),
         S('punto de marca', '<span class="dot8"></span>',
           'brand.default #0065BB · 8×8px · radio 50% (NotificationBell.tsx:296-302)'),
         S('fila no leída', '<div class="unread">Se compartió el tablero Norte</div>',
           ('fondo bg.unread rgba(0,101,187,0.04) · texto peso 600 (leído 400) · hover overlay.hover',
            'fondo rgba(0,101,187,0.08) (base del claro, D11) · texto peso 600'),
           gap=('', '⚠ base del claro (D11)'))]))

    out.append(A('d-table', 'Tabla · cabecera, celda, fila y contenedor', 'theme/ctsTheme.ts:213-275 · ItemRow.tsx:252-357 · ui/UsersTable.tsx:113-119',
        [('D12', 'cabecera y filas oscuras: #2d3c53 frente a #253662 del fondo.'),
         ('D1', 'fila seleccionada: MUI rgba(0,101,187,0.08) / 0.16.'),
         ('D9', 'borde de celda 0.1 frente a 0.12 del divisor.'),
         ('D15', 'letterSpacing del token 0.06em; el real es 0.01em.'),
         ('D23', 'hover legacy #e8eef5 / #344463 en tablas antiguas.')],
        [S('cabecera', '<table class="tbl" style="width:100%"><tr><th>Nombre</th><th>Estado</th></tr></table>',
           ('fondo bg.tableHead #0065BB · texto #ffffff · 11px / 600 · padding 9px 12px · sin mayúsculas · separador rgba(255,255,255,0.12)',
            'fondo #2d3c53 · texto #ffffff · separador rgba(74,144,226,0.12)'),
           gap=('', False)),
         S('celda · reposo', '<table class="tbl" style="width:100%"><tr><td>Celda de dato</td><td>Activo</td></tr></table>',
           ('texto text.primary · 13px · alto 38px (T:239-240) · borde derecho e inferior 1px #dde3ec',
            'texto #e8edf4 · borde rgba(74,144,226,0.1) (D9)'),
           gap=('', '⚠ 0.1 frente a 0.12 (D9)')),
         S('fila · hover', '<table class="tbl" style="width:100%"><tr class="is-hover"><td>Celda de dato</td><td>Activo</td></tr></table>',
           ('fondo bg.rowHover #f7fafd (sólido, por las celdas sticky)', 'fondo bg.rowHover #2f435e (D12)')),
         S('fila · seleccionada', '<table class="tbl" style="width:100%"><tr class="is-sel"><td>Celda de dato</td><td>Activo</td></tr></table>',
           'MUI rgba(0,101,187,0.08) L / rgba(0,101,187,0.16) D (D1) · hover 0.12 / 0.24', gap='⚠ MUI calcula (D1)'),
         S('fila · inactiva', '<table class="tbl" style="width:100%"><tr class="is-inact"><td>Celda de dato</td><td>Inactivo</td></tr></table>',
           'opacity 0.55 (UsersTable.tsx:117)'),
         S('celda · solo lectura', '<table class="tbl" style="width:100%"><tr><td class="ro">Calculado</td><td>Activo</td></tr></table>',
           ('fondo bg.readOnly rgba(15,23,42,0.035)', 'fondo rgba(255,255,255,0.045) (dark: ninguno en ItemRow.tsx:496)'),
           gap=('', '⚠ solo grilla tiene oscuro (D12)')),
         S('destino de arrastre', '<table class="tbl" style="width:100%"><tr class="is-drop"><td>Soltar aquí</td><td>Activo</td></tr></table>',
           'línea borders.indicator 3px #0065BB arriba y abajo · centro outline 2px offset -2px · fondo rgba(0,101,187,0.08)')]))

    out.append(A('d-grid', 'Grilla virtualizada · composición', 'features/board-view/components/BoardGridV2.tsx (fila :193-204 · banda :340-352 · cabecera :1346 · valores de texto :235, :378-388)',
        [('D12', 'cabecera y banda: #2d3c53 aparece 18 veces en src frente a #253662 del tema.'),
         ('D2', 'fila y celda sin hover ni foco: brecha de accesibilidad.'),
         ('D4', 'celda de solo lectura: candado en text.disabled sin definir.'),
         ('D11', 'conteo de la banda: tint(c,\'20\') 11px / 700.'),
         ('D9', 'CONNECT con borde #7c5cfc fuera de toda paleta.')],
        [S('cabecera · reposo', '<div class="grid"><div class="gh" style="width:100%">Tarea</div></div>',
           ('fondo bg.groupHeader #f0f4f9 · texto text.secondary #5a6a80 · 13px / 700 · alto 40px · borde derecho border.subtle · sombra 0 1px 3px rgba(0,0,0,0.07) (BoardGridV2.tsx:1399; fuera de tokens.ts)',
            'fondo #2d3c53 · texto #a6b4c8 · sombra 0 1px 3px rgba(0,0,0,0.07) (sin valor oscuro en ATOMOS)'),
           gap=('', '⚠ sombra oscura sin valor (D12)')),
         S('fila · reposo', '<div class="grid"><div class="gr">Revisar planos</div></div>',
           'fondo bg.surface #ffffff / #2d3c53 · texto text.secondary · nombre 14px / 600 (BoardGridV2.tsx:235) · alto 40px (density.gridRow)'),
         S('fila · seleccionada', '<div class="grid"><div class="gr is-sel">Revisar planos</div></div>',
           'fondo bg.selected #eff5fe / #2f476d (sólido; aplica a columna sticky)'),
         S('fila · hover', '<div class="grid"><div class="gr">Revisar planos</div></div>',
           'MUI: sin hover (los div no tienen :hover; la tabla MUI sí)', gap='⚠ sin valor (D2)'),
         S('celda · solo lectura', '<div class="grid"><div class="gr ro">Total <span style="margin-left:auto;opacity:.6">🔒</span></div></div>',
           'fondo bg.readOnly rgba(15,23,42,0.035) / rgba(255,255,255,0.045) · wrapper opacity 0.7 · candado 12px (cells/CellRenderer.tsx:292-295)'),
         S('banda de grupo', '<div class="grid"><div class="gband" style="--c:#0065bb"><span>Obra norte</span><span class="cnt2" style="--gt:rgba(0,101,187,.125)">4</span></div></div>',
           'fondo bg.groupHeader · rail borders.groupRail 4px del color de grupo · texto del grupo 14px / 700 · alto 44px · conteo tint(c,\'20\')'),
         S('fila resumen', '<div class="grid"><div class="gr resumen">Suma 1 240</div></div>',
           'fondo bg.surface · borde inferior 2px border.subtle · alto 36px (density.groupSummary)'),
         S('vacío', '<div class="grid"><div class="vacio">Aún no hay grupos</div></div>',
           'texto text.disabled (D4) · borde 2px dashed border.subtle · radio 30px (borderRadius 3, D7) · EmptyGroupState.tsx:12-19',
           gap='⚠ text.disabled sin valor (D4)')]))

    out.append(A('d-alert', 'Alert · standard (por severidad)', 'theme/ctsTheme.ts:337-341 (solo radio 8 y peso 500) · colores de MUI',
        [('D17', 'no existen feedback.*.subtle: el fondo es MUI y en oscuro sale casi negro.'),
         ('D21', 'texto y fondo sin valor en el tema: se ven los de MUI.'),
         ('D8', 'ícono de cada severidad: ver tabla de roles.'),
         ('D22', 'peso 500 del alert (los toasts usan 600).')],
        [S('error', '<div class="alert err"><span class="ico">⛔</span><span>No se pudo guardar el tablero.</span></div>',
           ('fondo MUI #FCF0F1 · texto MUI #5C2A31 · ícono feedback.error.default #e2445c · radio 8px · peso 500',
            'fondo MUI #180A0A · texto MUI #F9C3C3 · ícono #ef4444'),
           gap='⚠ fondo y texto de MUI (D17, D21)'),
         S('aviso', '<div class="alert warn"><span class="ico">⚠</span><span>Quedan 2 días para vencer.</span></div>',
           ('fondo MUI #FEF8EF · texto MUI #654A27 · ícono #fdab3d', 'fondo MUI #181105 · texto MUI #FBDFB0 · ícono #f59e0b'),
           gap='⚠ fondo y texto de MUI (D17)'),
         S('éxito', '<div class="alert ok"><span class="ico">✓</span><span>Tablero guardado.</span></div>',
           ('fondo MUI #EAFAF3 · texto MUI #145439 · ícono #00c875', 'fondo MUI #07140C · texto MUI #B8ECCB · ícono #22c55e'),
           gap='⚠ fondo y texto de MUI (D17)'),
         S('info', '<div class="alert info"><span class="ico">ℹ</span><span>Hay cambios sin guardar.</span></div>',
           ('fondo MUI #EDF8FC · texto MUI #214A5C · ícono #29ABE2', 'fondo MUI #051315 · texto MUI #AFE7F1 · ícono #06b6d4'),
           gap='⚠ fondo y texto de MUI (D17)'),
         S('outlined', '<div class="alert warn" style="background:transparent;border:1px solid #FDBB63"><span class="ico">⚠</span><span>Carga incompleta</span></div>',
           'borde MUI palette.light #FDBB63 (AvisoCargaIncompleta.tsx:32,84) · solo ese archivo', gap='⚠ borde de MUI (D21)')]))

    out.append(A('d-snack', 'Alert · relleno y Snackbar', 'ui/GlobalSnackbar.tsx:18-52 · ui/UpdateAvailableBanner.tsx:36-72 · SharedViewPage.tsx:819-833',
        [('D8', 'texto #1a2236 sobre error: 3.93:1; blanco sobre info oscuro (#06b6d4): 2.43:1.'),
         ('D21', 'relleno: MUI palette.dark en oscuro; contrastText calculado.'),
         ('D16', 'sombra del toast: 0.25 frente a 0.3 del banner.'),
         ('D22', 'peso 600 del toast (tema: 500).'),
         ('D15', 'Slide 225ms / 195ms de MUI, no tokenizado.')],
        [S('relleno · error', '<div class="alert fill err"><span>Error al sincronizar</span></div>',
           ('fondo feedback.error.default #e2445c · texto #fff (MUI error.contrastText)', 'fondo #ef4444 · texto #fff')),
         S('relleno · aviso', '<div class="alert fill warn"><span>Sin conexión</span></div>',
           ('fondo #fdab3d · texto MUI rgba(0,0,0,0.87)', 'fondo #f59e0b · texto MUI rgba(0,0,0,0.87)'),
           gap='⚠ onColor (D8, D21)'),
         S('toast (GlobalSnackbar)', '<div class="snack">Tablero creado <span class="act">Deshacer</span></div>',
           ('texto #1a2236 · acción Button small 800 subrayado · sombra 0 4px 20px rgba(0,0,0,0.25) · peso 600 · ancho 100% · bottom/right',
            'texto #ffffff · sombra 0 4px 20px rgba(0,0,0,0.3) (banner)'),
           gap=('⚠ fondo del toast sin valor (sin decisión)', '⚠ fondo del toast sin valor (sin decisión)')),
         S('banner (UpdateAvailableBanner)', '<div class="snack" style="background:#253662;color:#fff">Hay una versión nueva <span class="act" style="color:#fff;opacity:.9">Actualizar</span></div>',
           'fondo del banner no documentado en ATOMOS; acción rgba(255,255,255,0.5) → #ffffff al pasar',
           gap='⚠ fondo sin documentar (sin decisión)')]))

    out.append(A('d-lp', 'LinearProgress', 'theme/ctsTheme.ts:355-363 · FormBuilder.tsx:3309',
        [('D21', 'pista sin valor: MUI calcula #9EC4E5 / #00325D.'),
         ('D15', 'animación de indeterminado y altura de 6px no tokenizadas.'),
         ('D11', 'pista de formulario: accent con alfa 33 (hex).')],
        [S('barra · reposo', '<div class="prog"><i></i></div>',
           'barra brand.default #0065BB (fuerza azul aunque color=error) · alto 3px · radio 4px'),
         S('pista', '<div class="prog"><i></i></div>',
           ('pista MUI #9EC4E5', 'pista MUI #00325D'), gap='⚠ pista de MUI (D21)'),
         S('indeterminado', '<div class="prog"><i style="width:35%;margin-left:30%"></i></div>',
           'animación MUI indeterminate1 2.1s cubic-bezier(0.65,0.815,0.735,0.395) · indeterminate2 2.1s 1.15s', gap='⚠ sin token (D15)'),
         S('variante formulario', '<div class="prog form"><i></i></div>',
           'pista #29ABE2 con alfa 33 (rgba 41,171,226,0.2) · barra accent #29ABE2 · alto 6px · radio 10px (FormBuilder.tsx:3309)',
           gap='⚠ alfa hex 33 fuera de tint() (D11)')]))

    out.append(A('d-cp', 'CircularProgress', 'MUI · ~50 usos · GlobalSnackbar.tsx:27 · SelectAllCheckbox.tsx:120-127',
        [('D15', 'tamaño por defecto de MUI (40) sin uso; los reales son 10 a 28px.'),
         ('D3', 'color inherit en botones sin valor en el tema.')],
        [S('reposo', '<span class="cprog"></span>',
           'brand.default #0065BB · 18px · grosor 5 (GlobalSnackbar.tsx:27) · MUI circularRotate 1.4s linear infinite'),
         S('grande', '<span class="cprog big"></span>',
           '28px (7 usos, según ATOMOS; no reverificado) · grosor 4px · sin escala de tamaños'),
         S('sobre el rail', '<span class="cprog rail"></span>',
           'rgba(255,255,255,0.5) / #fff sobre el rail (BrandLoader y rail)'),
         S('dentro de botón', '<span class="cprog inh"></span>',
           'color inherit: copia el color del botón · size 14 explícito (SelectAllCheckbox.tsx:121)', gap='⚠ tamaño por defecto de MUI (D15)')]))

    out.append(A('d-sk', 'Skeleton', 'MUI · ~50 usos · ui/LoadingScreen.tsx:11-100',
        [('D21', 'color de fondo sin valor: MUI calcula el 11% / 13%.'),
         ('D7', 'radios locales 5, 10 y 20 px de LoadingScreen.'),
         ('D15', 'pulso de 2s con delay 0.5s, no tokenizado.')],
        [S('texto', '<div class="sk t"></div>',
           ('fondo MUI rgba(26,34,54,0.11)', 'fondo MUI rgba(232,237,244,0.13)'), gap='⚠ sin valor → MUI (D21)'),
         S('circular', '<div class="sk round"></div>',
           'radio 50% · MUI · pulso 2s ease-in-out 0.5s infinite opacity 1 → 0.4 → 1', gap='⚠ sin valor → MUI (D21)'),
         S('pantalla de carga (tablero)', '<div style="width:100%;border-left:4px solid #0065bb;padding:6px 10px;background:var(--overlay-hover);border-radius:6px"><div class="sk" style="width:70%"></div><div class="sk" style="width:50%;margin-top:8px"></div></div>',
           'fondo overlay.hover · rail borders.groupRail 4px #0065BB · filas 1px solid border.subtle · alto 38px · cabecera 36px',
           gap='⚠ radio 10px y 20px locales (D7)')]))

    out.append(A('d-avatar', 'Avatar', 'MUI defaults · PersonCell.tsx:63,105 · ui/UsersTable.tsx:166-173 · layout/Sidebar.tsx:701-712 · WorkspaceAvatar.tsx:10-40',
        [('D9', 'paleta de color de usuario (8 colores) distinta de swatch.group; fallback del espacio #2979c4.'),
         ('D10', 'avatar del rail: 0.2 de fondo y 0.35 de borde.'),
         ('D7', 'avatar de inicio con radio 20px.'),
         ('D21', 'color por defecto de MUI sin valor.')],
        [S('marca', '<span class="av brand">CTS</span>',
           'fondo brand.default #0065BB · texto bg.canvas por herencia (algunos sitios #fff, GlobalCommentsPage.tsx:310) · 24px y 22px en PersonCell.tsx:63,105 · density.avatar 32px'),
         S('usuario por nombre', '<span class="av user">AM</span>',
           'fondo #6366f1 (paleta de 8: #6366f1 #0ea5e9 #10b981 #f59e0b #ef4444 #8b5cf6 #ec4899 #14b8a6) · texto #ffffff · 34px · 13px / 700',
           gap='⚠ paleta propia (D9)'),
         S('rail (pie)', '<span class="av rail">JD</span>',
           'fondo rgba(255,255,255,0.2) · borde 2px rgba(255,255,255,0.35) · texto text.onRail · 32px · 11px / 700'),
         S('espacio de trabajo', '<span class="av ws">A</span>',
           'fondo workspace.color, fallback #2979c4 (fuera de paleta) · texto #ffffff · borde 2px rgba(255,255,255,0.28) · sombra 0 2px 6px rgba(0,0,0,0.25)',
           gap='⚠ fallback fuera de paleta (D9)'),
         S('grupo (AvatarGroup)', '<span style="display:inline-flex"><span class="av group" style="background:#0065bb">A</span><span class="av group" style="background:#29abe2">B</span><span class="av group" style="background:#00c875">C</span></span>',
           'borde 2px bg.surface · 22px · 10px · máximo 3 (AvatarGroup)'),
         S('sin color (MUI)', '<span class="av nodef">?</span>',
           ('MUI #bdbdbd · sin bgcolor (ComentariosDelElemento.tsx:467) · texto background.default #f0f4f9',
            'MUI #757575 · texto #2A3547'), gap='⚠ MUI (D21)')]))

    out.append(A('d-divider', 'Divider', 'theme/ctsTheme.ts:366-372',
        [('D9', 'divisor 0.12 frente a 0.1 de la tabla; el tema y palette.divider son redundantes.'),
         ('D10', 'divisor del rail: rgba(255,255,255,0.1) con margen 12px 16px.')],
        [S('reposo', '<div class="hr"></div>',
           'borde border.subtle #dde3ec L / rgba(74,144,226,0.12) D · 1px thin · igual a palette.divider'),
         S('sobre el rail', '<div class="railp" style="padding:8px 0"><div class="rdiv"></div></div>',
           'border.onRail rgba(255,255,255,0.1) · margen 12px 16px (rail)'),
         S('punteado', '<div class="hr dash"></div>',
           'dashed · 4 variantes en el código · sin token')]))

    out.append(A('d-scroll', 'Scrollbar', 'theme/ctsTheme.ts:87-117 · index.css · features/board-view/components/WFlowScrollbar.tsx:20-62',
        [('D18', 'doble definición: el tema 6px frente a index.css 8px en gris, sin modo oscuro.'),
         ('D10', 'pista de W-Flow: rgba(13,40,73,0.05) frente a rgba(255,255,255,0.05).'),
         ('D2', 'pulgar activo sin valor.')],
        [S('pista + pulgar · reposo', '<div style="display:flex;gap:10px"><div class="sb"><i></i></div></div>',
           ('pista scrollbar.track #f0f4f9 · pulgar #c0c8d4 · 6px · radio 3px',
            'pista #253662 · pulgar #3d4f6f')),
         S('pulgar · hover', '<div style="display:flex;gap:10px"><div class="sb"><i class="hov"></i></div></div>',
           ('pulgar #a0aab8 (sin transición)', 'pulgar #4a6090')),
         S('pulgar · activo', '<div style="display:flex;gap:10px"><div class="sb"><i></i></div></div>',
           'MUI: default del navegador', gap='⚠ sin valor (D2)'),
         S('W-Flow · reposo', '<div class="sb wf"><i></i></div>',
           ('pista rgba(13,40,73,0.05) · pulgar alpha(brand.default, 0.5) · alto 8px · radio 4px · min 48px',
            'pista rgba(255,255,255,0.05) · pulgar alpha(brand, 0.5)')),
         S('W-Flow · hover / arrastre', '<div class="sb wf"><i class="hov"></i></div>',
           'hover alpha(brand, 0.75) · arrastre brand.default #0065BB · transición background-color 0.15s (WFlowScrollbar.tsx:213, :230-235)')]))

    out.append(A('d-stat', 'StatCard, mosaico de ícono y estados vacíos', 'features/admin/AdminPage.tsx:60-75, 67-70, 357-360 · ui/EmptyState.tsx:14-23 · TrashPanel.tsx:258-263 · ErrorScreen.tsx:13-18',
        [('D7', 'radio 20px de StatCard y 15px del mosaico.'),
         ('D11', 'tinte del mosaico: alpha(c, 0.1) claro / alpha(c, 0.15) oscuro; no está tokenizado.'),
         ('D16', 'anillo de hover de StatCard: sombra sin rol.'),
         ('D22', 'valor h6 700 con lh 1.2 sin token.')],
        [S('StatCard · reposo', '<div class="acard"><div class="l">Activos</div><div class="v">128</div></div>',
           ('fondo bg.surface #ffffff · borde 1px #dde3ec · radio 20px · padding 16px 20px · valor 20px / 700 · etiqueta 12px text.secondary',
            'fondo #253662 · borde rgba(74,144,226,0.12)'),
           gap=('⚠ radio 20px (D7)', '⚠ radio 20px (D7)')),
         S('StatCard · hover', '<div class="acard is-hover"><div class="l">Activos</div><div class="v" style="color:#0065bb">128</div></div>',
           'anillo 0 0 0 1px alpha(c, 0.3) · sin rol de sombra', gap='⚠ anillo sin rol (D16)'),
         S('mosaico · stat', '<span class="stile" style="--c:#0065bb">▦</span>',
           ('fondo alpha(c, 0.1) · ícono #0065BB · 38×38 · radio 15px (borderRadius 1.5)',
            'fondo alpha(c, 0.15) · ícono #0065BB'),
           gap=('⚠ radio 15px (D7)', '⚠ alfa de oscuro sin decidir (D11)')),
         S('vacío · papelera', '<span class="empty">🗑</span>',
           'fondo overlay.hover · ícono text.disabled 28px (D4) · 56×56 · radio 16px (fuera de radii)',
           gap='⚠ radio 16px (D7)'),
         S('error', '<span class="errt">!</span>',
           'fondo feedback.error.default · ícono #ffffff 36px · 64×64 · radio 16px', gap='⚠ radio 16px (D7)'),
         S('logo de acceso (OTP)', '<span class="logo-otp">✉</span>',
           'gradiente 135deg #0065BB 0% → #29ABE2 100% · ícono #ffffff 28px · 56×56 · radio 14px (radii.dialog) · OtpEmailScreen.tsx:47')]))
    return out


def sec_controles():
    return SEC('controles', '2', 'Controles',
               'Átomos de entrada y acción: botones, íconos, campos, selección, switch, swatches y enlaces. '
               'Cada estado se muestra en claro y en oscuro.', controles())


def sec_nav():
    return SEC('navegacion', '3', 'Navegación y capas flotantes',
               'Rail azul, pestañas, menús, tooltips, diálogos y el resto de capas que flotan sobre la página.',
               navegacion())


def sec_datos():
    return SEC('datos', '4', 'Datos y retroalimentación',
               'Chips, estados, tablas, grilla, alertas, progreso, avatares y estadísticas.',
               datos())


# ── Página ──────────────────────────────────────────────────────────────────
def page():
    global GAPS, PENDS
    GAPS = 0
    PENDS = 0
    secs = [sec1(), sec_controles(), sec_nav(), sec_datos()]
    body = ''.join(secs)
    toc = ('<a href="#primitivos">1 · Primitivos y roles</a>'
           '<a href="#controles">2 · Controles</a>'
           '<a href="#navegacion">3 · Navegación</a>'
           '<a href="#datos">4 · Datos y retroalimentación</a>')
    n_atoms = body.count('<article class="atom"')
    summary = (f'<div class="summary">'
               f'<div><b>{n_atoms}</b>átomos y composiciones</div>'
               f'<div><b>{PENDS}</b>átomos con decisión abierta</div>'
               f'<div><b>{GAPS}</b>estados sin valor (claro)</div>'
               f'</div>')
    legend = ('<ul class="legend">'
              '<li><span class="pd" style="display:inline-block;background:#fdab3d;color:#3b2a00;font-weight:700;font-size:11px;border-radius:4px;padding:2px 6px">⚠ Sin decidir</span> decisión D1–D23 abierta. Aviso amarillo con qué falta.</li>'
              '<li><span style="display:inline-block;width:14px;height:14px;background:#fff;box-shadow:inset 5px 0 0 #fdab3d;border:1px solid #bbb"></span> franja amarilla: estado sin valor en cts-manager; se ve el valor de MUI.</li>'
              '<li><span class="mono">T:131</span> = theme/ctsTheme.ts línea 131. Las demás rutas son relativas a cts-manager/frontend/src.</li>'
              '</ul>')
    head = (f'<header class="top"><h1>Átomos del Sistema de Diseño CTS · demo estática</h1>'
            f'<p>Generada desde <code>docs/ATOMOS.md</code> (paso 1, borrador). Nada de esto está decidido: '
            f'lo que tiene decisión abierta lleva aviso amarillo.</p>'
            f'{summary}{legend}</header>')
    return ('<!doctype html><html lang="es"><head><meta charset="utf-8">'
            '<meta name="viewport" content="width=device-width, initial-scale=1">'
            '<title>Átomos CTS · demo</title>'
            '<link rel="preconnect" href="https://fonts.googleapis.com">'
            '<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>'
            '<link href="https://fonts.googleapis.com/css2?family=Titillium+Web:wght@300;400;600;700;900&display=swap" rel="stylesheet">'
            f'<style>{CSS}\n{mode_block()}</style></head><body><main>'
            f'{head}<nav class="toc">{toc}</nav>{body}'
            '</main></body></html>')


if __name__ == '__main__':
    OUT.write_text(page(), encoding='utf-8')
    print(f'escrito {OUT} · átomos={PENDS} con pendientes · huecos={GAPS}')
