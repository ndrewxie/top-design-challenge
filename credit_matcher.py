import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv("card_terms_cleaned.csv", sep = ",", usecols=[
    "APR Credit 1",
    "Intro APR Credit 1",
    "Annualized Periodic Fees",
    "Targeted Credit Tiers",
    "Provider",
    "Product Name"
])
df.drop(df[~df["Targeted Credit Tiers"].str.contains("1")].index, inplace=True)

print(df.loc[df["APR Credit 1"] == df["APR Credit 1"].min()])

"""
fig = plt.figure()
plot = fig.add_subplot(projection='3d')
plot.scatter(df["APR Credit 1"], df["Intro APR Credit 1"], df["Annualized Periodic Fees"])
plot.set_xlabel('APR')
plot.set_ylabel('Intro APR')
plot.set_zlabel('Fees')
plt.xlim(0, 50)
plt.ylim(0, 50)
"""

fig = plt.figure()
plot = fig.add_subplot()
plot.scatter(df["APR Credit 1"], df["Annualized Periodic Fees"])
plot.set_xlabel('APR')
plot.set_ylabel('Fees')
plt.xlim(0, 50)

plt.show()