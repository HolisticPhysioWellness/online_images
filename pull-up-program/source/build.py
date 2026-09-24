"""Build the pull-up program handout (HTML -> PDF) from the exercise drawings."""
import html
import re
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

HERE = os.path.dirname(os.path.abspath(__file__))

CLINIC = "Holistic Physiotherapy &amp; Wellness"
SITE = "holisticphysiowellness.ca"

# --------------------------------------------------------------------------
# Exercise content
# --------------------------------------------------------------------------
E = {}


def ex(key, title, dose, steps, tip=None, easier=None, harder=None, img=None, caps=None):
    E[key] = dict(title=title, dose=dose, steps=steps, tip=tip, easier=easier, harder=harder,
                  img=img or key, caps=caps)


ex("90-90-breathing", "90/90 breathing", "5 slow breaths",
   ["Lie on your back with your feet flat on a wall and your hips and knees bent to 90°. Rest one hand on your lower ribs.",
    "Breathe in through your nose for 4 seconds. Feel your ribs widen to the sides and into the floor.",
    "Breathe out slowly through your mouth for 6–8 seconds, as if fogging a mirror. Let your lower ribs drop down and in. Your low back settles gently toward the floor.",
    "Pause for 2–3 seconds before the next breath."],
   tip="This sets your ribs in the 'down' position you will keep during every exercise.")

ex("cat-camel", "Cat–camel", "8–10 slow reps",
   ["Start on your hands and knees, with your hands under your shoulders and your knees under your hips.",
    "Breathe out as you round your back up, tucking your tailbone and chin.",
    "Breathe in as you let your back gently sag and look slightly forward.",
    "Move slowly and only in a range that feels comfortable."])

ex("band-pull-aparts", "Band pull-aparts", "2 sets × 12–15",
   ["Hold a light band at shoulder height. Keep your arms straight and your hands shoulder-width apart.",
    "Pull the band apart until it reaches your chest, drawing your shoulder blades back and down.",
    "Keep your ribs down and your shoulders away from your ears. Return slowly."],
   easier="Use a lighter band or start with your hands wider apart.")

ex("scapular-push-ups", "Scapular push-ups", "2 sets × 10",
   ["Start on your hands and knees (or on your toes), with your hands under your shoulders and your arms straight.",
    "Keeping your elbows straight, let your chest sink between your shoulder blades.",
    "Push the floor away to spread your shoulder blades apart. Only your shoulder blades move."],
   harder="Do these from your toes in a full plank.")

ex("dead-bug", "Dead bug", "2 sets × 6 each side",
   ["Lie on your back with your arms pointing to the ceiling and your hips and knees at 90°.",
    "Breathe out to set your ribs down and your low back gently into the floor.",
    "Slowly reach one arm overhead and the opposite leg out, only as far as your low back stays down.",
    "Return to the start and switch sides. Breathe out on each reach."],
   easier="Move only your legs, or keep the knee bent as you tap your heel toward the floor.")

ex("scapular-pull-ups", "Scapular pull-ups (active hang)", "3 sets × 5–8, 2-second hold",
   ["Hang with a full grip, thumbs wrapped around the bar and hands just wider than your shoulders.",
    "Without bending your elbows, pull your shoulders down away from your ears. Your body will rise a few centimetres.",
    "Hold for 2 seconds with your ribs down and your legs together slightly in front. Lower with control.",
    "Finish with 2 active hangs of 15–30 seconds, holding the 'active' position."],
   tip="Keep your toes on a box if your grip or shoulders need a break.")

ex("band-lat-pulldown", "Band lat pull-down", "3 sets × 10–12",
   ["Loop a band over the pull-up bar. Kneel tall facing the bar, with your ribs down.",
    "Start with your arms reaching up. Pull your elbows down and back toward your ribs until your hands are near your shoulders.",
    "Squeeze for 1 second, then return over 2 seconds without shrugging."],
   harder="Use a heavier band, or pause for 3 seconds at the bottom.")

