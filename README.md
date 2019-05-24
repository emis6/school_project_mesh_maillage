# school_project_mesh_maillage
Maillage project MAIN5 2019


Brief descirption of files:

- outils.py : contains a mesh class, read/write functions and some lines to call read and create a mesh then solve and write into a paraview file

- *.vtu : is a file readable by paraview to illustrate the found solution

- *.msh contains the mesh to find the problem's solution to this particular mesh

- *.edp a script written in freefem++ to find the solution of the problem(for verification)

- *.geo file containing the description of the submarine to be read by gmsh to generate the mesh
