"""
Title: Urban Tree Planting and Air Pollution:
       Analysis of NetLogo Simulation Experiments
Author: Rongling Liu
Course: ENVSCI 704
Date: 5 October 2026

Background
----------
This project uses a simplified educational model to help Auckland
Council explain how urban tree planting can influence air pollution.
Tree planting may reduce pollution, but its effectiveness also depends
on pollution transport and where trees are planted.

The model explores these relationships using abstract model units.
It is not designed to predict actual air pollution levels in Auckland.

Purpose of this script
----------------------
This Python script analyses and visualises simulation results to answer
three questions:

1. How does planting intensity affect mean environmental pollution?
2. How does wind influence pollution transport and the pollution
   reduction associated with tree planting?
3. With an equal tree budget, how does planting location affect
   mean environmental pollution and pollution hotspots?

Data source
-----------
The simulations were run in NetLogo using a model adapted from
Urban Suite - Pollution (Uri Wilensky, 2007).

The adapted model includes continuous pollution emissions,
simplified directional wind transport, and council-controlled planting.
Experiment 3 also compares different planting priorities.

Numerical results from repeated runs were exported as CSV files
using NetLogo BehaviorSpace. Each scenario used 20 random seeds
to examine variation between runs.

For Experiment 2, separate spatial CSV files were exported from NetLogo.
These record patch pollution at selected ticks for one illustrative
source layout, showing how pollution spreads with and without wind.

Analysis workflow
-----------------
NetLogo generates the simulation data. Python then checks the data,
summarises repeated runs, compares scenarios, and creates figures.

The figures show:
- how pollution changes with planting intensity;
- how wind changes pollution levels and spatial distribution;
- how planting strategies perform under equal tree budgets.

Means, standard deviations, boxplots, and individual paired differences
describe both average outcomes and variation between runs.
The results support an educational explanation of model behaviour;
they do not establish the best planting policy for real Auckland.

How to use
----------
Place the input CSV files in the project's data folder.
Run this script to analyse the data and save figures in the figures folder.
"""

from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.colors import PowerNorm

# Find the data folder beside this Python script.
project_folder = Path(__file__).resolve().parent
data_folder = project_folder / "data"

# ============================================================
# EXPERIMENT 1: PLANTING INTENSITY
# ============================================================

# Research question
# How does increasing planting intensity affect mean environmental
# pollution under fixed emissions and no wind?

# Experimental design and analysis
# Compare five planting intensities: 0, 0.5, 1, 2 and 5 new trees
# per tick. A rate of 0 provides the no-planting reference.
# Each intensity is tested using 20 random seeds.
# Hold other settings constant: two pollution sources, an emission
# rate of 0.1 units per source per tick, no wind, random planting,
# fixed tree cleanup capacities and a duration of 100 ticks.
#
# Check that the data contain final results at step 100 and
# 20 runs for each planting intensity before summarising them.
# Calculate the mean pollution across runs to describe each
# condition, and its standard deviation to show variation between runs.
# Calculate mean tree numbers to show the planting actually achieved.

# Read Experiment 1.
# NetLogo exports six description lines before the column headings.
# Skip these lines to read the correct table header.
experiment1 = pd.read_csv(
    data_folder / "Experiment1_Planting.csv",
    skiprows=6
)

# Inspect the table before calculating any statistics.
print(experiment1.head())
print("Number of rows:", len(experiment1))
print("Column names:", experiment1.columns.tolist())

# Check which simulation steps are recorded in the data.
print("Recorded steps:", experiment1["[step]"].unique())

# Count the number of runs for each planting intensity.
runs_per_setting = experiment1.groupby("planting-rate").size()
print("Runs per planting intensity:")
print(runs_per_setting)

# Summarise the results of repeated runs at each planting intensity.
experiment1_summary = experiment1.groupby("planting-rate").agg(
    mean_pollution=("mean-pollution", "mean"),
    sd_pollution=("mean-pollution", "std"),
    mean_trees=("count trees", "mean")
).reset_index()

# Display the summary table.
print("Experiment 1 summary:")
print(experiment1_summary)

