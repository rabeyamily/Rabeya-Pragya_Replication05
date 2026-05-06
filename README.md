# RQ1 Replication

## Project title and overview 
  - Paper Title:  Beyond Bug Fixes: An Empirical Investigation of Post-Merge Code Quality Issues in Agent-Generated Pull Requests
  - Authors: Shamse Tasnim Cynthia, Al Muttakin, Banani Roy
  - Replication Team: Pragya Chapagain and Rabeya Zahan Mily
  - Course: CS-UH 3260 Software Analytics, NYUAD
  - The original paper analyzed 1,210 merged agent-generated bug-fix pull requests from 206 Python repositories using differential SonarQube analysis to identify code quality issues newly introduced by each PR. The study examines issue frequency, density, severity profiles, and rule-level violations across five AI coding agents: OpenAI Codex, Copilot, Devin, Cursor, and Claude Code. This replication reproduces both research questions from the original study using the scripts and dataset provided in the authors' replication package. We replicate RQ1 (issue frequency and distribution across agents) and RQ2 (severity profiles and most violated SonarQube rules), and additionally complete a data inspection task verifying the dataset files and manually checking three randomly selected pull requests against their GitHub records.

  - NOTE: Due to the large size of the files produced by the RQ 2 replication scripts, we were not able to push them to this repo but this is the google drive link to access them: https://drive.google.com/drive/folders/1eIP83_OHaJj029GzuDSZNv6luihzjilg?usp=sharing 
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
