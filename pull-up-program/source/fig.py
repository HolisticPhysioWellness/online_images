"""Parametric line-illustration figures for physio exercise handouts.

Side-view figures face right. Angles are absolute world angles in degrees
(0 = right, 90 = up, 180 = left, -90/270 = down). SVG y grows downward.
"""
import math

INK = "#241a0d"
SKIN = "#f7ece8"
SKIN_FAR = "#e2cdc7"
TOP = "#b98c80"
TOP_FAR = "#9e7266"
SHORTS = "#5b4a42"
SHORTS_FAR = "#46382f"
HAIR = "#3a2a1c"
ACCENT = "#c0573e"
BAND = "#d9822b"
PROP = "#e9e4e0"
PROP_DARK = "#8c7f76"
GOOD = "#3f8f5b"
BAD = "#c0392b"
OUTLINE = 2.6

# segment lengths
L = dict(trunk=116, neck=14, head=23, uarm=60, farm=56, hand=17,
         thigh=92, shank=88, foot=30)


def d2r(a):
    return a * math.pi / 180


def vec(a):
    return (math.cos(d2r(a)), -math.sin(d2r(a)))


def add(p, v, s=1.0):
    return (p[0] + v[0] * s, p[1] + v[1] * s)


def f(n):
    return f"{n:.1f}"


def capsule_pts(p1, r1, p2, r2, n=10):
    dx, dy = p2[0] - p1[0], p2[1] - p1[1]
    d = math.hypot(dx, dy) or 1e-6
    v = (dx / d, dy / d)
    w = (-v[1], v[0])
    s = max(-0.99, min(0.99, (r1 - r2) / d))
    al = math.asin(s)
    base = math.atan2(v[1], v[0])
    # m = sin(al) v + cos(al) (+/-w)  -> angle of m relative to v is +/-(90-al)
    t = math.pi / 2 - al
    pts = []
    # around p2 from +t to -t through 0 (forward)
    for i in range(n + 1):
        a = base + t - 2 * t * i / n
        pts.append((p2[0] + r2 * math.cos(a), p2[1] + r2 * math.sin(a)))
    # around p1 from -t to -(2pi - t) through pi (backward)
    for i in range(n + 1):
        a = base - t - (2 * math.pi - 2 * t) * i / n
        pts.append((p1[0] + r1 * math.cos(a), p1[1] + r1 * math.sin(a)))
    return pts


def poly_path(pts):
    return "M" + " L".join(f"{f(x)},{f(y)}" for x, y in pts) + " Z"


def smooth_closed(pts, tension=0.5):
    n = len(pts)
    d = f"M{f(pts[0][0])},{f(pts[0][1])}"
    for i in range(n):
        p0, p1, p2, p3 = pts[i - 1], pts[i], pts[(i + 1) % n], pts[(i + 2) % n]
        c1 = (p1[0] + (p2[0] - p0[0]) * tension / 3, p1[1] + (p2[1] - p0[1]) * tension / 3)
        c2 = (p2[0] - (p3[0] - p1[0]) * tension / 3, p2[1] - (p3[1] - p1[1]) * tension / 3)
        d += f" C{f(c1[0])},{f(c1[1])} {f(c2[0])},{f(c2[1])} {f(p2[0])},{f(p2[1])}"
    return d + " Z"


def ang_of(p, q):
    return math.degrees(math.atan2(-(q[1] - p[1]), q[0] - p[0]))


def ik(s, t, l1, l2, bend=1):
    d = math.hypot(t[0] - s[0], t[1] - s[1])
    d = max(1e-3, min(d, (l1 + l2) * 0.9995))
    base = ang_of(s, t)
    a = math.degrees(math.acos(max(-1, min(1, (l1 * l1 + d * d - l2 * l2) / (2 * l1 * d)))))
    up = base + bend * a
    e = add(s, vec(up), l1)
    return up, ang_of(e, t)