# Create two panels to show pollution outcomes and tree numbers.
# Visualisation approach
# Panel (a) plots final mean pollution against planting intensity,
# directly showing the model's response to increased planting effort.
# Other settings are held constant, allowing comparison of planting
# intensities under the same emission and environmental conditions.
# Error bars show ±1 SD across 20 runs, not confidence intervals.
#
# Panel (b) plots mean tree numbers against planting intensity.
# It helps explain panel (a) by showing how planting effort translates
# into tree establishment. Tree numbers are counts, not canopy coverage.
# Both horizontal axes use the actual numerical planting intensities,
# so the unequal distances between tested settings remain visible.
fig, axes = plt.subplots(1, 2, figsize=(10, 4))
# Plot mean pollution with error bars showing ±1 standard deviation.
axes[0].errorbar(
    experiment1_summary["planting-rate"],
    experiment1_summary["mean_pollution"],
    yerr=experiment1_summary["sd_pollution"],
    fmt="o-",
    capsize=4,
    color="#0072B2",
    label="Mean ± SD (20 runs)"
)

# Label the axes and start the pollution scale at zero.
axes[0].set_xlabel("Planting intensity (new trees per tick)")
axes[0].set_ylabel("Mean environmental pollution (model units)")
axes[0].set_title("(a) Pollution at tick 100")
axes[0].set_ylim(bottom=0)
axes[0].legend()

# Show how planting intensity translates into tree numbers at tick 100.
axes[1].plot(
    experiment1_summary["planting-rate"],
    experiment1_summary["mean_trees"],
    "o-",
    color="#009E73"
)

axes[1].set_xlabel("Planting intensity (new trees per tick)")
axes[1].set_ylabel("Mean number of trees")
axes[1].set_title("(b) Trees at tick 100")
axes[1].set_ylim(bottom=0)

# Display the tested planting intensities on both horizontal axes.
axes[0].set_xticks(experiment1_summary["planting-rate"])
axes[1].set_xticks(experiment1_summary["planting-rate"])# Show how planting intensity translates into tree numbers at tick 100.
axes[1].plot(
    experiment1_summary["planting-rate"],
    experiment1_summary["mean_trees"],
    "o-",
    color="#009E73"
)

axes[1].set_xlabel("Planting intensity (new trees per tick)")
axes[1].set_ylabel("Mean number of trees")
axes[1].set_title("(b) Trees at tick 100")
axes[1].set_ylim(bottom=0)

# Display the tested planting intensities on both horizontal axes.
axes[0].set_xticks(experiment1_summary["planting-rate"])
axes[1].set_xticks(experiment1_summary["planting-rate"])

# Interpretation
# Higher planting intensity produced more trees and lower mean
# pollution at tick 100 under fixed emissions and no wind.
# Panel (a) answers the question by comparing pollution levels;
# panel (b) shows the resulting tree numbers.
# These results describe the model, not actual Auckland predictions.

# Create the figure folder if it does not already exist.
figure_folder = project_folder / "figures"
figure_folder.mkdir(exist_ok=True)

# Adjust spacing so labels fit within the figure.
fig.tight_layout()

# Save a high-resolution PNG for the report and a vector PDF.
fig.savefig(
    figure_folder / "Fig1_Planting_Intensity.png",
    dpi=300,
    bbox_inches="tight"
)
fig.savefig(
    figure_folder / "Fig1_Planting_Intensity.pdf",
    bbox_inches="tight"
)

# Display the figure after saving.
plt.show()

# ============================================================
# EXPERIMENT 2: WIND AND TREE PLANTING
# ============================================================
# Research question
# How does wind strength affect mean pollution and the additional
# pollution reduction associated with tree planting?

# Experimental design and analysis
# Compare four wind strengths: 0, 0.1, 0.2 and 0.4, with planting
# rates of 0 or 1 new tree per tick. Each scenario has 20 runs.
# Keep two pollution sources, emissions of 0.1 units per source
# per tick, eastward wind, random planting, tree cleanup capacities
# and a duration of 100 ticks constant.
#
# Calculate mean pollution and SD for each scenario.
# Pair planting and no-planting runs by wind strength and seed;
# matched runs share the same initial pollution-source locations.
# Calculate no-planting pollution minus planting pollution,
# then summarise these differences using their mean and SD.
# This compares planting outcomes under the same wind conditions,
# because wind itself can transport pollution out of the model.
# Read the final results exported from NetLogo BehaviorSpace.

experiment2 = pd.read_csv(
    data_folder / "Experiment2_Wind.csv",
    skiprows=6
)

