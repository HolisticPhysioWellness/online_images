import os
from fig import *

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "svg")
os.makedirs(OUT, exist_ok=True)
EX = {}


def solve(fn, lo, hi, it=50):
    """Bisection: find x in [lo,hi] with fn(x)=0 (fn monotonic)."""
    flo = fn(lo)
    for _ in range(it):
        mid = (lo + hi) / 2
        fm = fn(mid)
        if (fm > 0) == (flo > 0):
            lo, flo = mid, fm
        else:
            hi = mid
    return (lo + hi) / 2


ARM = L["uarm"] + L["farm"]


def reg(key, *panels):
    EX[key] = panels


def cue_tick(x, y, good=True):
    c = GOOD if good else BAD
    sym = ('<path d="M-7,0 L-2,6 L8,-6" fill="none" stroke="#fff" stroke-width="3.2" stroke-linecap="round" stroke-linejoin="round"/>'
           if good else '<path d="M-6,-6 L6,6 M6,-6 L-6,6" fill="none" stroke="#fff" stroke-width="3.2" stroke-linecap="round"/>')
    return f'<g transform="translate({x},{y})"><circle r="14" fill="{c}"/>{sym}</g>'


# ----------------------------------------------------------------- wall angel
def wall_angel(up):
    W, H = 340, 470
    fl = 455
    pel = (170, fl - 186)
    if up:
        fr = Front(pel, arm=(128, 108))
    else:
        fr = Front(pel, arm=(178, 90))
    c = wall_back(40, 40, 300, fl) + floor(fl, 10, 330) + fr.svg()
    if up:
        c += arrow("M58,200 Q48,150 70,108") + arrow("M282,200 Q292,150 270,108")
    else:
        c += label(170, 60, "", 1)
    return panel(c, W, H, "FINISH" if up else "START")


def wall_side_pose(good):
    W, H = 300, 470
    fl = 455
    f_ = Side((0, 0), trunk=90 if good else 97, neck=90 if good else 72, curve=0 if good else -9,
              flare=0 if good else 9, arm=(100, 96), leg=(-86, -94), foot=0)
    f_.place("hip", (118, fl - 186))
    back = f_.axis(0.75)[0] - 22
    c = wall_side(min(back, f_.axis(0.1)[0] - 24) + 1, 40, fl, -1) + floor(fl, 10, 290) + f_.svg()
    sh = f_.pts()
    if good:
        c += cue_tick(262, 70, True) + label(196, 214, "ribs down", 18, GOOD, "start")
        c += label(196, 290, "low back", 18, GOOD, "start") + label(196, 312, "near wall", 18, GOOD, "start")
    else:
        c += cue_tick(262, 70, False) + label(200, 214, "ribs flare", 18, BAD, "start")
        c += label(200, 290, "low back", 18, BAD, "start") + label(200, 312, "arches", 18, BAD, "start")
    return panel(c, W, H)


reg("wall-angels", wall_angel(False), wall_angel(True))
reg("wall-angels-ribs", wall_side_pose(True), wall_side_pose(False))


# ------------------------------------------------------------ 90/90 breathing
def breathing(exhale):
    W, H = 380, 300
    fl = 262
    f_ = Side((0, 0), trunk=180, neck=178, arm=(-15, 45), farm=(-5, 0), hand_n=5,
              leg=(92, -2), foot=90)
    f_.place("hip", (205, fl - 25))
    f_.leg_to((f_.pts()["hip"][0] + 90, fl - 25 - 90), "both", 1, 90)
    ank = f_.pts()["ankle_n"]
    c = mat(fl, 30, 320) + wall_side(ank[0] + 16, 30, fl + 2, 1) + f_.svg()
    if exhale:
        c += arrow("M175,168 L175,196") + label(175, 158, "ribs down", 18, ACCENT)
    else:
        c += arrow("M160,205 L160,178") + arrow("M188,205 L188,178")
    return panel(c, W, H, "EXHALE" if exhale else "INHALE")


reg("90-90-breathing", breathing(False), breathing(True))


