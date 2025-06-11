import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# -----------------------------
# Create dataset
# -----------------------------
np.random.seed(42) 

# 50 rows of fake financial data
data = pd.DataFrame({
    "stock_price": np.random.normal(100, 10, 50),
    "volume": np.random.randint(1000, 100000, 50),
    "pe_ratio": np.random.normal(20, 5, 50),
    "market_cap": np.random.uniform(1e9, 1e12, 50),
    "dividend_yield": np.random.uniform(0, 5, 50),
    "beta": np.random.normal(1, 0.2, 50),
    "eps": np.random.normal(5, 1, 50),
    "debt_equity_ratio": np.random.normal(0.5, 0.1, 50),
    "current_ratio": np.random.normal(1.5, 0.3, 50),
    "quick_ratio": np.random.normal(1.2, 0.2, 50),
    "return_on_equity": np.random.uniform(5, 20, 50),
    "profit_margin": np.random.uniform(5, 30, 50),
    "revenue": np.random.uniform(1e6, 1e8, 50),
    "gross_margin": np.random.uniform(20, 60, 50),
    "operating_margin": np.random.uniform(10, 50, 50)
})

# -----------------------------
# Basic EDA
# -----------------------------
print("Dataset shape:", data.shape)
print("\nFirst 5 rows:")
print(data.head())

print("\nSummary Statistics:")
print(data.describe())

print("\nMissing Values:")
print(data.isnull().sum())

# Correlation heatmap
plt.figure(figsize=(12, 8))
sns.heatmap(data.corr(), annot=True, cmap="coolwarm")
plt.title("Correlation Heatmap")
plt.tight_layout()
plt.show()

# -----------------------------
# Task 1: Team Function
# -----------------------------
def team_function():
    """
    This function is for us to practice editing code!
    Your task: Add one print() statement below with your name.
    """
    print('\n' + '*' * 25)
    print("BitBridge Team Members:")
    # Add your line below
    print(" - Faeze Safari")
    print(" - Faeze Safari: 2nd time for practice")
    print(" - Dmitrii Practicing this github task, Faeze thank you for your work!!!") # Dmitrii's comment

# Run the team function
team_function()

# -----------------------------
# Task 2: Create a histogram
# -----------------------------
# Pick any column from the dataset and create a histogram using matplotlib or seaborn.
# Example:
sns.histplot(data['stock_price'], kde=True)
plt.title("Distribution of Stock Prices")
plt.show()

# Faeze added the histogram of revenue
sns.histplot(data['revenue'], kde=True)
plt.title("Distribution of Revenues")
plt.show()

# Dmitrii added the histogram of stock gross margin
sns.histplot(data['gross_margin'], kde=True)
plt.title("Distribution of Gross Margins")
plt.show()
# -----------------------------

# Plot Jon Rahardjo - PE Ratio v Stock Price

plt.figure(figsize=(10, 6))
sns.scatterplot(x=data['pe_ratio'], y=data['stock_price']) 
plt.title('P/E Ratio vs. Stock Price', fontsize=16)
plt.xlabel('P/E Ratio', fontsize=12)
plt.ylabel('Stock Price', fontsize=12)
plt.grid(True)
plt.tight_layout()
plt.show()
