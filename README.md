# DXF to KCL Converter

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](https://opensource.org/licenses/MIT)

A Python utility for converting DXF (Drawing Exchange Format) files to KCL (KittyCAD Language) code. This tool enables seamless integration between traditional CAD workflows and the modern, code-first approach of KittyCAD.

## Overview

This converter transforms 2D sketches from DXF files into executable KCL code that can be used in [KittyCAD's Modeling App](https://zoo.dev/modeling-app/download) (now Zoo Design Studio). The tool is specifically designed for 2D sketches in the XY plane.

## Features

- Converts DXF entities to KCL code
- Supports common geometric primitives:
  - Lines
  - Circles
  - Arcs
  - Polylines
- Maintains geometric relationships and dimensions
- Generates clean, readable KCL code

## Limitations

- Currently only supports 2D sketches in the XY plane
- Splines are not currently supported
- Complex DXF features like blocks or hatches are not implemented

## Installation

1. Clone this repository:
   ```bash
   git clone https://github.com/Joe-Spencer/dxf2kcl.git
   cd dxf2kcl
   ```

2. Install dependencies:
   ```bash
   pip install ezdxf
   ```

## Usage

Basic usage:

```bash
python dxf2kcl.py input.dxf output.kcl
```

### Example

1. Create or obtain a DXF file with your 2D sketch
2. Run the converter:
   ```bash
   python dxf2kcl.py my_sketch.dxf my_sketch.kcl
   ```
3. Open the generated KCL file in KittyCAD's Modeling App

## How It Works

The converter reads the DXF file using the `ezdxf` library, processes each supported entity, and generates equivalent KCL code. The process involves:

1. Parsing the DXF file structure
2. Identifying supported entities
3. Converting coordinates and geometric properties
4. Generating appropriate KCL commands
5. Writing the result to a KCL file

## Contributing

Contributions are welcome! Here are some ways you can contribute:

- Add support for additional DXF entities
- Improve conversion accuracy
- Enhance error handling
- Add tests and examples

Please feel free to submit issues and pull requests.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- [ezdxf](https://ezdxf.readthedocs.io/) - Python library for DXF processing
- [KittyCAD](https://zoo.dev/) - For their innovative approach to CAD with code
