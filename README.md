# UAC Program Analytics Dashboard

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://streamlit.io/cloud)

## Overview
This complete end-to-end data analytics project, named **uac-analytics**, evaluates the operational flow of the HHS Unaccompanied Alien Children (UAC) Program. It analyzes how children progress through the care pipeline—from initial apprehension by CBP, into HHS care, and ultimately to sponsor placement. By extracting key performance metrics from historical flow data, this project surfaces crucial insights into process bottlenecks and system load, aiding stakeholders in optimizing child welfare outcomes.

## Screenshots
*(Placeholder for dashboard screenshots)*
![Dashboard Screenshot 1](#)
![Dashboard Screenshot 2](#)

## Key Findings
* **Intake and Apprehension Load**: A total of 67,337 children were apprehended and placed into CBP custody between Jan 2023 and Dec 2025.
* **Discharge Efficiency**: The system successfully discharged 124,853 children from HHS care over this time span, outpacing intake likely due to clearing historical backlogs.
* **HHS Capacity Management**: The number of children actively in HHS care varied considerably, reaching a maximum of 9,988 children at peak load.
* **Data Limitations**: The dataset provides aggregate custody counts but lacks specific demographic (age, gender, origin) and geographic placement data.

## Installation & Usage
To run the dashboard locally:
1. Clone the repository:
   ```bash
   git clone https://github.com/Animey13/uac-analyzer.git
   cd uac-analyzer
   ```
2. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Run the Streamlit dashboard:
   ```bash
   streamlit run dashboard/app.py
   ```

## Deploy to Streamlit Cloud
To deploy this app publicly for free:
1. Push this repository to your GitHub account.
2. Go to [share.streamlit.io](https://share.streamlit.io/) and log in with GitHub.
3. Click "New app", select your repository, branch, and set the main file path to `dashboard/app.py`.
4. Click "Deploy"!

## Data Dictionary
For detailed information about the dataset schema, columns, and data types, please refer to the [Data Dictionary](data/README.md).

## License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
