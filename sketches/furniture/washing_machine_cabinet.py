# %%
from build123d import *
from ocp_vscode import *

# %%
thickness = 15 * MM

width = 650 * MM
height = 950 * MM
depth = 650 * MM

reinforce_panel_height = 100 * MM
front_width = width - thickness * 2
front_height = height - reinforce_panel_height * 2

side_panel = Box(
    length=depth,
    width=thickness,
    height=height,
    align=(Align.CENTER, Align.CENTER, Align.MIN),
)
side_panel.label = "Side"

top_panel = Box(
    length=depth,
    width=width,
    height=thickness,
    align=(Align.CENTER, Align.CENTER, Align.MIN),
)
top_panel.label = "Top"

front_panel = Box(
    length=thickness,
    width=front_width,
    # width=600*MM,
    height=front_height,
    align=(Align.CENTER, Align.CENTER, Align.MIN),
)
front_panel.label = "Front"

reinforce_panel = Box(
    length=thickness,
    width=front_width,
    height=reinforce_panel_height,
    align=(Align.CENTER, Align.CENTER, Align.MIN),
)
reinforce_panel.label = "Reinforce"

carcass: list[Box] = [
    # top and side panels
    Plane.XY.offset(height) * top_panel,
    Pos(0, width / 2 - thickness / 2, 0) * side_panel,
    Pos(0, -width / 2 + thickness / 2, 0) * side_panel,
    # reinforcements
    Pos(depth / 2 - thickness / 2, 0, 0) * reinforce_panel,
    Pos(depth / 2 - thickness / 2, 0, height - reinforce_panel_height)
    * reinforce_panel,
    Pos(-depth / 2 + thickness / 2, 0, height - reinforce_panel_height)
    * reinforce_panel,
    # front panel
    Pos(depth / 2 - thickness / 2, 0, reinforce_panel_height) * front_panel,
]

washing_machine = Box(
    length=520 * MM,
    width=600 * MM,
    height=850 * MM,
    align=(Align.CENTER, Align.CENTER, Align.MIN),
)
washing_machine.label = "Washing machine"
washing_machine.color = Color(0.75, 0.75, 0.75)


print("========= Parts =========")
parts_count: dict[str, tuple[int, Box]] = {}
for p in carcass:
    parts_count[p.label] = (parts_count.get(p.label, (0, p))[0] + 1, p)

for label, (count, part) in sorted(
    parts_count.items(), key=lambda item: item[1][0], reverse=True
):
    print(
        f"  {count}x {label}: width={part.width} height={part.box_height} depth={part.length}"
    )


try:
    show([washing_machine, *carcass])
except RuntimeError:
    export_stl(Compound(carcass), "washing_machine_cabinet.stl")

# %%
