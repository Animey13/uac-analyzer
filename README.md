# UAC Care Transition Efficiency & Placement Outcome Analytics

## Overview
This complete end-to-end data analytics project, named **uac-analytics**, evaluates the operational efficiency of the HHS Unaccompanied Alien Children (UAC) Program. It analyzes how effectively children progress through the care pipeline—from initial apprehension by CBP into HHS care, and ultimately to sponsor placement. By extracting key performance metrics from historical flow data, this project surfaces crucial insights into process bottlenecks and anomalies, aiding government stakeholders in optimizing child welfare outcomes.

## Setup
Install all required dependencies before running scripts or the dashboard:
```bash
pip install -r requirements.txt
```

## Run the Dashboard
To launch the interactive multi-page dashboard, run:
```bash
streamlit run dashboard/app.py
```

## Project Structure
- `data/`: Contains the original raw dataset alongside locally generated, cleaned, and enriched datasets (e.g., anomalies, bottlenecks, monthly trends).
- `plots/`: Houses eight automatically generated static EDA visualization charts in PNG format.
- `dashboard/`: Contains the source code (`app.py`) for the fully functional, interactive Streamlit application.
- `report/`: Stores the formal auto-generated executive summary markdown report intended for stakeholders.
- `README.md`: Project documentation containing setup instructions and structural definitions.
- `requirements.txt`: Python package dependency list.

## KPI Definitions
| KPI | Formula | Interpretation |
|-----|---------|----------------|
| **Transfer Efficiency Ratio** | `transferred / apprehended` | Measures the speed and proportion at which children are successfully moved from CBP custody into HHS care. High = smooth transition; Low = potential intake delays. |
| **Discharge Effectiveness Index** | `discharged / hhs_care` | Represents the daily placement success rate relative to the total population under HHS care. High = swift sponsor placement; Low = prolonged facility stays. |
| **Pipeline Throughput Rate** | `(transferred + discharged) / (apprehended + hhs_care)` | Captures overall system momentum and fluidity across all care phases. High = active and unblocked pipeline; Low = widespread stagnation. |
| **Backlog Accumulation Rate** | `apprehended - discharged` | Tracks the net daily change in the overarching system load. Positive values = growing backlog; Negative values = shrinking backlog. |
| **Outcome Stability Score** | Rolling 7-day std of `discharge_effectiveness_index` | Evaluates the consistency and predictability of daily placements. High = erratic and volatile outcomes; Low = reliable and stable processes. |

## Data Source
U.S. Department of Health and Human Services
HHS Unaccompanied Alien Children Program
