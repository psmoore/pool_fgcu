#!/usr/bin/env python3
"""Build the Lee County/FGCU Aquatics Center preview: the Aquatics page and the pages it links to,
with every hour, lane count and course date read live from Pool Relay by finder.js (data-live,
#today, #week). Nothing about WHEN the pool is open is typed here; only fees, policies and facts
about the water. Run: python3 build.py"""
import html, json

E = html.escape
VIEW = "nspJC3cZSItvCm4H1MvKNY"  # Pool Relay: Lee County/FGCU Aquatics Center, lane by lane (public)
FAC = "Lee County/FGCU Aquatics Center"
SITE = "https://www.fgcu.edu/university-recreation-and-wellness/aquatics/"
POOLS = json.dumps([dict(slug="fgcu", name=FAC, facility=FAC, hideHead=True,
                         address="10501 FGCU Blvd S, Fort Myers, FL 33965", phone="(239) 590-7700")])

def live(mode, **kw):
    attrs = "".join(f' data-{k.replace("_", "-")}="{E(str(v))}"' for k, v in kw.items())
    return f'data-live="{mode}" data-view="{VIEW}" data-pool="fgcu"{attrs}'

PAGES = [  # (file, menu label, title)
    ("index.html", "Aquatics", "Aquatics Center"),
    ("lane-availability.html", "Lane Availability", "Lane Availability"),
    ("operating-hours.html", "Operating Hours", "Aquatics Center Hours"),
    ("swim-lessons.html", "Swim Lessons", "Swim Lessons"),
    ("certification-courses.html", "Certification Courses", "Certification Courses"),
]

def page(file, crumb, body):
    title = next(t for f, _, t in PAGES if f == file)
    menu = "".join(f'<a class="{"sub" if f != "index.html" else ""}{" here" if f == file else ""}" href="{f}">{E(label)}</a>'
                   for f, label, _ in PAGES)
    doc = f"""<!doctype html>
<!-- UNOFFICIAL PREVIEW. Not a Florida Gulf Coast University website. A mock-up of {SITE}
     with the Aquatics Center's lane availability and hours on one live Pool Relay schedule. -->
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="robots" content="noindex, nofollow">
<title>{E(title)} | FGCU preview</title>
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Jost:wght@400;500;600&family=Source+Sans+3:wght@400;600;700&display=swap" rel="stylesheet">
<link rel="stylesheet" href="style.css">
</head>
<body>
<div class="preview-note"><b>Unofficial preview.</b> Not an FGCU page &mdash; a mock-up of <a href="{SITE}" target="_blank" rel="noopener noreferrer">the Aquatics Center pages</a> with every hour and lane count read from one live schedule.</div>
<div class="util"><div class="in"><span>APPLY</span><span>DIRECTORY</span><span>MYFGCU</span></div></div>
<header class="site"><div class="hdr">
  <a class="brand" href="index.html"><img src="https://fgcucdn.fgcu.edu/_resources/images/fgcu-lettermark-fullcolor-logo.svg" alt="FGCU" onerror="this.parentNode.classList.add('noimg')"><span class="wm">FGCU</span></a>
  <nav class="nav" aria-label="Main"><span>About</span><span>Academics</span><span>Admissions &amp; Aid</span><span>Student Life</span><span>Community</span><span>Resources</span><span>Athletics</span></nav>
</div></header>
<div class="band"><h1>{E(title)}</h1></div>
<div class="crumbrow"><span class="tab">&#9776;&nbsp; Menu</span>
  <div class="crumbs"><a href="#">Florida Gulf Coast University</a> › <a href="#">University Recreation &amp; Wellness</a> › {crumb}</div></div>
<div class="wrap"><div class="cols">
  <nav class="menu" aria-label="Aquatics">{menu}</nav>
  <main class="sheet">{body}</main>
</div></div>
<footer class="site"><div class="in">
  <div><h4>Lee County/FGCU Aquatics Center</h4><p>10501 FGCU Blvd S<br>Fort Myers, FL 33965<br>(239) 590-7700</p></div>
  <div><h4>University Recreation &amp; Wellness</h4><p>Florida Gulf Coast University</p></div>
  <div><h4>About this preview</h4><p>Built to demonstrate embedded <a href="https://www.poolrelay.com" target="_blank" rel="noopener">Pool Relay</a> schedules. Not operated by or affiliated with Florida Gulf Coast University or Lee County. Schedule entered from FGCU's lane availability calendar, Operating Hours and Certification Courses pages on October 23, 2026.</p></div>
</div></footer>
<script>window.POOLS = {POOLS};</script>
<script src="finder.js"></script>
</body>
</html>
"""
    open(file, "w").write(doc)

