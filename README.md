# carbonstructures

**Authors:** Anthony Dee and Nhi Nguyen  
**Description:** A Python package for generating and functionalizing carbon structures, with support for exporting to LAMMPS and XYZ formats.



## **Overview**

carbonstructures is a Python package designed to generate graphene-based carbon structures. It provides an interactive command-line interface (CLI) for defining structural parameters, applying functionalization, and exporting the final structure for molecular simulations.



## **Features**
- **Structure Generation:** Create various carbon structures, including graphene sheets, sandwiches, pistons, and carbon nanotubes.
- **Functionalization:** Apply functional groups to carbon structures with customizable patterns and coverage.
- **Export Capabilities:** Export generated structures in LAMMPS and XYZ file formats for use in external simulation tools.



## **Installation**
Ensure you have **Python 3** installed on your system. Clone the repository and navigate to the source directory:

```bash
git clone https://github.com/YueGroup/carbonstructures.git
cd carbonstructures/src/carbonstructures
```
To make the script executable:

```bash
chmod +x generate.py 
```

## **Usage**
### **Running the Interactive Generator**
To start generating carbon structures, run:

```bash
./generate.py
```

or if not executable:

```bash
python generate.py
```

This will launch an interactive CLI where you can:

1. Select the structure type.
2. Define structural parameters.
3. Apply functionalization.
4. Export the final structure in LAMMPS (.data) or XYZ (.xyz) format.


## **License**
Copyright 2024, BSD 3-Clause License, Yue Research Group.



## **Acknowledgments**
Thanks to Yue Research Group for supporting the development of this package.