# Inspect the data before calculating group statistics.
print("Experiment 2 preview:")
print(experiment2.head())
print("Number of rows:", len(experiment2))
print("Recorded steps:", experiment2["[step]"].unique())

# Each wind-strength and planting-rate combination is a scenario.
# Check that every scenario contains the intended 20 repeated runs.
experiment2_runs = experiment2.groupby(
    ["wind-strength", "planting-rate"]
).size()

print("Runs per wind and planting scenario:")
print(experiment2_runs)

# Summarise planting and no-planting runs separately at each wind strength.
# This provides a no-planting reference under the same wind condition.
# Means describe the overall outcomes across 20 runs.
# Standard deviations show variation between random spatial configurations.
experiment2_summary = experiment2.groupby(
    ["wind-strength", "planting-rate"]
).agg(
    mean_pollution=("mean-pollution", "mean"),
    sd_pollution=("mean-pollution", "std")
).reset_index()

# Display the eight scenario summaries before plotting.
print("Experiment 2 summary:")
print(experiment2_summary)

# Match planting and no-planting runs by wind strength and random seed.
# Matched runs share the same initial pollution-source locations.
# This allows us to compare planting outcomes under the same wind
# condition and initial source layout.
experiment2_paired = experiment2.pivot(
    index=["wind-strength", "random-seed"],
    columns="planting-rate",
    values="mean-pollution"
)

# Check that every pair has both a no-planting and a planting result.
print("Missing values in paired results:")
print(experiment2_paired.isna().sum())

# Calculate the absolute pollution reduction associated with planting.
# A positive difference means pollution was lower in the planting run.
experiment2_paired["pollution_reduction"] = (
    experiment2_paired[0] - experiment2_paired[1]
)

# Restore wind strength and random seed as ordinary columns.
experiment2_paired = experiment2_paired.reset_index()

print("Paired pollution reductions:")
print(experiment2_paired.head())
print("Number of pairs:", len(experiment2_paired))

# Summarise the 20 paired pollution differences at each wind strength.
# The mean describes the additional reduction associated with planting.
# The standard deviation shows how this reduction varies between pairs.
# Calculate variability from the paired differences themselves.
experiment2_reduction_summary = experiment2_paired.groupby(
    "wind-strength"
).agg(
    mean_reduction=("pollution_reduction", "mean"),
    sd_reduction=("pollution_reduction", "std"),
    pairs=("pollution_reduction", "size")
).reset_index()

print("Pollution reduction by wind strength:")
print(experiment2_reduction_summary)

# Visualisation approach
# Panel (a) shows how mean pollution changes with wind strength
# in planting and no-planting runs.
# Panel (b) compares their paired differences across wind strengths,
# showing how the absolute planting benefit changes with wind.
# Positive differences indicate lower pollution with planting.
# Error bars show ±1 SD across 20 runs or pairs.
# Separate spatial maps are needed to show where pollution travels.

fig2, axes2 = plt.subplots(1, 2, figsize=(11, 4.5))

# Select the two planting conditions from the scenario summary.
no_planting = experiment2_summary[
    experiment2_summary["planting-rate"] == 0
]
with_planting = experiment2_summary[
    experiment2_summary["planting-rate"] == 1
]

# Plot pollution levels under the same set of wind conditions.
axes2[0].errorbar(
    no_planting["wind-strength"],
    no_planting["mean_pollution"],
    yerr=no_planting["sd_pollution"],
    fmt="o-",
    capsize=4,
    color="#0072B2",
    label="No planting"
)

axes2[0].errorbar(
    with_planting["wind-strength"],
    with_planting["mean_pollution"],
    yerr=with_planting["sd_pollution"],
    fmt="s-",
    capsize=4,
    color="#009E73",
    label="1 new tree per tick"
)

axes2[0].set_title("(a) Pollution at tick 100")
axes2[0].set_ylabel("Mean environmental pollution (model units)")
axes2[0].set_ylim(bottom=0)
axes2[0].legend()

# Plot the mean and variability of the paired pollution reductions.
axes2[1].errorbar(
    experiment2_reduction_summary["wind-strength"],
    experiment2_reduction_summary["mean_reduction"],
    yerr=experiment2_reduction_summary["sd_reduction"],
    fmt="o-",
    capsize=4,
    color="#D55E00",
    label="Mean ± SD (20 pairs)"
)

