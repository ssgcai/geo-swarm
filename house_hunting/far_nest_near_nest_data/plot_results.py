import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt


#plot far good site vs. poor close site 
normal_2x = {
	"type" : ["fixed quorum"]*100,
	"dist" : ["2x"]*100,
	"accuracy": [1.0, 0.0, 1.0, 1.0, 0.0, 1.0, 1.0, 1.0, 1.0, 1.0, 0.0, 1.0, 1.0, 1.0, 1.0, 1.0, 0.0, 1.0, 0.0, 1.0, 1.0, 0.0, 1.0, 1.0, 1.0, 0.0, 0.0, 1.0, 1.0, 0.0, 1.0, 1.0, 0.0, 1.0, 1.0, 0.0, 1.0, 1.0, 0.0, 1.0, 1.0, 0.0, 1.0, 1.0, 0.0, 1.0, 0.0, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0, 1.0, 1.0, 1.0, 1.0, 1.0, 0.0, 1.0, 0.0, 1.0, 1.0, 1.0, 0.0, 1.0, 0.0, 0.0, 1.0, 1.0, 0.0, 1.0, 0.0, 1.0, 1.0, 1.0, 1.0, 0.0, 0.0, 0.0, 0.0, 1.0, 1.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0],
	"time": [1687, 1277, 1402, 1515, 681, 1776, 1307, 1209, 2251, 1052, 646, 1451, 1675, 1373, 1340, 1635, 1932, 1408, 856, 1133, 1264, 1248, 1910, 1544, 1838, 1364, 1282, 1485, 1689, 1348, 1463, 1745, 473, 1351, 1406, 1059, 1403, 2031, 288, 2169, 1225, 646, 1761, 1271, 664, 2378, 1030, 2053, 577, 412, 563, 1817, 619, 336, 1020, 1700, 1705, 1639, 1464, 1106, 1416, 1491, 680, 1450, 488, 1912, 1996, 2507, 1406, 1492, 489, 475, 1716, 1554, 1124, 1062, 753, 1841, 1825, 1496, 1330, 704, 471, 753, 1158, 1256, 2103, 1745, 237, 1064, 297, 1503, 738, 1723, 1537, 1519, 865, 1810, 1552, 1520],
	"splits": [False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False]
}

good_2x = {
	"type" : ["scaled quorum"]*100,
	"dist" : ["2x"]*100,
	"time": [980, 1116, 2402, 1978, 2324, 1141, 1869, 1588, 1274, 1387, 2045, 2366, 1708, 1068, 1216, 2248, 1727, 1625, 1020, 1460, 1218, 1763, 1478, 1641, 1224, 2155, 1744, 941, 1481, 2538, 1801, 721, 2070, 1545, 2389, 1925, 1163, 1382, 1035, 1636, 1481, 2136, 1680, 1041, 1110, 1208, 1791, 976, 2065, 622, 1424, 1641, 2242, 1718, 1242, 2400, 2497, 1023, 963, 2243, 2126, 2638, 1761, 1466, 901, 2027, 2024, 1085, 1747, 1948, 1093, 1434, 1309, 1087, 1544, 1773, 1433, 1567, 1366, 2154, 1839, 1213, 1704, 1423, 2492, 2476, 1318, 1887, 1009, 1101, 1416, 1271, 1032, 1444, 1832, 1845, 2121, 1538, 1845, 1310],
	"accuracy": [1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 0.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0],
	"splits": [False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False]
}

