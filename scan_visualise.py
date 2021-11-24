from psbody.mesh import Mesh, MeshViewer
import argparse
from global_var import scan_dir
import ipdb
import os
import cv2
import numpy as np

from mesh_utils import read_obj, label_colours, get_submesh, garms
from get_garment import getLabels
def visualise_scan(sub_scan):

    scan_obj = os.path.join(scan_dir, sub_scan, 'model_0.8.obj')
    scan_tex = os.path.join(scan_dir, sub_scan, 'model_0.8.jpg')
    scan_seg = os.path.join(scan_dir, sub_scan, 'seg_0.8_new.png')

    if os.path.exists(scan_obj):
        scan_raw = read_obj(scan_obj)
        scan_mesh = Mesh(v=scan_raw.v, f=scan_raw.f)
        scan_mesh.vt = scan_raw.vt
        scan_mesh.ft = scan_raw.ft
    else:
        print('obj file missing for: ', sub_scan)
        return

    if os.path.exists(scan_tex):
        scan_mesh.set_texture_image(scan_tex)
    else:
        print('texture file missing')
    mv = MeshViewer()
    mv.set_static_meshes([scan_mesh])
    print(' press c for segmenation visualisation')
    ipdb.set_trace()
    if os.path.exists(scan_tex):
        scan_mesh.set_texture_image(scan_seg)
    else:
        print('segmentation file missing')
    mv = MeshViewer()
    mv.set_static_meshes([scan_mesh])
    ipdb.set_trace()

    print(' press c ')


def remove_noise(sub_scan, display=False):

    scan_obj = os.path.join(scan_dir, sub_scan, 'model_0.8.obj')
    scan_tex = os.path.join(scan_dir, sub_scan, 'model_0.8.jpg')
    scan_seg = os.path.join(scan_dir, sub_scan, 'seg_0.8_new.png')

    if os.path.exists(scan_obj):
        scan_raw = read_obj(scan_obj)
        scan_mesh = Mesh(v=scan_raw.v, f=scan_raw.f)
        scan_mesh.vt = scan_raw.vt
        scan_mesh.ft = scan_raw.ft
    else:
        print('obj file missing for: ', sub_scan)
        return
    if os.path.exists(scan_seg):
        scan_mesh.set_texture_image(scan_seg)
    else:
        print('segmentation file missing')
        return
    # check segmentation quantisation
    ###change texture file into vertex color
    seg_labels = getLabels(cv2.imread(scan_seg), scan_mesh.vt, scan_mesh.ft, scan_mesh.f)

    ###get submesh, where vc != 0
    bg_vid = np.where(seg_labels != 0)
    tmp = get_submesh(scan_mesh.v, scan_mesh.f, np.array(bg_vid))
    new_mesh = Mesh(v=tmp[0], f=tmp[1])
    new_mesh.vt = scan_mesh.vt
    new_mesh.ft = scan_mesh.ft[tmp[2]]

    # you can save the new mesh, if needed
    if display:
        mv = MeshViewer()
        mv.set_static_meshes([new_mesh])
        ipdb.set_trace()

    return new_mesh

if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Visualise scan with texture and/or segmentation. Please mention sub_id/scan_id'
    )
    parser.add_argument('--scan', '-s')
    parser.add_argument('--process', '-p')
    args = parser.parse_args()

    visualise_scan( args.scan)

    if args.process == 'remove_floor':
        clean_mesh = remove_noise(args.scan, True)