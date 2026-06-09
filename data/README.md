# Data Dictionary

This document describes the structure and schema of the `HHS_Unaccompanied_Alien_Children_Program.csv` file.

| Column Name | Description | Data Type | Example Values | Missing Data Notes |
| :--- | :--- | :--- | :--- | :--- |
| **Date** | The reporting date for the aggregate counts. | `string` (Date format) | `December 21, 2025` | Significant missing data (450 rows empty). Used as primary index for time-series analysis. |
| **Children apprehended and placed in CBP custody\*** | The number of children taken into border patrol custody on the given date. | `float64` | `6.0`, `11.0` | 450 rows missing. Missing matching the empty dates. |
| **Children in CBP custody** | The total running count of children currently held in CBP facilities. | `float64` | `18.0`, `50.0` | 450 rows missing. |
| **Children transferred out of CBP custody** | The number of children transferred from CBP custody to HHS care on the given date. | `float64` | `11.0`, `6.0` | 450 rows missing. |
| **Children in HHS Care** | The total running count of children currently in HHS care facilities. | `string` (Numbers with commas, e.g. "2,484") | `"2,484"`, `"2,472"` | 450 rows missing. Requires data cleaning to parse as numerical float. |
| **Children discharged from HHS Care** | The number of children discharged from HHS care (usually placed with sponsors) on the given date. | `float64` | `14.0`, `16.0` | 450 rows missing. |

**Note**: The raw dataset contains many blank rows (450) appended to the bottom of the active data. There are no demographic columns such as country of origin, US state distribution, age, or gender breakdowns.