# ----------------------------------------------------------------- cat camel
def catcamel(cat):
    W, H = 360, 280
    fl = 250
    def mk(t):
        g = Side((0, 0), trunk=t, neck=(t - 45) if cat else (t + 14),
                 curve=16 if cat else -11, arm=(-90, -90), hand_n=0, hand_f=0,
                 leg=(-90, 180), foot=180)
        g.place("knee_n", (120, fl - 10))
        return g
    t = solve(lambda t: mk(t).shoulder()[1] - (fl - 9 - ARM * 0.99), -10, 30)
    f_ = mk(t)
    s_ = f_.shoulder()
    f_.arm_to((s_[0] + 2, fl - 9), "both", 1, 0)
    c = mat(fl, 30, 330) + f_.svg()
    if cat:
        c += arrow("M150,78 Q175,58 200,78")
    else:
        c += arrow("M150,100 Q175,122 200,100")
    return panel(c, W, H, "ROUND UP" if cat else "LET SAG")


reg("cat-camel", catcamel(True), catcamel(False))


# -------------------------------------------------------- band pull-aparts
def pullapart(out):
    W, H = 340, 400
    fl = 385
    pel = (170, fl - 186)
    if out:
        fr = Front(pel, arm=(180, 180))
    else:
        fr = Front(pel, arm=(-75, -20), ascale=(0.3, 0.3))
    c = floor(fl, 10, 330) + fr.svg()
    sr, sl = fr.shoulders()
    if out:
        hy = sr[1]
        c += band_path(f"M{sr[0]-128},{hy+4} Q170,{hy+22} {sl[0]+128},{hy+4}")
        c += arrow(f"M110,{hy-26} L50,{hy-26}") + arrow(f"M230,{hy-26} L290,{hy-26}")
    else:
        hr = (sr[0] + 6, sr[1] + 18)
        c += band_path(f"M{sr[0]+4},{sr[1]+22} L{sl[0]-4},{sl[1]+22}")
        for hx in (sr[0] + 4, sl[0] - 4):
            c += f'<circle cx="{hx}" cy="{sr[1]+22}" r="11" fill="{SKIN}" stroke="{INK}" stroke-width="2.6"/>'
        c += label(170, sr[1] - 70, "", 1)
    return panel(c, W, H, "PULL APART" if out else "START")


reg("band-pull-aparts", pullapart(False), pullapart(True))


# ---------------------------------------------------- scapular push-ups
def scap_pushup(plus):
    W, H = 380, 260
    fl = 235
    lift = 6 if plus else -2

    def mk(t):
        g = Side((0, 0), trunk=t, neck=t - 8, curve=7 if plus else -4,
                 leg=(t - 180, 180), foot=180)
        g.place("knee_n", (110, fl - 10))
        return g
    t = solve(lambda t: mk(t).shoulder()[1] - (fl - 9 - ARM * 0.97 - lift), 0, 45)
    f_ = mk(t)
    s = f_.shoulder()
    f_.arm_to((s[0] + 2, fl - 9), "both", 1, 0)
    c = mat(fl, 30, 350) + f_.svg()
    sh = f_.shoulder()
    if plus:
        c += arrow(f"M{sh[0]-40},{sh[1]-38} L{sh[0]-40},{sh[1]-62}")
        c += label(sh[0] - 40, sh[1] - 70, "push floor away", 17, ACCENT)
    else:
        c += arrow(f"M{sh[0]-40},{sh[1]-62} L{sh[0]-40},{sh[1]-40}")
        c += label(sh[0] - 40, sh[1] - 70, "chest sinks", 17, ACCENT)
    return panel(c, W, H, "PUSH UP" if plus else "START")


reg("scapular-push-ups", scap_pushup(False), scap_pushup(True))


