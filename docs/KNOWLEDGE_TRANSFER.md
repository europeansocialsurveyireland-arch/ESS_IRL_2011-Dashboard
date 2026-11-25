# Knowledge Transfer: Irish Social Attitudes 2023 Dashboard

| | |
|---|---|
| **System** | Interactive Streamlit dashboard for ESS Round 11 (Ireland) |
| **Prepared by** | Gokulnath G L |
| **Date** | 25 November 2026 |
| **Audience** | Anyone on the ESS team who needs to rebuild, host, update or hand on the dashboard |
| **Repository** | `https://github.com/europeansocialsurveyireland-arch/ESS_IRL_2011-Dashboard` (owned by the official ESS account) |
| **Live app** | `https://essirl2011-dashboard.streamlit.app/` |

## 1. Why this document exists

The dashboard was first built and deployed on personal accounts during the internship, because no
ESS-owned account existed then. It has since been moved to an official ESS account so that it no
longer depends on any individual. The official repository was started fresh: it contains no personal
email addresses or machine-specific paths.

This document lets anyone on the ESS team run, update, or move the dashboard again (for example to
another account or host) from the repository alone. Nothing in the system is secret.

**How to use this document**

- Just want it running on your own machine? Section 3.
- Moving it to another account or host? Section 6.
- Updating numbers or adding a topic? Sections 5 and 7.
- Something looks wrong? Section 8 lists every problem known at handover.

## 2. What the system is

A multi-page web app with a landing page and 12 topic pages. Each page shows trend and breakdown
charts from the European Social Survey Round 11 for Ireland, with a short written insight under
each chart. Topics: Trust, Trust in Institutions, Health & Health Services, Europe, Life
Satisfaction & Happiness, Economic Satisfaction, Immigration, Religion, Climate Change, Gender,
COVID-19, Precarity.

It is built from two supplied files, both stored in the repository root:

| File | What it is | Used for |
|---|---|---|
| `ESS11 Public Report.docx.pdf` | The UCD *Irish Social Attitudes: 2023* report (66 pages) | Wording of insights; cross-checking numbers |
| `ESS11_graphs_Ausra (version2)_20241209.xlsx` | Workbook of aggregated tables behind the report's figures (18 sheets) | The only data source for every chart |

Upstream respondent-level data is published by ESS at
`https://ess.sikt.no/en/datafile/242aaa39-3bbb-40f5-98bf-bfb1ce53d8ef`. **The dashboard does not
use that file.** It uses only the aggregated workbook above.

### How the pieces fit together

```
ESS11_graphs_...xlsx            raw workbook, laid out like a printed report
        |
        |  etl/parse_*.py        15 scripts, one per topic (plus etl/_ess_helpers.py)
        v
data/processed/*.csv            68 tidy CSV files (committed to the repo)
        |
        |  app/utils/data_loader.py   reads CSVs, cached
        v
app/pages/*.py  ->  Plotly charts (app/utils/charts.py, theme.py)  ->  browser
app/Home.py     landing page with topic tiles
```

Two consequences worth knowing:

1. **The running app reads the CSVs, not the workbook.** The workbook and the ETL scripts are only
   needed when the numbers change. A deployment only needs `app/`, `data/processed/`,
   `.streamlit/` and `requirements.txt`.
2. **The app has no database, no API keys, no secrets and no environment variables.** There is
   nothing to hand over securely.

## 3. Quick start: run it on your own machine

Requirements: Python 3.11 or newer (developed on 3.13; the Codespaces dev container uses 3.11) and git.

```bash
git clone <repository-url> ess-dashboard
cd ess-dashboard

python -m venv .venv
# macOS / Linux:   source .venv/bin/activate
# Windows (PowerShell):   .venv\Scripts\Activate.ps1

pip install -r requirements.txt
streamlit run app/Home.py
```

The app opens at `http://localhost:8501`. Streamlit reloads automatically when a file is saved.

**Library versions are pinned** in `requirements.txt` (streamlit 1.66.1, pandas 3.1.1, plotly 7.1.0,
openpyxl 3.1.5), so a future library release cannot change the live site without anyone deciding it
should. This set was verified on a clean install: all pages render and all ETL scripts run. pandas 3
needs Python 3.11 or newer. To upgrade, change a version, run the smoke test (7.5), and click
through the site before pushing.

## 4. Repository map