HOURS_BOX = f"""<aside class="hours">
        <h2>Open swim hours</h2>
        <div {live("hours", format="dl", title="Lap & Rec Swim")}><p class="muted">…</p></div>
        <div class="adjusted" {live("exceptions", title="Lap & Rec Swim")} hidden></div>
        <p class="muted small" style="margin:8px 0 0">Scheduled through <span {live("last", title="Lap & Rec Swim")}>…</span>. The facility closes at 55&deg;F and below, and for 30 minutes after lightning within 10 miles.</p>
      </aside>"""

NOW_BOX = f"""<section class="now" aria-live="polite">
        <h2>Right now</h2>
        <div id="today" data-view="{VIEW}" data-pool="fgcu"><p class="muted">Loading today’s schedule…</p></div>
      </section>"""

# ── Aquatics ─────────────────────────────────────────────────────────────────
page("index.html", "Aquatics", f"""
    <h2>Dive in — We're Here for the Whole Community</h2>
    <p class="lede">The Lee County/FGCU Aquatics Center opened in 2004 with over 1 million gallons of water. The 50-meter pool hosts
      meets and practices and serves the community's lap swimmers; the 25-yard pool and diving well is for recreational swimmers and divers.</p>
    <div class="top2">
      {NOW_BOX}
      {HOURS_BOX}
    </div>
    <div class="btns"><a class="btn" href="lane-availability.html">Daily lane availability</a><a class="btn blue" href="operating-hours.html">Hours of operation</a></div>

    <h2>The water</h2>
    <div class="cards3">
      <div class="card"><h3>50-meter pool</h3><p>8 long-course lanes, or 20 short-course lanes with the bulkhead in. Which layout it's in shows on the lane calendar.</p></div>
      <div class="card"><h3>25-yard pool &amp; diving well</h3><p>8 lanes, with 1-meter and 3-meter diving boards.</p></div>
      <div class="card"><h3>Heated and chilled</h3><p>Pool water is heated or chilled depending on the season. Locker rooms, a family restroom with shower, loungers and picnic tables.</p></div>
    </div>

    <h2>Getting in</h2>
    <p>FGCU students get in with their Eagle ID. Faculty, staff, Southwest Florida residents and visitors pay a daily fee or buy a membership.</p>
    <div class="fees">
      <table><tr><th>Daily fee</th><th></th></tr>
        <tr><td>Adult guest pass</td><td>$5</td></tr><tr><td>Senior (55+) or child (under 12)</td><td>$4</td></tr></table>
      <table><tr><th>Aquatics Center membership</th><th></th></tr>
        <tr><td>Month</td><td>$28</td></tr><tr><td>Year</td><td>$160</td></tr><tr><td>Monthly auto pay</td><td>$13.33</td></tr>
        <tr><td>Youth (member's dependent), month / year</td><td>$10 / $80</td></tr></table>
    </div>
    <p class="muted small">Prices include sales tax. FGCU faculty, staff and alumni, military, seniors 55+ and Plus Ones get 25% off the adult membership.</p>

    <h2>Policies</h2>
    <details class="more"><summary>General policies</summary><div><ul>
      <li>Check in at the front desk with a valid FGCU ID or pass.</li>
      <li>Children younger than 13 must be under direct adult supervision; children younger than 5 must have an adult with them in the water.</li>
      <li>No food, glass, gum, tobacco or alcohol on deck; plastic water bottles with a lid are fine.</li>
      <li>Return borrowed kickboards, paddles, pull buoys and aqua joggers to the front desk.</li>
      <li>No rain passes or refunds when weather closes the facility.</li></ul></div></details>
    <details class="more"><summary>Pool policies</summary><div><ul>
      <li>A lifeguard must be on duty. Lap swimmers may have to share lanes and circle swim at busy times.</li>
      <li>Swimwear is required; infants and toddlers need swim diapers.</li>
      <li>No running, rough play, starting blocks, diving into shallow water, swimming under the bulkhead, or hypoxic breath-holding.</li></ul></div></details>
    <details class="more"><summary>Diving board policies</summary><div><ul>
      <li>Children 13 and younger may need to pass a swim test first. The 3-meter board needs staff permission.</li>
      <li>One person on the board; one bounce; forward dives only; leave the diving area right away.</li>
      <li>The diving well may close for programs or open swim.</li></ul></div></details>

    <h2>More from Aquatics</h2>
    <div class="cards3">
      <div class="card"><h3>Swim lessons</h3><p>Group lessons for every age, and private lessons.</p><a href="swim-lessons.html">Learn more</a></div>
      <div class="card"><h3>Certification courses</h3><p>Red Cross lifeguard and water safety instructor training.</p><a href="certification-courses.html">Learn more</a></div>
      <div class="card"><h3>Facility rentals</h3><p>Training space for swim teams, and birthday parties.</p><a href="https://www.fgcu.edu/university-recreation-and-wellness/facilities/facilityreservations" target="_blank" rel="noopener">Learn more</a></div>
    </div>

    <h2>Aquatics staff</h2>
    <div class="staff"><div><b>Emma Reeners</b>Associate Director, Aquatics &amp; Adventure<br>(239) 590-7701</div>
      <div><b>Megan Price</b>Aquatics Coordinator<br>(239) 590-7629</div></div>

    <div class="replaces">
      <h2>What this replaces</h2>
      <ul>
        <li><b>Hours in two places that don't know about each other.</b> The Operating Hours page lists the fall open swim hours and a
          hand-typed "Upcoming Adjusted Hours" list (on October 23 it still listed October 21 and 22). The lane calendar is a separate Google
          Calendar. Here the hours, the adjusted days and the lane counts are one schedule: the hours box above is computed from it.</li>
        <li><b>A lane calendar a week deep.</b> Lane counts are posted about a week ahead; beyond that the calendar holds only "POOL CLOSED"
          on Sundays, into January.</li>
        <li><b>Lane counts as typed titles.</b> Each block is a title like "25Y: 4 Lanes", typed as "25Y", "25 Y" and "25&nbsp;&nbsp;Y", "SC" and "SCY",
          "50M" and "50m". Some October blocks said "50M: 10 LC Lanes", but FGCU's visitor page gives the 50-meter pool 8 long-course lanes.
          Here a block is booked on real lanes in the pool's real layout, so the count can't disagree with the pool.</li>
        <li><b>Which pool is which, by color.</b> The calendar tells the pools apart only by green and blue, and the page says to phone
          (239) 590-7700 to learn whether the 50-meter pool is short course or long course. Here each block names its pool and layout.</li>
        <li><b>Courses on a third page.</b> The lifeguard course dates are only on the Certification Courses page, not on the lane calendar
          or the hours, so nothing shows that a course is in the water on a Saturday when open swim is also listed.</li>
      </ul>
    </div>
""")

