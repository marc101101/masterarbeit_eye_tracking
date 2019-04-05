from sys import platform as sys_pf

import matplotlib.patches as patches
import numpy as np


if sys_pf == 'darwin':
    import matplotlib
    matplotlib.use("TkAgg")
    import matplotlib.pyplot as plt
    import matplotlib.image as mpimg
    import matplotlib.animation as animation

class DrawCurrentData:

    def get_sub_plots(self, title):
        fig = plt.figure(1, figsize=(20, 5))

        sp1 = fig.add_subplot(131)
        sp1.set_title("X - Y")
        sp1.set_xlabel('X - Koordinaten')
        sp1.set_ylabel('Y - Koordinaten')

        sp2 = fig.add_subplot(132)
        sp2.set_title("X - Z")
        sp2.set_xlabel('X - Koordinaten')
        sp2.set_ylabel('Z - Koordinaten')

        sp3 = fig.add_subplot(133)
        sp3.set_title("Z - Y")
        sp3.set_xlabel('Z - Koordinaten')
        sp3.set_ylabel('Y - Koordinaten')

        plt.suptitle(title)

        return sp1, sp2, sp3

    def show_images(self, sp1, sp2, sp3):
        img1 = mpimg.imread('front.jpg')
        sp1.imshow(img1, origin='lower')

        img2 = mpimg.imread('top.jpg')
        sp2.imshow(img2, origin='lower')

        img3 = mpimg.imread('side.jpg')
        sp3.imshow(img3, origin='lower')

    def get_vector_colors(colors, size):
        if colors == None:
            colors = [['r', 'g']] * size
        return colors

    def add_vectors(self, sp, start_x, end_x, start_y, end_y, colors, start_fmt, line_width):
        lines = sp.plot([start_x, end_x], [start_y, end_y], '-', linewidth=line_width, markersize=0)
        for i in range(len(colors)):
            lines[i].set_color(colors[i][0])
        lines = sp.plot([start_x, start_x], [start_y, start_y], start_fmt, markersize=4)
        for i in range(len(colors)):
            lines[i].set_color(colors[i][1])

    def add_rect(self, sp, x, y, w, h, color):
        rect = patches.Rectangle((x, y), w, h, linewidth=1, edgecolor=color, facecolor=color)
        sp.add_patch(rect)

    def plot(self, coords, title):
        sp1, sp2, sp3 = self.get_sub_plots(title)

        sp1.scatter(x=coords[0], y=coords[1], c='r', s=1)
        sp2.scatter(x=coords[0], y=coords[2], c='r', s=1)
        sp3.scatter(x=coords[2], y=coords[1], c='r', s=1)

        plt.show()

    def plot_with_image(self, coords, title):
        sp1, sp2, sp3 = self.get_sub_plots(title)

        sp1.scatter(x=coords[0], y=coords[1], c='r', s=1)
        sp2.scatter(x=coords[0], y=coords[2], c='r', s=1)
        sp3.scatter(x=coords[2], y=coords[1], c='r', s=1)

        self.show_images(sp1, sp2, sp3)

        plt.show()

    def plot_vectors(self, start, end, title, start_fmt='x', line_width=0.5, colors=None):
        colors = self.get_vector_colors(colors, len(start[0]))

        sp1, sp2, sp3 = self.get_sub_plots(title)

        self.add_vectors(sp1, start[0], end[0], start[1], end[1], colors, start_fmt, line_width)
        self.add_vectors(sp2, start[0], end[0], start[2], end[2], colors, start_fmt, line_width)
        self.add_vectors(sp3, start[2], end[2], start[1], end[1], colors, start_fmt, line_width)

        plt.show()

    def plot_vectors_with_image(self, start, end, title, start_fmt='x', line_width=0.5, colors=None):
        colors = self.get_vector_colors(colors, len(start[0]))

        sp1, sp2, sp3 = self.get_sub_plots(title)

        self.add_vectors(sp1, start[0], end[0], start[1], end[1], colors, start_fmt, line_width)
        self.add_vectors(sp2, start[0], end[0], start[2], end[2], colors, start_fmt, line_width)
        self.add_vectors(sp3, start[2], end[2], start[1], end[1], colors, start_fmt, line_width)

        self.show_images(sp1, sp2, sp3)

        plt.show()

    def plot_vectors_with_image_and_aois(self, start, end, aois, title, start_fmt='x', line_width=0.5, colors=None):
        colors = self.get_vector_colors(colors, len(start[0]))

        sp1, sp2, sp3 = self.get_sub_plots(title)

        self.add_vectors(sp1, start[0], end[0], start[1], end[1], colors, start_fmt, line_width)
        self.add_vectors(sp2, start[0], end[0], start[2], end[2], colors, start_fmt, line_width)
        self.add_vectors(sp3, start[2], end[2], start[1], end[1], colors, start_fmt, line_width)

        for aoi in aois:
            self.add_rect(sp1, aoi.x, aoi.y, aoi.w, aoi.h, aoi.color)
            self.add_rect(sp2, aoi.x, aoi.z, aoi.w, aoi.d, aoi.color)
            self.add_rect(sp3, aoi.z, aoi.y, aoi.d, aoi.h, aoi.color)

        self.show_images(sp1, sp2, sp3)

        plt.show()

    def plot_heatmap(self, aoi, title):
        sp1, sp2, sp3 = self.get_sub_plots(title)

        self.add_rect(sp1, aoi.x, aoi.y, aoi.w, aoi.h, aoi.color)
        self.add_rect(sp2, aoi.x, aoi.z, aoi.w, aoi.d, aoi.color)
        self.add_rect(sp3, aoi.z, aoi.y, aoi.d, aoi.h, aoi.color)

        if len(aoi.points) > 0:
            points = np.swapaxes(np.array(aoi.points), 0, 1)

            sp1.scatter(x=points[0], y=points[1], c=[[1, 0, 0, 0.2]], s=50, zorder=2)
            sp2.scatter(x=points[0], y=points[2], c=[[1, 0, 0, 0.2]], s=50, zorder=2)
            sp3.scatter(x=points[2], y=points[1], c=[[1, 0, 0, 0.2]], s=50, zorder=2)

        self.show_images(sp1, sp2, sp3)

        plt.show()
