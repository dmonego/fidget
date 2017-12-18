import math
import argparse
from toolz.itertoolz import concat
import svgwrite

description = "Draw an outline of a fidget spinner."

def circle_points(center_x, center_y, radius, num_points=32):
    def helper():
        rad = math.pi * 2 / (num_points + 1)
        cursor = 0
        while cursor < math.pi * 2 - 0.000001:
            x_dist = math.sin(cursor) * radius
            y_dist = math.cos(cursor) * radius
            yield (center_x + x_dist, center_y + y_dist)
            cursor += rad
    return list(helper())

def circularize(points):
    "Make a circle from a set of points passed in"
    circlepoints = points + points[0:1]
    shape = ["M %f,%f" % circlepoints[0]]
    for point in circlepoints[1:]:
        shape.append("L %f,%f" % point)
    return " ".join(shape)
    

def spinner(inner, outer, repeats):
    "Make a path that repeats a flat part and a curve. The shape is 11 points long and repeats, with an overlap on the first point"
    all_innerpoints = inner # + inner[0:1]
    all_outerpoints = outer # + outer[0:1]
    shape = []
    start = "M %f,%f" % outer[-1]
    shape.append(start)
    for offset in range(repeats):
        offset_value = offset * 11
        innerpoints = all_innerpoints[offset * 11:(offset+1) * 11]
        outerpoints = all_outerpoints[offset * 11:(offset+1) * 11]
        cap = "L %f,%f" % outerpoints[2]
        shape.append(cap)
        curve_points = concat([innerpoints[5], innerpoints[7], outerpoints[10]]) 
        curve = "C %f,%f %f,%f %f,%f" % tuple(curve_points)
        shape.append(curve)
    return " ".join(shape)
    
def write_svg(svg_out, center_path, spinner_path):
    dwg = svgwrite.Drawing(svg_out, size=('210mm', '297mm'), viewBox=('0, 0, 210, 297'))
    dwg.add(dwg.style("""
    .outline {
    	stroke: black;
    	fill: none;
    }
	"""))
    dwg.add(dwg.path(d=center_path, **{"class": "outline"}))
    dwg.add(dwg.path(d=spinner_path, **{"class": "outline"}))
    dwg.save()


def make_spinner(svg_out="spinner.svg", repeats=3):
    num_points = repeats * 11 - 1
    dpi = 24.1
    dist_bearing = 0.25 * dpi
    dist_inner = 0.6 * dpi
    dist_outer = 1.5 * dpi
    center_point_x = center_point_y = dpi * 4.0
    points_bearing = circle_points(center_point_x, center_point_y, dist_bearing)
    points_inner = circle_points(center_point_x, center_point_y, dist_inner, num_points)
    points_outer = circle_points(center_point_x, center_point_y, dist_outer, num_points)
    spinner_path = spinner(points_inner, points_outer, repeats)
    center_path = circularize(points_bearing)
    write_svg(svg_out, center_path, spinner_path)

def launch_with_cli():
    parser = argparse.ArgumentParser(description=description)
    parser.add_argument(dest="svg_out", help="Location to place the svg file")
    parser.add_argument("--points", dest="spinner_points", default=3, type=int, help="Location to place the svg file")
    args = parser.parse_args()
    make_spinner(svg_out=args.svg_out, repeats=args.spinner_points)

if __name__ == "__main__":
    launch_with_cli()
