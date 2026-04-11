import matplotlib.pyplot as plt
import numpy as np
import os
import logging
from MongoDB import retrieve_expense_monthly_data, retrieve_expense_data_weekly

# Setup logging
logging.basicConfig(level=logging.INFO)

# Helper function to plot bars with text labels
def plot_bar_with_labels(ax, ind, amounts, bottom, color, label, width):
    ax.bar(ind, amounts, width, bottom=bottom, color=color, label=label)
    for i, amount in enumerate(amounts):
        if amount > 0:
            ax.text(
                i,
                bottom[i] + amount / 2,
                f'£{amount:.2f}',
                ha='center',
                va='center',
                fontsize=8,
                color='white' if amount > 50 else 'black'
            )

def create_expense_plot(current_date=None, mode=None, categories_set=[], sort=None):
    # Retrieve data from MongoDB
    if mode is None or mode == "Monthly":
        data = retrieve_expense_monthly_data(current_date, categories_set)
        x_label = data['months']
    elif mode == "Weekly":
        data = retrieve_expense_data_weekly(current_date, categories_set)
        x_label = data['week_labels']
    else:
        raise ValueError("Invalid mode. Must be 'Monthly' or 'Weekly'.")

    # Extract and process data
    if sort == "All Category":
        categories = data['categories']
        category_data = data['category_data']
        stack_totals = data['stack_totals']
    else:
        category = sort
        categories = [category]
        category_data = data['category_data'][category]
        stack_totals = category_data
        
    start_date = data['start_date']
    end_date = data['end_date']

    # Define color palette
    color_palette = [
        [1.0, 0.4, 0.4],
        [0.2, 0.6, 0.3],
        [0.8, 0.5, 0.2],
        [0.68, 0.85, 0.90],
        [0.7, 0.7, 0.7],
        [0.5, 0.5, 1.0],
        [1.0, 0.8, 0.2],
        [0.6, 0.4, 0.8],
        [0.9, 0.3, 0.6]
    ]
    category_colors = dict(zip(categories_set, color_palette))

    # Set up plot
    ind = np.arange(len(x_label))
    width = 0.6
    fig, ax = plt.subplots(figsize=(10, 6))
    bottom = np.zeros(len(x_label))

    # Plot
    if sort == "All Category":
        for category in categories:
            amounts = category_data[category]
            plot_bar_with_labels(ax, ind, amounts, bottom, category_colors[category], category.capitalize(), width)
            bottom += np.array(amounts)
    else:
        amounts = category_data
        category = sort.lower()
        plot_bar_with_labels(ax, ind, amounts, bottom, category_colors[category], category.capitalize(), width)

    # Add total stack labels
    for i, total in enumerate(stack_totals):
        ax.text(
            i,
            total + 1,
            f'£{total:.2f}',
            ha='center',
            va='bottom',
            fontsize=10
        )

    # Labels and layout
    ax.set_ylabel('Amount (£)')
    ax.set_title(f'Expenses by {"Month" if mode == "Monthly" else "Week"} ({start_date.strftime("%d %b %Y")} - {end_date.strftime("%d %b %Y")})')
    ax.set_xticks(ind)
    ax.set_xticklabels(x_label)
    ax.legend(bbox_to_anchor=(1.05, 1), loc='upper left', borderaxespad=0.)
    ax.grid(axis='y')
    ax.set_ylim(0, max(stack_totals) * 1.2)

    # Save figure
    plt.subplots_adjust(left=0.05, right=0.75, top=0.9, bottom=0.1)
    current_dir = os.path.dirname(os.path.abspath(__file__))
    save_path = os.getenv("OUTPUT_PATH") or os.path.join(current_dir, '..', 'static', 'Trend_1.png')
    plt.savefig(save_path, dpi=300)
    plt.close()

if __name__ == "__main__":
    create_expense_plot(mode="Weekly")