ex("inverted-row", "Inverted table row", "3 sets × 6–10",
   ["First check that the table is heavy and will not tip. Have someone sit on it if you are unsure. A low bar at the gym also works.",
    "Lie under the edge and grip it with your hands shoulder-width apart. Keep your body straight from ears to ankles and squeeze your glutes.",
    "Pull your chest to the edge, elbows angled toward your ribs. Pause for 1 second, then lower over 3 seconds."],
   easier="Bend your knees with your feet flat.", harder="Straighten your legs, or add a 3-second pause at the top.")

ex("prone-y-raise", "Prone Y raise", "2 sets × 10, 2-second hold",
   ["Lie face down with your forehead on a folded towel and your arms overhead in a 'Y', thumbs up.",
    "Draw your shoulder blades down toward your back pockets, then lift your arms a few centimetres.",
    "Hold for 2 seconds and lower slowly. Keep your neck long and don't arch your back."],
   tip="These target the lower trapezius, which helps start the pull-up.")

ex("hollow-body", "Hollow body hold", "3 sets × 15–30 seconds",
   ["Lie on your back. Breathe out to set your ribs down and press your low back into the floor.",
    "Lift your head and shoulders. Start tucked: knees over hips, arms reaching toward your feet.",
    "Hold with small breaths. Stop the set if your low back lifts or your ribs flare."],
   harder="Straighten one leg, then both. Then take your arms overhead ('Full').")

ex("band-assisted-pull-up", "Band-assisted pull-up", "3 sets × 4–6",
   ["Loop a strong band over the bar. Kneel into the loop with one knee (or put your foot in it).",
    "Start from an active hang: shoulders down, ribs down.",
    "Pull your elbows down to your ribs until your chin clears the bar. Lower over 3 seconds.",
    "Choose a band where the last rep is hard but still clean."],
   tip="Move to a lighter band once you can do 3 × 6 with good form.")

ex("flexed-arm-hang", "Flexed-arm hang", "3 sets × 10–20 seconds",
   ["Step up on a sturdy box or chair so your chin is above the bar.",
    "Grip the bar, lift your feet and hold. Keep your shoulders down, your elbows tucked in and your ribs down.",
    "Step back down to finish. Don't drop."],
   tip="Keep breathing. Don't hold your breath.")

ex("negative-pull-up", "Negative (lowering) pull-up", "3 sets × 3, lowering over 3–5 seconds",
   ["Step up to the top position with your chin over the bar.",
    "Lift your feet and lower yourself slowly, counting, until your arms are straight and your shoulders are still 'active'.",
    "Step back up for the next rep. Don't jump up from the bottom."],
   tip="Slow lowering (eccentric) work builds strength quickly. Expect some muscle soreness in the first week.")

ex("slow-negatives", "Slow negatives with pauses", "3 sets × 2, lowering over 6–8 seconds",
   ["Start at the top as for negatives.",
    "Lower slowly, pausing for 2 seconds at the top, at halfway (elbows at 90°) and just before your arms are straight.",
    "Step back up between reps."],
   img="negative-pull-up")

ex("pull-up", "Pull-up attempts", "3–5 single attempts, 2–3 minutes' rest",
   ["Do these straight after your warm-up, while you are fresh.",
    "From an active hang, pull your elbows down to your ribs and drive your chest toward the bar.",
    "If you don't reach the bar, pull as high as you can, hold for 2 seconds, then lower slowly. That still counts as training."],
   tip="Test day: in week 12 (or once you can hold a flexed-arm hang for 30 s and lower over 8 s), rest well, warm up, and give it 1–2 attempts.")

# --------------------------------------------------------------------------
# Rendering helpers
# --------------------------------------------------------------------------


def load(key):
    out = []
    i = 1
    while os.path.exists(os.path.join(HERE, "svg_cropped", f"{key}-{i}.svg")):
        out.append(open(os.path.join(HERE, "svg_cropped", f"{key}-{i}.svg")).read())
        i += 1
    return out