# Zero represents no difference between planting and no planting.
axes2[1].axhline(0, color="gray", linestyle="--", linewidth=1)
axes2[1].set_title("(b) Additional planting benefit")
axes2[1].set_ylabel("Pollution difference: no planting − planting")
axes2[1].legend()

# Wind strength is a transport fraction, not a wind speed in m/s.
for ax in axes2:
    ax.set_xlabel("Wind strength (transport fraction per tick)")
    ax.set_xticks([0, 0.1, 0.2, 0.4])

# 3. Interpretation
# Planting reduced mean pollution at every tested wind strength.
# The mean absolute planting benefit varied with wind strength
# and did not increase monotonically.
# Panel (a) shows pollution levels; panel (b) directly compares
# the additional planting benefit under each wind condition.
# These results describe the model, not actual Auckland predictions.

# Adjust spacing and save both panels as one figure.
fig2.tight_layout()

# Save a high-resolution image for the report and a vector PDF.
fig2.savefig(
    figure_folder / "Fig2_Wind_and_Planting.png",
    dpi=300,
    bbox_inches="tight"
)
fig2.savefig(
    figure_folder / "Fig2_Wind_and_Planting.pdf",
    bbox_inches="tight"
)

# Display the figure after saving.
plt.show()

# ============================================================
# EXPERIMENT 2: SPATIAL POLLUTION TRANSPORT
# ============================================================

# 1. Research question
# How does wind change the spatial distribution of pollution over time?

# 2. Experimental design and analysis
# Compare no wind and eastward wind of strength 0.2, without trees.
# Both runs use seed 1001 and the same initial pollution sources.
# Examine snapshots at ticks 10, 30, 60 and 100.
# These snapshots illustrate transport in one source layout;
# they are not averages across the 20 repeated runs.

# Store each snapshot using its wind strength and tick as the key.
spatial_data = {}

for strength in [0, 0.2]:
    for snapshot_tick in [10, 30, 60, 100]:
        filename = f"wind_{strength}_tick_{snapshot_tick}.csv"

        # Spatial exports start with column headings, so do not skip rows.
        snapshot = pd.read_csv(data_folder / filename)
        spatial_data[(strength, snapshot_tick)] = snapshot

        # Check the file size and recorded simulation time.
        print(
            filename,
            "Rows:", len(snapshot),
            "Recorded ticks:", snapshot["tick"].unique()
        )

# Convert patch records into grids for spatial plotting.
# Rows represent y coordinates; columns represent x coordinates.
# Each grid cell contains the pollution value at that location.
pollution_grids = {}

for key, snapshot in spatial_data.items():
    grid = snapshot.pivot(
        index="y",
        columns="x",
        values="pollution"
    )

    # Sort coordinates so all maps use the same spatial order.
    grid = grid.sort_index().sort_index(axis=1)
    pollution_grids[key] = grid

    # Check grid dimensions and missing locations.
    print(
        "Wind and tick:", key,
        "Grid shape:", grid.shape,
        "Missing cells:", grid.isna().sum().sum()
    )

# Visualisation approach
# Compare wind conditions vertically at the same tick.
# Compare successive ticks horizontally to show changes over time.
# All panels share one colour scale, so equal colours represent
# equal pollution values throughout the figure.

# Find the highest pollution value across all eight snapshots.
maximum_pollution = max(
    snapshot["pollution"].max()
    for snapshot in spatial_data.values()
)

# Use a square-root colour scale to make low-pollution plumes visible.
# This changes colour mapping only; the pollution data remain unchanged.
colour_scale = PowerNorm(
    gamma=0.5,
    vmin=0,
    vmax=maximum_pollution
)

fig3, axes3 = plt.subplots(
    2, 4,
    figsize=(13, 7),
    sharex=True,
    sharey=True,
    constrained_layout=True
)

