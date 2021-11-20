import numpy as np

from models.model import Base_Model
from models.light_model import Light_Model
from models.dynamic_model import Dynamic_Model
from models.enviro_map_model import Enviro_Map_Model

class Obj_File:
    """
    This class represents the contents of an obj file.

    Attributes
    ----------
    object_name: string | The name of the object within the file.
    model_coords: list  | The object file's geometric vertices.
    tex_coords:    list | The object file's texture vertices.
    norm_coords:   list | The object file's vertex normals.
    """

    def __init__(self,
                 object_name,
                 model_coords,
                 tex_coords,
                 norm_coords):

        self.object_name = object_name
        self.vertices = model_coords
        self.uv_coords = tex_coords
        self.vertex_normals = norm_coords

def read_obj(filepath):

    object_name = ''

    model_coords = []
    tex_coords = []
    norm_coords = []

    vert_indices = []
    tex_indices = []
    norm_indices = []

    with open(filepath, 'r') as f:
        # Loop through each line in the file.
        for line in f.readlines():
            line = line.split()
            if (len(line) > 0):
                # Object name.
                if line[0] == 'o':
                    object_name = line[1]

                # Object geometric vertices.
                if line[0] == 'v':
                    model_coords.append((float(line[1]), float(line[2]), float(line[3])))

                # Object texture vertices.
                elif line[0] == 'vt':
                    tex_coords.append((float(line[1]), float(line[2])))

                # Object vertex normals.
                elif line[0] == 'vn':
                    norm_coords.append((float(line[1]), float(line[2]), float(line[3])))

                # Object faces.
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

                    # Converts quads into pairs of triangles.
                    elif len(face) == 4:
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

    all_vertex_coords = []
    all_tex_coords = []
    all_norm_coords = []

    for i in vert_indices:
        all_vertex_coords.append(model_coords[i])
    for i in tex_indices:
        all_tex_coords.append(tex_coords[i])
    for i in norm_indices:
        all_norm_coords.append(norm_coords[i])

    all_vertex_coords = list(np.concatenate(all_vertex_coords).flat)
    all_tex_coords = list(np.concatenate(all_tex_coords).flat)
    all_norm_coords = list(np.concatenate(all_norm_coords).flat)

    return Obj_File(object_name, all_vertex_coords, all_tex_coords, all_norm_coords)

def load_obj(ctx,
             obj_file,
             texture_filepath,
             position,
             rotation    = 0.0,
             scale       = 1.0,
             translation = [0.0, 0.0, 0.0],
             light_type  = '',
             translate   = False,
             rotate      = False,
             mirror      = False):
    """Loads object file contents into a specific model type."""

    if light_type:
        return Light_Model(ctx,
                           position,
                           light_type,
                           texture_filepath,
                           obj_file.vertices,
                           obj_file.uv_coords,
                           obj_file.vertex_normals,
                           rotation,
                           scale)
    elif translate or rotate:
        return Dynamic_Model(ctx,
                             position,
                             texture_filepath,
                             obj_file.vertices,
                             obj_file.uv_coords,
                             obj_file.vertex_normals,
                             rotation,
                             scale,
                             translation)
    elif mirror:
        return Enviro_Map_Model(ctx,
                                position,
                                texture_filepath,
                                obj_file.vertices,
                                obj_file.uv_coords,
                                obj_file.vertex_normals,
                                rotation,
                                scale)
    else:
        return Base_Model(ctx,
                          position,
                          texture_filepath,
                          obj_file.vertices,
                          obj_file.uv_coords,
                          obj_file.vertex_normals,
                          rotation,
                          scale)