# --------------------------------------------------------------- dead bug
def deadbug(ext):
    W, H = 460, 300
    fl = 268
    if ext:
        f_ = Side((0, 0), trunk=180, neck=180, arm=(170, 172), farm=(90, 90),
                  leg=(90, 0), fleg=(12, 8), foot=90, ffoot=60)
    else:
        f_ = Side((0, 0), trunk=180, neck=180, arm=(90, 90), farm=(92, 92),
                  leg=(90, 0), fleg=(90, 0), foot=60, ffoot=60)
    f_.place("hip", (255, fl - 25))
    c = mat(fl, 20, 440) + f_.svg()
    if ext:
        c += arrow("M140,110 Q95,125 80,195") + arrow("M295,130 Q360,160 380,205")
    return panel(c, W, H, "REACH" if ext else "START")


reg("dead-bug", deadbug(False), deadbug(True))


# ----------------------------------------------- scapular pull-ups (back view)
def scap_pullup(active):
    W, H = 340, 420
    bar_y = 44
    fr = Front((170, 0), shrug=12 if not active else -3, back=True)
    sr, sl = fr.shoulders()
    # arms straight: shoulders ~ (uarm+farm)*0.99 below bar, hands slightly wider
    hand_r, hand_l = (105, bar_y + 6), (235, bar_y + 6)
    drop = (L["uarm"] + L["farm"]) * 0.985
    import math as _m
    dy = _m.sqrt(drop ** 2 - (hand_r[0] - sr[0]) ** 2)
    shift = (hand_r[1] + dy) - sr[1]
    fr.p = (170, shift)
    if active:
        fr.p = (170, fr.p[1] + 0)
    fr = Front(fr.p, shrug=12 if not active else -3, back=True, leg=(-93, -95))
    sr, sl = fr.shoulders()
    fr.arms_to(hand_r, hand_l)
    c = bar_front(bar_y, 50, 290) + fr.svg()
    for hx in (hand_r[0], hand_l[0]):
        c += f'<rect x="{hx-9}" y="{bar_y-7}" width="18" height="14" rx="6" fill="{SKIN}" stroke="{INK}" stroke-width="2.4"/>'
    if active:
        c += arrow(f"M{sr[0]-40},{sr[1]-4} L{sr[0]-40},{sr[1]+24}") + arrow(f"M{sl[0]+40},{sl[1]-4} L{sl[0]+40},{sl[1]+24}")
        c += f'<rect x="50" y="{H-34}" width="240" height="30" rx="13" fill="#fff" opacity="0.92"/>' + label(170, H - 13, "shoulders down &amp; back", 18, ACCENT)
    else:
        c += f'<rect x="50" y="{H-34}" width="240" height="30" rx="13" fill="#fff" opacity="0.92"/>' + label(170, H - 13, "shoulders up by ears", 18, INK, weight=500)
    return panel(c, W, H, "ACTIVE" if active else "HANG")


reg("scapular-pull-ups", scap_pullup(False), scap_pullup(True))


# ----------------------------------------------------- band lat pulldown
def pulldown(down):
    W, H = 340, 400
    fl = 385
    bar = (282, 40)
    f_ = Side((0, 0), trunk=92, neck=90, leg=(-90, 180), foot=180)
    f_.place("knee_n", (140, fl - 10))
    s = f_.shoulder()
    if down:
        f_.arm = (-96, 62)
        f_.farm = (-100, 60)
        f_.hand_n = f_.hand_f = 60
    else:
        f_.arm_to((bar[0] - 12, s[1] - 104), "both", -1, 80)
    hand = f_.pts()["hand_n"]
    c = f'<line x1="120" y1="{bar[1]}" x2="320" y2="{bar[1]}" stroke="{PROP_DARK}" stroke-width="12" stroke-linecap="round"/>'
    c += floor(fl, 10, 310) + band_path(f"M{bar[0]},{bar[1]} L{hand[0]-2},{hand[1]+2}") + f_.svg()
    c += f'<circle cx="{bar[0]}" cy="{bar[1]}" r="8" fill="{BAND}" stroke="{INK}" stroke-width="2"/>'
    if down:
        e = f_.pts()["elbow_n"]
        c += arrow(f"M{e[0]-62},{e[1]-80} L{e[0]-62},{e[1]-20}")
        c += label(e[0] - 62, e[1] + 4, "elbows", 17, ACCENT) + label(e[0] - 62, e[1] + 24, "to ribs", 17, ACCENT)
    return panel(c, W, H, "PULL" if down else "START")