class Layer:
    def __init__(self):
        self.shapes = []  # (path_d, fill)

    def add(self, d, fill):
        self.shapes.append((d, fill))

    def svg(self):
        out = [f'<path d="{d}" fill="{INK}" stroke="{INK}" stroke-width="{OUTLINE*2}" stroke-linejoin="round"/>'
               for d, _ in self.shapes]
        out += [f'<path d="{d}" fill="{c}"/>' for d, c in self.shapes]
        return "<g>" + "".join(out) + "</g>"


def limb(layer, pts_radii, fill):
    for (p1, r1), (p2, r2) in zip(pts_radii, pts_radii[1:]):
        layer.add(poly_path(capsule_pts(p1, r1, p2, r2)), fill)


def head_svg(c, r, up_dir, face_dir, far=False):
    """Head circle with a hair cap. up_dir: unit vector neck->crown, face_dir: unit toward face."""
    out = f'<circle cx="{f(c[0])}" cy="{f(c[1])}" r="{f(r)}" fill="{SKIN}" stroke="{INK}" stroke-width="{OUTLINE}"/>'
    pts = []
    for i in range(25):
        phi = d2r(-160 + 190 * i / 24)
        pts.append((c[0] + r * (math.cos(phi) * up_dir[0] + math.sin(phi) * face_dir[0]),
                    c[1] + r * (math.cos(phi) * up_dir[1] + math.sin(phi) * face_dir[1])))
    for i in range(25):
        phi = d2r(30 - 190 * i / 24)
        rr = r * (0.62 + 0.25 * abs(math.sin(d2r(phi if phi > -60 else -60))))
        k = 0.35
        cx, cy = c[0] + r * k * -face_dir[0] * 0.3, c[1] + r * k * -face_dir[1] * 0.3
        pts.append((cx + rr * (math.cos(phi) * up_dir[0] + math.sin(phi) * face_dir[0]),
                    cy + rr * (math.cos(phi) * up_dir[1] + math.sin(phi) * face_dir[1])))
    out += f'<path d="{smooth_closed(pts, 0.3)}" fill="{HAIR}" stroke="{INK}" stroke-width="{OUTLINE*0.6}"/>'
    # eye
    eye = add(add(c, face_dir, r * 0.55), up_dir, r * 0.12)
    out += f'<circle cx="{f(eye[0])}" cy="{f(eye[1])}" r="1.9" fill="{INK}"/>'
    # nose hint
    nose = add(c, face_dir, r * 0.98)
    nose = add(nose, up_dir, -r * 0.05)
    tip = add(nose, face_dir, r * 0.16)
    tip = add(tip, up_dir, -r * 0.14)
    out += (f'<path d="M{f(nose[0])},{f(nose[1])} L{f(tip[0])},{f(tip[1])} L{f(add(nose, up_dir, -r*0.22)[0])},'
            f'{f(add(nose, up_dir, -r*0.22)[1])}" fill="{SKIN}" stroke="{INK}" stroke-width="{OUTLINE*0.7}" stroke-linejoin="round"/>')
    return out


