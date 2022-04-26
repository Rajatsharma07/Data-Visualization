from bokeh.models import ColumnDataSource, HoverTool, FactorRange
from bokeh.plotting import show
import pandas as pd
import numpy as np
from Visualization import Visualization
from typing import List
from bokeh.plotting import figure

# output_file("Statistics Plots.html", title="Statistics Plots")


class StatisticsPlots(Visualization):
    def __init__(
        self,
        x_range: any = None,
        x_label: str = "X-Child",
        y_label: str = "Y-Child",
        plot_title: str = "Child Plot",
        plt_width: int = 900,
        plt_height: int = 500,
    ) -> None:
        """[Constructor to initialize the instances of the class, which will be used for
         'figure' object creation]

        Keyword Arguments:
            x_range {any} -- [By default it's None and only set when creating figure object for
            Bar-chart, Satcked Bar chart and Box plot; if applicable, it is referenced by
            'FactorRange' object and instantiated later in the method]
            x_label {str} -- [Value of x-axis label] (default: {"X-Child"})
            y_label {str} -- [Value of y-axis label] (default: {"Y-Child"})
            plot_title {str} -- [title of the plot] (default: {"Child Plot"})
            plt_width {int} -- [width of the plot] (default: {900})
            plt_height {int} -- [height of the plot] (default: {500})

        Returns:
            [None]
        """
        self.__create_fig(
            x_range=x_range,
            x_label=x_label,
            y_label=y_label,
            plot_title=plot_title,
            plt_height=plt_height,
            plt_width=plt_width,
        )

    def __create_fig(
        self,
        x_label: str,
        y_label: str,
        plot_title: str,
        plt_width: int,
        plt_height: int,
        x_range: any,
    ) -> None:
        """[Private method creating 'figure' object for the instances]

        Arguments:
            x_label {str} -- [Value of x-axis label]
            y_label {str} -- [Value of y-axis label]
            plot_title {str} -- [title of the plot]
            plt_width {int} -- [width of the plot]
            plt_height {int} -- [height of the plot]
            x_range {any} -- [x-axis range variable]
        """
        self.figure = figure(
            title=plot_title,
            x_axis_label=x_label,
            y_axis_label=y_label,
            plot_width=plt_width,
            plot_height=plt_height,
            x_range=x_range,
        )

    def generate_histogram_plot(
        self,
        data: pd.DataFrame,
        column_names: List[str],
        number_of_bins: int = 10,
        size_of_bin: int = 10,
        use_bin_size: bool = False,
        transparency: float = 0.6,
        legend_title: str = "Legends",
        xaxis_padding: float = 0.1,
    ) -> None:
        """[Generate the histogram plot]

        Arguments:
            data {pd.DataFrame} -- [pandas Dataframe]
            column_names {List[str]} -- [columns of the passed dataframe]

        Keyword Arguments:
            number_of_bins {int} -- [Number of bins to be used] (default: {10})
            size_of_bin {int} -- [description] (default: {10})
            use_bin_size {bool} -- [If 'True', 'bin size' will be used and 'number
             of bins' parameter will be neglected while plotting] (default: {False})
            transparency {float} -- [Alpha value of the whiskers] (default: {0.6})
            legend_title {str} -- [Legends of the plot] (default: {"Legends"})
            xaxis_padding {float} -- [Padding for x-axis] (default: {0.1})

        Returns:
            [None] -- [Shows the figure]
        """
        try:
            data = [data[col] for col in column_names]
            if use_bin_size:
                min_value = min(map(min, zip(*data)))
                max_value = max(map(max, zip(*data)))
                ranges = np.arange(min_value, max_value + 1, size_of_bin)

            p = self.figure
            count = 0
            for color, dt, name in zip(self.colors, data, column_names):
                if use_bin_size:
                    frequencies, edges = np.histogram(dt, ranges, density=False)
                    print(count)
                    p.quad(
                        top=frequencies,
                        bottom=0,
                        left=edges[:-1],
                        right=edges[1:],
                        fill_color=color,
                        line_color="black",
                        alpha=transparency,
                        legend_label=name,
                    )
                    count += 1
                elif not use_bin_size:
                    frequencies, edges = np.histogram(dt, number_of_bins, density=False)
                    p.quad(
                        top=frequencies,
                        bottom=0,
                        left=edges[:-1],
                        right=edges[1:],
                        fill_color=color,
                        line_color="black",
                        alpha=transparency,
                        legend_label=name,
                    )
            p.y_range.start = 0
            self.legend_settings(legend_title=legend_title, legend_clickable=True)
            self.styling_figure(xaxis_padding=xaxis_padding)
            hover_tool = HoverTool(
                tooltips=[
                    ("Frequency", "@top{0f}"),
                    ("X Value", "$x{0f}"),
                    ("Y Value", "$y{0f}"),
                ]
            )
            p.add_tools(hover_tool)
            p.legend.title = legend_title
            show(p)
            return None
        except Exception as e:
            if hasattr(e, "message"):
                print(e.message)
            else:
                print(e)

    def generate_bar_chart(
        self,
        category: List[str],
        frequency: List[int],
        width_bar: float = 0.6,
        xaxis_padding: float = 0.2,
        transparency: float = 0.6,
        xlabel_orientation: float = 1.1,
    ) -> None:
        """[Generate Bar graph]

        Arguments:
            category {List[str]} -- [List of unique categories]
            frequency {List[int]} -- [Frequency of associated categories]

        Keyword Arguments:
            width_bar {float} -- [Width of the bar] (default: {0.6})
            xaxis_padding {float} -- [Padding for x-axis] (default: {0.2})
            transparency {float} -- [Alpha value for the bar] (default: {0.6})
            xlabel_orientation {float} -- [Rotation of x-axis labels] (default: {1.1})

        Returns:
            [None] -- [Shows the figure]
        """
        try:
            p = self.figure
            source = ColumnDataSource(
                dict(x=category, values=frequency, color=self.colors[: len(category)])
            )
            # hover info
            hover_tool = HoverTool(tooltips=[("Frequency", "@values")])
            p.add_tools(hover_tool)
            p.vbar(
                x="x",
                top="values",
                width=width_bar,
                source=source,
                line_color="#020B13",
                fill_color=self.colors[0],
                fill_alpha=transparency,
            )
            self.styling_figure(
                xlabel_orientation=xlabel_orientation, xaxis_padding=xaxis_padding
            )
            self.legend_settings(has_legend=False)
            p.x_range.factors = category
            p.y_range.start = 0
            show(p)
            return None
        except Exception as e:
            if hasattr(e, "message"):
                print(e.message)
            else:
                print(e)

    def generate_stacked_bar_chart(
        self,
        data: dict,
        legend_title: str,
        width_bar: int = 0.5,
        xlabel_orientation: float = 1.1,
        xaxis_padding: float = 0.3,
        transparency: float = 0.6,
    ) -> None:
        """[Generating Stacked Bar chart]

        Arguments:
            data {dict} -- [First 'Key-Value' pair represents first Category with 'Key' as
            'Category' name 'Values' as unique values of that category, next rows represents
            second Category, with 'Keys' as unique category and 'Values' as 'Frequency' of
            those categories. For e.g.:
            {
            'Category 1': ['Value1', 'Value2'],
            'Category2_1': [165, 0],
            'Category2_2': [3, 100],
            'Category2_3': [7, 50],
            'Category2_4': [99, 29]
            }]

            legend_title {str} -- [Title of the leegnds of the plot]

        Keyword Arguments:
            width_bar {int} -- [Width of the bars] (default: {0.5})
            xlabel_orientation {float} -- [Rotating the x-axis labels] (default: {1.1})
            xaxis_padding {float} -- [Padding for x-axis] (default: {0.3})
            transparency {float} -- [Alpha value for the bars] (default: {0.6})

        Returns:
            [None] -- [Shows the figure]
        """
        try:
            category1 = next(iter(data))
            category2 = list(data.keys())[1:]
            p = self.figure
            # hover info
            hover_tool = HoverTool(
                tooltips=[(legend_title, "$name"), ("Frequency", "@$name")]
            )
            colors = self.colors[: len(category2)]

            p.vbar_stack(
                category2,
                x=category1,
                source=data,
                width=width_bar,
                legend_label=category2,
                color=colors,
                line_color="#020B13",
                fill_alpha=transparency,
            )
            self.styling_figure(
                xlabel_orientation=xlabel_orientation, xaxis_padding=xaxis_padding
            )
            self.legend_settings(
                legend_title=legend_title,
                legend_clickable=False,
                legend_location="top_left",
                legend_orientation="vertical",
                legend_fontsize="8pt",
            )
            p.y_range.start = 0
            p.x_range.factors = data[category1]
            p.add_tools(hover_tool)
            show(p)
            return None
        except Exception as e:
            if hasattr(e, "message"):
                print(e.message)
            else:
                print(e)

    def generate_box_plot(
        self,
        df: pd.DataFrame,
        value_column: str,
        category_column: str,
        outlier_transparency: float = 0.7,
        xlabel_orientation: float = 0.4,
        outlier_color: str = "red",
        outlier_size: int = 6,
    ) -> None:
        """[summary]

        Arguments:
            df {pd.DataFrame} -- [Datafram consists of Value and category clms]
            value_column {str} -- [Name of the value column]
            category_column {str} -- [Name of the category column]

        Keyword Arguments:
            outlier_transparency {float} -- [alpha value for the outlier] (default: {0.7})
            xlabel_orientation {float} -- [Roatation of x-axis labels] (default: {0.4})
            outlier_color {str} -- [Set the color of outlier #Hex code/red/yellow] (default: {"red"})
            outlier_size {int} -- [Size of the outlier] (default: {6})

        Returns:
            [None] -- [Shows the plot]
        """
        try:
            p = self.figure
            dt = pd.DataFrame(dict(freq=df[value_column], group=df[category_column]))
            groups = dt.groupby("group")
            lst_categories = df[category_column].unique()
            # Calculating Quartiles
            q1 = groups.quantile(q=0.25)
            q2 = groups.quantile(q=0.5)
            q3 = groups.quantile(q=0.75)
            # Interquartile range
            iqr = q3 - q1
            upper = q3 + 1.5 * iqr
            lower = q1 - 1.5 * iqr

            def outliers(group):
                cat = group.name
                out = group[
                    (group.freq > upper.loc[cat]["freq"])
                    | (group.freq < lower.loc[cat]["freq"])
                ]
                return out["freq"]

            out = groups.apply(outliers).dropna()
            # prepare outlier data for plotting, we need coordinates for every outlier.
            if not out.empty:
                outx = []
                outy = []
                for keys in out.index:
                    outx.append(keys[0])
                    outy.append(out.loc[keys[0]].loc[keys[1]])

            # if no outliers, shrink lengths of stems to be no longer than the minimums or maximums
            qmin = groups.quantile(q=0.00)
            qmax = groups.quantile(q=1.00)
            upper.freq = [
                min([x, y]) for (x, y) in zip(list(qmax.loc[:, "freq"]), upper.freq)
            ]
            lower.freq = [
                max([x, y]) for (x, y) in zip(list(qmin.loc[:, "freq"]), lower.freq)
            ]

            # Upper stem
            p.segment(
                lst_categories, upper.freq, lst_categories, q3.freq, line_color="black"
            )
            # Lower stem
            p.segment(
                lst_categories, lower.freq, lst_categories, q1.freq, line_color="black"
            )

            p.vbar(
                lst_categories,
                0.7,
                q1.freq,
                q3.freq,
                fill_color=self.colors[0],
                line_color="black",
                fill_alpha=0.6,
            )

            p.rect(
                x=lst_categories, y=q2.freq, width=0.7, height=0.07, line_color="black"
            )

            # Whiskers (almost-0 height rectangles simpler than segments)
            p.rect(lst_categories, lower.freq, 0.2, 0.01, line_color="black")
            p.rect(lst_categories, upper.freq, 0.2, 0.01, line_color="black")

            # outliers
            if not out.empty:
                p.circle(
                    outx,
                    outy,
                    size=outlier_size,
                    color=outlier_color,
                    fill_alpha=outlier_transparency,
                )
            self.styling_figure(
                xlabel_orientation=xlabel_orientation, yaxis_notation=False
            )
            p.grid.grid_line_width = 2
            hover_tool = HoverTool(
                tooltips=[
                    ("Y Value", "$y{1f}"),
                    ("Quartile 3", "@bottom{1f}"),
                    ("Quartile 1", "@top{1f}"),
                ]
            )
            p.x_range.factors = lst_categories
            p.add_tools(hover_tool)
            show(p)
        except Exception as e:
            if hasattr(e, "message"):
                print(e.message)
            else:
                print(e)
