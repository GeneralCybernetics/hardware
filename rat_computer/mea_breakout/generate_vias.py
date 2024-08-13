import sys
from uuid import uuid4

################
# FOR KICAD V6 #
################

def generate_segment(start_x: float, start_y: float, end_x: float, end_y: float, width: float, layer: str, net: int) -> str:
    # example: (segment (start 48.675 19.595) (end 48.675 19.625) (width 0.2) (layer "F.Cu") (net 0) (tstamp c2524bbd-0c89-4e5a-98de-d05485e4de15))
    return f"(segment (start {start_x} {start_y}) (end {end_x} {end_y}) (width {width}) (layer {layer}) (net {net}) (tstamp {uuid4()}))\n"

def generate_via(x: float, y: float, size: float, drill: float, layers: (str, str), net: int) -> str:
    # example: (via (at 48.675 19.625) (size 0.8) (drill 0.4) (layers "F.Cu" "B.Cu") (net 0) (tstamp dd3affe4-8d37-41a2-b278-aa25b0f34241))
    return f"(via (at {x} {y}) (size {size}) (drill {drill}) (layers \"{layers[0]}\" \"{layers[1]}\") (net {net}) (tstamp {uuid4()}))\n"


def main():
    # Check if the filename is provided
    if len(sys.argv) < 2:
        print("Usage: python script.py <filename>")
        sys.exit(1)

    filename = sys.argv[1]

    # rows
    n_outer_row = 34
    n_inner_row = 28
    n_rows = 4
    row_separation_distance = 10
    inner_outer_separation_distance = 5

    # vias
    start_x = 100
    start_y = 100
    pitch = 1.21
    size = 0.8
    drill = 0.4
    layers = ("F.Cu", "B.Cu")
    net = 0

    with open(filename, "w") as f:
        for j in range(1, n_rows + 1):
            for i in range(n_outer_row):
                x = start_x + pitch * i
                y = start_y + row_separation_distance * j
                f.write(generate_via(x, y, size, drill, layers, net))
            
            for i in range(n_inner_row):
                x = start_x + pitch * i
                y = start_y + row_separation_distance * j + inner_outer_separation_distance
                f.write(generate_via(x, y, size, drill, layers, net))

if __name__ == "__main__":
    main()
