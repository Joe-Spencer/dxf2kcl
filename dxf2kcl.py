import ezdxf


def convert_dxf_to_kcl(dxf_path, kcl_path):
    # Load the DXF file
    dxf_doc = ezdxf.readfile(dxf_path)
    modelspace = dxf_doc.modelspace()

    with open(kcl_path, "w") as kcl_file:
        kcl_file.write("// KCL code generated from DXF\n")
        kcl_file.write("// Generator created by Joseph Spencer\n")
        num_entities = 0
        for entity in modelspace:
            # each entity is treated as its own sketch
            num_entities += 1
            kcl_file.write(f"sketch" + str(num_entities)  + f"= startSketchOn('XY')" + "\n")
            try:
                #account for lines 
                if entity.dxftype() == "LINE":
                    x1=entity.dxf.start[0]
                    y1=entity.dxf.start[1]
                    kcl_file.write(f"   |> startProfileAt([{x1}, {y1}], %)\n")
                    #calulate the delta x and delta y
                    deltaX=entity.dxf.end[0]-entity.dxf.start[0]
                    deltaY=entity.dxf.end[1]-entity.dxf.start[1]
                    kcl_file.write(f"   |> line([{deltaX}, {deltaY}], %)\n")
                #account for circles   
                elif entity.dxftype() == "CIRCLE":
                    x=entity.dxf.center[0]
                    y=entity.dxf.center[1]
                    radius = entity.dxf.radius
                    kcl_file.write("   |> circle({"+"center: [" + str(x) + ","+str(y)+"], radius: "+str(radius)+"}, %)\n")
                #account for arcs
                elif entity.dxftype() == "ARC":
                    x1=entity.start_point[0]
                    y1=entity.start_point[1]
                    kcl_file.write(f"   |> startProfileAt([{x1}, {y1}], %)\n")
                    anglestart = entity.dxf.start_angle
                    angleend = entity.dxf.end_angle
                    radius = entity.dxf.radius
                    kcl_file.write("     |> arc({"+"angleStart: " + str(anglestart) + ", angleEnd:"+str(angleend)+", radius: "+str(radius)+"}, %)\n")
                #account for most types of polylines
                elif entity.dxftype() == "LWPOLYLINE":
                    points = entity.get_points()
                    start = points[0]
                    kcl_file.write(f"   |> startProfileAt([{start[0]}, {start[1]}], %)\n")
                    for point in points[1:]:
                        kcl_file.write(f"     |> lineTo([{point[0]}, {point[1]}], %)\n")
                    kcl_file.write("     |> close(%)\n")
                #splines are not currently supported
                elif entity.dxftype() == "SPLINE":
                    print("sorry no spline for you")
                    kcl_file.write("// sorry no spline for you\n")
                else:
                    print(f"Entity type {entity.dxftype()} is not supported and will be skipped.")
            except Exception as e:
                print(f"Error processing entity: {entity} - {e}")


if __name__ == "__main__":
    dxf_path = r"dxf2kcl\input.dxf"  # Path to your DXF file
    kcl_path = r"dxf2kcl\output.kcl"
    convert_dxf_to_kcl(dxf_path, kcl_path)
    