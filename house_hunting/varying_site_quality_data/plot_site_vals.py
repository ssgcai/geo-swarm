import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from scipy.stats import ttest_ind

eq_df = pd.concat((pd.read_csv("site_val_eq"+str(0.1*i)+"_1.0.csv", sep="\t") for i in range(3, 10, 3)))
eq_df["type"] = "scaled quorum, equidistant sites"
eq_f_df = pd.concat((pd.read_csv("site_val_fixed_eq"+str(0.1*i)+"_1.0.csv", sep="\t") for i in range(3, 10, 3)))
eq_f_df["type"] = "fixed quorum, equidistant sites"
neq_df = pd.concat((pd.read_csv("site_val_neq"+str(0.1*i)+"_1.0.csv", sep="\t") for i in range(3, 10, 3)))
neq_df["type"] = "scaled quorum, 2x far nest"
neq_f_df = pd.concat((pd.read_csv("site_val_fixed_neq"+str(0.1*i)+"_1.0.csv", sep="\t") for i in range(3, 10, 3)))
neq_f_df["type"] = "fixed, 2x far nest"


df = pd.concat([eq_df, eq_f_df, neq_df, neq_f_df], axis=0, ignore_index=True)
df['time'] = df['time'] / 60.0

fig, ax = plt.subplots()

sns.lineplot(x = df['siteA'],
            y = df['accuracy'],
            hue = df['type'],
            palette = sns.cubehelix_palette(4),
            #err_style = "bars",
            ax=ax)

ax.set_title("Decision Accuracy vs. Close Nest Site Quality")
ax.set_xlabel("close nest site quality")
plt.savefig("varying_site_quality_accuracy.pdf")

fig, ax = plt.subplots()

sns.lineplot(x = df['siteA'],
            y = df['time'],
            hue = df['type'],
            palette = sns.cubehelix_palette(4),
            #err_style = "bars",
            ax=ax)

ax.set_title("Decision Time vs. Close Nest Site Quality")
ax.set_xlabel("close nest site quality")
plt.savefig("varying_site_quality_time.pdf")


sq = df[(df['type']=="scaled quorum, 2x far nest") & (df["siteA"] == 0.3)]
sqo = df[(df['type']=="scaled quorum, 2x far nest") & ((df["siteA"]-0.5)**2 < 0.05)]
print(sqo)
print(ttest_ind(sq['accuracy'], sqo['accuracy']))