# RQ1 Replication

## Directory Structure

- `datasets/`  
  Input data used in RQ1:
  - `All_PR_Sonar_Results.csv`
  - `All_PR_Issues_Details_with_LOC.csv`

- `replication_scripts/`  
  Scripts/notebook for replication:
  - `run_rq1.py` (main script to run)
  - `result-analysis.ipynb` (original notebook reference)
  - `requirements.txt` (dependencies)

- `outputs/`  
  Generated RQ1 results:
  - `Agent_Statistics_Summary.csv`
  - `Agent_Statistics_Summary.tex`
  - `RQ1_PR_IssueDensity.csv` (intermediate)
  - `Issue_Density_Stats_By_Agent.csv` (intermediate)
  - `RQ1_Boxplot_Data_NoOutliers.csv` (intermediate)
  - `issue_density.png`
  - `RQ1_Stat_Test.txt`

## How to Run

From the repository root:

```bash
cd "/Users/rabeyazahanmily/Desktop/Rabeya-Pragya_Replication05"
```

(Optional) activate virtual environment:

```bash
source .venv/bin/activate
```

Install dependencies (if needed):

```bash
pip install -r replication_scripts/requirements.txt
```

Run full RQ1 replication:

```bash
python3 replication_scripts/run_rq1.py
```
