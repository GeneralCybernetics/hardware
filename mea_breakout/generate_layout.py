import os
import yaml

ORIGIN_X = 0
ORIGIN_Y = 0

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
    
    n_connectors_outer_row = 33
    n_connectors_inner_row = 29 # it's actually 30, but we're omitting the last one so we have space for the spring contact on a different pad

    conn_refdes = "U"
    pad_refdes = "J"

    inter_pad_spacing = 1.21
    pad_to_conn_spacing = 3
    row_to_row_spacing = 3

    layout = Layout()

    pad_footprint = Footprint("1mm_x_1mm_solder_pad", "1mm_x_1mm_solder_pad.pretty")
    conn_footprint = Footprint("TE_2329497-2", "/home/aydin/Documents/Hardware/mea_breakout/mea_breakout/2329497_2.pretty")

    refdes_ctr = 0

    # This code just aligns the connectos with the breakout pads
    # it still requires manual work to align them in the square shape
    # but this drastically reduces the manual workload

    # for outer row
    for i in range(n_connectors_outer_row + 1):
        layout.add_component(f"{conn_refdes}{i + refdes_ctr + 1}", [inter_pad_spacing * i, ORIGIN_Y], 90, False, conn_footprint)
        layout.add_component(f"{pad_refdes}{i + refdes_ctr + 1}", [inter_pad_spacing * i, ORIGIN_Y - pad_to_conn_spacing], 90, False, pad_footprint)

    refdes_ctr += n_connectors_outer_row + 1

    for i in range(n_connectors_outer_row + 1):
        layout.add_component(f"{conn_refdes}{i + refdes_ctr + 1}", [inter_pad_spacing * i, ORIGIN_Y + 10], 90, False, conn_footprint)
        layout.add_component(f"{pad_refdes}{i + refdes_ctr + 1}", [inter_pad_spacing * i, ORIGIN_Y - pad_to_conn_spacing + 10], 90, False, pad_footprint)

    refdes_ctr += n_connectors_outer_row + 1

    for i in range(n_connectors_outer_row - 1):
        layout.add_component(f"{conn_refdes}{i + refdes_ctr + 1}", [inter_pad_spacing * i, ORIGIN_Y + 20], 90, False, conn_footprint)
        layout.add_component(f"{pad_refdes}{i + refdes_ctr + 1}", [inter_pad_spacing * i, ORIGIN_Y - pad_to_conn_spacing + 20], 90, False, pad_footprint)

    refdes_ctr += n_connectors_outer_row - 1

    for i in range(n_connectors_outer_row - 1):
        layout.add_component(f"{conn_refdes}{i + refdes_ctr + 1}", [inter_pad_spacing * i, ORIGIN_Y + 30], 90, False, conn_footprint)
        layout.add_component(f"{pad_refdes}{i + refdes_ctr + 1}", [inter_pad_spacing * i, ORIGIN_Y - pad_to_conn_spacing + 30], 90, False, pad_footprint)

    refdes_ctr += n_connectors_outer_row - 1
        
    # for inner row
    for i in range(n_connectors_inner_row):
        layout.add_component(f"{conn_refdes}{i + refdes_ctr + 1}", [inter_pad_spacing * i, ORIGIN_Y + 40], 90, False, conn_footprint)
        layout.add_component(f"{pad_refdes}{i + refdes_ctr + 1}", [inter_pad_spacing * i, ORIGIN_Y - pad_to_conn_spacing + 40], 90, False, pad_footprint)

    refdes_ctr += n_connectors_inner_row

    for i in range(n_connectors_inner_row):
        layout.add_component(f"{conn_refdes}{i + refdes_ctr + 1}", [inter_pad_spacing * i, ORIGIN_Y + 50], 90, False, conn_footprint)
        layout.add_component(f"{pad_refdes}{i + refdes_ctr + 1}", [inter_pad_spacing * i, ORIGIN_Y - pad_to_conn_spacing + 50], 90, False, pad_footprint)

    refdes_ctr += n_connectors_inner_row

    for i in range(n_connectors_inner_row):
        layout.add_component(f"{conn_refdes}{i + refdes_ctr + 1}", [inter_pad_spacing * i, ORIGIN_Y + 60], 90, False, conn_footprint)
        layout.add_component(f"{pad_refdes}{i + refdes_ctr + 1}", [inter_pad_spacing * i, ORIGIN_Y - pad_to_conn_spacing + 60], 90, False, pad_footprint)

    refdes_ctr += n_connectors_inner_row

    for i in range(n_connectors_inner_row):
        layout.add_component(f"{conn_refdes}{i + refdes_ctr + 1}", [inter_pad_spacing * i, ORIGIN_Y + 70], 90, False, conn_footprint)
        layout.add_component(f"{pad_refdes}{i + refdes_ctr + 1}", [inter_pad_spacing * i, ORIGIN_Y - pad_to_conn_spacing + 70], 90, False, pad_footprint)

    refdes_ctr += n_connectors_inner_row

    for i in range(256 - refdes_ctr):
        layout.add_component(f"{conn_refdes}{i + refdes_ctr + 1}", [inter_pad_spacing * i, ORIGIN_Y + 80], 90, False, conn_footprint)
        layout.add_component(f"{pad_refdes}{i + refdes_ctr + 1}", [inter_pad_spacing * i, ORIGIN_Y - pad_to_conn_spacing + 80], 90, False, pad_footprint)

    refdes_ctr = 256

    layout.save()