class Side:
    """Side-view figure facing right."""

    def __init__(self, hip, trunk=90, neck=None, curve=0.0, flare=0.0,
                 arm=(-90, -90), farm=None, hand=None,
                 leg=(-90, -90), fleg=None, foot=0, ffoot=None,
                 hand_n=None, hand_f=None, grip=False, face=0.0):
        self.hip = hip
        self.trunk = trunk
        self.neck = trunk if neck is None else neck
        self.curve = curve
        self.flare = flare
        self.arm = arm
        self.farm = farm if farm is not None else arm
        self.hand_n = hand_n if hand_n is not None else self.arm[1]
        self.hand_f = hand_f if hand_f is not None else self.farm[1]
        self.leg = leg
        self.fleg = fleg if fleg is not None else leg
        self.foot = foot
        self.ffoot = ffoot if ffoot is not None else foot
        self.face = face  # extra head tilt

    # geometry helpers ------------------------------------------------------
    def frame(self):
        u = vec(self.trunk)
        n = (-u[1], u[0])  # front
        # front normal must point to the facing side (right) when upright
        if self.trunk == 90 or True:
            n = (u[1] * -1, u[0]) if False else (-u[1], u[0])
        # For u=(0,-1) -> n=(1,0) : front is right. good.
        return u, n

    def axis(self, t):
        u, n = self.frame()
        p = add(self.hip, u, L["trunk"] * t)
        return add(p, n, -self.curve * math.sin(math.pi * t))

    def shoulder(self):
        return self.axis(0.86)

    def neck_base(self):
        return self.axis(0.99)

    def joints(self):
        s = self.shoulder()
        j = {}
        for key, ang, hang in (("n", self.arm, self.hand_n), ("f", self.farm, self.hand_f)):
            e = add(s, vec(ang[0]), L["uarm"])
            w = add(e, vec(ang[1]), L["farm"])
            h = add(w, vec(hang), L["hand"])
            j["arm_" + key] = (s, e, w, h)
        hp = self.axis(0.02)
        for key, ang, ft in (("n", self.leg, self.foot), ("f", self.fleg, self.ffoot)):
            k = add(hp, vec(ang[0]), L["thigh"])
            a = add(k, vec(ang[1]), L["shank"])
            heel = add(a, vec(ang[1]), 4)
            toe = add(heel, vec(ft), L["foot"])
            j["leg_" + key] = (hp, k, a, toe)
        u = vec(self.neck)
        nb = self.neck_base()
        hc = add(nb, u, L["neck"] + L["head"] * 0.8)
        j["head"] = (nb, hc)
        return j

    def torso_path(self):
        u, n = self.frame()
        fr = [(0.0, 19), (0.12, 20), (0.3, 18), (0.45, 19), (0.62, 25), (0.78, 26), (0.9, 21), (1.0, 11)]
        bk = [(1.0, -11), (0.9, -20), (0.75, -22), (0.55, -19), (0.35, -17), (0.15, -22), (0.02, -24)]
        pts = []
        for t, o in fr + bk:
            if o > 0 and 0.5 < t < 0.8:
                o += self.flare * math.sin(math.pi * (t - 0.5) / 0.3)
            p = self.axis(t)
            pts.append(add(p, n, o))
        # rounded bottom
        p0 = self.axis(0.0)
        pts.append(add(add(p0, u, -8), n, -8))
        pts.append(add(add(p0, u, -9), n, 6))
        return smooth_closed(pts, 0.55)

    def svg(self, band_shorts=True):
        j = self.joints()
        far, body, near = Layer(), Layer(), Layer()
        s, e, w, h = j["arm_f"]
        limb(far, [(s, 11), (e, 8.5), (w, 6.5)], SKIN_FAR)
        limb(far, [(w, 6.5), (h, 6)], SKIN_FAR)
        hp, k, a, t = j["leg_f"]
        limb(far, [(hp, 17), (k, 12), (a, 8)], SKIN_FAR)
        limb(far, [(add(a, vec(self.fleg[1]), 3), 8), (t, 5.5)], SKIN_FAR)
        far.add(poly_path(capsule_pts(hp, 17.5, add(hp, vec(self.fleg[0]), L["thigh"] * 0.45), 14)), SHORTS_FAR)
        # body
        nb, hc = j["head"]
        body.add(poly_path(capsule_pts(nb, 9, add(nb, vec(self.neck), L["neck"] + 6), 8)), SKIN)
        body.add(self.torso_path(), TOP)
        # shorts over hip region
        hp, k, a, t = j["leg_n"]
        near_leg = Layer()
        limb(near_leg, [(hp, 18), (k, 12.5), (a, 8.5)], SKIN)
        limb(near_leg, [(add(a, vec(self.leg[1]), 3), 8.5), (t, 6)], SKIN)
        near_leg.add(poly_path(capsule_pts(hp, 18.5, add(hp, vec(self.leg[0]), L["thigh"] * 0.45), 14.5)), SHORTS)
        s, e, w, h = j["arm_n"]
        limb(near, [(s, 11.5), (e, 9), (w, 7)], SKIN)
        limb(near, [(w, 7), (h, 6.5)], SKIN)
        # short sleeve
        near.add(poly_path(capsule_pts(s, 13.5, add(s, vec(self.arm[0]), L["uarm"] * 0.35), 11.5)), TOP)
        u = vec(self.neck + self.face)
        fdir = (-u[1], u[0])
        # draw head before near arm so an overhead arm can pass in front
        return (far.svg() + body.svg() + head_svg(hc, L["head"], u, fdir)
                + near_leg.svg() + near.svg())

    def pts(self):
        j = self.joints()
        d = {"hip": j["leg_n"][0], "head": j["head"][1], "shoulder": j["arm_n"][0]}
        for k in "nf":
            d["elbow_" + k], d["wrist_" + k], d["hand_" + k] = j["arm_" + k][1:]
            d["knee_" + k], d["ankle_" + k], d["toe_" + k] = j["leg_" + k][1:]
        return d

    def place(self, key, target):
        p = self.pts()[key]
        self.hip = (self.hip[0] + target[0] - p[0], self.hip[1] + target[1] - p[1])
        return self

    def arm_to(self, target, which="n", bend=1, hand=None):
        a = ik(self.shoulder(), target, L["uarm"], L["farm"], bend)
        if which in ("n", "both"):
            self.arm = a
            self.hand_n = a[1] if hand is None else hand
        if which in ("f", "both"):
            self.farm = a
            self.hand_f = a[1] if hand is None else hand
        return self

    def leg_to(self, target, which="n", bend=-1, foot=None):
        a = ik(self.axis(0.02), target, L["thigh"], L["shank"], bend)
        if which in ("n", "both"):
            self.leg = a
            if foot is not None: self.foot = foot
        if which in ("f", "both"):
            self.fleg = a
            if foot is not None: self.ffoot = foot
        return self

    def hand(self, which="n"):
        return self.joints()["arm_" + which][3]

    def wrist(self, which="n"):
        return self.joints()["arm_" + which][2]