normal_3x = {
	"type" : ["fixed quorum"]*100,
	"dist" : ["3x"]*100,
	"accuracy": [0.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 0.0, 0.0, 1.0, 1.0, 1.0, 1.0, 1.0, 0.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 0.0, 1.0, 1.0, 1.0, 1.0, 0.0, 1.0, 0.0, 1.0, 1.0, 0.0, 0.0, 1.0, 1.0, 0.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 0.0, 1.0, 1.0, 1.0, 1.0, 1.0, 0.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 0.0, 0.0, 0.0, 0.0, 1.0, 1.0, 0.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 0.0, 1.0, 1.0, 1.0, 1.0, 0.0, 1.0, 1.0, 1.0, 1.0, 0.0, 1.0, 1.0, 0.0, 1.0, 0.0, 1.0, 1.0, 0.0, 1.0],
	"time": [1994, 2332, 1679, 2878, 2794, 3336, 4408, 3127, 2690, 3653, 577, 1840, 1637, 2310, 3749, 2511, 3935, 1063, 2220, 1425, 1324, 3247, 2565, 2920, 1560, 2274, 3589, 2400, 2347, 1176, 2402, 1554, 2477, 1822, 1604, 897, 5243, 2707, 977, 1747, 2902, 2365, 1352, 3387, 1910, 2740, 1296, 3290, 2788, 4221, 1937, 4963, 1319, 2921, 1212, 2986, 1653, 1493, 3806, 4403, 3553, 1723, 3709, 3258, 2337, 1716, 1262, 1235, 1100, 2215, 4145, 1842, 3167, 2503, 2171, 1712, 2987, 3229, 1772, 2635, 1464, 2787, 3819, 2454, 3164, 953, 1912, 2821, 3266, 3332, 3305, 3622, 2107, 1936, 2681, 2360, 2526, 2976, 889, 4269],
	"splits": [False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False]
}

good_3x = {
	"type" : ["scaled quorum"]*100,
	"dist" : ["3x"]*100,
	"accuracy": [1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 0.1, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0],
	"time": [3669, 3894, 4121, 2763, 2132, 4606, 1861, 1389, 2695, 3734, 3932, 2747, 1465, 2410, 2933, 2542, 2878, 2172, 2891, 2547, 4976, 2180, 3309, 2302, 2582, 3414, 2944, 3259, 3314, 2435, 3416, 3618, 3873, 2636, 2480, 3691, 2855, 2201, 3548, 4074, 3052, 3175, 2676, 2529, 3270, 2356, 2620, 2304, 3370, 3232, 4180, 3346, 1516, 2329, 2948, 2217, 2077, 2241, 3030, 3179, 3257, 2135, 3904, 3509, 3167, 3363, 2709, 2459, 2304, 2049, 925, 2725, 5462, 3739, 2992, 2085, 3809, 3720, 3001, 3078, 2852, 3586, 1906, 1564, 3505, 3116, 3002, 3647, 2385, 3730, 2534, 2274, 2322, 3299, 1410, 1767, 2356, 2473, 3471, 3230],
	"splits": [False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, True, False, False, False, False, False, False, False, False, False]
}

normal_9x = {
	"type" : ["fixed quorum"]*100,
	"dist" : ["9x"]*100,
	"accuracy": [0.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 0.0, 1.0, 1.0, 1.0, 0.0, 1.0, 1.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0, 1.0, 1.0, 1.0, 0.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 0.0, 1.0, 0.0, 1.0, 0.0, 1.0, 1.0, 0.0, 0.0, 1.0, 0.0, 1.0, 1.0, 1.0, 1.0, 0.0, 1.0, 0.0, 1.0, 0.0, 1.0, 1.0, 1.0, 1.0, 0.0, 1.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0, 1.0, 1.0, 1.0, 0.0, 1.0, 1.0, 0.0, 0.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 0.0, 1.0, 0.0, 1.0, 0.0],
	"time": [2106, 3647, 4977, 4670, 6413, 4852, 7481, 9045, 4923, 6750, 4423, 2318, 5140, 2421, 6957, 2821, 8336, 6465, 2250, 2425, 4674, 4911, 3897, 7224, 4509, 1066, 2116, 4679, 2132, 5351, 4591, 6383, 6565, 7128, 2765, 6533, 4813, 5200, 5828, 4190, 6519, 6561, 4146, 5188, 4658, 6944, 7460, 7698, 6483, 4442, 7159, 2634, 5387, 4005, 5467, 4440, 2442, 1133, 5108, 1414, 2346, 6207, 6003, 4860, 1002, 2245, 3041, 7790, 2158, 3809, 5600, 4178, 2842, 2259, 6759, 2492, 3207, 972, 2367, 4687, 1779, 4938, 3978, 4126, 4496, 6420, 4232, 2800, 2261, 4166, 2513, 4038, 5099, 2871, 6111, 3314, 6760, 1743, 4376, 2366],
	"splits": [False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False]
}