for row, strength in enumerate([0, 0.2]):
    for column, snapshot_tick in enumerate([10, 30, 60, 100]):
        ax = axes3[row, column]
        grid = pollution_grids[(strength, snapshot_tick)]
        snapshot = spatial_data[(strength, snapshot_tick)]

        # Match image boundaries to patch edges and put north at the top.
        image = ax.imshow(
            grid.to_numpy(),
            origin="lower",
            extent=[
                grid.columns.min() - 0.5,
                grid.columns.max() + 0.5,
                grid.index.min() - 0.5,
                grid.index.max() + 0.5
            ],
            cmap="Blues",
            norm=colour_scale,
            interpolation="nearest"
        )

        # Mark emission sources to show pollution relative to its origins.
        sources = snapshot[snapshot["is_source"] == True]
        ax.scatter(
            sources["x"],
            sources["y"],
            marker="D",
            s=25,
            color="#D55E00",
            edgecolors="black",
            linewidths=0.5
        )

        if row == 0:
            ax.set_title(f"Tick {snapshot_tick}")

        if column == 0:
            condition = "No wind" if strength == 0 else "Eastward wind (0.2)"
            ax.set_ylabel(f"{condition}\ny (patch coordinates)")

        if row == 1:
            ax.set_xlabel("x (patch coordinates)")

            # Show the direction pollution is transported.
            ax.annotate(
                "Wind",
                xy=(-10, 23),
                xytext=(-28, 23),
                arrowprops=dict(arrowstyle="->", color="black"),
                va="center"
            )

# A shared colour bar makes pollution levels comparable across panels.
colour_bar = fig3.colorbar(
    image,
    ax=axes3.ravel().tolist(),
    shrink=0.8,
    pad=0.02
)
colour_bar.set_label("Pollution (model units; square-root colour scale)")

fig3.suptitle(
    "Pollution transport without trees\n"
    "Seed 1001; orange diamonds mark pollution sources"
)

# 3. Interpretation
# Without wind, pollution spreads around the sources.
# Eastward wind produces a plume extending towards the eastern boundary.
# Comparing rows at the same tick shows the effect of wind;
# comparing columns shows how the spatial pattern develops over time.
# This illustrates one source layout, not an average across repeated runs.

# Save the spatial comparison for the report.
# constrained_layout already manages spacing for this figure.
fig3.savefig(
    figure_folder / "Fig3_Wind_Spatial_Propagation.png",
    dpi=300,
    bbox_inches="tight"
)
fig3.savefig(
    figure_folder / "Fig3_Wind_Spatial_Propagation.pdf",
    bbox_inches="tight"
)

plt.show()

# ============================================================
# EXPERIMENT 3: PLANTING STRATEGY AND TREE BUDGET
# ============================================================

# 1. Research question
# Under a limited tree budget, how does planting strategy affect
# pollution, and does strategy performance change with the budget?

# 2. Experimental design and analysis
# Compare random, source-targeted and high-pollution-targeted planting
# at budgets of 5, 10 and 30 trees, using 20 seeds per scenario.
# Compare strategies within the same budget to assess placement
# effects without differences in the number of trees planted.
#
# Keep two sources, emissions of 0.1 units per source per tick,
# eastward wind of strength 0.2 and tree cleanup capacities constant.
# Run without trees for 30 ticks, then plant the full budget once.
# High-pollution targeting uses the pollution distribution at tick 30.
# Continue for 100 ticks after planting and record results at tick 130.
# There is no further planting during this period.

# Read the final BehaviorSpace results.
experiment3 = pd.read_csv(
    data_folder / "Experiment3_Budget.csv",
    skiprows=6
)

# Inspect the data and distinguish model ticks from BehaviorSpace steps.
# The 30 warm-up ticks occur during setup, so step 100 is model tick 130.
print("Experiment 3 preview:")
print(experiment3.head())
print("Number of rows:", len(experiment3))
print("BehaviorSpace steps:", experiment3["[step]"].unique())
print("Model ticks:", experiment3["ticks"].unique())

# Check the number of runs for each budget and strategy combination.
experiment3_runs = experiment3.groupby(
    ["tree-budget", "planting-strategy"]
).size()

print("Runs per budget and strategy:")
print(experiment3_runs)

# Check that every run planted exactly the assigned number of trees.
budget_matches = (
    experiment3["count trees"] == experiment3["tree-budget"]
).all()
print("Tree counts match budgets:", budget_matches)

# Summarise pollution outcomes within each budget and strategy.
# Mean environmental pollution describes the whole model area.
# Maximum patch pollution describes the strongest remaining hotspot.
# Comparing both outcomes allows strategy performance to be assessed
# against overall pollution and hotspot pollution separately.
experiment3_summary = experiment3.groupby(
    ["tree-budget", "planting-strategy"]
).agg(
    mean_pollution=("mean-pollution", "mean"),
    sd_pollution=("mean-pollution", "std"),
    mean_max_pollution=("max-pollution", "mean"),
    sd_max_pollution=("max-pollution", "std")
).reset_index()

