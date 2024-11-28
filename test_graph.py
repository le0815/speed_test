# import plotly.graph_objects as go
#
# fig = go.Figure(go.Indicator(
#     mode= 'gauge+number',
#     value=124,
#     # title={'text': 'Speed'}
# ))
#
# fig.show()

import matplotlib
# import matplotlib.pyplot as plt
#
# colors = ['red', 'blue', 'green']
# value = [100, 60, 50, 30]
# x_axis = [0, 0.44, 0.88, 1.32, 1.76, 2.2, 2.64]
# fig = plt.figure(figsize=(18, 18))
# ax = fig.add_subplot(projection='polar')
# ax.bar(x=x_axis, width=0.5, height=0.5, bottom=2)
# fig.show()


import numpy as np
from matplotlib import pyplot as plt
plt.rcParams["figure.figsize"] = [7.50, 3.50]
plt.rcParams["figure.autolayout"] = True
x = np.linspace(-1, 1, 1000)
y = np.exp(x)
c = np.tan(x)
plt.scatter(x, y, c=c, marker='_')
plt.show()