def aspect(svg):
    vb = re.search(r'viewBox="([^"]+)"', svg).group(1).split()
    return float(vb[2]) / float(vb[3])


def imgs(key, cls="pair"):
    ps = load(key)
    return f'<div class="{cls}">' + "".join(f'<div class="fig">{p}</div>' for p in ps) + "</div>"


def card(key, num=None, dose=None):
    e = E[key]
    steps = "".join(f"<li>{s}</li>" for s in e["steps"])
    extra = ""
    if e["tip"]:
        extra += f'<p class="note"><b>Tip:</b> {e["tip"]}</p>'
    if e["easier"]:
        extra += f'<p class="note"><b>Easier:</b> {e["easier"]}</p>'
    if e["harder"]:
        extra += f'<p class="note"><b>Harder:</b> {e["harder"]}</p>'
    n = f'<span class="num">{num}</span>' if num else ""
    wide = aspect(load(e["img"])[0]) >= 1.25
    if wide:
        return f'''<section class="card wide">
  {imgs(e["img"])}
  <div class="txt">
    <div class="lead"><h3>{n}{e["title"]}</h3><div class="dose">{dose or e["dose"]}</div>{extra}</div>
    <ol>{steps}</ol>
  </div>
</section>'''
    return f'''<section class="card">
  {imgs(e["img"])}
  <div class="txt">
    <h3>{n}{e["title"]}</h3>
    <div class="dose">{dose or e["dose"]}</div>
    <ol>{steps}</ol>{extra}
  </div>
</section>'''


def header(kicker, title, sub=""):
    return f'''<header class="ph">
  <div class="brand"><div class="logo" aria-label="clinic logo">HP</div><div>{CLINIC}</div></div>
  <div class="kicker">{kicker}</div>
</header>
<h2 class="ptitle">{title}</h2>{f'<p class="psub">{sub}</p>' if sub else ''}'''


def footer(n):
    return f'<footer class="pf"><span>Road to Your First Pull-Up</span><span>{SITE}</span><span>Page {n}</span></footer>'


def page(n, body, cls=""):
    return f'<div class="page {cls}">{body}{footer(n)}</div>'


def summary(rows):
    r = "".join(f"<tr><td>{a}</td><td>{b}</td></tr>" for a, b in rows)
    return f'<table class="sum"><thead><tr><th>Exercise</th><th>Sets × reps / time</th></tr></thead><tbody>{r}</tbody></table>'


def gate(items):
    return ('<div class="gate"><b>Ready for the next phase when you can do:</b><ul>'
            + "".join(f"<li>{i}</li>" for i in items) + "</ul></div>")


# --------------------------------------------------------------------------
# Pages
# --------------------------------------------------------------------------
pages = []