class Front:
    """Front (or back) view figure, symmetrical frame, independent limbs.

    arms: (upper, fore) angles for the figure's RIGHT arm (viewer's left) as
    drawn on the viewer's left side; left arm is mirrored unless given.
    """

    def __init__(self, pelvis, arm=(-100, -95), larm=None, leg=(-92, -90), lleg=None,
                 shrug=0.0, back=False, width=1.0, hands_up=False, ascale=(1.0, 1.0), hand_open=False):
        self.p = pelvis
        self.arm = arm
        self.larm = larm if larm is not None else (180 - arm[0], 180 - arm[1])
        self.leg = leg
        self.lleg = lleg if lleg is not None else (180 - leg[0], 180 - leg[1])
        self.shrug = shrug
        self.back = back
        self.w = width
        self.ascale = ascale

    def shoulders(self):
        x, y = self.p
        top = y - L["trunk"]
        sh_y = top + 12 - self.shrug
        sw = 36 * self.w
        return (x - (sw - 8), sh_y + 3), (x + (sw - 8), sh_y + 3)

    def arms_to(self, tr, tl):
        sr, sl = self.shoulders()
        self.arm = ik(sr, tr, L["uarm"], L["farm"], -1)
        self.larm = ik(sl, tl, L["uarm"], L["farm"], 1)
        return self

    def svg(self):
        x, y = self.p
        top = y - L["trunk"]
        sh_y = top + 12 - self.shrug
        sw = 36 * self.w
        body, arms, legs = Layer(), Layer(), Layer()
        # legs
        for side, ang in ((-1, self.leg), (1, self.lleg)):
            hp = (x + side * 17, y + 4)
            k = add(hp, vec(ang[0]), L["thigh"])
            a = add(k, vec(ang[1]), L["shank"])
            limb(legs, [(hp, 17), (k, 12), (a, 8.5)], SKIN)
            toe = (a[0] + side * 9, a[1] + 11)
            legs.add(poly_path(capsule_pts((a[0], a[1] + 3), 8, toe, 7)), SKIN)
            legs.add(poly_path(capsule_pts(hp, 17.5, add(hp, vec(ang[0]), L["thigh"] * 0.42), 14)), SHORTS)
        # torso
        pts = [(x - 20, y + 16), (x - 23, y - 10), (x - 20, y - 38), (x - 27, top + 34),
               (x - sw, sh_y + 2), (x - sw + 8, sh_y - 9), (x - 9, top - 1 - self.shrug * 0.3),
               (x + 9, top - 1 - self.shrug * 0.3), (x + sw - 8, sh_y - 9), (x + sw, sh_y + 2),
               (x + 27, top + 34), (x + 20, y - 38), (x + 23, y - 10), (x + 20, y + 16), (x, y + 20)]
        # neck
        nb = (x, top + 2)
        hc = (x, top - 14 - L["head"] + self.shrug * 0.15)
        body.add(poly_path(capsule_pts(nb, 9, (x, top - 16), 8)), SKIN)
        body.add(smooth_closed(pts, 0.5), TOP)
        body.add(smooth_closed([(x - 22, y - 6), (x + 22, y - 6), (x + 21, y + 16), (x, y + 21), (x - 21, y + 16)], 0.3), SHORTS)
        # arms
        for side, ang, sc in ((-1, self.arm, self.ascale[0]), (1, self.larm, self.ascale[1])):
            s = (x + side * (sw - 8), sh_y + 3)
            e = add(s, vec(ang[0]), L["uarm"] * sc)
            w = add(e, vec(ang[1]), L["farm"] * sc)
            h = add(w, vec(ang[1]), L["hand"] * max(sc, 0.8))
            limb(arms, [(s, 11.5), (e, 9), (w, 7)], SKIN)
            limb(arms, [(w, 7), (h, 7.5)], SKIN)
            arms.add(poly_path(capsule_pts(s, 13.5, add(s, vec(ang[0]), L["uarm"] * 0.33), 11.5)), TOP)
        r = L["head"]
        head = f'<circle cx="{f(hc[0])}" cy="{f(hc[1])}" r="{r}" fill="{SKIN}" stroke="{INK}" stroke-width="{OUTLINE}"/>'
        if self.back:
            head += (f'<path d="M{f(hc[0]-r)},{f(hc[1]+2)} A{r},{r} 0 0 1 {f(hc[0]+r)},{f(hc[1]+2)} '
                     f'Q{f(hc[0])},{f(hc[1]+r*0.95)} {f(hc[0]-r)},{f(hc[1]+2)} Z" fill="{HAIR}" stroke="{INK}" stroke-width="{OUTLINE*0.6}"/>')
        else:
            head += (f'<path d="M{f(hc[0]-r)},{f(hc[1]+3)} A{r},{r} 0 0 1 {f(hc[0]+r)},{f(hc[1]+3)} '
                     f'Q{f(hc[0]+r*0.3)},{f(hc[1]-r*0.55)} {f(hc[0]-r*0.2)},{f(hc[1]-r*0.35)} '
                     f'Q{f(hc[0]-r*0.7)},{f(hc[1]-r*0.2)} {f(hc[0]-r)},{f(hc[1]+3)} Z" fill="{HAIR}" stroke="{INK}" stroke-width="{OUTLINE*0.6}"/>')
            for sx in (-1, 1):
                head += f'<circle cx="{f(hc[0]+sx*r*0.35)}" cy="{f(hc[1]+r*0.15)}" r="1.8" fill="{INK}"/>'
            head += (f'<path d="M{f(hc[0]-r*0.28)},{f(hc[1]+r*0.5)} Q{f(hc[0])},{f(hc[1]+r*0.65)} '
                     f'{f(hc[0]+r*0.28)},{f(hc[1]+r*0.5)}" fill="none" stroke="{INK}" stroke-width="1.6" stroke-linecap="round"/>')
        return legs.svg() + body.svg() + head + arms.svg()


