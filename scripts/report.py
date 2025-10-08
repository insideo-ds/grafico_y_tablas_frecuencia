import matplotlib.pyplot as plt


def report_olas(rows = 2, cols = 3, figsize = (10, 6)):

    fig, axes = plt.subplots(rows, cols, figsize=figsize)
    axes = axes.flatten()

    for i in range(5):  # only fill 5 subplots
        axes[i].plot([0, 1], [i, i + 1])
        axes[i].set_title(f"Plot {i+1}")

    # Hide the unused subplot
    axes[5].axis('off')

    plt.tight_layout()
    plt.show()

