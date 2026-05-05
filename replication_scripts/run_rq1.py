#!/usr/bin/env python3
from pathlib import Path
import pandas as pd
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.stats import kruskal

ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = ROOT / "datasets"
OUT_DIR = ROOT / "outputs"
OUT_DIR.mkdir(parents=True, exist_ok=True)

sonar = pd.read_csv(DATA_DIR / "All_PR_Sonar_Results.csv")
issues = pd.read_csv(DATA_DIR / "All_PR_Issues_Details_with_LOC.csv")

# RQ1-A: incidence/frequency statistics
pr_issues = sonar.groupby(["Agent", "pr_html_url"])["issues_count"].sum().reset_index()
pr_issues.columns = ["Agent", "PR_URL", "Issues_Count"]

rows = []
for agent in sorted(pr_issues["Agent"].unique()):
    x = pr_issues.loc[pr_issues["Agent"] == agent, "Issues_Count"]
    q1 = x.quantile(0.25)
    q3 = x.quantile(0.75)
    iqr = q3 - q1
    lb = q1 - 1.5 * iqr
    ub = q3 + 1.5 * iqr
    outliers = x[(x < lb) | (x > ub)]
    prs_with = int((x > 0).sum())
    n = int(len(x))
    rows.append({
        "Agent": agent,
        "Total PRs": n,
        "PRs with Issues": prs_with,
        "PRs without Issues": n - prs_with,
        "% PRs with Issues": round((prs_with / n) * 100, 2),
        "Total Issues": int(x.sum()),
        "Mean": round(x.mean(), 2),
        "Median": round(x.median(), 2),
        "Std Dev": round(x.std(), 2),
        "Min": int(x.min()),
        "Max": int(x.max()),
        "Q1": round(q1, 2),
        "Q3": round(q3, 2),
        "IQR": round(iqr, 2),
        "Outliers": int(len(outliers)),
    })

agent_stats = pd.DataFrame(rows)
agent_stats.to_csv(OUT_DIR / "Agent_Statistics_Summary.csv", index=False)

header = (
    "\\begin{table}[h]\n"
    "\\centering\n"
    "\\caption{Statistical Analysis of Issues per PR by Coding Agent}\n"
    "\\label{tab:agent_statistics}\n"
    "\\resizebox{\\textwidth}{!}{%\n"
    "\\begin{tabular}{lrrrrrrrrrrrrrr}\n"
    "\\hline\n"
    "\\textbf{Agent} & \\textbf{Total PRs} & \\textbf{PRs w/ Issues} & \\textbf{PRs w/o Issues} & "
    "\\textbf{\\% w/ Issues} & \\textbf{Total Issues} & \\textbf{Mean} & \\textbf{Median} & \\textbf{Std Dev} & "
    "\\textbf{Min} & \\textbf{Max} & \\textbf{Q1} & \\textbf{Q3} & \\textbf{IQR} & \\textbf{Outliers} \\\\n"
    "\\hline\n"
)
body = ""
for _, r in agent_stats.iterrows():
    body += (
        f"{r['Agent']} & {r['Total PRs']} & {r['PRs with Issues']} & {r['PRs without Issues']} & "
        f"{r['% PRs with Issues']:.2f} & {r['Total Issues']} & {r['Mean']:.2f} & {r['Median']:.2f} & "
        f"{r['Std Dev']:.2f} & {r['Min']} & {r['Max']} & {r['Q1']:.2f} & {r['Q3']:.2f} & {r['IQR']:.2f} & {r['Outliers']} \\\\n"
    )
footer = "\\hline\n\\end{tabular}%\n}\n\\end{table}\n"
(OUT_DIR / "Agent_Statistics_Summary.tex").write_text(header + body + footer)

# RQ1-B: issue density
agent_col = "Agent" if "Agent" in issues.columns else "agent"
pr_col = "html_url" if "html_url" in issues.columns else "pr_html_url"
pr = issues.groupby([agent_col, pr_col]).agg({"Issue Type": "count", "changed_loc": "first"}).reset_index()
pr.columns = ["Agent", "PR_URL", "issues_count", "changed_loc"]
pr = pr[pr["changed_loc"] > 0].copy()
pr["issue_density"] = (pr["issues_count"] / pr["changed_loc"]) * 1000
pr.replace([np.inf, -np.inf], np.nan, inplace=True)
pr.dropna(subset=["issue_density"], inplace=True)
pr.to_csv(OUT_DIR / "RQ1_PR_IssueDensity.csv", index=False)

density_rows = []
for a in sorted(pr["Agent"].unique()):
    s = pr.loc[pr["Agent"] == a, "issue_density"]
    density_rows.append({
        "Agent": a,
        "N": len(s),
        "Mean": s.mean(),
        "Median": s.median(),
        "Std Dev": s.std(),
        "Min": s.min(),
        "Q1": s.quantile(0.25),
        "Q3": s.quantile(0.75),
        "Max": s.max(),
    })

pd.DataFrame(density_rows).to_csv(OUT_DIR / "Issue_Density_Stats_By_Agent.csv", index=False)

h, p = kruskal(*[pr.loc[pr["Agent"] == a, "issue_density"].values for a in sorted(pr["Agent"].unique())])
(OUT_DIR / "RQ1_Stat_Test.txt").write_text(f"Kruskal-Wallis H-statistic: {h:.4f}\np-value: {p:.6g}\n")

# plot data: remove outliers by IQR per agent
filtered = []
for a in sorted(pr["Agent"].unique()):
    s = pr.loc[pr["Agent"] == a, "issue_density"]
    q1 = s.quantile(0.25)
    q3 = s.quantile(0.75)
    iqr = q3 - q1
    lb = q1 - 1.5 * iqr
    ub = q3 + 1.5 * iqr
    filtered.append(pr[(pr["Agent"] == a) & (pr["issue_density"] >= lb) & (pr["issue_density"] <= ub)])
plot_df = pd.concat(filtered, ignore_index=True)
plot_df.to_csv(OUT_DIR / "RQ1_Boxplot_Data_NoOutliers.csv", index=False)

sns.set_style("whitegrid")
plt.figure(figsize=(8, 5))
ax = sns.boxplot(
    data=plot_df,
    x="Agent",
    y="issue_density",
    showmeans=True,
    meanprops=dict(marker="o", markerfacecolor="darkblue", markeredgecolor="black", markersize=8),
)
ax.set_yscale("log")
ax.set_ylabel("Issue Density", fontsize=16)
ax.set_xlabel("Agent", fontsize=16)
plt.xticks(rotation=20, fontsize=12)
plt.yticks(fontsize=12)
plt.tight_layout()
plt.savefig(OUT_DIR / "issue_density.png", dpi=300)

print("RQ1 replication complete")
print(f"Output directory: {OUT_DIR}")
print(f"Kruskal-Wallis p-value: {p:.6g}")
