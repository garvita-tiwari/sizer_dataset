"""
    #python pytorch_renderer.py --mesh_path=/BS/RVH_3dscan/static00/sizer_dataset/dataset/10001/1937/model_0.8.obj --out_dir=/BS/RVH_3dscan_raw2/static00/all_tests
"""
import os
import torch
import cv2
import numpy as np
# Util function for loading meshes
from pytorch3d.io import load_objs_as_meshes, load_obj
from render_utils import normalize_scan, create_rotmat
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
        renderer = MeshRenderer(
            rasterizer=MeshRasterizer(
                cameras=cameras,
                raster_settings=raster_settings
            ),
            shader=SoftPhongShader(
                device=device,
                cameras=cameras,
                lights=lights
            )
        )
        meshes = mesh.extend(len(R))
        images = renderer(meshes)
        [cv2.imwrite(os.path.join(out_path, '{}.jpg'.format(idx+b_id)), cv2.cvtColor(images[b_id, ..., :3].cpu().numpy()*255, cv2.COLOR_RGB2BGR)) for b_id in range(len(T))]


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
        '--batch_size', default=6,
        type=int)
    parser.add_argument(
        '--img_size', default=1024,
        type=int)


    args = parser.parse_args()

    if not os.path.exists(args.out_dir):
        os.makedirs(args.out_dir)
    # align the mesh
    smpl_ref = 'smpl_ref.obj'
    # Load obj file
    mesh = load_objs_as_meshes([args.mesh_path], device=device)
    mesh_verts, _ = mesh.get_mesh_verts_faces(0)
    smpl_verts, smpl_faces, _ = load_obj(smpl_ref, device=device)
    dist = normalize_scan(mesh_verts, smpl_verts)
    mesh = mesh.offset_verts(dist)

    render_mesh(mesh, args.out_dir, args.batch_size, args.img_size)