# ── Lane availability ────────────────────────────────────────────────────────
page("lane-availability.html", '<a href="index.html">Aquatics</a> › Lane Availability', f"""
    <p class="lede">How many lanes are open for lap and recreational swimming, in which pool, hour by hour. The same schedule
      drives this page, the hours, and the calendar below.</p>
    <div class="top2">
      {NOW_BOX}
      {HOURS_BOX}
    </div>
    <h2>This week, pool by pool</h2>
    <p class="lanes-legend">Lanes open to the public in each pool. Days where FGCU hasn't posted lane counts yet show the open swim hours under "Pool not posted yet".</p>
    <div id="week" data-view="{VIEW}" data-pools="50-Meter Pool|25-Yard Pool"><p class="muted">Loading the week…</p></div>
    <h2>Lane by lane</h2>
    <p class="muted small">Pick a day to see which lanes are open. The 50-meter pool shows the layout it's set up in that day: 20 short-course lanes or 8 long-course lanes.</p>
    <div class="frame"><iframe src="https://www.poolrelay.com/embed/{VIEW}" height="760" title="Lee County/FGCU Aquatics Center, lane by lane" loading="lazy"></iframe></div>
    <h2>Weather</h2>
    <div class="policy"><p><b>Lightning:</b> pools clear when lightning is detected within 10 miles and reopen 30 minutes after the last strike.</p>
      <p><b>Rain:</b> the facility stays open as long as the main drains are visible from the lifeguard stand.</p>
      <p><b>Temperature:</b> closed when the air is 55&deg;F or below.</p></div>
""")

# ── Operating hours ──────────────────────────────────────────────────────────
page("operating-hours.html", 'Operating Hours', f"""
    <p class="lede">All facility hours are subject to change without notice; this page always shows the current schedule. Other University
      Recreation &amp; Wellness facilities are on FGCU's <a href="https://www.fgcu.edu/university-recreation-and-wellness/operatinghours" target="_blank" rel="noopener">Operating Hours page</a>.</p>
    <div class="top2">
      <section class="now"><h2>Regular open swim hours</h2><div class="hours" style="border:0;background:none;padding:0"><div {live("hours", format="dl", title="Lap & Rec Swim")}><p class="muted">…</p></div></div>
        <p class="muted small" style="margin:6px 0 0">Scheduled through <span {live("last", title="Lap & Rec Swim")}>…</span>.</p></section>
      <aside class="hours"><h2>Adjusted hours</h2><div class="adjusted" {live("exceptions", title="Lap & Rec Swim")}><p class="muted">None coming up.</p></div></aside>
    </div>
    <div class="btns"><a class="btn" href="lane-availability.html">Daily lane availability</a></div>
    <h2>Weather policies</h2>
    <div class="policy"><p><b>Lightning:</b> pools clear when lightning is detected within 10 miles and reopen 30 minutes after the last strike.</p>
      <p><b>Rain:</b> the facility stays open as long as the main drains are visible from the lifeguard stand.</p>
      <p><b>Temperature:</b> closed when the air is 55&deg;F or below.</p></div>
""")

