# Executive Summary

The analysis covers daily UAC pipeline activity from 2023-01-12 to 2025-12-21, highlighting system flow and discharge performance across 720 reporting days. Average transfer efficiency was 1.48 and discharge effectiveness averaged 0.024, with pipeline throughput averaging 0.041. Backlog changes averaged -79.9 per day, while positive backlog occurred on 17.8% of days, indicating intermittent congestion. The strongest discharge month was 2023-03 (mean index 0.036), while the highest average backlog month was 2025-05 (mean 0.7).

## Key Findings

- Coverage period: 2023-01-12 to 2025-12-21 (720 days).
- Average ratios: transfer efficiency 1.48, discharge effectiveness 0.024, pipeline throughput 0.041.
- Backlog change averaged -79.9 per day; 17.8% of days showed net backlog growth.
- Best discharge month was 2023-03 (mean 0.036); worst backlog month was 2025-05 (mean 0.7).
- Total anomaly days flagged: 8.

## KPI Performance Table

| KPI | Average | Status |
| --- | ---: | :--- |
| Transfer Efficiency Ratio | 1.484 | Warning |
| Discharge Effectiveness Index | 0.024 | Warning |
| Pipeline Throughput Rate | 0.041 | Good |
| Backlog Accumulation Rate | -79.883 | Good |
| Outcome Stability Score | 0.006 | Good |

## Bottleneck Analysis

No sustained backlog periods (7+ consecutive days) were detected in this timeframe.

## Anomaly Events

Total anomaly days flagged: 8.
Worst anomaly instances (lowest z-scores):
- 2025-02-17: Discharge Effectiveness Index = 0.006 (z=-2.43).
- 2024-07-30: Discharge Effectiveness Index = 0.016 (z=-2.35).
- 2025-02-18: Discharge Effectiveness Index = 0.004 (z=-2.31).

## Recommendations

- Expand CBP-to-HHS transfer capacity on high-volume days to raise transfer efficiency above 1.5 on average.
- Accelerate discharge planning for cases exceeding median HHS care levels to push the discharge index consistently above 0.03.
- Prioritize operational surge staffing during months with elevated backlog means (e.g., 2025-05) to prevent sustained congestion.
- Implement early-warning triggers tied to the 30-day rolling anomaly detection to address sudden performance drops within 48 hours.
- Strengthen weekend discharge staffing and logistics to reduce weekday-weekend disparities and stabilize outcome variability.

## Methodology Note

Data were sourced from the cleaned UAC program dataset (daily records). KPI metrics were calculated as ratios of transfers, discharges, and care volumes; backlog accumulation reflects daily apprehensions minus discharges. Sustained bottlenecks were defined as >0 backlog for at least 7 consecutive days. Anomalies were flagged when transfer efficiency or discharge effectiveness fell more than 2 standard deviations below a 30-day rolling mean. KPI status thresholds were set as: transfer efficiency >=1.5 (Good), 1.0-1.49 (Warning), <1.0 (Critical); discharge effectiveness >=0.03 (Good), 0.02-0.029 (Warning), <0.02 (Critical); pipeline throughput >=0.035 (Good), 0.025-0.034 (Warning), <0.025 (Critical); backlog accumulation <=0 (Good), 0-50 (Warning), >50 (Critical); outcome stability score <=0.006 (Good), 0.006-0.01 (Warning), >0.01 (Critical).
