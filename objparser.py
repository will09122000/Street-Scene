'''
Converts OBJ (Wavefront) files to vertex, texture and
normal coordinates.

The parser currently doesn't examine material data.
Only triangular faces are supported
  (f v/vt/vn v/vt/vn v/vt/vn)
'''

from typing import Union

from pathlib import Path
import numpy as np


class ObjFile:
    def __init__(self,
            object_name: str,
            vert_coords: list[tuple[float, float, float]],
            tex_coords: list[tuple[float, float, float]],
            norm_coords: list[tuple[float, float, float]],
            smooth_shading: bool):

        self.object_name = object_name
        self.vertices = vert_coords
        self.uv_coords = tex_coords
        self.vertex_normals = norm_coords
        self.smooth_shading = smooth_shading
class Material:
    def __init__(self, name=None, Ka=[1.,1.,1.], Kd=[1.,1.,1.], Ks=[1.,1.,1.], Ns=10.0, texture=None):
        self.name = name
        self.Ka = Ka
        self.Kd = Kd
        self.Ks = Ks
        self.Ns = Ns
        self.texture = texture

class MaterialLibrary:
    def __init__(self):
        self.materials = []
        self.names = {}

    def add_material(self,material):
        self.names[material.name] = len(self.materials)
        self.materials.append(material)

def parse(filepath: Union[Path, str]) -> ObjFile:
    object_name = ''

    vert_coords = []
    tex_coords = []
    norm_coords = []

    vert_indices = []
    tex_indices = []
    norm_indices = []

    smooth_shading = False

    with open(filepath, 'r') as f:

        for line in f.readlines():
            line = line.split()
            if (len(line) > 0):
                if line[0] == 'o':
                    object_name = line[1]

                if line[0] == 'v':
                    vert_coords.append((float(line[1]), float(line[2]), float(line[3])))

                elif line[0] == 'vt':
                    tex_coords.append((float(line[1]), float(line[2])))

                elif line[0] == 'vn':
                    norm_coords.append((float(line[1]), float(line[2]), float(line[3])))

                elif line[0] == 'f':
                    face = []
                    for v in line[1:]:
                        indice = []
                        for i in v.split('/'):
                            try:
                                value = int(i)
                            except:
                                value = 0
                            indice.append(value)
                        face.append(indice)

                    if len(face) == 3:
                        for indice in face:
                            vert_indices.append(int(indice[0])-1)
                            tex_indices.append(int(indice[1])-1)
                            norm_indices.append(int(indice[2])-1)
                    elif len(face) == 4:
                        # converts quads into pairs of triangles
                        face1 = [face[0], face[1], face[2]]
                        for indice in face1:
                            vert_indices.append(int(indice[0])-1)
                            tex_indices.append(int(indice[1])-1)
                            norm_indices.append(int(indice[2])-1)

                        face2 = [face[0], face[2], face[3]]
                        for indice in face2:
                            vert_indices.append(int(indice[0])-1)
                            tex_indices.append(int(indice[1])-1)
                            norm_indices.append(int(indice[2])-1)

                elif line[0] == 's':
                    if line[1] in ('on', '1'):
                        smooth_shading = True
                    else:
                        smooth_shading = False
   
    final_vert = []
    final_tex = []
    final_norm = []

    for i in vert_indices:
        final_vert.append(vert_coords[i])

    for j in tex_indices:
        final_tex.append(tex_coords[j])

    for k in norm_indices:
        final_norm.append(norm_coords[k])


    final_vert = list(np.concatenate(final_vert).flat)
    final_tex = list(np.concatenate(final_tex).flat)
    final_norm = list(np.concatenate(final_norm).flat)

    return ObjFile(object_name, final_vert, final_tex, final_norm, smooth_shading)

def load_material_library(file_name):
    library = MaterialLibrary()
    material = None

    print('-- Loading material library {}'.format(file_name))

    mtlfile = open(file_name)
    for line in mtlfile:
        fields = line.split()
        if len(fields) != 0:
            if fields[0] == 'newmtl':
                if material is not None:
                    library.add_material(material)

                material = Material(fields[1])
                print('Found material definition: {}'.format(material.name))
            elif fields[0] == 'Ka':
                material.Ka = np.array(fields[1:], 'f')
            elif fields[0] == 'Kd':
                material.Kd = np.array(fields[1:], 'f')
            elif fields[0] == 'Ks':
                material.Ks = np.array(fields[1:], 'f')
            elif fields[0] == 'Ns':
                material.Ns = float(fields[1])
            elif fields[0] == 'd':
                material.d = float(fields[1])
            elif fields[0] == 'Tr':
                material.d = 1.0 - float(fields[1])
            elif fields[0] == 'illum':
                material.illumination = int(fields[1])
            elif fields[0] == 'map_Kd':
                material.texture = fields[1]

    library.add_material(material)

    print('- Done, loaded {} materials'.format(len(library.materials)))

    return library