reg("band-lat-pulldown", pulldown(False), pulldown(True))


# ------------------------------------------------------ inverted table row
def table(x0, x1, top, fl):
    col = "#ddd2c9"
    return (f'<rect x="{x0+30}" y="{top+14}" width="12" height="{fl-top-14}" fill="{col}" stroke="{PROP_DARK}" stroke-width="2"/>'
            f'<rect x="{x0}" y="{top}" width="{x1-x0}" height="14" rx="3" fill="#cdbfb4" stroke="{PROP_DARK}" stroke-width="2"/>')


def inv_row(top_pos):
    W, H = 480, 300
    fl = 285
    edge = (190, 110)
    sh_t = (edge[0] - 4, edge[1] + (40 if top_pos else 10 + ARM * 0.97))

    def mk(t):
        g = Side((0, 0), trunk=t, neck=t + (10 if top_pos else 0),
                 leg=(t - 180, t - 180), foot=t - 90)
        g.place("shoulder", sh_t)
        return g
    t = solve(lambda t: mk(t).pts()["ankle_n"][1] - (fl - 11), 110, 180)
    f_ = mk(t)
    f_.arm_to((edge[0] + 6, edge[1] + 10), "both", -1, 90)
    c = floor(fl, 10, 470) + table(-20, edge[0] + 18, edge[1] - 14, fl) + f_.svg()
    c += f'<rect x="{edge[0]}" y="{edge[1]-18}" width="17" height="24" rx="7" fill="{SKIN}" stroke="{INK}" stroke-width="2.4"/>'
    if top_pos:
        c += arrow(f"M{edge[0]+95},{edge[1]-22} Q{edge[0]+40},{edge[1]-30} {edge[0]+26},{edge[1]+4}")
        c += label(edge[0] + 100, edge[1] - 18, "chest to the edge", 17, ACCENT, "start")
    else:
        c += label(W - 12, edge[1] - 30, "body straight like a plank", 17, ACCENT, "end")
    return panel(c, W, H, "PULL" if top_pos else "START")


reg("inverted-row", inv_row(False), inv_row(True))


# -------------------------------------------------------------- prone Y
def prone_y(lift):
    W, H = 420, 220
    fl = 190
    f_ = Side((0, 0), trunk=0, neck=-3 if not lift else 0, arm=(14 if lift else 2, 15 if lift else 1),
              hand_n=15 if lift else 1, leg=(180, 180), foot=-120)
    f_.place("hip", (150, fl - 24))
    c = mat(fl, 20, 400) + f_.svg()
    if lift:
        c += arrow("M370,150 L370,120") + label(365, 108, "thumbs up, lift", 17, ACCENT)
    return panel(c, W, H, "LIFT" if lift else "START")


reg("prone-y-raise", prone_y(False), prone_y(True))


# --------------------------------------------------------- hollow body
def hollow(full):
    W, H = 460, 260
    fl = 230
    if full:
        f_ = Side((0, 0), trunk=166, neck=150, arm=(174, 174), farm=(176, 176), leg=(14, 14), foot=40)
        f_.place("hip", (250, fl - 24))
    else:
        f_ = Side((0, 0), trunk=164, neck=140, arm=(8, 8), farm=(10, 10), leg=(100, -5), foot=40)
        f_.place("hip", (230, fl - 24))
    c = mat(fl, 20, 440) + f_.svg()
    c += label(230, 252, "low back pressed down, ribs down", 17, ACCENT)
    return panel(c, W, H, "FULL" if full else "TUCKED")


reg("hollow-body", hollow(False), hollow(True))


# ----------------------------------------------------- pull-up family (side)
BAR = (180, 96)


