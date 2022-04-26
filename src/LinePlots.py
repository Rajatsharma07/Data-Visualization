from bokeh.models import (
    ColumnDataSource,
    HoverTool,
    CategoricalColorMapper,
)
from bokeh.models.formatters import DatetimeTickFormatter
from bokeh.plotting import show
import pandas as pd
import numpy as np
from Visualization import Visualization

# output_file("Line Plots.html", title="Line Plots")


class LinePlots(Visualization):
    def __init__(
        self,
        x_label: str = "X-Child",
        y_label: str = "Y-Child",
        plot_title: str = "Child Plot",
        plt_width: int = 900,
        plt_height: int = 600,
        transparency: float = 1,
        line_width: float = 1,
    ) -> None:
        """[Constructor to initialize the instances of the class, which will be passed to parent
        class for the 'figure' object creation]

        Keyword Arguments:
            x_label {str} -- [Value of x-axis label] (default: {"X-Child"})
            y_label {str} -- [Value of y-axis label] (default: {"Y-Child"})
            plot_title {str} -- [title of the plot] (default: {"Child Plot"})
            plt_width {int} -- [width of the plot] (default: {900})
            plt_height {int} -- [height of the plot] (default: {600})
            transparency {float} -- [Alpha value of the lines] (default: {1})
            line_width {float} -- [width of the lines] (default: {1})

        """
        self.transparency = transparency
        self.line_width = line_width
        # Caling the parent constructor and passing the required parameters
        super().__init__(
            x_label=x_label,
            y_label=y_label,
            plt_width=plt_width,
            plt_height=plt_height,
            plot_title=plot_title,
        )

    def generate_multiline_plot_by_columns(
        self, data: dict, df: pd.DataFrame, legend_title: str, xaxis_padding: float = 0
    ) -> None:
        """[Generate multiline plot by passing the dataframe 'columns' as 'values' and 'category'
        as 'keys' in the input dictionary - 'data']

        Arguments:
            data {dict} -- [Accepts keys as unique categories and values as columns in the
            dataframe. For e.g.:
            {
                "Category1": ["col1", "col2", "col3"],
                "Category2": ["col4", "col5", "col6"]
            }
            ]
            df {pd.DataFrame} -- [Dataframe with columns as different curves]
            legend_title {str} -- [Legends of the plot]

        Keyword Arguments:
            xaxis_padding {float} -- [Padding for x-axis] (default: {0})

        Returns:
            [None]
        """
        try:
            categories = list(data.keys())
            p = self.figure
            color_mapper = CategoricalColorMapper(
                factors=categories, palette=self.colors[: len(categories)]
            )

            for category in categories:
                count = len(data.get(category))
                source = ColumnDataSource(
                    dict(
                        y=[df[col].tolist() for col in list(data.get(category))],
                        x=[list(np.arange(0, df.shape[0]))] * count,
                        category=[category] * count,
                        hoverInformation=[category] * count,
                    )
                )
                p.multi_line(
                    xs="x",
                    ys="y",
                    source=source,
                    alpha=self.transparency,
                    color={"field": "category", "transform": color_mapper},
                    line_width=self.line_width,
                    legend_group="category",
                )
            self.legend_settings(
                legend_title=legend_title,
                legend_clickable=True,
                legend_location="top_right",
                legend_orientation="vertical",
            )
            self.styling_figure(xaxis_padding=xaxis_padding)
            p.add_tools(
                HoverTool(
                    tooltips=[
                        (legend_title, "@hoverInformation"),
                        ("X Value", "$x{1f}"),
                        ("Y Value", "$y{1f}"),
                    ]
                )
            )
            show(p)
            return True
        except Exception as e:
            if hasattr(e, "message"):
                print(e.message)
            else:
                print(e)

    def generate_multiline_plot_by_rows(
        self,
        df: pd.DataFrame,
        category_clmn: str,
        legend_title: str = "Legends",
        xaxis_padding: float = 0,
    ) -> None:
        """[Generate multiline plot by passing the dataframe, where each row represents one curve,
        all columns represents values of each curve and one additonal column represents category
        for each curve.]

        Arguments:
            df {pd.DataFrame} -- [each row represents one curve, plus one additional column for
            category of the curve]
            category_clmn {str} -- [Name of the category column in dataframe]

        Keyword Arguments:
            legend_title {str} -- [Legends of the plot] (default: {"Legends"})
            xaxis_padding {float} -- [Padding for x-axis] (default: {0})

        Returns:
            [None]
        """
        try:
            categories = df[category_clmn].unique()
            color_mapper = CategoricalColorMapper(
                factors=categories, palette=self.colors[: len(categories)]
            )

            for category in df[category_clmn].unique():
                dfnew = df.loc[(df[category_clmn] == category)]
                source = ColumnDataSource(
                    dict(
                        y=dfnew.drop([category_clmn], axis=1).values.tolist(),
                        x=[list(np.arange(0, dfnew.shape[1]))] * dfnew.shape[0],
                        category_clmn=dfnew[category_clmn],
                        hoverInformation=dfnew[category_clmn],
                    )
                )
                self.figure.multi_line(
                    xs="x",
                    ys="y",
                    source=source,
                    alpha=self.transparency,
                    color={"field": "category_clmn", "transform": color_mapper},
                    line_width=self.line_width,
                    legend_group="category_clmn",
                )

            self.legend_settings(
                legend_title=legend_title,
                legend_clickable=True,
                legend_location="top_left",
                legend_orientation="vertical",
            )
            self.styling_figure(xaxis_padding=xaxis_padding)
            self.figure.add_tools(
                HoverTool(
                    tooltips=[
                        (legend_title, "@hoverInformation"),
                        ("X Value", "$x{1f}"),
                        ("Y Value", "$y{1f}"),
                    ]
                )
            )
            show(self.figure)
        except Exception as e:
            if hasattr(e, "message"):
                print(e.message)
            else:
                print(e)

    def generate_timeseries_plot(
        self,
        df: pd.DataFrame,
        x_values_clmn: str,
        y_value_clmn: str,
        category_clmn: str,
        xlabel_orientation: float = 0.9,
        xaxis_padding: float = 0.1,
        use_xaxis_Datetime: bool = False,
        format_for_xaxis: str = "",
    ) -> None:
        """[summary]

        Arguments:
            df {pd.DataFrame} -- [Dataframe having category column, y-values column, x-values
            column/Datetime column. For e.g.:
            Converting column in to Datetime format and then assigning to parameter x_values_clmn ]
            x_values_clmn {str} -- [Name of the x-value column (either number column or
            Datatime column). You can use below command for converting reqd column into datetime:

            df["index"] = pd.to_datetime(df["index"], format="%m/%d/%Y %H:%M:%S:%f")
            where format may vary. Also, set the parameter 'use_xaxis_Datetime' to 'True',
            Also, define format for x-axis labels to display: "%Y-%m-%d  %H:%M:%S"
            ]
            y_value_clmn {str} -- [Name of the y-value column]
            category_clmn {str} -- [Name of the category column]

        Keyword Arguments:
            xlabel_orientation {float} -- [Rotating x-labels to fit the plot] (default: {0.9})
            xaxis_padding {float} -- [Padding for x-axis] (default: {0.1})
            use_xaxis_Datetime {bool} -- [If x-value column is datetime, then 'True']
            (default: {False})
            format_for_xaxis {str} -- [If x-value column is datetime, mention format for x-axis
            labels.
            For e.g.: "%Y-%m-%d  %H:%M:%S"
            ] (default: {""})

        Returns:
            [None]
        """
        try:
            palette = self.colors[: len(df[category_clmn].unique())]
            p = self.figure
            for category, color in zip(df[category_clmn].unique(), palette):
                dfnew = df.loc[(df[category_clmn] == category)]
                source = ColumnDataSource(
                    dict(
                        x_values=list(dfnew[x_values_clmn]),
                        y_values=list(dfnew[y_value_clmn]),
                        category_clmn=dfnew[category_clmn],
                    )
                )
                p.line(
                    x="x_values",
                    y="y_values",
                    source=source,
                    line_alpha=self.transparency,
                    color=color,
                    line_width=self.line_width,
                    legend_group="category_clmn",
                )
            self.styling_figure(
                xlabel_orientation=xlabel_orientation if use_xaxis_Datetime else None,
                xaxis_padding=xaxis_padding,
                yaxis_notation=False,
            )
            self.legend_settings(
                legend_title=category_clmn,
                legend_clickable=True,
                legend_location="top_right",
                legend_orientation="vertical",
            )
            p.add_tools(
                HoverTool(
                    tooltips=[
                        # Formatting the x-axis tooltips in the provided format
                        (category_clmn, "@category_clmn"),
                        #  Below code sets the X-Value in given format
                        (
                            ("X Value",)
                            + (
                                ("$x{" + format_for_xaxis + "}",)
                                if use_xaxis_Datetime
                                else ("$x{1f}",)
                            )
                        ),
                        (y_value_clmn, "$y{1f}"),
                    ],
                    #  Below code formats the above set X-Value
                    formatters={"$x": "datetime"}
                    if use_xaxis_Datetime
                    else {"$x": "numeral"},
                )
            )
            if use_xaxis_Datetime:
                p.xaxis.formatter = DatetimeTickFormatter(days=[format_for_xaxis])
            show(self.figure)
        except Exception as e:
            if hasattr(e, "message"):
                print(e.message)
            else:
                print(e)