| Path | Purpose | Edit when... |
|---|---|---|
| `app/Home.py` | Landing page: intro, fieldwork stats, red topic tiles, "About the survey" | Changing the home page or adding a topic tile |
| `app/pages/NN_Name.py` | One file per topic; the number sets sidebar order | Changing a chart or its insight text |
| `app/utils/data_loader.py` | Finds and loads CSVs by topic name; normalises the "2021/22" label | Rarely |
| `app/utils/charts.py` | Chart helpers (line, grouped bar, stacked bar, horizontal bars, colour ramps) | Changing chart behaviour everywhere |
| `app/utils/theme.py` | Colours, fonts, grid and legend styling shared by every chart | Rebranding charts |
| `app/utils/components.py` | `page_header()` and the "Insight" callout boxes | Changing page or callout layout |
| `etl/parse_*.py` | Turn workbook sheets into CSVs | The workbook layout or contents change |
| `etl/NOTES.md` | Per-sheet notes: what was found, what was skipped, every judgement call | **Read before touching any parser** |
| `data/processed/` | The 68 generated CSVs | Never by hand; regenerate (section 5) |
| `.streamlit/config.toml` | Light theme and basic server settings | Changing the app's overall look |
| `.devcontainer/devcontainer.json` | Optional: GitHub Codespaces dev environment (Python 3.11) | Rarely |
| `requirements.txt` | Python dependencies | Pinning or adding libraries |
| `.github/workflows/keep-awake.yml`, `.github/scripts/keep_awake.py` | Scheduled job that keeps the live app awake and checks it loads (section 6.4) | The app URL or home page title changes |

### Topic map: sheet to script to CSVs to page

| Page | Workbook sheet(s) | ETL script | CSV prefix |
|---|---|---|---|
| 01 Trust | Trust in Others | `parse_trust_others.py` | `trust_others__` |
| 02 Trust in Institutions | Trust in Institutions | `parse_trust_institutions.py` | `trust_institutions__` |
| 03 Health & Health Services | Health and Health Services; Hlth inequalities | `parse_health.py`, `parse_health_inequalities.py` | `health__`, `health_inequalities__` |
| 04 Europe | Europ Unif and Attach to Europ | `parse_eu_attachment.py` | `eu_attachment__` |
| 05 Life Satisfaction & Happiness | Life Sat and Happiness | `parse_life_satisfaction_happiness.py` | `life_satisfaction_happiness__` |
| 06 Economic Satisfaction | Econ Sat and HH Inc Adequacy | `parse_economic_satisfaction.py` | `economic_satisfaction__` |
| 07 Immigration | Immigration | `parse_immigration.py` | `immigration__` |
| 08 Religion | Relig | `parse_religion.py` | `religion__` |
| 09 Climate Change | Climate Change | `parse_climate_change.py` | `climate_change__` |
| 10 Gender | Gender | `parse_gender.py` | `gender__` |
| 11 COVID-19 | C19 - Personal experience; C19 - Prioritisations; C19 - Satisfaction | `parse_c19_personal_experience.py`, `parse_c19_prioritisations.py`, `parse_c19_satisfaction.py` | `c19_personal_experience__`, `c19_prioritisations__`, `c19_satisfaction__` |
| 12 Precarity | Precarity | `parse_precarity.py` | `precarity__` |

