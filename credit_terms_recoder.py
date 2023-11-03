import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv("card_terms.csv", sep = ",")

df.drop(df[df["Provider"].str.contains("(?i)police")].index, inplace=True)

# Generally too specific for us to care about
df.drop(df[df["Pertains to Specific Counties?"] == "Yes"].index, inplace=True)
# These are really fine-grained - often just saying "within the geographic boundaries of our bank" (not even a ZIP code)
df.drop(df[df["Geographic Restrictions"].notnull()].index, inplace=True)
df.drop(df[df["Professional Affiliation"].notnull()].index, inplace=True)
df.drop(df[df["Requirements: Other"].notnull()].index, inplace=True)
# Is this even a credit card?
df.drop(df[df["Purchase APR Offered?"] == "No"].index, inplace=True)
# Unifying state columns
# State (Multiple) is now clearly redundant, and so is regional/national availability, cuz that can be inferred from NaN/Not NaN
df.loc[df["State"].isnull(), "State"] = df["State (Multiple)"]
df.drop([
    "Report Date", "Pertains to Specific Counties?", "Geographic Restrictions", "Professional Affiliation", 
    "Requirements for Opening Types", "Requirements for Opening", "State (Multiple)", "Availability of Credit Card Plan",
    "Requirements: Other", "Purchase APR Offered?", "Balance Computation Method", "Balance Computation Method Details"
], axis=1, inplace=True)
df.drop([
    "Cash Advance APR Offered?", "Cash Advance APR Vary by Credit Tier", "Poor or Fair Credit.3", "Good Credit.3", 
    "Great Credit.3", "Minimum APR.3", "Median APR.3", "Maximum APR.3"
], axis=1, inplace=True)
# These rows literally are not used
df.drop([
    "Purchase APR Vary by Balance", "Balance Range (From)", "Balance Range (To)", "APR - 2nd Tier", "Balance Range (From) - 2nd Tier",
    "Balance Range (To) - 2nd Tier", "APR - 3rd Tier", "Balance Range (From) - 3rd Tier", "Balance Range (To) - 3rd Tier", 
    "APR - 4th Tier", "Balance Range (From) - 4th Tier", "Balance Range (To) - 4th Tier"
], axis=1, inplace=True)
# Too specific for us to care about
df.drop(["Purchase APR Index", "Variable Rate Index"], axis=1, inplace=True)
df.rename(columns = {"Index": "APRVariableFixed"}, inplace=True)
# Recode target credit scores. 1=Poor or Fair Credit, 2 = Good Credit, 3 = Great Credit
def recode(value):
    value = value.replace("Poor or fair credit (credit score 619 or less)", "1")
    value = value.replace("Good credit (credit scores from 620 to 719)", "2")
    value = value.replace("Great Credit (credit score of 720 or greater)", "3")
    value = value.replace(" ", "")
    value = value.replace(";", "")
    return '"' + value + '"'
df["Targeted Credit Tiers"] = df["Targeted Credit Tiers"].map(recode)

# Rename cols and impute APR
df.rename(columns = {
    "Poor or Fair Credit": "APR Credit 1", 
    "Good Credit": "APR Credit 2", 
    "Great Credit": "APR Credit 3"
}, inplace=True)
df.rename(columns = {
    "Poor or Fair Credit.1": "Intro APR Credit 1", 
    "Good Credit.1": "Intro APR Credit 2", 
    "Great Credit.1": "Intro APR Credit 3"
}, inplace=True)
df.rename(columns = {
    "Poor or Fair Credit.2": "Balance Transfer APR Credit 1", 
    "Good Credit.2": "Balance Transfer APR Credit 2", 
    "Great Credit.2": "Balance Transfer APR Credit 3"
}, inplace=True)
for fixes in [("APR", ""), ("Intro APR", ".1"), ("Balance Transfer APR", ".2")]:
    for apr_mask in [("1", "1", "Maximum"), ("2", "1|2", "Median"), ("3", "1|2|3", "Minimum")]:
        name = fixes[0] + " Credit " + apr_mask[0]
        df.loc[(df[name].isnull() | df[name].str.contains("999.00%")) & df['Targeted Credit Tiers'].str.contains(apr_mask[1]), name] = df[apr_mask[2] + " APR" + fixes[1]]
        df.loc[df[name].isnull(), name] = "999.00%"
        df.loc[~df['Targeted Credit Tiers'].str.contains(apr_mask[1]), name] = "999.00%"
        df[name] = df[name].str.rstrip('%').astype('float')
    df.drop(["Minimum APR" + fixes[1], "Median APR" + fixes[1], "Maximum APR" + fixes[1]], axis=1, inplace=True)
df.drop(["Purchase APR Vary by Credit Tier", "Introductory APR Vary By Credit Tier", "Balance Transfer APR Vary by Credit Tier"], axis=1, inplace=True)
df.drop(["Balance Transfer Offered?"], axis=1, inplace=True)
df.rename(columns = {
    "Median Length of Introductory APR": "Intro APR Length",
    "Median Length of Balance Transfer APR": "Balance Transfer APR Length"
}, inplace=True)

# Lump all periodic fees into an annualized estimate
fee_multipliers = {
    "Annual": 1.0,
    "Monthly": 12.0,
    "Weekly": 52.0,
    "Daily": 365.0,
}
df.rename(columns = {"Periodic Fee Type": "Annualized Periodic Fees"}, inplace=True)
df["Annualized Periodic Fees"] = 0.00
for period in fee_multipliers:
    if not ((period + " Fee") in df):
        continue
    df[period + " Fee"] = df[period + " Fee"].replace('[\$,]', '', regex=True).astype(float)
    df.loc[df[period + " Fee"].isnull(), period + " Fee"] = 0.0
    df["Annualized Periodic Fees"] = df["Annualized Periodic Fees"] + df[period + " Fee"] * fee_multipliers[period]
    df.drop([period + " Fee"], axis=1, inplace=True)

df.to_csv("card_terms_cleaned.csv")