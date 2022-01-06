import pandas as pd

filename = "tempPCA.csv"
data = pd.read_csv(filename)

x = data["Id"]
print(x)


df = pd.read_csv("myPCAclass_Testing.csv")
df["Id"] = x

df.to_csv("myPCAclass_Testing.csv", index=False)

