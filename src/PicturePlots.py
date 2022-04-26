from bokeh.plotting import show, output_file
import holoviews as hv
import numpy as np
from functools import reduce
from typing import List, Tuple
import cv2
from pathlib import Path

hv.extension("bokeh")


class PicturePlots:
    def __scaling_images(
        self,
        img,  # Image object
        max_width: int,  # Maximum Width pixels
        max_height: int,  # Maximum Height pixels,
    ) -> Tuple[hv.RGB, float]:
        img = cv2.imread(img)
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        RGB_flag = 0
        if len(img.shape) == 3:
            RGB_flag = 1
        else:
            print(img.shape)
        # Aspect Ratio Before width/height
        aspect = img.shape[1] / img.shape[0]
        width_factor = int((max_width / img.shape[1]) * 100)
        height_factor = int((max_height / img.shape[0]) * 100)
        factor = width_factor if width_factor < height_factor else height_factor
        new_width = int(img.shape[1] * factor / 100)
        new_height = int(img.shape[0] * factor / 100)
        dim = (new_width, new_height)
        # Resizing image
        resized = cv2.resize(img, dim, interpolation=cv2.INTER_AREA)
        if RGB_flag == 0:
            new_img = np.stack((resized, resized, resized), axis=2)
        elif RGB_flag == 1:
            new_img = resized
        # Returning resized image and original aspect ratio

        return new_img, aspect

    def generate_picture_plot(
        self,
        images: List[str],
        labels: List[str] = [],
        use_original_aspect: bool = True,
        plot_title: str = "Picture Plot",
        max_height_pixels: int = 1600,
        max_width_pixels: int = 2200,
        output_file_path: str = "",
        output_file_name: str = "",
    ) -> hv.render:
        """
        Arguments:
            images {List[images]} -- [Relative or Absolute path of the Image]
            labels {List[labels]} -- [It refers to title of the individual plot to be displayed]

        Keyword Arguments:
            use_original_aspect {bool} -- [Original aspect ratio is used to plot otherwise default
            when False] (default: {True})
            plot_title {str} -- [Title of the plot] (default: {"Picture Plot"})
            max_height_pixels {int} -- [Maximum Height pixels, for Scaling image] (default: {1600})
            max_width_pixels {int} -- [Maximum Width pixels, for Scaling image] (default: {2200})
            output_file_path {str} -- [Path of the output file which you want to keep (if not
            provided, store in current folder with the 'filename' provided))
            output_file_name {str} -- [Name of the output file which you want to keep
            (without .html)] (default: {None})

        Returns:
            hv.render -- [Render object which shows Holoviews Layout plot]
        """
        try:
            if output_file_name != "":
                if output_file_path == "":
                    output_file(
                        str(Path.cwd() / output_file_name) + ".html",
                        title="Picture Plot",
                    )
                else:
                    output_file(
                        output_file_path + "/" + output_file_name + ".html",
                        title="Picture Plot",
                    )
            lst_img = []
            Aspect = None

            for i in range(len(images) - len(labels)):
                labels.append("Plot")
            for img, name in zip(images, labels):
                new_img, Aspect = self.__scaling_images(
                    img=img, max_height=max_height_pixels, max_width=max_width_pixels
                )
                lst_img.append(
                    hv.RGB(new_img, label=name).opts(
                        xaxis=None,
                        yaxis=None,
                        toolbar="below",
                        default_tools=[
                            "pan",
                            "box_zoom",
                            "wheel_zoom",
                            "reset",
                            "save",
                        ],
                        aspect=Aspect if use_original_aspect else "Alpha",
                        bgcolor="#F9F9F9",
                    )
                )
            if len(lst_img) == 1:
                # Displaying only 1 image
                return show(hv.render(lst_img[0]))
            else:
                plot = (
                    # Adds the Images to the Holoviews frame (e.g.: Original + Label + Predicted )
                    hv.Layout(reduce((lambda x, y: x + y), lst_img)).cols(len(images))
                ).opts(
                    toolbar="left",
                    merge_tools=True,
                    title=plot_title,
                    fontsize={"title": "20pt"},
                )
                return show(hv.render(plot))
        except Exception as e:
            if hasattr(e, "message"):
                print(e.message)
            else:
                print(e)


if __name__ == "__main__":

    # Calling a Picture plot
    obj_pictureplot = PicturePlots()
    obj_pictureplot.generate_picture_plot(
        max_height_pixels=1800,
        max_width_pixels=2200,
        images=[
            "C:/Users/SR00036792/Documents/Projects/D019/Image/0270.png",
            "./Tempo/label.png",
            "./Tempo/prediction.png",
        ],
        labels=[],
        output_file_name="NewFile",
        output_file_path=".\Tempo",
    )
