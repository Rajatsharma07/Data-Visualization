from bokeh.palettes import Blues8
from bokeh.plotting import figure

# Creation of Parent class


class Visualization:
    # Defining the Color palette
    colors = [
        "#0097AC",
        "#020B13",
        "#888E95",
        "#C0873A",
        "#F8DA00",
        "#F28B00",
        "#F4D7AE",
        "#5EB342",
        "#E72D34",
    ]
    colors += Blues8[:5]

    def __init__(
        self,
        x_label: str,
        y_label: str,
        plot_title: str,
        plt_width: int,
        plt_height: int,
    ) -> None:
        """[Constructor to initialize the instances of the child classes for 'figure'
        object creation]

        Arguments:
            x_label {str} -- [Value of x-axis label, set by child instances])
            y_label {str} -- [Value of y-axis label, set by child instances])
            plot_title {str} -- [title of the plot, set by child instances])
            plt_width {int} -- [width of the plot, set by child instances] )
            plt_height {int} -- [height of the plot, set by child instances])
        """
        # These attributes can be unique for each instance
        self.x_label = x_label
        self.y_label = y_label
        self.title = plot_title
        self.plt_width = plt_width
        self.plt_height = plt_height
        self.__create_fig()
        self.styling_figure()

    def __create_fig(self) -> None:
        """[Private method creating 'figure' object for the child instances]"""
        self.figure = figure(
            title=self.title,
            x_axis_label=self.x_label,
            y_axis_label=self.y_label,
            plot_width=self.plt_width,
            plot_height=self.plt_height,
        )

    def styling_figure(
        self,
        labels_font_size: str = "12pt",
        title_font_size: str = "20pt",
        figure_outline_color: str = "#020B13",
        figure_background_color: str = "#F9F9F9",
        xlabel_orientation: int = 1.2,
        xaxis_padding: float = 0,
        yaxis_notation: bool = True,
    ) -> None:
        """[Method to style the 'figure' object. Can be accessed by all child classes]

        Keyword Arguments:
            labels_font_size {str} -- [Font size for the labels] (default: {"12pt"})
            title_font_size {str} -- [Font size of the plot title] (default: {"20pt"})
            figure_outline_color {str} -- [Color of the figure outline] (default: {"#020B13"})
            figure_background_color {str} -- [Color of the figure background] (default: {"#F9F9F9"})
            xlabel_orientation {int} -- [Rotation of the x-axis labels] (default: {1.2})
            xaxis_padding {float} -- [Padding for x-axis labels] (default: {0})
            yaxis_notation {bool} -- [When True, y-axis labels use scientific notations] (default: {True})
        """
        self.figure.xaxis.major_label_orientation = xlabel_orientation
        self.figure.outline_line_color = figure_outline_color
        self.figure.xaxis.major_label_text_font_size = labels_font_size
        self.figure.yaxis.major_label_text_font_size = labels_font_size
        self.figure.yaxis.axis_label_text_font_size = labels_font_size
        self.figure.xaxis.axis_label_text_font_size = labels_font_size
        self.figure.yaxis.axis_label_text_font_style = "bold"
        self.figure.xaxis.axis_label_text_font_style = "bold"
        self.figure.title.text_font_size = title_font_size
        self.figure.background_fill_color = figure_background_color
        self.figure.x_range.range_padding = xaxis_padding
        self.figure.yaxis.formatter.use_scientific = yaxis_notation

    def legend_settings(
        self,
        has_legend: bool = True,
        legend_title: str = "Legend",
        legend_orientation: str = "horizontal",
        legend_clickable: bool = False,
        legend_location: str = "top_right",
        legend_fontsize: str = "12pt",
    ) -> None:
        """[Change the legend settings of the plot, can be accessed by all child classes]

        Keyword Arguments:
            has_legend {bool} -- [When False, no legends appears ] (default: {True})
            legend_title {str} -- [Title of the legends] (default: {"Legend"})
            legend_orientation {str} -- [vertical/horizontal] (default: {"horizontal"})
            legend_clickable {bool} -- [description] (default: {False})
            legend_location {str} -- ["top_left", "top_center", "top_right" (the default),
            "center_right", "bottom_right", "bottom_center", "bottom_left", "center_left",
            "center"] (default: {"top_right"})
            legend_fontsize {str} -- [set the fon size of the legends] (default: {"12pt"})
        """
        if has_legend:
            self.figure.legend.title = legend_title
            if legend_clickable:
                self.figure.legend.click_policy = "hide"
            self.figure.legend.title_text_font_size = legend_fontsize
            self.figure.legend.label_text_font_size = legend_fontsize
            self.figure.legend.orientation = legend_orientation
            self.figure.legend.location = legend_location

    @classmethod
    def display_palette(cls) -> None:
        """[Displays the color palette on the terminal, along with hex code]"""
        RESET = "\033[0m"

        def get_color_escape(r, g, b, background=False):
            return "\033[{};2;{};{};{}m".format(48 if background else 38, r, g, b)

        for color in cls.colors:
            r, g, b = tuple(int(color.lstrip("#")[i : i + 2], 16) for i in (0, 2, 4))
            print(
                get_color_escape(255, 255, 255)
                + get_color_escape(r, g, b, True)
                + " "
                + color
                + " "
                + RESET,
                end="",
            )