# ---------------------------------------------------------------- props ----
def floor(y, x0=0, x1=400):
    return (f'<line x1="{x0}" y1="{y}" x2="{x1}" y2="{y}" stroke="{PROP_DARK}" stroke-width="3" stroke-linecap="round"/>')


def mat(y, x0, x1):
    return (f'<rect x="{x0}" y="{y-5}" width="{x1-x0}" height="7" rx="3" fill="#d8c3bc" stroke="{PROP_DARK}" stroke-width="1.5"/>'
            + floor(y + 2, x0 - 30, x1 + 30))


def wall_side(x, y0, y1, side=-1):
    w = 18
    xx = x if side > 0 else x - w
    return (f'<rect x="{xx}" y="{y0}" width="{w}" height="{y1-y0}" fill="{PROP}" stroke="{PROP_DARK}" stroke-width="2"/>')


def wall_back(x0, y0, x1, y1):
    return (f'<rect x="{x0}" y="{y0}" width="{x1-x0}" height="{y1-y0}" rx="4" fill="{PROP}" stroke="{PROP_DARK}" stroke-width="2"/>')


def bar_side(c, posts=True):
    s = f'<circle cx="{c[0]}" cy="{c[1]}" r="7" fill="{PROP_DARK}" stroke="{INK}" stroke-width="2"/>'
    return s