print("Experiment 3 summary:")
print(experiment3_summary.to_string(index=False))

# Visualisation approach
# Group the three strategies within each tree budget to compare
# placement effects while keeping tree numbers equal.
# Compare budget groups to examine how strategy outcomes change
# with available planting resources.
# Panel (a) shows whole-area pollution; panel (b) shows hotspot pollution.
#
# Boxplots show the distribution of the 20 runs in each scenario.
# Boxes contain the middle 50% of results; lines mark medians.
# Whiskers extend to the most extreme results within 1.5 IQR.
# Circles show results beyond the whiskers; diamonds mark means.
# Boxplots describe variation, not statistical significance.

strategies = ["random", "source-targeted", "high-pollution"]
strategy_labels = ["Random", "Source-targeted", "High-pollution targeted"]
strategy_colours = ["#0072B2", "#009E73", "#D55E00"]
budgets = [5, 10, 30]

fig4, axes4 = plt.subplots(1, 2, figsize=(12, 5))

# Draw the same comparison for the two pollution outcomes.
for panel, outcome in enumerate(["mean-pollution", "max-pollution"]):
    ax = axes4[panel]
    legend_handles = []

    for strategy_index, strategy in enumerate(strategies):
        values_by_budget = []
        positions = []

        for budget_index, budget in enumerate(budgets):
            # Select all 20 runs for this strategy and budget.
            values = experiment3.loc[
                (experiment3["tree-budget"] == budget)
                & (experiment3["planting-strategy"] == strategy),
                outcome
            ]
            values_by_budget.append(values)

            # Offset strategies slightly around each budget group.
            positions.append(
                budget_index + 1 + (strategy_index - 1) * 0.25
            )

        boxes = ax.boxplot(
            values_by_budget,
            positions=positions,
            widths=0.2,
            patch_artist=True,
            manage_ticks=False,
            showmeans=True,
            boxprops=dict(
                facecolor=strategy_colours[strategy_index],
                alpha=0.6
            ),
            medianprops=dict(color="black"),
            meanprops=dict(
                marker="D",
                markerfacecolor="white",
                markeredgecolor="black",
                markersize=4
            ),
            flierprops=dict(marker="o", markersize=3)
        )

        legend_handles.append(boxes["boxes"][0])

    # Budgets are displayed as categories, with strategies grouped together.
    ax.set_xticks([1, 2, 3])
    ax.set_xticklabels(budgets)
    ax.set_xlabel("Tree budget (number of trees)")
    ax.set_ylim(bottom=0)
    ax.legend(
        legend_handles,
        strategy_labels,
        fontsize=8,
        loc="upper right"
    )

axes4[0].set_title("(a) Whole-area pollution at tick 130")
axes4[0].set_ylabel("Mean environmental pollution (model units)")

axes4[1].set_title("(b) Hotspot pollution at tick 130")
axes4[1].set_ylabel("Maximum patch pollution (model units)")

# Interpretation
# Both targeted strategies had lower average whole-area and hotspot
# pollution than random planting at each tested budget.
# Comparing strategies within each budget shows that tree placement
# matters even when the number of trees is equal.
# The relative performance of the two targeted strategies depends
# on the budget and pollution outcome used for comparison.
# These findings apply to the tested model conditions.

# Save the strategy and budget comparison.
fig4.tight_layout()

fig4.savefig(
    figure_folder / "Fig4_Strategy_and_Budget.png",
    dpi=300,
    bbox_inches="tight"
)
fig4.savefig(
    figure_folder / "Fig4_Strategy_and_Budget.pdf",
    bbox_inches="tight"
)

plt.show()

# Further comparison: the two targeted planting strategies
#
# Question:
# Which targeted strategy produces lower mean pollution
# at each tree budget?
#
# Method:
# Pair runs with the same tree budget and random seed.
# This compares strategies under the same initial source layout.

experiment3_paired = experiment3.pivot(
    index=["tree-budget", "random-seed"],
    columns="planting-strategy",
    values="mean-pollution"
)

# Check that each pair contains both targeted strategies.
print("\nMissing values in the paired strategies:")
print(
    experiment3_paired[
        ["source-targeted", "high-pollution"]
    ].isna().sum()
)