good_9x = {
	"type" : ["scaled quorum"]*100,
	"dist" : ["9x"]*100,
	"accuracy": [1.0, 1.0, 1.0, 1.0, 1.0, 0.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 0.0, 1.0, 1.0, 0.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 0.0, 1.0, 1.0, 1.0, 0.0, 1.0, 0.0, 1.0, 1.0, 1.0, 0.0, 1.0, 1.0, 0.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 0.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 0.09, 0.0, 0.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0],
	"time": [3678, 2874, 5034, 5805, 3884, 3553, 3796, 3910, 3184, 5071, 4085, 3852, 4019, 3090, 6165, 3029, 5121, 6260, 4335, 3552, 5252, 7112, 3339, 3865, 4077, 4001, 4492, 3519, 5901, 4014, 6228, 4456, 2521, 3914, 6911, 6323, 5201, 4582, 5167, 5021, 3843, 2036, 6914, 5913, 3247, 4024, 4202, 5143, 5681, 5690, 6060, 2061, 2946, 2035, 2914, 2962, 4255, 2275, 2653, 5427, 4428, 1400, 3796, 4734, 2786, 2448, 3613, 5032, 3192, 6516, 3536, 5099, 5057, 1584, 1889, 3937, 3469, 3160, 4755, 2896, 6771, 5442, 5795, 5244, 3843, 5068, 3580, 3016, 2283, 3660, 4448, 2639, 4739, 5653, 3599, 4668, 5010, 4473, 5090, 4978],
	"splits": [False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, True, False, False, False, False, False, False, False, False, False, False, False, False, False]}

#controls (normal quorum)
control2_2x = {
	"type": ["control fixed quorum"]*100,
	"dist": ["2x"]*100,
	"accuracy":[1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 0.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0],
	"time":[987, 2165, 1962, 1347, 1335, 2260, 1862, 546, 1205, 1297, 2308, 1126, 1656, 729, 1176, 1560, 723, 1343, 1403, 678, 1936, 2863, 1034, 1342, 1144, 1378, 452, 342, 2827, 1514, 734, 2773, 1381, 1584, 1569, 1197, 2295, 1559, 1439, 1003, 489, 1052, 2118, 1021, 920, 1203, 1857, 455, 2355, 1936, 1720, 2649, 1440, 1509, 1561, 924, 1124, 935, 1453, 1719, 623, 1020, 841, 1231, 894, 1886, 1309, 2086, 1239, 2117, 1710, 1709, 2354, 1035, 1104, 1175, 4053, 651, 600, 1191, 1159, 492, 879, 895, 652, 1074, 1485, 273, 1522, 741, 1530, 1174, 1643, 1990, 875, 2842, 1819, 1474, 1681, 294],
	"splits":[False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False]
}

