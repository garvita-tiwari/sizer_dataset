"""get 3D garment segmentation using segmentation UV tex"""
from psbody.mesh import Mesh, MeshViewer
import argparse
from config.global_var import scan_dir
import ipdb
import os
import cv2
import numpy as np
import ipdb

from utils.mesh_utils import get_submesh, label_colours, garms, read_obj
def getLabels(model_seg, vth, fth, fh):

    _, tex_indices_ = np.unique(fh.ravel(), return_index=True)
    tex_indices = np.array(vth[fth.ravel()[tex_indices_]] * model_seg.shape[:2], dtype='int32')
    #this is for sizer and frl dataset, where vt max is 1 and hence last index = img size
    labels = [tuple(model_seg[::-1, ...][y-1, x-1]) for x, y in tex_indices]
    dic = {}
    for n, l in enumerate(label_colours):
        dic[l] = garms[n]
    model_label = np.array([dic[x] for x in labels])
    return model_label


def get_garment(sub_scan):
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
        scan_mesh.set_texture_image(scan_seg)
    else:
        print('segmentation file missing')
        return
    # check segmentation quantisation
    ###change texture file into vertex color
    seg_labels = getLabels(cv2.imread(scan_seg), scan_mesh.vt, scan_mesh.ft, scan_mesh.f)

    ###get submesh, where vc != 0
    for garm in garms[1:]:
        bg_vid = np.where(seg_labels == garm)
        tmp = get_submesh(scan_mesh.v, scan_mesh.f, np.array(bg_vid))
        new_mesh = Mesh(v=tmp[0], f=tmp[1])
        new_mesh.vt = scan_mesh.vt
        new_mesh.ft = scan_mesh.ft[tmp[2]]

        #you can save the new mesh, if needed
        mv = MeshViewer()
        mv.set_background_color(np.array([1, 1, 1]))

        mv.set_static_meshes([new_mesh])
        ipdb.set_trace()

        print(' press c for next layer')




if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Get separate garment for every scan'
    )
    parser.add_argument('--scan', '-s')
    args = parser.parse_args()
    get_garment( args.scan)