# ── Swim lessons ─────────────────────────────────────────────────────────────
page("swim-lessons.html", '<a href="index.html">Aquatics</a> › Swim Lessons', f"""
    <p class="lede">Group lessons for every age and ability, and private lessons. Each group session is six 25-minute lessons.</p>
    <div class="now" style="margin-top:14px"><b>Next group lessons:</b> <span {live("dates", title="Swim Lessons", empty="None are on the schedule yet. When FGCU enters a session, its dates appear here.")}>…</span></div>
    <h2>Group lessons</h2>
    <p><b>$55</b> per session for the public, <b>$50</b> for FGCU affiliates. Registration closes the Friday before a session starts, at 3pm;
      late registration by phone ((239) 590-7701) adds a $10 fee.</p>
    <div class="cards3">
      <div class="card"><h3>Water Babies</h3><p>6 months to 3 years, with a parent or guardian in the water.</p></div>
      <div class="card"><h3>Preschool</h3><p>Ages 3 to 5, in beginner, intermediate and advanced levels.</p></div>
      <div class="card"><h3>Learn-to-Swim</h3><p>Ages 6 to 13, in four levels.</p></div>
      <div class="card"><h3>Adult</h3><p>13 and older, from beginner to stroke performance.</p></div>
    </div>
    <p class="muted small">Not sure of the level? Ask for an in-person swim test with a Water Safety Instructor: (239) 590-7701.</p>
    <h2>Private lessons</h2>
    <p>Half-hour lessons, one-on-one or for two swimmers of similar ability, scheduled with your instructor during open hours (not during group lessons).</p>
    <div class="fees"><table><tr><th>Lessons</th><th>1:1</th><th>1:2</th></tr>
      <tr><td>1 lesson</td><td>$35</td><td>$45</td></tr><tr><td>4 lessons</td><td>$120</td><td>$160</td></tr><tr><td>6 lessons</td><td>$165</td><td>$240</td></tr></table></div>
    <p class="muted small">FGCU students: $20 for a 30-minute lesson, shared with a friend at no extra cost. FGCU faculty and staff: $5 off any package.</p>
""")

# ── Certification courses ───────────────────────────────────────────────────
page("certification-courses.html", '<a href="index.html">Aquatics</a> › Certification Courses', f"""
    <h2>Lifeguard (American Red Cross, blended)</h2>
    <p>Prepares you to prevent, recognize and respond to aquatic and medical emergencies, and to give care until EMS arrives.
      Attendance is required on every day of a course.</p>
    <div class="now"><b>Coming course days:</b> <span {live("dates", title="Lifeguard Training", empty="No course is on the schedule right now.")}>…</span></div>
    <p><b>Cost:</b> $200 FGCU students, faculty and staff; $225 community.</p>
    <details class="more"><summary>Prerequisites</summary><div><ul>
      <li>Swim 150 yards continuously (front crawl, breaststroke or both, face in the water), tread water 2 minutes with hands in armpits, then swim 50 more yards.</li>
      <li>Swim 20 yards, surface dive 7–10 feet, bring up a 10-pound brick and swim 20 yards back on your back holding it, without goggles.</li>
      <li>Finish the online course before the first day and bring the completion printout.</li></ul></div></details>
    <h2>Water Safety Instructor (WSI)</h2>
    <p>Required to teach swim lessons; covers the American Red Cross Swimming and Water Safety program.</p>
    <div class="now"><b>Coming course days:</b> <span {live("dates", title="Water Safety Instructor", empty="No course is on the schedule right now.")}>…</span></div>
    <p><b>Cost:</b> $200 FGCU students; $225 community.</p>
    <details class="more"><summary>Prerequisites</summary><div><ul>
      <li>25 yards each of front crawl, back crawl, breaststroke, elementary backstroke and sidestroke; 15 yards of butterfly.</li>
      <li>1 minute each of back float and treading water.</li>
      <li>Finish the online course before the first day and bring the completion printout.</li></ul></div></details>
""")
print("built", len(PAGES), "pages")
