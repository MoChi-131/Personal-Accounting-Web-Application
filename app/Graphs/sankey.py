import plotly.graph_objects as go
import os

def sankey(data):
    node_colors = [
        '#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd', '#8c564b',
        '#e377c2', '#7f7f7f', '#bcbd22', '#17becf', '#aec7e8', '#ffbb78', '#6baed6'
    ]
    targets = [2, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
    sources = [0, 1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2]

    link_colors = [
        f"rgba({int(node_colors[src][1:3], 16)}, {int(node_colors[src][3:5], 16)}, {int(node_colors[src][5:7], 16)}, 0.6)"
        if src in [0, 1] else
        f"rgba({int(node_colors[tgt][1:3], 16)}, {int(node_colors[tgt][3:5], 16)}, {int(node_colors[tgt][5:7], 16)}, 0.6)"
        for src, tgt in zip(sources, targets)
    ]

    fig = go.Figure(data=[go.Sankey(
        node=dict(
            pad=15,
            thickness=20,
            line=dict(color="black", width=0.5),
            label=['Wages', 'Others', 'Budget', 'Toll', 'Food', 'Parking', 'Transport', 'Accommodation', 'Shopping', 'Telecom', 'Miscellaneous', 'Other', 'Savings'],
            color=node_colors
        ),
        link=dict(
            source=sources,
            target=targets,
            value=data,
            color=link_colors
        )
    )])

    fig.update_layout(
        width=700,
        height=500,
        margin=dict(l=0, r=0, b=0, t=10),
        font=dict(size=15.5, color='black')
    )

    current_dir = os.path.dirname(os.path.abspath(__file__))
    output_path = os.getenv("OUTPUT_PATH") or os.path.join(current_dir, '..', 'static', 'Sankey.html')

    fig.write_html(output_path)
    print("saved")

if __name__ == "__main__":
    value = [1500, 250, 200, 300, 100, 150, 200, 100, 50, 300, 250, 100]
    sankey(value)