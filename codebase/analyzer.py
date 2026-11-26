import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv("patients.csv")

before_count = len(df)
df = df.drop_duplicates()
dup_count = before_count - len(df)

median_age = int(df["Age"].median())
df["Age"] = df["Age"].replace(pd.NA, median_age)

stay_days = []
for i in range(len(df)):
    d1 = pd.to_datetime(df["Admit_Date"].iloc[i])
    d2 = pd.to_datetime(df["Discharge_Date"].iloc[i])
    diff = d2 - d1
    stay_days.append(diff.days)

df["Stay_Days"] = stay_days
df = df[df["Stay_Days"] >= 0]

def get_age_group(age):
    if age <= 40:
        return "0-40"
    elif age <= 60:
        return "41-60"
    else:
        return "61+"

age_groups = []
for age in df["Age"]:
    age_groups.append(get_age_group(age))
df["Age_Group"] = age_groups

while True:
    print("\n1. Department count")
    print("2. Length of stay")
    print("3. Stay and age groups")
    print("4. Cleaning report")
    print("5. Exit")

    choice = input("Enter option (1-5): ")

    if choice == "1":
        dept_counts = df.groupby("Department").size()
        parts = []
        for dept, count in dept_counts.items():
            parts.append(dept + ": " + str(count))
        print(" | ".join(parts))
        print("Total patients:", len(df))

    elif choice == "2":
        for i in range(len(df)):
            pid = "P" + str(i + 1)
            print(pid + ":", df["Stay_Days"].iloc[i], "days")
        print("Average stay:", f"{df['Stay_Days'].mean():.2f}", "days")

    elif choice == "3":
        print("Average stay:", f"{df['Stay_Days'].mean():.2f}", "days")
        g1 = 0
        g2 = 0
        g3 = 0
        for grp in df["Age_Group"]:
            if grp == "0-40":
                g1 = g1 + 1
            elif grp == "41-60":
                g2 = g2 + 1
            else:
                g3 = g3 + 1
        print("Age groups: 0-40:", g1, "| 41-60:", g2, "| 61+:", g3)

        df.groupby("Department").size().plot(kind="bar", color="skyblue")
        plt.title("Patient Count by Department")
        plt.xlabel("Department")
        plt.ylabel("Number of Patients")
        plt.show()
        print("Bar chart displayed")

    elif choice == "4":
        print("Duplicates removed:", dup_count)
        print("Missing Age filled with median:", median_age)

    elif choice == "5":
        break

    else:
        print("Invalid option.")