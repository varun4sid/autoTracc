# autoTracc

autoTracc is an interactive Streamlit dashboard for students of PSG College of Technology to view advanced insights into attendance, CGPA, exam schedule, internal marks, and to autofill periodic feedback forms from the college portals.

Live app: https://autotracc.streamlit.app

## What It Does

- Login using Studzone credentials from inside the app.
- Fetch and display attendance data with three modes:
  - Physical attendance and leave calculation.
  - Regular Exemption based leave calculation.
  - Medical Exemption based leave calculation.
- Show semester-wise GPA and CGPA
- Provide a target CGPA simulator using editable expected grades for current semester courses.
- Consolidated display of Continuous Assessment Test timetable
- Show internal marks and required end-semester score:
  - Required score to pass.
  - Required score to hit a custom target.
- Provide a one-click feedback autofill flow for Intermediate and End-Semester forms.

## How It Works

- User login credentials are obtained at index page and are validated through responses from POST requests to the portal
- Once validated, data is fetched from specified PSG eCampus portal client-side routes and scraping the frontend pages with requests + BeautifulSoup.
- The raw HTML is processed into data structures and desired information is extracted.
- Streamlit is then used to display this information in an interactive UI.
- Feedback autofill uses Selenium with headless Chromium and chromedriver.
- Most computed values are stored in session state and rendered via Streamlit API.


## Tech Stack

- Python 3.11
- Streamlit
- requests
- BeautifulSoup4 + lxml
- pandas
- Selenium (Chromium + chromedriver)

## Project Structure

- app.py: Entry point and page routing.
- pages/loginPage.py: Login form, demo trigger, and session initialization.
- pages/processingPage.py: Data fetching and preprocessing.
- pages/dashBoardPage.py: Main dashboard tabs and footer.
- src/pagerequests.py: Portal login/session + greeting helpers.
- src/attendance.py: Attendance parsing and leave calculations.
- src/cgpa.py: Course parsing and GPA/CGPA computation.
- src/exams.py: Exam schedule parsing.
- src/internals.py: Internal marks and target score calculations.
- src/feedback.py: Selenium automation for feedback forms.
- src/tabs/: UI logic for each dashboard tab.

## Local Setup

#### 1. Clone and enter the project

```bash
git clone https://github.com/varun4sid/autoTracc.git
cd autoTracc
```

#### 2. Create and activate virtual environment

```bash
python -m venv .venv
source .venv/bin/activate
```

#### 3. Install Python dependencies

```bash
pip install -r requirements.txt
```

#### 4. Install system dependencies for Selenium

On Debian/Ubuntu, install the packages listed in packages.txt. This is only to use the autofill feedback feature.
```bash
sudo apt-get update
sudo apt-get install -y $(cat packages.txt)
```

#### 5. Run Streamlit app

```bash
streamlit run app.py
```

Open the local URL shown in terminal (usually http://localhost:8501).


## Privacy

- Credentials are used only to create authenticated sessions against official Studzone portals.
- Data is fetched and processed in memory during the active Streamlit session.
- This repository does not implement persistent storage for user credentials or fetched academic data.

## Limitations

- Depends on PSG portal availability and HTML structure.
- Scraping-based extraction may break when portal markup changes.
- Feedback automation requires compatible Chromium and chromedriver setup.
- Some tabs may show warnings when source data is temporarily unavailable.

# Acknowledgements

Thanks to Streamlit's [Community Cloud](https://streamlit.io/cloud), this app can be hosted in the Web for FREE!

## Contributing

Issues and feature ideas are welcome via GitHub discussions and pull requests.