def hang_fig(top, knees=True):
    legs = (-100, -145) if knees else (-88, -95)
    if top:
        f_ = Side((0, 0), trunk=94, neck=96, leg=legs, foot=-60)
        f_.place("shoulder", (BAR[0] - 24, BAR[1] + 28))
        f_.arm_to((BAR[0] + 2, BAR[1] + 4), "both", -1, 100)
    else:
        f_ = Side((0, 0), trunk=96, neck=92, leg=legs, foot=-60)
        f_.place("shoulder", (BAR[0] - 10, BAR[1] + ARM * 0.985))
        f_.arm_to((BAR[0] + 2, BAR[1] + 4), "both", -1, 80)
    return f_


def rig():
    return (f'<rect x="34" y="{BAR[1]-60}" width="14" height="{480-BAR[1]+60}" fill="{PROP}" stroke="{PROP_DARK}" stroke-width="2"/>'
            f'<line x1="41" y1="{BAR[1]}" x2="{BAR[0]+14}" y2="{BAR[1]}" stroke="{PROP_DARK}" stroke-width="13" stroke-linecap="round"/>'
            f'<line x1="41" y1="{BAR[1]}" x2="{BAR[0]+14}" y2="{BAR[1]}" stroke="#b3a79e" stroke-width="7" stroke-linecap="round"/>')


def hang_panel(tag, top, band=False, box=False, arrow_d=None, extra=""):
    W, H = 320, 500
    fl = 485
    f_ = hang_fig(top)
    c = rig()
    if box:
        p_ = f_.pts()
        by = max(p_["toe_n"][1], p_["ankle_n"][1]) + 7
        c += f'<rect x="{p_["toe_n"][0]-50}" y="{by}" width="120" height="{fl-by}" rx="4" fill="#cdbfb4" stroke="{PROP_DARK}" stroke-width="2"/>'
    c += floor(fl, 10, 310)
    c += f_.svg()
    c += f'<ellipse cx="{BAR[0]+2}" cy="{BAR[1]-3}" rx="10" ry="9" fill="{SKIN}" stroke="{INK}" stroke-width="2.4"/>'
    if band:
        k = f_.pts()["knee_n"]
        a_ = f_.pts()["ankle_n"]
        m = ((k[0] + a_[0]) / 2, (k[1] + a_[1]) / 2)
        c += band_path(f"M{BAR[0]-8},{BAR[1]+6} L{m[0]-10},{m[1]+12} Q{m[0]},{m[1]+20} {m[0]+8},{m[1]+10} L{BAR[0]-2},{BAR[1]+6}", 5)
    if arrow_d:
        c += arrow(arrow_d)
    return panel(c + extra, W, H, tag)


UP = "M270,330 L270,250"
reg("band-assisted-pull-up",
    hang_panel("START", False, band=True),
    hang_panel("PULL", True, band=True, arrow_d=UP))
reg("flexed-arm-hang",
    hang_panel("STEP UP", True, box=True),
    hang_panel("HOLD", True, extra=label(262, 250, "hold", 19, ACCENT) + label(262, 274, "chin over", 17, ACCENT) + label(262, 294, "the bar", 17, ACCENT)))
reg("negative-pull-up",
    hang_panel("TOP", True, box=True),
    hang_panel("LOWER SLOWLY", False, arrow_d="M270,220 L270,320",
               extra=label(270, 350, "3–8 sec", 19, ACCENT)))
reg("pull-up",
    hang_panel("HANG", False),
    hang_panel("PULL", True, arrow_d=UP))


if __name__ == "__main__":
    html = ["<html><head><meta charset='utf-8'></head><body style='margin:0;background:#fff;font-family:sans-serif'>"]
    import sys
    only = sys.argv[1:]
    for k, ps in EX.items():
        if only and k not in only: continue
        html.append(f"<div style='border-bottom:1px solid #ccc'><b>{k}</b><br>")
        for i, p in enumerate(ps):
            open(os.path.join(OUT, f"{k}-{i+1}.svg"), "w").write(p)
            html.append(f"<span style='display:inline-block;border:1px solid #eee;margin:2px'>{p}</span>")
        html.append("</div>")
    open(os.path.join(os.path.dirname(OUT), "sheet.html"), "w").write("".join(html) + "</body></html>")
    print(len(EX))
