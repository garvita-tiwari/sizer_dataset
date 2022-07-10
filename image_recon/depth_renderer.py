"""
    #python image_recon/depth_renderer.py --mesh_path=/BS/RVH_3dscan/static00/sizer_dataset/dataset/10001/1937/model_0.8.obj --out_dir=/BS/RVH_3dscan_raw2/static00/all_tests
"""
import os
import torch
import torch.nn as nn
import ipdb
import cv2
import numpy as np
# Util function for loading meshes
from pytorch3d.io import load_objs_as_meshes, load_obj
from pytorch3d.renderer.mesh.renderer import  MeshRendererWithFragments
from render_utils import normalize_scan, create_rotmat
from  pytorch3d.ops.interp_face_attrs import interpolate_face_attributes
from pytorch3d.renderer import (
    FoVPerspectiveCameras,
    AmbientLights,
    RasterizationSettings,
    MeshRenderer,
    MeshRasterizer,
    SoftPhongShader,
)

# Setup
if torch.cuda.is_available():
    device = torch.device("cuda:0")
    torch.cuda.set_device(device)
else:
    device = torch.device("cpu")

class MeshRendererWithDepth(nn.Module):
    def __init__(self, rasterizer, shader):
        super().__init__()
        self.rasterizer = rasterizer
        self.shader = shader

    def forward(self, meshes_world):

        fragments = self.rasterizer(meshes_world)
        images = self.shader(fragments, meshes_world)
        return images, fragments.zbuf


def phong_normal_shading(meshes, fragments) :
    faces = meshes.faces_packed()  # (F, 3)
    vertex_normals = meshes.verts_normals_packed()  # (V, 3)
    faces_normals = vertex_normals[faces]

    pixel_normals = interpolate_face_attributes(fragments.pix_to_face, fragments.bary_coords, faces_normals)
        # pixel_vals = (barycentric_coords[..., None] * pixel_face_vals).sum(dim=-2)

    return pixel_normals[:,:,:,0, :]

def render_mesh(mesh, out_path, batch_size, img_size):

    rt, t = create_rotmat()

    raster_settings = RasterizationSettings(
        image_size=img_size,
        blur_radius=0.0,
        faces_per_pixel=1,
    )

    lights = AmbientLights(device=device)
    for idx in range(0, len(t), batch_size):
        R = rt[idx: idx+batch_size]
        T = t[idx: idx+batch_size]
        print(len(T))
        cameras = FoVPerspectiveCameras(device=device, R=R, T=T)

        # Create a Phong renderer by composing a rasterizer and a shader. The textured Phong shader will
        # interpolate the texture uv coordinates for each vertex, sample from a texture image and
        # apply the Phong lighting model

        rasterizer=MeshRasterizer(
            cameras=cameras,
            raster_settings=raster_settings)

        shader=SoftPhongShader(
            device=device,
            cameras=cameras,
            lights=lights)

        # renderer = MeshRenderer(rasterizer, shader)
        meshes = mesh.extend(len(R))
        fragments = rasterizer(meshes)
        images = shader(fragments, meshes)
        pixel_normals = phong_normal_shading(meshes, fragments)
        depth = fragments.zbuf
        #normalise depth map

        #
        # images, depth = renderer.forward(meshes)
        [cv2.imwrite(os.path.join(out_path, '{}.jpg'.format(idx+b_id)), cv2.cvtColor(images[b_id, ..., :3].cpu().numpy()*255, cv2.COLOR_RGB2BGR)) for b_id in range(len(T))]
        for b_id in range(batch_size):
            #todo: make this better

            depth_b = depth[b_id].cpu().numpy()[:,:,0]
            mask = depth_b == -1
            v_min, v_max = np.min(depth_b[mask==0]), np.max(depth_b)
            new_min, new_max = 0.0, 1.0
            depth_b = (depth_b - v_min) / (v_max - v_min) * (new_max - new_min) + new_min
            depth_b[mask == 1] = 0.0
            cv2.imwrite(os.path.join(out_path, '{}_depth.jpg'.format(idx+b_id)),depth_b*255)

            pixel_norm_b = pixel_normals[b_id].cpu().numpy()
            cv2.imwrite(os.path.join(out_path, '{}_normal.jpg'.format(idx+b_id)),pixel_norm_b*255)





if __name__ == "__main__":

    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--mesh_path',
        type=str)
    parser.add_argument(
        '--out_dir',
        type=str)
    parser.add_argument(
        '--batch_size', default=2,
        type=int)
    parser.add_argument(
        '--img_size', default=256,
        type=int)


    args = parser.parse_args()

    if not os.path.exists(args.out_dir):
        os.makedirs(args.out_dir)
    # align the mesh
    smpl_ref = '/BS/garvita/work/code/sizer_data/data/smpl_ref.obj'
    # Load obj file
    mesh = load_objs_as_meshes([args.mesh_path], device=device)
    mesh_verts, _ = mesh.get_mesh_verts_faces(0)
    smpl_verts, smpl_faces, _ = load_obj(smpl_ref, device=device)
    dist = normalize_scan(mesh_verts, smpl_verts)
    mesh = mesh.offset_verts(dist)

    render_mesh(mesh, args.out_dir, args.batch_size, args.img_size)