# 1 - overview
pages.append(f'''
<header class="ph">
  <div class="brand"><div class="logo">HP</div><div>{CLINIC}</div></div>
  <div class="kicker">Home exercise program</div>
</header>
<div class="hero">
  <div>
    <h1>Road to Your<br>First Pull-Up</h1>
    <p class="lede">A 12-week bodyweight program for people who can hang from a bar but can't pull up yet. It takes 2 sessions a week, plus a few minutes of daily posture work.</p>
    <div class="fields">
      <div><span>Name</span></div><div><span>Physiotherapist</span></div>
      <div><span>Start date</span></div><div><span>Target test date</span></div>
    </div>
  </div>
  <div class="herofig">{load("pull-up")[1]}</div>
</div>

<div class="grid3">
  <div class="phase"><div class="pn">Phase 1</div><div class="pw">Weeks 1–4</div><b>Foundation</b><p>Shoulder blade control, grip, pulling strength and a strong trunk.</p></div>
  <div class="phase"><div class="pn">Phase 2</div><div class="pw">Weeks 5–8</div><b>Build the pull</b><p>Band-assisted pull-ups, top-position holds and slow lowering.</p></div>
  <div class="phase"><div class="pn">Phase 3</div><div class="pw">Weeks 9–12</div><b>First pull-up</b><p>Less help from the band, paused negatives and pull-up attempts.</p></div>
</div>

<div class="two">
  <div class="box">
    <h4>Your week</h4>
    <table class="week">
      <tr><th>Every day</th><td>Wall angels: 2–3 minutes (page 2)</td></tr>
      <tr><th>Day A</th><td>Warm-up (10 min) + phase workout (25–35 min)</td></tr>
      <tr><th>Day B</th><td>Same as Day A, 2–3 days later (e.g. Mon &amp; Thu)</td></tr>
    </table>
    <h4>Equipment</h4>
    <p>Pull-up bar · resistance loop bands (light, medium, heavy) · wall · mat · sturdy table · step or sturdy box</p>
  </div>
  <div class="box">
    <h4>How hard?</h4>
    <p>Finish each set with 2–3 good reps left in the tank, about <b>7–8 out of 10</b> effort. Rest 90 seconds to 2 minutes between pulling sets.</p>
    <h4>When to move on</h4>
    <p>Each phase ends with a checklist. Move on when you pass it, not just because the weeks are up. Taking 8 weeks or more than 12 is normal.</p>
  </div>
</div>

<div class="safety">
  <h4>Safety: stop and contact your physiotherapist if you notice</h4>
  <ul>
    <li>sharp or pinching pain in your shoulder, elbow or neck</li>
    <li>pins and needles or numbness down your arm</li>
    <li>your shoulder feels like it slips or gives way</li>
    <li>pain that is worse the next morning</li>
  </ul>
  <p>Mild muscle soreness is normal. Any discomfort during exercise should stay at <b>3/10 or less</b> and settle by the next day. Check the band and bar before every session.</p>
</div>
''')

# 2 - wall angels
pages.append(header("Daily posture exercise", "Wall angels",
                     "Do these every day, and as the last part of every warm-up. They teach your shoulder blades to move overhead while your ribs stay down. That's the position you want when you hang from the bar.") + f'''
<div class="wa">
  <div class="wa-imgs">{imgs("wall-angels")}</div>
  <div class="txt">
    <div class="dose">Daily · 2 sets × 8–10 slow reps (3 seconds up, 3 seconds down)</div>
    <h4>Set-up</h4>
    <ol>
      <li>Stand with your heels about a hand's length from the wall and your knees soft.</li>
      <li>Rest the back of your head, your upper back and your tailbone on the wall.</li>
      <li>Start in the "goalpost" position: elbows at shoulder height and bent to 90°, forearms toward the wall.</li>
    </ol>
    <h4>Move</h4>
    <ol start="4">
      <li>Slowly slide your arms up into a "Y". Stop where your ribs start to lift or your arms leave the wall.</li>
      <li>Pause for 2 seconds and breathe out. Then slide down, drawing your elbows toward your back pockets.</li>
    </ol>
  </div>
</div>
<div class="ribs">
  <div class="ribs-imgs">{imgs("wall-angels-ribs")}</div>
  <div class="txt">
    <h4 class="accent">Keep your ribs down: stop them flaring</h4>
    <ul class="checks">
      <li><b>Breathe out first.</b> Before each rep, breathe out fully through your mouth and feel your lower ribs soften down toward your hips. Keep them there as your arms rise.</li>
      <li><b>Zip up gently.</b> Tighten your lower tummy to about 20–30% effort. That's just enough to stop your ribs popping forward, not a hard brace.</li>
      <li><b>Keep the low-back gap small.</b> A flat hand should just fit behind your low back. If the gap grows as your arms go up, you've gone too high.</li>
      <li><b>Keep your chin gently tucked</b> and the back of your head on the wall. Don't let your chin poke up.</li>
      <li><b>Work within your range.</b> Your hands don't have to touch the wall at the top. Ribs down matters more than height.</li>
    </ul>
    <p class="note"><b>Easier:</b> step your feet further from the wall and bend your knees more, or do the same movement lying on your back with your knees bent ("floor angels").<br>
    <b>Harder:</b> hold the top "Y" for a 5-second breath out before sliding down.</p>
  </div>
</div>''')

