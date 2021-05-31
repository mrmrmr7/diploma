import plotly.graph_objects as go 

with open("output/res_2021-04-12_17:52:23", 'r') as f:
    data_x = []
    data_y = []
    for l in f.readlines():
        sp = l.split(":")
        data_x.append(sp[0])
        data_y.append(sp[1])


fig = go.Figure(data=go.Scatter(
    x=data_x,
    y=data_y
))

fig.update_layout(
    title="Dependence Rho on t",
    xaxis_title="rho, circle area percent",
    yaxis_title="t, circles locating time",
)

fig.show()