**Sheets deliberately skipped** (three of the workbook's 18): `Religion` and `Economic Sat` are older
drafts superseded by `Relig` and `Econ Sat and HH Inc Adequacy`; `Sheet1` is a redundant older cut
of the Trust in Institutions education table.

### CSV naming and shape

File names follow `<topic>__<kind>[_detail].csv`. There are three shapes:

| Kind | Columns |
|---|---|
| `trend` | `ess_round`, `year`, `series`, `value` |
| `breakdown_*` | `category`, `group_type`, `group_value`, `value`, `unit` |
| `distribution*` | `ess_round`, `year`, `response_category`, `freq`, `percent`, `cum_percent` (the EU file also has `series`) |

Pages find files by topic prefix plus a substring, for example `load("immigration", "breakdown_employment")`.
Renaming a CSV or adding one whose name contains an existing substring can silently change which
file a page loads. The loader returns the **first** match alphabetically.

Some generated CSVs are not displayed anywhere yet (for example the `*_detail` files for Europe and
Immigration, the COVID breakdowns by COVID experience, and several raw `trend`/`distribution`
duplicates). They are kept as ready-made material for future charts.

## 5. Regenerating the data

You only need this if the source workbook changes. Each script finds the workbook in the repository
root relative to its own location, so it works from any folder on any machine, and overwrites
`data/processed/`.

```bash
# macOS / Linux
for f in etl/parse_*.py; do python "$f"; done
```

```powershell
# Windows PowerShell
Get-ChildItem etl\parse_*.py | ForEach-Object { python $_.FullName }
```

**Verified at handover:** in a clean environment with the pinned versions, all 15 scripts ran without
error and reproduced all 68 CSVs with content identical to the committed files. Running them again
should therefore produce no changes in `git status`; if it does, the workbook or a script has changed.

Practical points:

- The workbook file name is hard-coded in every parser as
  `ESS11_graphs_Ausra (version2)_20241209.xlsx`. If you receive a new version, either keep the file
  name or update the `WORKBOOK` / `SRC` / `XLSX_PATH` line at the top of each script.
- **The parsers are tied to the workbook's exact layout.** Most of them read tables from fixed row and
  column positions (these are recorded per sheet in `etl/NOTES.md`); only the Health parsers mostly
  find tables by scanning for markers such as the literal cell `Freq.`. Inserting a single row, or
  receiving a re-laid-out workbook, can make a parser read the wrong cells *without raising an error*.
  After any workbook change, re-check each affected script against `etl/NOTES.md` and compare the
  output with the report (7.4).
- Several parsers write the Round 10 label as `2021/2022` and others as `2021/22`. This is harmless:
  `data_loader.py` converts both to `2021/22` on load. **Do not remove that conversion.**
- After regenerating, check the numbers against the report (section 7.4). The parsers were
  validated by comparing outputs with figures quoted in the PDF, for example 66% high trust among
  graduates, 68.97% trusting the Garda, 52.8% response rate.

## 6. Moving or rebuilding the deployment

The dashboard currently lives in the official ESS repository and Streamlit app listed at the top of
this document. Use this section if it ever has to move again, for example to a different account,
a GitHub organisation, or ESS's own servers.

### 6.1 Decide these first

| Decision | Options and notes |
|---|---|
| **Which account owns the code?** | A GitHub organisation or shared account the ESS team controls. Use an account that more than one person can recover. |
| **Which account owns the hosting?** | Streamlit Community Cloud is tied to the GitHub account you sign in with. Use the same organisation-controlled account. |
| **Public or private repository?** | The app works with either; a private repository needs Streamlit's GitHub access granted to it. |
| **May the PDF and workbook be published?** | Both are in the repository root. If the repository is public, confirm with the report authors (UCD Geary Institute) that they may be redistributed. The app itself needs only `data/processed/`. |
| **Hosting** | Streamlit Community Cloud is free and the simplest. Check its current limits and terms before relying on it for a public page (section 6.4). Any host that can run `streamlit run app/Home.py` works. |
| **Who maintains it, and who reviews the insight text?** | See sections 7.2 and 8. |

### 6.2 Copy the code to the new location

Either use GitHub's *Settings, Transfer repository* (moves the repository with its history to another
account or organisation; GitHub redirects the old address), or copy it to a new, empty repository:

```bash
git clone https://github.com/europeansocialsurveyireland-arch/ESS_IRL_2011-Dashboard.git ess-dashboard
cd ess-dashboard
git remote set-url origin https://github.com/<new-account>/<repo-name>.git
git push -u origin main
```

If this machine is already signed in to GitHub as someone else, put the new account's username in the
URL (`https://<new-username>@github.com/<new-account>/<repo-name>.git`) so git asks you to sign in as
that account instead of reusing the stored one. Note the branch name: the hosting step asks for it.

### 6.3 Deploy on Streamlit Community Cloud

Button labels on Streamlit's site change from time to time; follow the intent if the wording differs.

1. Go to `https://share.streamlit.io` and sign in with the **GitHub account that owns the repository**. Authorise Streamlit
   to read the repository (for a private repository, grant it access to that repository specifically).
2. Choose **Create app** and point it at the repository.
3. Enter these settings:

   | Field | Value |
   |---|---|
   | Repository | `<account>/<repo-name>` |
   | Branch | `main` (or whichever branch you pushed) |
   | Main file path | `app/Home.py` |
   | App URL | Choose a readable sub-domain |
   | Python version (under Advanced settings) | 3.11 or newer |

4. Deploy. The first build installs `requirements.txt` and takes a few minutes.
5. Open the app and click through **all 12 topic tiles**. Each should show charts and an Insight box
   with no red error banner.

**Updating later:** push a commit to the tracked branch and Streamlit redeploys automatically. If a
page looks stale, use the app menu on the deployed page to reboot it.

**Record the result.** Fill in this table so the next person knows what exists:

| Item | Value |
|---|---|
| Repository URL | |
| Branch | |
| Streamlit app URL | |
| Account that owns the Streamlit app | |
| Date deployed | |

### 6.4 Things to know about Community Cloud before relying on it

- Apps with no recent visitors are put to sleep, and the next visitor sees a "wake this app" screen
  and waits. To prevent this, the repository has a scheduled GitHub Actions job
  (`.github/workflows/keep-awake.yml`) that opens the dashboard in a headless browser every 4 hours
  and clicks the wake-up button if needed. It runs free on GitHub for public repositories.
  - **It doubles as an uptime check:** a failed run (red cross on the repository's *Actions* tab)
    means the dashboard did not load, and GitHub emails the account. Failed runs keep a screenshot
    of what the browser saw.
  - **Run it by hand:** *Actions* tab, *Keep dashboard awake*, *Run workflow*.
  - **If the home page title changes,** update `HOME_HEADING` in `.github/scripts/keep_awake.py`,
    otherwise every run fails even though the site is fine.
  - **If the app moves,** update `APP_URL` in the workflow file.
  - GitHub switches off scheduled jobs in public repositories after 60 days without commits. The
    job re-enables itself on every run to avoid this, but glance at the *Actions* tab now and then
    to confirm runs are still happening.
- The app is tied to the account that created it. This is the exact situation this document is meant
  to avoid, so choose an account the organisation can always access.
- Free-tier limits and terms can change. Check Streamlit's current documentation rather than assuming.

### 6.5 Embed in the ESS WordPress site

The dashboard is a separate web app; WordPress simply displays it in a frame. In a Custom HTML block:

```html
<iframe
  src="https://<your-streamlit-app-url>/?embed=true"
  width="100%"
  height="1200"
  style="border:none;"
  loading="lazy">
</iframe>
```

- `?embed=true` hides Streamlit's own menu and footer.
- Frames do not resize to their content, so set a generous height and test on a phone-width screen.
- The topic tiles on the home page are plain links such as `/Trust`. Inside the frame they navigate
  within the frame, which is the intended behaviour. They assume the app is served at the **root** of
  its address. If you later host it under a sub-path (for example `example.org/dashboard/`), those
  links will break and `app/Home.py` will need adjusting.
- Some WordPress hosts and security plugins block frames from other domains. If the frame stays blank,
  check the host's content-security settings first.

### 6.6 Optional: Codespaces / dev container

`.devcontainer/devcontainer.json` lets anyone open the repository in a GitHub Codespace and have the
app start automatically. A Codespace keeps its **own copy** of the code and does not update when
commits are pushed elsewhere. If a Codespace preview shows an old version, run `git pull` in its
terminal and restart `streamlit run app/Home.py`. A Codespace is a development environment, not the
live website.

## 7. Maintaining and changing the dashboard

### 7.1 Add a new topic page

1. Add the sheet to the workbook and write `etl/parse_<topic>.py`, copying the closest existing script.
   Write outputs to `data/processed/` using the `<topic>__<kind>.csv` naming.
2. Run the script and inspect the CSVs. Compare a few values against a trusted source.
3. Copy a similar page in `app/pages/` and name it `13_Topic_Name.py` (the number sets sidebar order,
   underscores become spaces in the sidebar).
4. Add `("Topic Name", "Topic_Name")` to the `topics` list in `app/Home.py` (the second value is the
   file name without number prefix or `.py`).
5. Run the smoke test (7.5).

### 7.2 Insight text is written by hand

**Every sentence and number in the Insight boxes is typed into the page file.** Nothing updates
automatically when data changes. If you regenerate the CSVs with new figures, read each insight box
and update it yourself. Insights for COVID-19 and Precarity were written from the data directly, because
the report does not cover those topics, so they deserve a subject-expert read (section 8).

### 7.3 Chart category orders are also hand-written

Pages pass explicit lists such as `["25 and under", "26-35", ..., "76 plus"]` to control chart order.
If a label in the CSV changes by even one character, that list no longer matches and the chart
shows an **empty phantom bar** or misorders categories, with no error message. This already happened
once at build time (`"76 plus"` in some files versus `"76+"` in another). After any data refresh,
look at every chart.

### 7.4 Checking numbers after a data refresh

- Pick 3 to 5 figures quoted in the report and confirm the dashboard shows the same value.
- Percent breakdowns should sum to about 100 within each group.
- 0 to 10 scale means should sit between 0 and 10.

### 7.5 Smoke test: does every page still load?

Run from the repository root after any change. It opens each page headlessly and reports Python errors:

```bash
python - <<'EOF'
import glob, os
from streamlit.testing.v1 import AppTest
bad = 0
for p in ["app/Home.py"] + sorted(glob.glob("app/pages/*.py")):
    at = AppTest.from_file(p, default_timeout=60).run()
    errors = [e.value for e in at.exception]
    print("OK  " if not errors else "FAIL", os.path.basename(p))
    for e in errors: print("   ", str(e)[:300]); bad += 1
print("pages with errors:", bad)
EOF
```

This catches crashes. It does **not** catch a wrong number or a misordered chart; those need eyes.

### 7.6 Adding a new ESS round (for example Round 12)

Expect real work, not a configuration change. Roughly: obtain the updated workbook, extend each
parser to read the new round, regenerate, then review every chart (new `year` labels, new category
spellings) and rewrite the insight text. Plan on re-reading `etl/NOTES.md` for every parser touched.

## 8. Known issues and limitations at handover

None of these stop the dashboard working. They are listed so nobody has to rediscover them.

| # | Issue | Where | Suggested action |
|---|---|---|---|
| 1 | **COVID round is inferred.** The COVID sheets carry no round marker; Round 10 was inferred from the report. | `etl/NOTES.md`, C19 sections; `C19_DATA` in `app/pages/11_COVID-19.py` | Confirm with the data team. |
| 2 | **The supplied report was a draft.** Its "Key points" section (p.5) is mostly placeholder text and several figure descriptions are cut off ("..."). Insights for those topics were written from the available text plus the data. | `app/pages/*.py` insight text | Check every insight against the final published report. |
| 3 | **Home page overstates coverage.** The intro says every page tracks Rounds 1 to 11, although several topics cover fewer rounds. | `app/Home.py` | Reword if it matters. |
| 4 | **Europe trend has two lines, not three.** The workbook has no historical series for emotional attachment to Europe; it appears only in the 2023 breakdowns. | `eu_attachment__trend.csv` | Mention on the page, or leave. |
| 5 | **Duplicate source table.** The Health workbook sheet contains the "good health by income decile" table twice with slightly different values for decile 6 and Top. The copy matching the sheet's own summary chart was used. | `etl/NOTES.md`, Health section | Confirm which copy is correct. |
| 6 | **Small group.** "Refusal/Don't know" in life satisfaction by employment has very few respondents; the 16.5% figure is not meaningful. A caption warns about it. | `app/pages/05_...py` | None needed. |
| 7 | **No automated tests.** The smoke test in 7.5 is a convenience, not a test suite. | whole repo | Add tests if the project grows. |
| 8 | **Sample size caveat.** Ireland's Round 11 sample is about 2,075 people. Small subgroups (for example the lowest education band) carry wide uncertainty, and the dashboard shows no confidence intervals. | all breakdown charts | Consider a note on the site. |

**Fixed when moving to the official account (November 2026):** library versions pinned; eight ETL
scripts that pointed at a folder on the original author's laptop now find the workbook relative to
themselves; the COVID-19 and Precarity footers now name the rounds they use (they previously said
"Round 11" for all); a pandas deprecation on the COVID page; "an interactive insights" on the home page.

## 9. Ownership inventory

| Item | Location | Notes |
|---|---|---|
| Source code | `https://github.com/europeansocialsurveyireland-arch/ESS_IRL_2011-Dashboard` | Owned by the official ESS account |
| Live app | `https://essirl2011-dashboard.streamlit.app/` | Streamlit Community Cloud, signed in with the same account; redeploys automatically on every push to `main` |
| Codespaces | Any Codespace created from the repository | Disposable; nothing unique is stored there |
| Secrets, API keys, databases | **None exist** | Nothing to hand over |

The original development copy on the author's personal accounts is not used by this deployment and is
being retired; nothing here depends on it.

## 10. Glossary

| Term | Meaning |
|---|---|
| **ESS** | European Social Survey, a cross-national survey run every two years |
| **Round 11 / ESS11** | The 2023 wave; Ireland fieldwork ran 27 June 2023 to 3 January 2024 |
| **ETL** | Extract, transform, load: the scripts that turn the awkward workbook into clean CSVs |
| **Tidy / long format** | One row per observation, with columns saying what it is, so one chart helper can plot any file |
| **Streamlit Community Cloud** | Streamlit's free hosting service that deploys an app directly from a GitHub repository |
| **Iframe** | A frame inside a web page that shows another web page, here the dashboard inside WordPress |
| **Distribution / breakdown / trend** | The three CSV shapes: counts per answer; values split by a group such as age; values across survey rounds |
