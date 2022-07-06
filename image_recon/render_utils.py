""""pytorch implementation of align_meshes"""
import cv2
import numpy as np
import torch
import ipdb
# def get_mesh_dims(vertices):
#
#     min_coord = vertices.min(dim=0)[0]
#     max_coord = vertices.max(dim=0)[0]
#     return max_coord - min_coord
#
#
# def upright_scan(vertices, dims):
#     if torch.abs(dims).argmax() == 2:
#         return vertices.dot(torch.from_numpy(cv2.Rodrigues(np.array([-np.pi / 2., 0, 0]))[0])), dims[[0, 2, 1]]
#     elif  torch.abs(dims).argmax() == 0:
#         return vertices.dot(torch.from_numpy(cv2.Rodrigues(np.array([0, 0, np.pi / 2.]))[0])), dims[[1, 0, 2]]
#     return vertices, dims

def create_rotmat():
    rt = []
    t = []
    #for r in np.arange(36) * np.pi * 2 / 36.:
    for r in np.arange(36) * np.pi * 2 / 36.:
        rt.append(cv2.Rodrigues(np.array([0., r, 0.]))[0])
        t.append(np.array([0., 0.1, 2.2]))
    for r in np.arange(18) * np.pi * 2 / 18.:
        rt.append(cv2.Rodrigues(np.array([0., r, 0.]))[0])
        t.append(np.array([0., 0.5, 1.5]))

    for r in np.arange(18) * np.pi * 2 / 18.:
        rt.append(cv2.Rodrigues(np.array([0., r, 0.]))[0])
        t.append(np.array([0., -0.4, 1.5]))


    t = torch.from_numpy(np.array(t).astype(np.float32))
    rt = torch.from_numpy(np.array(rt).astype(np.float32))
    return rt, t
def align_meshes_centroids(scan_verts, smpl_verts):

    """
    Compute bounding boxes of the meshes and align the center of the
    :param scan_mesh: psbody.mesh.Mesh object
    :param smpl_mesh: SMPL model instance
    :return: None
    """
    c1 = get_bounding_box_center(scan_verts)
    c2 = get_bounding_box_center(smpl_verts)
    dist = c2 - c1
    return dist


def get_bounding_box_center(vertices):

    """
    Returns the center of the bounding box of a given mesh
    :param vertices: a Vx3 matrix with vertex coordinates
    :return: 1X3 ndarray with the coordinates of the centroid
    """
    min_coord = vertices.min(dim=0)[0]
    max_coord = vertices.max(dim=0)[0]

    return min_coord + (max_coord - min_coord) / 2


def normalize_scan(scan_verts, smpl_verts):
    ###Thanks to Thiemo for this code
    #
    # dims_scan = get_mesh_dims(scan_verts)
    # #scan_verts, dims_scan = upright_scan(scan_verts, dims_scan)
    # dims_smpl = get_mesh_dims(smpl_verts)
    dist = align_meshes_centroids(scan_verts, smpl_verts)

    return dist
