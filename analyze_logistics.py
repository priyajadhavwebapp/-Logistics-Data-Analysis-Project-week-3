from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt

# Project folders
ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "hypothetical_logistics_dataset.csv"
OUT = ROOT / "outputs"
CHARTS = OUT / "charts"
TABLES = OUT / "tables"

CHARTS.mkdir(parents=True, exist_ok=True)
TABLES.mkdir(parents=True, exist_ok=True)

# Load dataset
df = pd.read_csv(DATA)

print("Dataset loaded successfully!")
print("Dataset shape:", df.shape)

# Check missing values
print("\nMissing values:")
print(df.isnull().sum())

# Clean missing values
for col in ["weight_kg", "transportation_cost_inr"]:
    df[col] = df[col].fillna(df[col].median())

df["region"] = df["region"].fillna(df["region"].mode()[0])

# Calculate delivery performance
df["on_time"] = (
    df["actual_delivery_days"]
    <= df["promised_delivery_days"]
)

df["delay_days"] = (
    df["actual_delivery_days"]
    - df["promised_delivery_days"]
).clip(lower=0)

# Descriptive statistics
stats = df.describe(include="all")
stats.to_csv(TABLES / "descriptive_statistics.csv")

# Correlation analysis
numeric = df.select_dtypes(include="number")
numeric.corr().to_csv(TABLES / "correlation_matrix.csv")

# Chart 1: Delivery time distribution
plt.figure(figsize=(8, 5))
plt.hist(df["actual_delivery_days"], bins=15, edgecolor="black")
plt.title("Delivery Time Distribution")
plt.xlabel("Delivery Time (Days)")
plt.ylabel("Number of Shipments")
plt.tight_layout()
plt.savefig(CHARTS / "delivery_time_distribution.png")
plt.close()

# Chart 2: Transportation cost by mode
df.groupby("transport_mode")["transportation_cost_inr"].mean().plot(
    kind="bar", figsize=(8, 5), edgecolor="black"
)
plt.title("Average Transportation Cost by Mode")
plt.xlabel("Transport Mode")
plt.ylabel("Average Cost (INR)")
plt.tight_layout()
plt.savefig(CHARTS / "cost_by_transport_mode.png")
plt.close()

# Chart 3: Distance versus cost
plt.figure(figsize=(8, 5))
plt.scatter(
    df["distance_km"],
    df["transportation_cost_inr"],
    alpha=0.6
)
plt.title("Distance vs Transportation Cost")
plt.xlabel("Distance (KM)")
plt.ylabel("Transportation Cost (INR)")
plt.tight_layout()
plt.savefig(CHARTS / "distance_vs_cost.png")
plt.close()

# Save cleaned dataset
df.to_csv(OUT / "cleaned_logistics_dataset.csv", index=False)

# Display key metrics
print("\nAverage delivery time:",
      round(df["actual_delivery_days"].mean(), 2), "days")

print("Average transportation cost: INR",
      round(df["transportation_cost_inr"].mean(), 2))

print("On-time delivery rate:",
      round(df["on_time"].mean() * 100, 2), "%")

print("\nAnalysis completed successfully!")
print("Charts saved in outputs/charts/")
print("Statistics saved in outputs/tables/")