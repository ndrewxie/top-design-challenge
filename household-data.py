import pandas as pd

renames = {
    #"FWB1_1": "I could handle a major unexpected expense (Rate statement accuracy - 1: very inaccurate, 5: very accurate)",
    #"FWB1_2": "I am securing my financial future (Rate statement accuracy - 1: very inaccurate, 5: very accurate)",
    #"FWB1_3": "Because of my money situation, I feel like I will never have the things I want in life (Rate statement accuracy - 1: very inaccurate, 5: very accurate)",
    #"FWB1_4": "I can enjoy life because of the way Im managing my money (Rate statement accuracy - 1: very inaccurate, 5: very accurate)",
    #"FWB1_5": "I am just getting by financially (Rate statement accuracy - 1: very inaccurate, 5: very accurate)",
    #"FWB1_6": "I am concerned that the money I have or will save wont last (Rate statement accuracy - 1: very inaccurate, 5: very accurate)",
    "FS1_1": "I know how to get myself to follow through on my financial intentions (Rate statement accuracy - 1: very inaccurate, 5: very accurate)",
    "FS1_2": "I know where to find the advice I need to make decisions involving money (Rate statement accuracy - 1: very inaccurate, 5: very accurate)",
    #"FS1_3": "I know how to make complex financial decisions (Rate statement accuracy - 1: very inaccurate, 5: very accurate)",
    #"FS1_4": "I am able to make good financial decisions that are new to me (Rate statement accuracy - 1: very inaccurate, 5: very accurate)",
    #"FS1_5": "I am able to recognize a good financial investment (Rate statement accuracy - 1: very inaccurate, 5: very accurate)",
    "FS1_6": "I know how to keep myself from spending too much (Rate statement accuracy - 1: very inaccurate, 5: very accurate)",
    "FS1_7": "I know how to make myself save (Rate statement accuracy - 1: very inaccurate, 5: very accurate)",   
    #"FS2_1": "I know when I do not have enough information to make a good decision involving my money (Rate how often - 1: Never, 5: Always)",   
    #"FS2_2": "I know when I need advice about my money (Rate how often - 1: Never, 5: Always)",   
    "FS2_3": "I struggle to understand financial information (Rate how often - 1: Never, 5: Always)",   
    #"SUBKNOWL1": "How would you assess your overall financial knowledge? (1: very low, 7: very high)",
    #"PROPPLAN_1": "I consult my budget to see how much money I have left (Rate statement accuracy - 1: very inaccurate, 5: very accurate)",
    #"PROPPLAN_2": "I actively consider the steps I need to take to stick to my budget (Rate statement accuracy - 1: very inaccurate, 5: very accurate)",
    #"PROPPLAN_3": "I set financial goals for what I want to achieve with my money. (Rate statement accuracy - 1: very inaccurate, 5: very accurate)",
    #"PROPPLAN_4": "I prepare a clear plan of action with detailed steps to achieve my financial goals (Rate statement accuracy - 1: very inaccurate, 5: very accurate)",
    "MANAGE1_1": "Paid all your bills on time (Rate how often - 1: NA, 2: never, 6: always)",
    #"MANAGE1_2": "Stayed within your budget or spending plan (Rate how often - 1: NA, 2: never, 6: always)",
    "MANAGE1_3": "Paid off credit card balance in full each month (Rate how often - 1: NA, 2: never, 6: always)",
    #"MANAGE1_4": "Checked your statements, bills and receipts to make sure there were no errors (Rate how often - 1: NA, 2: never, 6: always)",
    "SAVEHABIT": "Putting money into savings is a habit for me (Rate how accurate: 1: strongly disagree, 6: strongly agree)",
    #"FRUGALITY": "If I can re-use an item I already have, theres no sense in buying something new (Rate how accurate: 1: strongly disagree, 6: strongly agree)",
    "SUBNUMERACY1": "How good are you at working with percentages? (1: not good at all, 6: very good)",
    #"CHANGEABLE": "A person's ability to manage money cannot be changed much (Rate how accurate: 1: strongly disagree, 7: strongly agree)",
    "FINKNOWL1": "Financial literacy: Suppose you had $100 in a savings account and the interest rate was 2% per year. After 5 years, how much do you think you would have in the account if you left the money to grow? (1: More than $102, 2: Exactly $102, 3. Less than $102)",
    "KHKNOWL7": "Suppose you owe $3,000 on your credit card. You pay a minimum payment of $30 each month. At an Annual Percentage Rate of 12% (or 1% per month), how many years would it take to eliminate your credit card debt if you made no additional new charges? (1. Less than 5 years, 2. Between 5 and 10 years, 3. Between 10 and 15 years, 4. Never, you will continue to be in debt)",
    "PRODUSE_1": "Have you used a payday loan or cash advance loan in the past 12 months? 0: No, 1: Yes",
    "PRODUSE_2": "Have you used a pawn loan or auto title loan in the past 12 months? 0: No, 1: Yes",
    "PRODUSE_3": "Have you used a reloadable credit card not linked with a bank account in the past 12 months? 0: No, 1: Yes",
    "PRODUSE_4": "Have you used a place other than a bank or credit union to give or send money in the past 12 months? 0: No, 1: Yes",
    "PRODUSE_5": "Have you used a place other than a bank or credit union to cash a check or purchas a money order in the past 12 months? 0: No, 1: Yes",
    "CONSPROTECT1": "How often have you had experiences with financial services where you did not feel respected or where you felt mistreated? (1: Never, 4: Often)",
    "CONSPROTECT2": "How familiar are you with any agencies or organizations that can help you resolve problems with financial services you are using? (1: Not familiar, 3: Very familar)",
    "REJECTED_1": "In the past 12 months, have you applied for a credit card and been turned down? (0: No, 1: Yes)",
    "REJECTED_2": "In the past 12 months, have decided not to apply for a credit card because you thought you would be turned down? (0: No, 1: Yes)",
}

df = pd.read_csv("Financial-wellbeing-survey-data.csv", sep = ",")
df = df[df.agecat == 1] # 18-24
df = df[df.EMPLOY1_5 == 1] # Full-Time students
df = df.filter(items = list(renames.keys()))
df.rename(columns = renames, inplace=True)

df.to_csv("processed.csv")