def bar_front(y, x0, x1):
    return (f'<rect x="{x0-10}" y="{y-40}" width="10" height="46" fill="{PROP}" stroke="{PROP_DARK}" stroke-width="2"/>'
            f'<rect x="{x1}" y="{y-40}" width="10" height="46" fill="{PROP}" stroke="{PROP_DARK}" stroke-width="2"/>'
            f'<rect x="{x0}" y="{y-6}" width="{x1-x0}" height="12" rx="6" fill="{PROP_DARK}" stroke="{INK}" stroke-width="2"/>')


def band_path(d, width=6):
    return f'<path d="{d}" fill="none" stroke="{BAND}" stroke-width="{width}" stroke-linecap="round" stroke-linejoin="round" opacity="0.95"/>'


def arrow(d, color=ACCENT, width=3.5):
    return (f'<path d="{d}" fill="none" stroke="{color}" stroke-width="{width}" stroke-linecap="round" '
            f'marker-end="url(#ah)"/>')


def label(x, y, text, size=15, color=INK, anchor="middle", weight=600):
    return (f'<text x="{x}" y="{y}" font-family="Nunito Sans, Liberation Sans, Arial, sans-serif" font-size="{size}" '
            f'font-weight="{weight}" fill="{color}" text-anchor="{anchor}">{text}</text>')


def defs():
    return (f'<defs><marker id="ah" viewBox="0 0 10 10" refX="6" refY="5" markerWidth="4" markerHeight="4" orient="auto-start-reverse">'
            f'<path d="M0,0 L10,5 L0,10 z" fill="{ACCENT}"/></marker>'
            f'<marker id="ahg" viewBox="0 0 10 10" refX="6" refY="5" markerWidth="4" markerHeight="4" orient="auto-start-reverse">'
            f'<path d="M0,0 L10,5 L0,10 z" fill="{GOOD}"/></marker></defs>')


def panel(content, w=320, h=300, tag=None):
    s = f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}">' + defs()
    s += '<g class="content">' + content + '</g>'
    if tag:
        tw = len(tag) * 9.6 + 24
        s += (f'<g class="tag"><rect x="0" y="0" rx="13" width="{tw:.0f}" height="27" fill="{INK}"/>'
              + label(tw / 2, 19, tag, 14.5, "#fff", "middle", 800) + '</g>')
    return s + "</svg>"
