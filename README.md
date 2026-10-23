# Lee County/FGCU Aquatics Center — unofficial preview

A mock-up of [FGCU's Aquatics pages](https://www.fgcu.edu/university-recreation-and-wellness/aquatics/) (Aquatics, Lane
Availability, Operating Hours, Swim Lessons, Certification Courses) with the Aquatics Center on one live
[Pool Relay](https://www.poolrelay.com) schedule. Not operated by or affiliated with Florida Gulf Coast University or Lee County.

No schedule is typed into the pages. The hours, adjusted days, last scheduled day, course dates, the "right now" card and
the week's lanes per pool are filled by `finder.js` from the live Pool Relay view; `build.py` holds only fees, policies and
facts about the water.

- `build.py`: generates the five pages.
- `finder.js`: `#today`, `#week` (one column per pool, with lane counts), and `data-live` elements
  (`hours`, `exceptions`, `last`, `dates`, `when`, `closures`).
- Pool Relay view: `nspJC3cZSItvCm4H1MvKNY` (Lee County/FGCU Aquatics Center, lane by lane).
