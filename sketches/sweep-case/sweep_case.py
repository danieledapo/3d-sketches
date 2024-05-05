# %% build123d script to generate a case for my Sweep split keyboard using the
# build123d framework. It is mostly parametric, the primary input is an SVG
# exported from KiCAD with the boundary of the PCB and with hand-drawn paths
# where holes must be made for the connectors.
import os.path

from build123d import *
from ocp_vscode import *


# %% case parameters
base_height = 2
border_clearance = 0.5
border_height = 7
border_radius = 3
support_clearance = 0.5
support_height = 4
tenting_rotation = (-5, 10, 0)
tenting_plane_base_height = 2


# %% utility functions
def Z(z=1):
    return Location((0, 0, z))


def readsvg(svg_path):
    # NOTE: build123d has an SVG importer, but the geometries it calculates are
    # too complicated and it makes the script too slow. Import it by hand and,
    # most importantly, sample the path every mm so that we do not end up with
    # too many points.
    from svgpathtools import svg2paths

    def sample(path):
        # kicad exports SVGs with DPI=96, go back to mm
        path = path.scaled(25.4 / 96.0)

        res = []
        nsamples = max(2, int(path.length()))
        for i in range(nsamples):
            p = path.point(i / (nsamples - 1))
            res.append((p.real, p.imag))
        return Polyline(*res).wire()

    paths, raws = svg2paths(svg_path)
    return {raw["id"]: sample(p) for p, raw in zip(paths, raws)}


# %% retrieve the geometries from the SVG exported from KiCAD
svg = readsvg(os.path.dirname(__file__) + "/sweep.svg")
boundary = svg["boundary"]
usbc = svg["usbc"]
trrs = svg["trrs"]
holes = [p for sid, p in svg.items() if sid.startswith("hole")]


# %% base
inner_base = make_face(boundary)
outer_base = offset(inner_base, border_radius)

case = extrude(outer_base, border_height)
case -= Z(base_height) * extrude(offset(inner_base, border_clearance), border_height)


# %% holes for the usbc and trrs connectors
profile = Rectangle(border_radius * 2 + 0.1, border_height * 2)
boundary_holes = sweep((usbc ^ 0) * profile, usbc) + sweep((trrs ^ 0) * profile, trrs)
case -= Z(base_height + border_height) * boundary_holes


# %% supports to keep the keyboard still
supports = [
    Z(base_height) * extrude(offset(make_face(h), -support_clearance), support_height)
    for h in holes
]
case += supports

# %%
if any((a != 0 for a in tenting_rotation)):
    # adjust the case so that the lower part of the geometry has the smallest
    # coordinate given that the tilting plane is built from 0,0
    case = mirror(case, Plane.XZ)
    case = Location(-case.bounding_box().min) * case

    tilt_plane = Plane.XY.rotated(tenting_rotation).offset(-tenting_plane_base_height)

    bottom_faces = case.faces().group_by(Axis.Z)[0]
    face = project(bottom_faces, tilt_plane)

    case += loft([bottom_faces, face])


# %% rendering
try:
    show(case)
except RuntimeError:
    export_stl(case, "sweep-case.stl")
