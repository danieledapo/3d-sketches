# %%
from build123d import *
from ocp_vscode import *

# %%
diameter = 100
segments = 100
profile_thickness = 5
profile_chamfer = 0.8

profile = RectangleRounded(profile_thickness, profile_thickness, radius=profile_chamfer)

straight_path = CenterArc((0, 0), diameter / 2, 0, 180)
straight = sweep((straight_path ^ 0) * profile, straight_path)

twisted_path = CenterArc((0, 0), diameter / 2, 180, 180)
twisted = sweep(
    [
        (twisted_path ^ t) * profile.rotate(Axis.Z, t * 180)
        for t in [i / (segments - 1) for i in range(segments)]
    ],
    twisted_path,
    multisection=True,
)

ring = straight + twisted

try:
    show(ring)
except RuntimeError:
    export_stl(ring, "mobius-ring.stl")
