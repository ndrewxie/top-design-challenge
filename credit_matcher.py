import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv("card_terms_cleaned.csv", sep = ",", usecols=[
    "Provider",
    "Product Name",
    "Targeted Credit Tiers",
    "APR Credit 3",
    "Intro APR Credit 3",
    "Balance Transfer APR Credit 3",
    "Grace Period",
    "Late Fee",
    "Very Late Fee",
    "Secured Card",
    "Annualized Periodic Fees",
])
df.drop(df[~df["Targeted Credit Tiers"].str.contains("1")].index, inplace=True)

# print(df.loc[df["APR Credit 3"] == df["APR Credit 1"].min()])
print(df.loc[df["APR Credit 3"] > 500].to_string())

fig = plt.figure()
plot = fig.add_subplot(projection='3d')
plot.scatter(df["APR Credit 3"], df["Intro APR Credit 3"], df["Annualized Periodic Fees"])
plot.set_xlabel('APR')
plot.set_ylabel('Intro APR')
plot.set_zlabel('Fees')

"""
fig = plt.figure()
plot = fig.add_subplot()
plot.scatter(df["APR Credit 3"], df["Annualized Periodic Fees"])
plot.set_xlabel('APR')
plot.set_ylabel('Fees')
plt.xlim(0, 50)
"""

plt.show()