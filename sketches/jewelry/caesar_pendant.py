# %%
from build123d import *
from ocp_vscode import *

# %%

radius = 25
height = 2
thickness = 1

pendant = extrude(Circle(radius), height)
pendant = offset(pendant, -thickness, openings=pendant.faces().filter_by(Axis.Z))

radius -= 0.05
arcs = [
    ThreePointArc(
        [
            (radius, 0),
            (radius * 0.3, radius * 0.3),
            (0, radius),
        ]
    ),
    ThreePointArc(
        (
            (0, radius),
            (-radius * 0.3, radius * 0.3),
            (-radius, 0),
        )
    ),
    ThreePointArc(
        (
            (0, -radius),
            (radius * 0.3, -radius * 0.3),
            (radius, 0),
        )
    ),
    ThreePointArc(
        (
            (-radius, 0),
            (-radius * 0.3, -radius * 0.3),
            (0, -radius),
        )
    ),
]

arc_profile = Rectangle(thickness, height, align=(Align.CENTER, Align.MAX))
pendant += [sweep((a.edge() ^ 0) * arc_profile, a.edge()) for a in arcs]

pendant = fillet(pendant.edges().filter_by(Plane.XY), 0.3)

try:
    show(pendant)
except RuntimeError:
    export_stl(pendant, "caesar_pendant.stl")
