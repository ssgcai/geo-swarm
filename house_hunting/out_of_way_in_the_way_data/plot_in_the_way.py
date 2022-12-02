import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from scipy.stats import ttest_ind


scaled_in_the_way_df = pd.concat((pd.read_csv("all_dists_"+str(i)+".csv", sep="\t") for i in range(2, 10)))
scaled_in_the_way_df["type"] = "scaled quorum, in the way"

fixed_in_the_way_df = pd.concat((pd.read_csv("fixed_all_dists_"+str(i)+".csv", sep="\t") for i in range(2, 10)))
fixed_in_the_way_df["type"] = "fixed quorum, in the way"

q = fixed_in_the_way_df["time"].quantile(0.99)

fixed_in_the_way_df=fixed_in_the_way_df[fixed_in_the_way_df["time"] < q]

scaled_out_of_way_df = pd.concat((pd.read_csv("all_dists_out_of_way"+str(i)+".csv", sep="\t") for i in range(2, 10)))
scaled_out_of_way_df["type"] = "scaled quorum, out of way"

fixed_out_of_way_df = pd.concat((pd.read_csv("fixed_all_dists_out_of_way"+str(i)+".csv", sep="\t") for i in range(2, 10)))
fixed_out_of_way_df["type"] = "fixed quorum, out of way"

fixed_itw_2x = {
	"type" : ["fixed quorum, in the way"]*100,
	"dist": ["2x"]*100, 
	"accuracy": [1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 0.0, 1.0, 1.0, 1.0, 1.0, 0.0, 1.0, 0.0, 1.0, 1.0, 0.0, 1.0, 1.0, 1.0, 1.0, 0.0, 1.0, 1.0, 1.0, 1.0, 0.06, 0.0, 1.0, 0.0, 0.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 0.0, 1.0, 1.0, 0.0, 1.0, 1.0, 1.0, 1.0, 1.0, 0.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 0.0, 0.0, 1.0, 1.0, 1.0, 0.0, 0.0, 1.0, 1.0, 0.0, 0.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 0.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 0.0, 1.0, 0.0, 1.0, 0.0, 1.0, 0.0, 1.0, 1.0, 1.0, 1.0, 1.0, 0.0, 0.0, 1.0],
	"time": [2139, 1418, 1091, 2279, 1460, 1023, 2487, 975, 1014, 2196, 1360, 1020, 1634, 9808, 2104, 2866, 1917, 1640, 2056, 1873, 1780, 1137, 999, 1502, 1385, 671, 2764, 1816, 666, 1485, 1997, 1072, 1159, 1980, 1629, 2768, 2205, 1095, 1910, 295, 1238, 1885, 736, 1709, 2242, 2111, 2019, 1309, 1914, 1858, 1815, 1650, 2197, 1664, 2288, 1361, 1831, 2464, 1779, 1100, 3839, 1187, 8462, 1660, 1881, 348, 1796, 2093, 1418, 1612, 916, 1744, 1701, 2515, 9233, 2080, 1685, 793, 1312, 1760, 1022, 2653, 950, 2110, 2090, 2338, 1684, 1099, 1770, 1035, 1119, 782, 1298, 1747, 1807, 1156, 2657, 1098, 1106, 2343],
	"splits": [False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, True, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False]	
}

fixed_itw_3x = {
	"type" : ["fixed quorum, in the way"]*100,
	"dist": ["3x"]*100, 
	"accuracy": [0.0, 1.0, 0.0, 1.0, 1.0, 0.0, 1.0, 1.0, 1.0, 0.0, 0.0, 1.0, 1.0, 0.0, 0.0, 1.0, 0.0, 1.0, 1.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0, 1.0, 0.0, 0.0, 1.0, 1.0, 0.0, 0.0, 0.0, 1.0, 1.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 1.0, 1.0, 0.0, 1.0, 0.0, 1.0, 0.0, 0.0, 1.0, 1.0, 1.0, 0.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 0.0, 1.0, 1.0, 1.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 1.0, 1.0, 1.0, 1.0, 1.0, 0.0, 1.0, 1.0, 1.0, 1.0, 0.0, 1.0, 0.1, 1.0, 0.0, 1.0, 0.0, 1.0, 1.0, 0.0, 1.0, 1.0, 0.0, 1.0, 0.0, 0.0, 1.0],
	"time": [559, 1768, 2072, 1417, 3258, 1045, 2082, 1768, 3049, 914, 786, 2890, 2866, 1663, 1953, 2034, 867, 1249, 1642, 824, 682, 1245, 1019, 2996, 862, 1660, 2103, 888, 1565, 1695, 1041, 836, 1080, 2219, 2871, 1613, 1492, 889, 1909, 458, 837, 2234, 2568, 1273, 1200, 1315, 2298, 1462, 1456, 1738, 2133, 2488, 448, 3337, 1168, 2909, 3170, 2774, 1762, 1813, 2172, 3242, 1902, 782, 1914, 1270, 2330, 1423, 1448, 517, 2852, 401, 1611, 1946, 2635, 2626, 1680, 2421, 1837, 1277, 2720, 1895, 2275, 1141, 1369, 2598, 1993, 1696, 2731, 2428, 2939, 2019, 373, 1674, 1634, 702, 2103, 1822, 639, 3259],
	"splits": [False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, True, False, False, False, False, False, False, False, False, False, False, False, False, False, False]
}

df = pd.concat([scaled_in_the_way_df, fixed_in_the_way_df, scaled_out_of_way_df, fixed_out_of_way_df, pd.DataFrame(fixed_itw_2x), pd.DataFrame(fixed_itw_3x)], axis=0, ignore_index=True)
print(df.tail())

df['time'] = df['time'] / 60.0


fig, ax = plt.subplots()

sns.lineplot(x = df['dist'],
            y = df['accuracy'],
            hue = df['type'],
            palette = sns.cubehelix_palette(4),
            #err_style = "bars",
            ax=ax)

ax.set_title("Decision Accuracy for Out-of-Way vs. In-the-Way Poor Nest")
ax.set_xlabel("far nest distance")

plt.savefig("out_of_way_in_the_way_accuracy.pdf")

fig, ax = plt.subplots()

sns.lineplot(x = df['dist'],
            y = df['time'],
            hue = df['type'],
            palette = sns.cubehelix_palette(4),
            #err_style = "bars",
            ax=ax)

ax.set_title("Decision Time for Out-of-Way vs. In-the-Way Poor Nest")
ax.set_xlabel("far nest distance")

plt.savefig("out_of_way_in_the_way_time.pdf")



sq = df[(df['type']=='fixed quorum, out of way') & (df["dist"] == "4x")]
sqo = df[(df['type']=='fixed quorum, in the way') & (df["dist"] == "4x")]
print(ttest_ind(sq['time'], sqo['time']))

sq = df[(df['type']=='fixed quorum, out of way') & (df["dist"] == "3x")]
sqo = df[(df['type']=='fixed quorum, in the way') & (df["dist"] == "3x")]
print(ttest_ind(sq['accuracy'], sqo['accuracy']))

sq = df[(df['type']=='fixed quorum, out of way') & (df["dist"] == "4x")]
sqo = df[(df['type']=='fixed quorum, in the way') & (df["dist"] == "4x")]
print(ttest_ind(sq['accuracy'], sqo['accuracy']))