# 3-4 - warm-up
pages.append(header("Every session · about 10 minutes", "Warm-up",
                     "Do these in order before every workout. Finish with 1 set of 8 wall angels.")
             + card("90-90-breathing", 1) + card("cat-camel", 2) + card("band-pull-aparts", 3))
pages.append(header("Warm-up, continued", "Warm-up")
             + card("scapular-push-ups", 4) + card("dead-bug", 5)
             + '<div class="finish"><b>6 · Wall angels</b> 1 set × 8 (page 2). Then start your phase workout.</div>')

# Phase 1
p1_sum = summary([("Scapular pull-ups + active hang", "3 × 5–8 (2-second hold), then 2 × 15–30 s hang"),
                  ("Band lat pull-down", "3 × 10–12"), ("Prone Y raise", "2 × 10 (2-second hold)"),
                  ("Inverted table row", "3 × 6–10"), ("Hollow body hold (tucked)", "3 × 15–30 s")])
pages.append(header("Phase 1 · Weeks 1–4", "Foundation",
                     "Build shoulder blade control, grip endurance and basic pulling strength.")
             + p1_sum + card("scapular-pull-ups", "A") + card("band-lat-pulldown", "B") + card("prone-y-raise", "C"))
pages.append(header("Phase 1 · Weeks 1–4", "Foundation, continued")
             + card("inverted-row", "D") + card("hollow-body", "E"))
pages[-1] += gate(["3 × 8 scapular pull-ups with 2-second holds", "a 30-second active hang",
                   "3 × 10 table rows", "a 30-second tucked hollow hold"])

# Phase 2
p2_sum = summary([("Band-assisted pull-up", "3 × 4–6"), ("Flexed-arm hang", "3 × 10–20 s"),
                  ("Negative pull-up", "3 × 3 (3–5 s lower)"), ("Inverted table row, legs straight", "3 × 8–10"),
                  ("Hollow body hold, legs straighter", "3 × 20–30 s")])
pages.append(header("Phase 2 · Weeks 5–8", "Build the pull",
                     "Practise the whole pull-up path with help from a band, and build strength at the top and on the way down.")
             + p2_sum + card("band-assisted-pull-up", "A") + card("flexed-arm-hang", "B"))
pages.append(header("Phase 2 · Weeks 5–8", "Build the pull, continued")
             + card("negative-pull-up", "C")
             + '<div class="finish"><b>D · Inverted table row</b> 3 × 8–10 with legs straight (page 6). &nbsp; <b>E · Hollow body hold</b> 3 × 20–30 s, straighten your legs as you are able (page 6).</div>'
             + gate(["a 20-second flexed-arm hang", "3 × 3 negatives, lowering over 5 seconds",
                     "3 × 6 band-assisted pull-ups with a medium band"]))

# Phase 3
p3_sum = summary([("Pull-up attempts", "3–5 singles, 2–3 min rest"), ("Slow negatives with pauses", "3 × 2 (6–8 s lower)"),
                  ("Light band-assisted pull-up", "3 × 5–6"), ("Inverted table row", "3 × 10"),
                  ("Hollow body hold (full)", "3 × 30 s")])
pages.append(header("Phase 3 · Weeks 9–12", "Your first pull-up",
                     "Less help, more control. Keep every rep clean. Grinding out ugly reps won't get you there faster.")
             + p3_sum + card("pull-up", "A") + card("slow-negatives", "B"))
