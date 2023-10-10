import pandas as pd

df = pd.read_csv("card_terms.csv", sep = ",")

# Generally, specific benefits and cash back is too hard to compare, and likely isn't the principal factor
df.drop(columns=df.columns[160:], inplace=True)
df.drop(columns=df.columns[(4*26+9-1):(4*26+18-1)], inplace=True)
# Generally too specific for us to care about
df.drop(df[df["Pertains to Specific Counties?"] == "Yes"].index, inplace=True)
# These are really fine-grained - often just saying "within the geographic boundaries of our bank" (not even a ZIP code)
df.drop(df[df["Geographic Restrictions"].notnull()].index, inplace=True)
df.drop(df[df["Professional Affiliation"].notnull()].index, inplace=True)
df.drop(df[df["Requirements: Other"].notnull()].index, inplace=True)
# Probably too prohibitive for college students!
df.drop(df[df["Secured Card"] == "Yes"].index, inplace=True)
# Is this even a credit card?
df.drop(df[df["Purchase APR Offered?"] == "No"].index, inplace=True)
# Unifying state columns
# State (Multiple) is now clearly redundant, and so is regional/national availability, cuz that can be inferred from NaN/Not NaN
df.loc[df["State"].isnull(), "State"] = df["State (Multiple)"]
df.drop([
    "Report Date", "Pertains to Specific Counties?", "Geographic Restrictions", "Professional Affiliation", 
    "Requirements for Opening Types", "Requirements for Opening", "Secured Card", "State (Multiple)", "Availability of Credit Card Plan",
    "Requirements: Other", "Purchase APR Offered?"
], axis=1, inplace=True)
# These rows literally are not used
df.drop([
    "Purchase APR Vary by Balance", "Balance Range (From)", "Balance Range (To)", "APR - 2nd Tier", "Balance Range (From) - 2nd Tier",
    "Balance Range (To) - 2nd Tier", "APR - 3rd Tier", "Balance Range (From) - 3rd Tier", "Balance Range (To) - 3rd Tier", 
    "APR - 4th Tier", "Balance Range (From) - 4th Tier", "Balance Range (To) - 4th Tier"
], axis=1, inplace=True)
# Too specific for us to care about
df.drop(["Purchase APR Index", "Variable Rate Index"], axis=1, inplace=True)
df.rename(columns = {"Index": "APRVariableFixed"})
# Recode target credit scores. 1=Poor or Fair Credit, 2 = Good Credit, 3 = Great Credit
def recode(value):
    value = value.replace("Poor or fair credit (credit score 619 or less)", "1")
    value = value.replace("Good credit (credit scores from 620 to 719)", "2")
    value = value.replace("Great Credit (credit score of 720 or greater)", "3")
    value = value.replace(" ", "")
    value = value.replace(";", "")
    return value
df["Targeted Credit Tiers"] = df["Targeted Credit Tiers"].map(recode)

df.to_csv("card_terms_cleaned.csv")