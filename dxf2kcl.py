import ezdxf
from pathlib import Path


def convert_dxf_to_kcl(dxf_path, kcl_path):
    # Load the DXF file
    dxf_doc = ezdxf.readfile(dxf_path)
    modelspace = dxf_doc.modelspace()

    with open(kcl_path, "w") as kcl_file:
        kcl_file.write("// KCL code generated from DXF\n")
        kcl_file.write("// Generator created by Joseph Spencer\n")
        num_entities = 0
        for entity in modelspace:
            # each entity is treated as its own sketch/profile
            num_entities += 1
            sketch_name = f"sketch{num_entities:03d}"
            profile_name = f"profile{num_entities:03d}"
            kcl_file.write(f"{sketch_name} = startSketchOn(XY)\n")
            try:
                # Lines
                if entity.dxftype() == "LINE":
                    x1 = entity.dxf.start[0]
                    y1 = entity.dxf.start[1]
                    x2 = entity.dxf.end[0]
                    y2 = entity.dxf.end[1]
                    delta_x = x2 - x1
                    delta_y = y2 - y1
                    kcl_file.write(f"{profile_name} = startProfile({sketch_name}, at = [{x1}, {y1}])\n")
                    if abs(delta_y) < 1e-12:
                        kcl_file.write(f"  |> xLine(length = {delta_x})\n")
                    elif abs(delta_x) < 1e-12:
                        kcl_file.write(f"  |> yLine(length = {delta_y})\n")
                    else:
                        kcl_file.write(f"  |> line(end = [{delta_x}, {delta_y}])\n")

                # Circles
                elif entity.dxftype() == "CIRCLE":
                    x = entity.dxf.center[0]
                    y = entity.dxf.center[1]
                    radius = entity.dxf.radius
                    kcl_file.write(f"{profile_name} = startProfile({sketch_name}, at = [{x}, {y}])\n")
                    kcl_file.write(f"  |> circle(center = [{x},{y}], radius = {radius})\n")

                # Arcs
                elif entity.dxftype() == "ARC":
                    x1 = entity.start_point[0]
                    y1 = entity.start_point[1]
                    anglestart = entity.dxf.start_angle
                    angleend = entity.dxf.end_angle
                    radius = entity.dxf.radius
                    kcl_file.write(f"{profile_name} = startProfile({sketch_name}, at = [{x1}, {y1}])\n")
                    kcl_file.write(f"  |> arc(angleStart = {anglestart}, angleEnd = {angleend}, radius = {radius})\n")

                # Polylines (assumed straight segments)
                elif entity.dxftype() == "LWPOLYLINE":
                    points = entity.get_points()
                    start = points[0]
                    kcl_file.write(f"{profile_name} = startProfile({sketch_name}, at = [{start[0]}, {start[1]}])\n")
                    prev_x, prev_y = start[0], start[1]
                    for point in points[1:]:
                        dx = point[0] - prev_x
                        dy = point[1] - prev_y
                        kcl_file.write(f"  |> line(end = [{dx}, {dy}])\n")
                        prev_x, prev_y = point[0], point[1]
                    kcl_file.write("  |> close()\n")

                # Unsupported splines
                elif entity.dxftype() == "SPLINE":
                    print("sorry no spline for you")
                    kcl_file.write("// sorry no spline for you\n")
                else:
                    print(f"Entity type {entity.dxftype()} is not supported and will be skipped.")
            except Exception as e:
                print(f"Error processing entity: {entity} - {e}")


if __name__ == "__main__":
    try:
        script_dir = Path(__file__).resolve().parent
        default_dxf = script_dir / "input.dxf"
        default_kcl = script_dir / "output.kcl"

        dxf_path_in = input(f"Enter path to input DXF file (default: {default_dxf}): ").strip().strip('"')
        dxf_path = Path(dxf_path_in) if dxf_path_in else default_dxf
        if not dxf_path.exists():
            raise FileNotFoundError(f"Input DXF not found: {dxf_path}")

        kcl_path_in = input(f"Enter path for output KCL file (default: {default_kcl}): ").strip().strip('"')
        kcl_path = Path(kcl_path_in) if kcl_path_in else default_kcl
        if kcl_path.parent and not kcl_path.parent.exists():
            kcl_path.parent.mkdir(parents=True, exist_ok=True)

        convert_dxf_to_kcl(str(dxf_path), str(kcl_path))
        print(f"KCL written to: {kcl_path}")
    except KeyboardInterrupt:
        print("\nOperation cancelled by user.")
    except Exception as e:
        print(f"Error: {e}")
    