pages.append(header("Phase 3 · Weeks 9–12", "Your first pull-up, continued")
             + card("band-assisted-pull-up", "C", "3 sets × 5–6 with your lightest band. Go down a band every 1–2 weeks.")
             + card("hollow-body", "D", "3 sets × 30 seconds, working toward the full position")
             + '<div class="finish"><b>E · Inverted table row</b> 3 × 10 with legs straight (page 6). &nbsp; <b>Next goal after your first pull-up:</b> 3 sets of 1–2 reps, then work toward 3 reps in a row.</div>')

# Log + references
rows = "".join(f"<tr><td>{w}</td><td></td><td></td><td></td><td></td><td></td><td></td></tr>" for w in range(1, 13))
pages.append(header("Track your progress", "Progress log",
                     "Write down your best set for each session. Small changes add up.") + f'''
<table class="log">
<thead><tr><th>Wk</th><th>Date</th><th>Main pull<br><small>(scap pull-ups / band pull-ups / attempts)</small></th><th>Hang / hold<br><small>(seconds)</small></th><th>Negatives<br><small>(seconds lowering)</small></th><th>Rows · hollow</th><th>Pain 0–10 · notes</th></tr></thead>
<tbody>{rows}</tbody></table>
<div class="refs">
  <h4>Why these exercises: the research</h4>
  <ul>
    <li>Pull-ups mainly work the lats (about 117–130% of maximum voluntary contraction), biceps and infraspinatus. The <b>lower trapezius and pecs switch on first</b> to start the pull, which is why scapular pull-ups and prone Y raises come first. <span>Youdas JW et al. J Strength Cond Res 2010;24(12):3404-14. doi:10.1519/JSC.0b013e3181f1598c</span></li>
    <li>Different grips (overhand, underhand, neutral) activate the muscles similarly over a full rep, so use whichever grip is comfortable. <span>Dickie JA et al. J Electromyogr Kinesiol 2017;32:30-36. doi:10.1016/j.jelekin.2016.11.004</span></li>
    <li>Face-down (prone) exercises target the middle and lower trapezius with little upper-trapezius (shrugging) activity. <span>Cools AM et al. Am J Sports Med 2007;35(10):1744-51. doi:10.1177/0363546507303560</span></li>
    <li>Wall slides activate the serratus anterior, and push-up "plus" variations favour serratus over upper trapezius. <span>Castelein B et al. J Orthop Sports Phys Ther 2016;46(3):184-93. doi:10.2519/jospt.2016.5927 · Maenhout A et al. Br J Sports Med 2010;44(14):1010-5. doi:10.1136/bjsm.2009.062810</span></li>
    <li>Gently tightening the abdominals increased serratus and trapezius activity during wall slides. This supports the "ribs down, zip up" cue. <span>Vega Toro AS et al. Man Ther 2016;25:11-8. doi:10.1016/j.math.2016.05.331</span></li>
    <li>Eccentric (lowering) training gives strong strength gains, which is why negatives are used in Phases 2–3. <span>Douglas J et al. Sports Med 2017;47(5):917-41. doi:10.1007/s40279-016-0628-4</span></li>
  </ul>
  <p class="small">References sourced via PubMed. This program is general education prepared by {CLINIC}. It does not replace an individual assessment. Talk to your physiotherapist before starting if you have had shoulder surgery, a dislocation or ongoing neck or shoulder pain.</p>
</div>''')

CSS = open(os.path.join(HERE, "handout.css")).read()
FONTS = open(os.path.join(HERE, "fonts.css")).read()
doc = ["<!doctype html><html lang='en'><head><meta charset='utf-8'><title>Road to Your First Pull-Up</title>",
       f"<style>{FONTS}\n{CSS}</style></head><body>"]
for i, p in enumerate(pages, 1):
    doc.append(page(i, p, "cover" if i == 1 else ""))
doc.append("</body></html>")
open(os.path.join(HERE, "handout.html"), "w").write("".join(doc))
print("pages:", len(pages))