control2_3x = {
	"type": ["control fixed quorum"]*100,
	"dist": ["3x"]*100,
	"accuracy":[1.0]*100,
	"time": [2347, 3819, 1082, 2292, 1935, 2398, 3720, 892, 3351, 1875, 2633, 2248, 1357, 1377, 1816, 2266, 2834, 1951, 1006, 3542, 3130, 1176, 1740, 3937, 1261, 1768, 2091, 2875, 1649, 1598, 2609, 2110, 2321, 1978, 2625, 1467, 1102, 2669, 2558, 2999, 972, 2474, 2309, 3178, 1232, 930, 2835, 2160, 1713, 1060, 2873, 1643, 1666, 3336, 2887, 2512, 2024, 3847, 2226, 3476, 1299, 2050, 1317, 4463, 2826, 2161, 1594, 3134, 1998, 3399, 3724, 1427, 2955, 2687, 2173, 2297, 2674, 2355, 1470, 2142, 1921, 2341, 2860, 3591, 1846, 2323, 2662, 3870, 3156, 2007, 5242, 2813, 2341, 4712, 3204, 2563, 2149, 2159, 1903, 1822],
	"splits": [False]*100
}

control2_9x = {
	"type": ["control fixed quorum"]*100,
	"dist": ["9x"]*100,
	"accuracy":[1.0]*100,
	"time": [2777, 3063, 4500, 1592, 1948, 4008, 1506, 4357, 1784, 3417, 2203, 2556, 2468, 3092, 2445, 2555, 1027, 1365, 1722, 2008, 2439, 3022, 2194, 4084, 643, 2761, 2171, 3453, 2406, 2969, 1900, 3896, 2869, 2012, 4219, 3546, 2525, 3600, 3200, 2192, 6280, 2927, 1800, 2118, 2506, 2582, 1744, 3279, 3282, 1942, 2260, 3019, 2304, 3818, 3654, 1481, 2603, 1450, 2347, 2322, 2402, 3282, 2836, 3230, 2664, 3110, 688, 2029, 3549, 4440, 3226, 2238, 715, 948, 2031, 3428, 2359, 3897, 1710, 1476, 1907, 2642, 2690, 2633, 4394, 2657, 3167, 1419, 1891, 3742, 3244, 3011, 3041, 2502, 3512, 2663, 3588, 1295, 4015, 1462],
	"splits": [False]*100
}

# controls
control_2x = {
	"type" : ["control scaled quorum"]*100,
	"dist": ["2x"]*100,
	"accuracy": [1.0]*100,
	"time":[3085, 2451, 3432, 3291, 4077, 2626, 3019, 2561, 3839, 2389, 2786, 2062, 1137, 2734, 2687, 2686, 4290, 1931, 2568, 4144, 3036, 2070, 2366, 3596, 2393, 868, 2325, 2960, 2476, 994, 1374, 3320, 2326, 1824, 2292, 4007, 3179, 2224, 2473, 2073, 2563, 1219, 1732, 2221, 2308, 2036, 2905, 3348, 3038, 2471, 3345, 1395, 1964, 2184, 2000, 2411, 2729, 2910, 3518, 1982, 2932, 3138, 2176, 1012, 3771, 1498, 2407, 1850, 2860, 2535, 3530, 2995, 1834, 3894, 2649, 2977, 2160, 2590, 3931, 1988, 2488, 2413, 2336, 2960, 2375, 2061, 3753, 2633, 1440, 3197, 2427, 2687, 3339, 3089, 1308, 3957, 3744, 2046, 2942, 2029],
	"splits": [False]*100
}

control_3x = {
	"type" : ["control scaled quorum"]*100,
	"dist": ["3x"]*100,
	"accuracy": [1.0]*100,
	"time": [3755, 3585, 5806, 5185, 2216, 4603, 3465, 3752, 4004, 4591, 3752, 4180, 4561, 3334, 4229, 4488, 3015, 3935, 3936, 3923, 5556, 5584, 3560, 6902, 3533, 6065, 4808, 4031, 3050, 3459, 3729, 4010, 2726, 2160, 4220, 4715, 3408, 4534, 3030, 3677, 3565, 6549, 3312, 3830, 6478, 3087, 1756, 4683, 4577, 4710, 2961, 3466, 3191, 2400, 2614, 4715, 3979, 3805, 5193, 3079, 4969, 2284, 2444, 4478, 6117, 4897, 4954, 2881, 3846, 4665, 3239, 5294, 3648, 5341, 2915, 3932, 6366, 5330, 4118, 2552, 5492, 4105, 3338, 1731, 3867, 5213, 3032, 4342, 5799, 3259, 3889, 5517, 2823, 4395, 6176, 3781, 2958, 3227, 5036, 4547],
	"splits": [False]*100
	
}

