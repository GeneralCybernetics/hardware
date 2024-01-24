import os
import yaml

NUM_CONNECTORS_INNER_ROW = 29 # it's actually 30, but we're omitting the last one so we have space for the spring contact on a different pad
NUM_CONNECTORS_OUTER_ROW = 33
INTER_PAD_SPACING = 1.275

ORIGIN_X = 68.64
ORIGIN_Y = 0.00

class Footprint:

    name: str
    path: os.PathLike

    def __init__(self, name: str, path: os.PathLike):
        self.name = name
        self.path = path

    def to_dict(self) -> dict:
        return {
            "path": str(self.path),
            "name": self.name
        }

class Layout:    
    toplevel: dict = {
        "origin": [ORIGIN_X, ORIGIN_Y],
        "components": {}
    }

    def add_component(self, refdes: str, loc: list, rot: float, flip: bool, footprint: Footprint):
        self.toplevel["components"][refdes] = {
            "location": loc,
            "rotation": rot,
            "flip": flip,
            "footprint": footprint.to_dict()
        }

    def save(self):
        with open('layout.yaml', 'w') as f:
            yaml.dump(self.toplevel, f)
        print("Saved layout.yaml")

if __name__ == "__main__":
    
    conn_refdes = "U"
    pad_refdes = "J"

    pad_to_conn_spacing = 0
    row_to_row_spacing = 3

    layout = Layout()

    pad_footprint = Footprint("1mm_x_1mm_solder_pad", "1mm_x_1mm_solder_pad.pretty")
    conn_footprint = Footprint("TE_2329497-2", "2329497_2.pretty")

    refdes_ctr = 0

    # This code just aligns the connectos with the breakout pads
    # it still requires manual work to align them in the square shape
    # but this drastically reduces the manual workload

    # for outer row

    # top
    for i in range(NUM_CONNECTORS_OUTER_ROW + 1):
        layout.add_component(f"{conn_refdes}{i + refdes_ctr + 1}", [ORIGIN_X + INTER_PAD_SPACING * i, ORIGIN_Y], 90, False, conn_footprint)
        layout.add_component(f"{pad_refdes}{i + refdes_ctr + 1}", [ORIGIN_X + INTER_PAD_SPACING * i, ORIGIN_Y - pad_to_conn_spacing], 90, True, pad_footprint)

    refdes_ctr += NUM_CONNECTORS_OUTER_ROW + 1

    # bottom
    for i in range(NUM_CONNECTORS_OUTER_ROW + 1):
        layout.add_component(f"{conn_refdes}{i + refdes_ctr + 1}", [ORIGIN_X + INTER_PAD_SPACING * i, ORIGIN_Y + INTER_PAD_SPACING * (NUM_CONNECTORS_OUTER_ROW)], 270, False, conn_footprint)
        layout.add_component(f"{pad_refdes}{i + refdes_ctr + 1}", [ORIGIN_X + INTER_PAD_SPACING * i, ORIGIN_Y - pad_to_conn_spacing + INTER_PAD_SPACING * (NUM_CONNECTORS_OUTER_ROW )], 270, True, pad_footprint)

    refdes_ctr += NUM_CONNECTORS_OUTER_ROW + 1

    # left
    for i in range(NUM_CONNECTORS_OUTER_ROW - 1):
        layout.add_component(f"{conn_refdes}{i + refdes_ctr + 1}", [ORIGIN_X, INTER_PAD_SPACING * (i + 1) + ORIGIN_Y], 180, False, conn_footprint)
        layout.add_component(f"{pad_refdes}{i + refdes_ctr + 1}", [ORIGIN_X - pad_to_conn_spacing, INTER_PAD_SPACING * (i + 1) + ORIGIN_Y], 180, True, pad_footprint)

    refdes_ctr += NUM_CONNECTORS_OUTER_ROW - 1

    # right
    for i in range(NUM_CONNECTORS_OUTER_ROW - 1):
        layout.add_component(f"{conn_refdes}{i + refdes_ctr + 1}", [ORIGIN_X + INTER_PAD_SPACING * (NUM_CONNECTORS_OUTER_ROW), ORIGIN_Y + INTER_PAD_SPACING * (i + 1)], 0, False, conn_footprint)
        layout.add_component(f"{pad_refdes}{i + refdes_ctr + 1}", [ORIGIN_X + pad_to_conn_spacing + INTER_PAD_SPACING * (NUM_CONNECTORS_OUTER_ROW), ORIGIN_Y + INTER_PAD_SPACING * (i + 1)], 0, True, pad_footprint)

    refdes_ctr += NUM_CONNECTORS_OUTER_ROW - 1
        
    # for inner row

    # top
    for i in range(NUM_CONNECTORS_INNER_ROW):
        layout.add_component(f"{conn_refdes}{i + refdes_ctr + 1}", [ORIGIN_X + INTER_PAD_SPACING * i + 0.8, ORIGIN_Y + INTER_PAD_SPACING], 270, False, conn_footprint)
        layout.add_component(f"{pad_refdes}{i + refdes_ctr + 1}", [ORIGIN_X + INTER_PAD_SPACING * i + 0.8, ORIGIN_Y - pad_to_conn_spacing + INTER_PAD_SPACING], 270, True, pad_footprint)

    refdes_ctr += NUM_CONNECTORS_INNER_ROW

    # bottom
    for i in range(NUM_CONNECTORS_INNER_ROW):
        layout.add_component(f"{conn_refdes}{i + refdes_ctr + 1}", [ORIGIN_X + INTER_PAD_SPACING * (NUM_CONNECTORS_OUTER_ROW) - (INTER_PAD_SPACING * i) - 0.8, ORIGIN_Y + INTER_PAD_SPACING * (NUM_CONNECTORS_OUTER_ROW - 1)], 90, False, conn_footprint)
        layout.add_component(f"{pad_refdes}{i + refdes_ctr + 1}", [ORIGIN_X + INTER_PAD_SPACING * (NUM_CONNECTORS_OUTER_ROW) - (INTER_PAD_SPACING * i) - 0.8, ORIGIN_Y + INTER_PAD_SPACING * (NUM_CONNECTORS_OUTER_ROW - 1) - pad_to_conn_spacing], 90, True, pad_footprint)

    refdes_ctr += NUM_CONNECTORS_INNER_ROW

    # left
    for i in range(NUM_CONNECTORS_INNER_ROW):
        layout.add_component(f"{conn_refdes}{i + refdes_ctr + 1}", [ORIGIN_X + INTER_PAD_SPACING, ORIGIN_Y + (NUM_CONNECTORS_OUTER_ROW * INTER_PAD_SPACING) - (i * INTER_PAD_SPACING) - 0.8], 0, False, conn_footprint)
        layout.add_component(f"{pad_refdes}{i + refdes_ctr + 1}", [ORIGIN_X + INTER_PAD_SPACING - pad_to_conn_spacing, ORIGIN_Y + (NUM_CONNECTORS_OUTER_ROW * INTER_PAD_SPACING) - (i * INTER_PAD_SPACING) - 0.8], 0, True, pad_footprint)

    refdes_ctr += NUM_CONNECTORS_INNER_ROW

    # right
    for i in range(NUM_CONNECTORS_INNER_ROW):
        layout.add_component(f"{conn_refdes}{i + refdes_ctr + 1}", [ORIGIN_X + INTER_PAD_SPACING * (NUM_CONNECTORS_OUTER_ROW - 1), ORIGIN_Y + (INTER_PAD_SPACING * i) + 0.8], 180, False, conn_footprint)
        layout.add_component(f"{pad_refdes}{i + refdes_ctr + 1}", [ORIGIN_X + INTER_PAD_SPACING * (NUM_CONNECTORS_OUTER_ROW - 1) - pad_to_conn_spacing, ORIGIN_Y + (INTER_PAD_SPACING * i) + 0.8], 180, True, pad_footprint)

    refdes_ctr += NUM_CONNECTORS_INNER_ROW

    # stragglers
    for i in range(256 - refdes_ctr):
        layout.add_component(f"{conn_refdes}{i + refdes_ctr + 1}", [ORIGIN_X + INTER_PAD_SPACING * i, ORIGIN_Y + 80], 90, False, conn_footprint)
        layout.add_component(f"{pad_refdes}{i + refdes_ctr + 1}", [ORIGIN_X + INTER_PAD_SPACING * i, ORIGIN_Y - pad_to_conn_spacing + 80], 90, True, pad_footprint)

    refdes_ctr = 256

    layout.save()