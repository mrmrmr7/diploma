import plotly.graph_objects as go

x_arr = []
y_arr = []

with open("output/dimension2_circle_uniform_dist_from_10_to_105_2021-05-07_00:52:03.txt", 'r') as f:
    lines = f.readlines()
    
    for line in lines[1:]:
        x_arr.append(int(line.split(':')[0]))
        y_arr.append(int(line.split(':')[1])/30)

fig = go.Figure(go.Scatter(
    x = x_arr,
    y = y_arr
))

fig.update_layout(
    # title=f'Autocorrelation_test, quantile: {round(alpha, 3)}',
    # width=1000,
    # height=1000,
    yaxis={"range":[0, 1.1]})

fig.show()