control_9x = {
	"type" : ["control scaled quorum"]*100,
	"dist": ["9x"]*100, 
	"accuracy": [1.0]*100,
	"time": [3923, 9647, 8116, 3794, 4997, 5800, 7992, 6528, 9906, 6254, 9234, 5861, 10472, 5438, 4640, 6725, 7963, 4852, 9678, 7763, 6163, 8243, 5777, 5390, 12198, 9573, 7410, 8339, 6148, 10097, 7124, 5639, 8329, 6595, 5374, 3928, 10740, 7806, 5262, 4509, 2966, 5434, 8364, 6636, 5437, 9709, 8820, 7463, 6501, 6047, 7518, 8315, 8814, 10617, 8041, 13275, 11219, 8570, 6361, 2067, 7797, 6110, 10026, 10745, 4365, 7866, 7550, 4475, 5421, 8530, 3315, 7480, 5316, 13099, 8877, 7458, 7730, 8255, 7874, 5533, 4259, 10781, 8101, 5974, 5807, 7681, 10999, 4661, 7439, 11804, 8643, 10724, 9693, 7543, 12097, 6671, 9550, 8422, 5770, 5566],
	"splits": [False]*100
	
}



# create dfs
df =  pd.concat([
	pd.DataFrame(data=normal_2x), 
	pd.DataFrame(data=good_2x),
	pd.DataFrame(data=normal_3x),
	pd.DataFrame(data=good_3x),
	pd.DataFrame(data=normal_9x),
	pd.DataFrame(data=good_9x),
	pd.DataFrame(data=control2_2x),
	pd.DataFrame(data=control2_3x),
	pd.DataFrame(data=control2_9x),
	pd.DataFrame(data=control_2x),
	pd.DataFrame(data=control_3x),
	pd.DataFrame(data=control_9x)
	],
	ignore_index=True)
df['time'] = df['time'] / 60.0

print(df.tail())

# create time plot
fig, ax = plt.subplots()

sns.boxplot(x = df['dist'],
            y = df['time'],
            hue = df['type'],
            palette = sns.cubehelix_palette(4),
            ax=ax)

ax.set_title("Decision Time for Fixed and Scaled Quorum")
ax.set_xlabel("distance")
ax.set_ylabel("time (min)")

plt.savefig("far_nest_vs_near_nest_time.png")

# add actual ants

ants_2x = {
	"type": "ants",
	"dist": ["2x"]*18,
	"accuracy": [1]*18,
	"time": [-1]*18,
	"splits": [False]*18
}

ants_3x = {
	"type": "ants",
	"dist": ["3x"]*18,
	"accuracy": [1]*18,
	"time": [-1]*18,
	"splits": [False]*18
}

ants_9x = {
	"type": "ants",
	"dist": ["9x"]*18,
	"accuracy": [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,0],
	"time": [-1]*18,
	"splits": [False]*18
}

df = pd.concat([
	df,
	pd.DataFrame(data=ants_2x),
	pd.DataFrame(data=ants_3x),
	pd.DataFrame(data=ants_9x)],
	ignore_index=True)

# create plot
fig, ax = plt.subplots()

sns.lineplot(x = df['dist'],
            y = df['accuracy'],
            hue = df['type'],
            palette = sns.cubehelix_palette(5),
            #err_style = "bars",
            ax=ax)

ax.set_title("Decision Accuracy for Fixed and Scaled Quorum")
ax.set_xlabel("distance")

plt.savefig("far_nest_vs_near_nest_accuracy.png")





