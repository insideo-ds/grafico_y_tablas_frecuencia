import plotly.express as px
import pandas as pd

# A small demo that only runs when this module is executed directly. Using
# a guarded demo prevents the sample data and interactive plot from running
# when the module is imported by other scripts.
def _demo_plotly_bar_polar():
    demo_df = pd.DataFrame({
        "direction": ["N", "NNE", "NE", "ENE"],
        "strength": ["0-1", "0-1", "0-1", "0-1"],
        "frequency": [0.5, 0.6, 0.5, 0.4],
    })
    print(demo_df.head())
    fig = px.bar_polar(
        demo_df,
        r="frequency",
        theta="direction",
        color="strength",
        template="plotly_dark",
        color_discrete_sequence=px.colors.sequential.Plasma_r,
    )
    fig.show()

if __name__ == "__main__":
    _demo_plotly_bar_polar()