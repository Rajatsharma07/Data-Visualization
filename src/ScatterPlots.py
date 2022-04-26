from bokeh.models import ColumnDataSource, CategoricalColorMapper, HoverTool
from bokeh.plotting import show, output_file
import pandas as pd
from Visualization import Visualization

# output_file("Scatter Plot.html", title="Scatter Plot")


class ScatterPlots(Visualization):
    def __init__(
        self,
        x_label: str = "X-Child",
        y_label: str = "Y-Child",
        plot_title: str = "Child Plot",
        plt_width: int = 900,
        plt_height: int = 600,
        transparency: float = 0.5,
        bubble_size: int = 8,
    ) -> None:
        """[Constructor to initialize the instances of the class, which will be passed to parent class for the 
        'figure' object creation]
        
        Keyword Arguments:
            x_label {str} -- [Value of x-axis label] (default: {"X-Child"})
            y_label {str} -- [Value of y-axis label] (default: {"Y-Child"})
            plot_title {str} -- [title of the plot] (default: {"Child Plot"})
            plt_width {int} -- [width of the plot] (default: {900})
            plt_height {int} -- [height of the plot] (default: {600})
            transparency {float} -- [Alpha value of the bubbles] (default: {1})
            bubble_size {int} -- [width of the lines] (default: {1})
        
        Returns:
            [None]

        """
        self.transparency = transparency
        self.bubble_size = bubble_size
        # Caling the parent constructor and passing the required parameters
        super().__init__(
            x_label=x_label,
            y_label=y_label,
            plt_width=plt_width,
            plt_height=plt_height,
            plot_title=plot_title,
        )

    def generate_scatter_plot(
        self,
        df: pd.DataFrame,
        x_column: str,
        y_column: str,
        category_clmn: str,
        legend_title: str,
        xlabel_orientation: float = 1.1,
        xaxis_padding: float = 0.2,
    ) -> None:
        """[Generate Scatter plot]
        
        Arguments:
            df {pd.DataFrame} -- [Dataframe with x-value column, y-values column, category column]    category of the curve]
            x_column {str} -- [Name of the x-value column]
            y_column {str} -- [Name of the y-value column]
            category_clmn {str} -- [Name of the category column]
            legend_title {str} -- [Legends of the plot]
        
        Keyword Arguments:
            xlabel_orientation {float} -- [Rotating x-labels to fit the plot] (default: {1.1})
            xaxis_padding {float} -- [Padding for x-axis] (default: {0.2})
        
        Returns:
            [None]
            
        """
        try:
            lst_categories = df[category_clmn].unique()
            color_mapper = CategoricalColorMapper(
                factors=lst_categories, palette=self.colors[: len(lst_categories)]
            )
            for category in df[category_clmn].unique():
                dfnew = df.loc[(df[category_clmn] == category)]
                source = ColumnDataSource(
                    dict(
                        x=dfnew[x_column],
                        y=dfnew[y_column],
                        category_clmn=dfnew[category_clmn],
                    )
                )
                self.figure.scatter(
                    x="x",
                    y="y",
                    source=source,
                    fill_alpha=self.transparency,
                    size=self.bubble_size,
                    fill_color={"field": "category_clmn", "transform": color_mapper},
                    legend_group="category_clmn",
                )
            self.styling_figure(
                xlabel_orientation=xlabel_orientation, xaxis_padding=xaxis_padding
            )
            self.legend_settings(
                legend_title=legend_title,
                legend_clickable=True,
                legend_location="top_left",
                legend_orientation="vertical",
            )
            self.figure.add_tools(
                HoverTool(tooltips=[("X Value", "$x{0f}"), ("Y Value", "$y{0f}")])
            )
            show(self.figure)
        except Exception as e:
            if hasattr(e, "message"):
                print(e.message)
            else:
                print(e)
