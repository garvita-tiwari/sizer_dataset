"""mesh reader and other geo uitils"""
from psbody.mesh import Mesh
import cv2
from os.path import split, splitext, join, exists, normpath
import numpy as np

def get_mesh_dims(vertices):
    ###Thanks to Thiemo for this code

    min_coord = vertices.min(axis=0)
    max_coord = vertices.max(axis=0)

    return max_coord - min_coord


def upright_scan(vertices, dims):
    ###Thanks to Thiemo for this code

    if np.abs(dims).argmax() == 2:
        return vertices.dot(cv2.Rodrigues(np.array([-np.pi / 2., 0, 0]))[0]), dims[[0, 2, 1]]
    elif np.abs(dims).argmax() == 0:
        return vertices.dot(cv2.Rodrigues(np.array([0, 0, np.pi / 2.]))[0]), dims[[1, 0, 2]]
    return vertices, dims


def align_meshes_centroids(scan_mesh, smpl_mesh):
    ###Thanks to Thiemo for this code

    """
    Compute bounding boxes of the meshes and align the center of the
    :param scan_mesh: psbody.mesh.Mesh object
    :param smpl_mesh: SMPL model instance
    :return: None
    """
    c1 = get_bounding_box_center(scan_mesh.v)
    try: c2 = get_bounding_box_center(smpl_mesh.r)
    except AttributeError: c2 = get_bounding_box_center(smpl_mesh.v)
    dist = c2 - c1
    scan_mesh.translate_vertices(translation=dist)


def get_bounding_box_center(vertices):
    ###Thanks to Thiemo for this code

    """
    Returns the center of the bounding box of a given mesh
    :param vertices: a Vx3 matrix with vertex coordinates
    :return: 1X3 ndarray with the coordinates of the centroid
    """
    min_coord = vertices.min(axis=0)
    max_coord = vertices.max(axis=0)
    return min_coord + (max_coord - min_coord) / 2


def normalize_scan(scan, smpl, change_height=False):
    ###Thanks to Thiemo for this code

    dims_scan = get_mesh_dims(scan.v)
    scan.v, dims_scan = upright_scan(scan.v, dims_scan)
    dims_smpl = get_mesh_dims(smpl.v)
    #print(np.max(scan.v[:,1]) - np.min(scan.v[:,1]))
    # import ipdb
    # ipdb.set_trace()

    """this was in original code, same height for all scans"""
    if change_height:
        scan.v *= (dims_smpl[1] / dims_scan[1])

    align_meshes_centroids(scan, smpl)

    print(np.max(scan.v[:, 1]) - np.min(scan.v[:, 1]))
    return scan

class Minimal(object):
    def __init__(self, **kwargs):
        self.__dict__ = kwargs

def read_obj(filename):
    ###Thanks to Thiemo for this code
    # from opendr.dummy import Minimal

    obj_directory = split(filename)[0]
    lines = open(filename).read().split('\n')

    d = {'v': [], 'vn': [], 'f': [], 'vt': [], 'ft': []}

    mtls = {}
    for line in lines:
        line = line.split()
        if len(line) < 2:
            continue

        key = line[0]
        values = line[1:]

        if key == 'v':
            d['v'].append([np.array([float(v) for v in values[:3]])])
        elif key == 'f':
            spl = [l.split('/') for l in values]
            d['f'].append([np.array([int(l[0])-1 for l in spl[:3]], dtype=np.int32)])
            if len(spl[0]) > 1 and spl[1] and len(spl[0][1]) > 0 and 'ft' in d:
                d['ft'].append([np.array([int(l[1])-1 for l in spl[:3]])])

            # TOO: redirect to actual vert normals?
            #if len(line[0]) > 2 and line[0][2]:
            #    d['fn'].append([np.concatenate([l[2] for l in spl[:3]])])
        elif key == 'vn':
            d['vn'].append([np.array([float(v) for v in values])])
        elif key == 'vt':
            d['vt'].append([np.array([float(v) for v in values])])


    for k, v in d.items():
        if k in ['v','vn','f','vt','ft']:
            if v:
                d[k] = np.vstack(v)
            else:
                del d[k]
        else:
            d[k] = v

    result = Minimal(**d)
    # result = (**d)

    return result




label_colours = [(0,0,0)
                ,(255,0,0),(0,255,0),(0,0,255)]

garms = [0, 1, 2, 3]

def get_submesh(verts, faces, verts_retained=None, faces_retained=None, min_vert_in_face=2):
    '''
        Given a mesh, create a (smaller) submesh
        indicate faces or verts to retain as indices or boolean

        @return new_verts: the new array of 3D vertices
                new_faces: the new array of faces
                bool_faces: the faces indices wrt the input mesh
                vetex_ids: the vertex_ids wrt the input mesh
        '''

    if verts_retained is not None:
        # Transform indices into bool array
        if verts_retained.dtype != 'bool':
            vert_mask = np.zeros(len(verts), dtype=bool)
            vert_mask[verts_retained] = True
        else:
            vert_mask = verts_retained

        # Faces with at least min_vert_in_face vertices
        bool_faces = np.sum(vert_mask[faces.ravel()].reshape(-1, 3), axis=1) > min_vert_in_face

    elif faces_retained is not None:
        # Transform indices into bool array
        if faces_retained.dtype != 'bool':
            bool_faces = np.zeros(len(faces_retained), dtype=bool)
        else:
            bool_faces = faces_retained

    new_faces = faces[bool_faces]
    # just in case additional vertices are added
    vertex_ids = list(set(new_faces.ravel()))

    oldtonew = -1 * np.ones([len(verts)])
    oldtonew[vertex_ids] = range(0, len(vertex_ids))

    new_verts = verts[vertex_ids]
    new_faces = oldtonew[new_faces].astype('int32')

    return (new_verts, new_faces, bool_faces, vertex_ids)