# Calculate the difference within each pair.
# Negative: source-targeted has lower mean pollution.
# Positive: high-pollution targeted has lower mean pollution.
experiment3_paired["strategy_difference"] = (
    experiment3_paired["source-targeted"]
    - experiment3_paired["high-pollution"]
)

# Return the budget and seed to ordinary columns.
experiment3_paired = experiment3_paired.reset_index()

print("\nFirst five paired comparisons:")
print(
    experiment3_paired[
        ["tree-budget", "random-seed", "strategy_difference"]
    ].head()
)

print("\nNumber of paired comparisons:", len(experiment3_paired))

# Summarise the paired differences at each tree budget.
# The mean shows which strategy performs better on average.
# The SD shows how much the difference varies across source layouts.

experiment3_difference_summary = (
    experiment3_paired.groupby("tree-budget")
    .agg(
        mean_difference=("strategy_difference", "mean"),
        sd_difference=("strategy_difference", "std"),
        pairs=("strategy_difference", "size")
    )
    .reset_index()
)

print("\nPaired strategy comparison by tree budget:")
print(experiment3_difference_summary.to_string(index=False))

# Visualisation:
# Each dot represents one paired strategy comparison.
# The zero line separates which strategy has lower pollution.
# Mean +/- SD summarises the differences across the 20 pairs.
#
# The left panel includes all budgets and all observations.
# The right panel shows budgets 10 and 30 on a finer vertical scale.

fig5, axes5 = plt.subplots(1, 2, figsize=(12, 5))

for panel, selected_budgets in enumerate([[5, 10, 30], [10, 30]]):
    ax = axes5[panel]

    for position, budget in enumerate(selected_budgets, start=1):
        differences = experiment3_paired.loc[
            experiment3_paired["tree-budget"] == budget,
            "strategy_difference"
        ].to_numpy()

        # Spread dots horizontally so overlapping values are easier to see.
        # This changes their display positions only, not their differences.
        dot_positions = [
            position + (i - (len(differences) - 1) / 2) * 0.012
            for i in range(len(differences))
        ]

        ax.scatter(
            dot_positions,
            differences,
            color="#0072B2",
            alpha=0.65,
            s=25,
            label="Individual pairs" if position == 1 else None
        )

        summary = experiment3_difference_summary.loc[
            experiment3_difference_summary["tree-budget"] == budget
        ].iloc[0]

        ax.errorbar(
            position,
            summary["mean_difference"],
            yerr=summary["sd_difference"],
            fmt="D",
            color="black",
            capsize=5,
            markersize=6,
            label="Mean ± SD" if position == 1 else None
        )

    # Negative differences favour source-targeted planting;
    # positive differences favour high-pollution targeted planting.
    ax.axhline(0, color="grey", linestyle="--", linewidth=1)

    ax.set_xticks(range(1, len(selected_budgets) + 1))
    ax.set_xticklabels(selected_budgets)
    ax.set_xlim(0.5, len(selected_budgets) + 0.5)
    ax.set_xlabel("Tree budget (number of trees)")
    ax.set_ylabel(
        "Mean pollution difference (model units)\n"
        "Source-targeted − high-pollution targeted"
    )
    ax.ticklabel_format(axis="y", style="sci", scilimits=(0, 0))
    ax.legend(fontsize=8)
        # Explain which strategy is favoured on each side of zero.
    ax.text(
        0.98, 0.97,
        "Above zero: high-pollution planting performs better",
        transform=ax.transAxes,
        ha="right", va="top", fontsize=8
    )

    ax.text(
        0.98, 0.03,
        "Below zero: planting near sources performs better",
        transform=ax.transAxes,
        ha="right", va="bottom", fontsize=8
    )

axes5[0].set_title("(a) All tested budgets")
axes5[1].set_title("(b) Budgets 10 and 30: finer scale")

# 3. Interpretation
# Source-targeted planting had lower mean pollution on average
# at budgets 5 and 10; high-pollution targeted planting did better at 30.
# Individual pairs show that neither strategy won in every run.
# The large variation at budget 5 makes its average less representative.
# These findings apply to the tested model conditions.

# Save the paired strategy comparison.
fig5.tight_layout()

fig5.savefig(
    figure_folder / "Fig5_Paired_Strategy_Comparison.png",
    dpi=300,
    bbox_inches="tight"
)

fig5.savefig(
    figure_folder / "Fig5_Paired_Strategy_Comparison.pdf",
    bbox_inches="tight"
)

plt.show()