# %%
import math

from build123d import *
from ocp_vscode import *

# %%
diameter = 100
segments = 100
profile_thickness = 5
profile_chamfer = 0.5


# %%
def half(rot, a0=0):
    pts = []
    for i in range(segments):
        a = a0 + i / (segments - 1) * math.pi
        pts.append((diameter / 2 * math.cos(a), diameter / 2 * math.sin(a)))

    line = Polyline(*pts).wire()

    sections = []
    for i in range(segments):
        t = i / (segments - 1)

        plane = Plane(line @ t, z_dir=line % t)
        sections += plane * RectangleRounded(
            profile_thickness,
            profile_thickness,
            radius=profile_chamfer,
            rotation=rot(t),
        )

    return sweep(sections, line, multisection=True)


ring = half(rot=lambda t: t * 180) + half(a0=math.pi, rot=lambda _: 0)


try:
    show(ring)
except RuntimeError:
    export_stl(ring, "mobius-ring.stl")
