# Executive Summary — UAC Care Transition Efficiency & Placement Outcome Analytics
**Prepared for:** U.S. Department of Health and Human Services
**Date:** May 25, 2026
**Data Source:** HHS Unaccompanied Alien Children Program Dataset

---

## 1. Executive Summary
This report analyzes the efficiency and outcomes of the Unaccompanied Alien Children (UAC) care pipeline, tracking the flow of children from CBP custody into HHS care and their subsequent placement with sponsors. By modeling this multi-stage transition, we aim to uncover hidden bottlenecks, evaluate placement effectiveness, and measure overall system throughput. These insights support proactive operational adjustments to ensure child welfare and operational stability.

## 2. Key Findings
- Average Transfer Efficiency Ratio: 94.3%
- Average Discharge Effectiveness Index: 2.4%
- Total anomaly days detected: 57
- Worst bottleneck period: None detected
- Best performing month for discharge: March 2023

## 3. KPI Performance Summary Table
| KPI | Average Value | Status |
|-----|--------------|--------|
| Transfer Efficiency Ratio | 94.3% | 🟢 Good |
| Discharge Effectiveness Index | 2.4% | 🔴 Critical |
| Pipeline Throughput Rate | 4.1% | 🔴 Critical |
| Backlog Accumulation Rate | -79.9 avg | N/A |
| Outcome Stability Score | 0.0056 std | N/A |

Status thresholds:
- Good: ratio > 0.6
- Warning: ratio 0.3–0.6
- Critical: ratio < 0.3

## 4. Bottleneck Analysis
The following are the most critical periods where the pipeline experienced sustained backlog accumulation (more incoming than discharged for 7+ consecutive days):
No major bottlenecks detected of 7+ consecutive days.

## 5. Anomaly Events
In total, 57 days were flagged as statistically significant anomalies (falling more than 2 standard deviations below the 30-day rolling mean for either transfer or discharge metrics).
The most severe recent anomalies include:
- **2025-11-30:** TE=1.00, DE=0.0000
- **2025-11-23:** TE=1.00, DE=0.0004
- **2025-11-09:** TE=0.45, DE=0.0017

## 6. Policy Recommendations
1. **Transfer Efficiency Optimization:** CBP to HHS transfers should be prioritized based on facility capacity and proximity to reduce initial delays in custody transitions.
2. **Discharge Outcome Improvements:** Streamline sponsor vetting processes without compromising safety, specifically addressing the low average discharge effectiveness identified.
3. **Backlog Mitigation:** Implement temporary capacity surges when backlog accumulation exceeds historical thresholds for more than 3 consecutive days.
4. **Weekend Staffing Models:** Re-evaluate weekend case-management staffing, as the weekday-vs-weekend analysis frequently indicates disparities in placement progression.
5. **Continuous Anomaly Monitoring:** Integrate the dashboard's anomaly alerts into daily stand-up briefings to catch localized drops in throughput early.

## 7. Methodology Note
The pipeline model leverages daily snapshots of custody and care volumes. Key Performance Indicators (KPIs) were derived using ratio and flow analysis, normalizing variables by intake to track proportional efficiency. Anomalies were identified statistically utilizing 30-day rolling distributions, avoiding hardcoded thresholds that fail to adapt to seasonal volume changes.
