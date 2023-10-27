import pandas as pd

score = input("Enter credit score (N/A if none): ")
if not score.isdigit():
    score = "0"
score = int(score)

scorecat = ""
if score <= 619:
    scorecat = "1"
elif score <= 719:
    scorecat = "2"
else:
    scorecat = "3"

df = pd.read_csv("card_terms_cleaned.csv", sep = ",", usecols=["Provider", "Product Name", "APR Credit " + scorecat, "Annualized Periodic Fees"])
df.rename(columns = {"APR Credit " + scorecat: "APR"}, inplace=True)
print(df[df["APR"] == df["APR"].min()].to_string())