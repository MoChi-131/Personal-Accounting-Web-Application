import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Agg')  # For use in non-interactive backends
import os

from MongoDB import fetch_category_data

def draw_pie_chart(date, categories):
    data, categories = fetch_category_data(date, categories)

    # Filter out categories with zero values
    filtered_data_labels = [(d, c) for d, c in zip(data, categories) if d > 0]
    filtered_data = [d for d, _ in filtered_data_labels]
    filtered_categories = [c for _, c in filtered_data_labels]
    filtered_labels = [f'{round((d / sum(filtered_data)) * 100, 1)}% {c}' for d, c in filtered_data_labels]

    fig, ax = plt.subplots()

    color_palette = [
        [1.0, 0.4, 0.4],  # Reddish
        [0.2, 0.6, 0.3],  # Greenish
        [0.8, 0.5, 0.2],  # Orangish
        [0.68, 0.85, 0.90],  # Light blue
        [0.7, 0.7, 0.7],  # Gray
        [0.5, 0.5, 1.0],  # Blue
        [1.0, 0.8, 0.2],  # Yellowish
        [0.6, 0.4, 0.8],  # Purple
        [0.9, 0.3, 0.6]   # Pinkish
    ]

    # Create a dictionary mapping categories to colors
    category_colors = dict(zip(categories, color_palette))

    # Use the filtered categories to get the corresponding colors
    pie_colors = [category_colors.get(c, [0.5, 0.5, 0.5]) for c in filtered_categories]

    wedges, texts = ax.pie(
        filtered_data,
        labels=filtered_labels,
        colors=pie_colors,
        startangle=90,
        counterclock=False
    )

    plt.title('Spending Category', fontsize=14, fontweight='bold', pad=20)

    total = sum(data)
    plt.text(0, 0, f'TOTAL:\n£{total:.2f}',
             horizontalalignment='center',
             verticalalignment='center',
             fontsize=12,
             fontweight='bold')

    ax.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.

    # Check if the directory exists, and if not, create it
    current_dir = os.path.dirname(os.path.abspath(__file__))
    output_path = os.getenv("OUTPUT_PATH") or os.path.join(current_dir, '..', 'static', 'pie_chart.png')
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    plt.savefig(output_path, bbox_inches='tight', dpi=300)
    print("Saved")

if __name__ == "__main__":
    draw_pie_chart("2017")
