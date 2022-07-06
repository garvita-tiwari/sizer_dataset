""""Remove floor and extra noise using segmentation mask and then visualise the registration mesh """

import os
import argparse
from psbody.mesh import Mesh
import cv2
import sys
import numpy as np
from config.global_var import scan_dir, registration_dir
import ipdb
from utils.mesh_utils import read_obj, label_colours, get_submesh, garms, normalize_scan
from scan_visualise import remove_noise


def align_scan(sub_scan):
    # for comparison for registration(with translation) and scan, first align the scan using this
    scan_raw = remove_noise(sub_scan)
    scan_tex = os.path.join(scan_dir, sub_scan, 'model_0.8.jpg')
    scan_seg = os.path.join(scan_dir, sub_scan, 'seg_0.8_new.png')

    if os.path.exists(scan_tex):
        scan_raw.set_texture_image(scan_tex)
    else:
        print('texture file missing')

    smpl = Mesh(filename='smpl_ref.obj')
    #smpl.pose[0] = np.pi
    ipdb.set_trace()
    # axyz have negative indices
    while np.max(scan_raw.f < 0):
        scan_raw.f[scan_raw.f < 0] = scan_raw.f[scan_raw.f < 0] + scan_raw.v.shape[0] + 1
    while np.max(scan_raw.ft < 0):
        scan_raw.ft[scan_raw.ft < 0] = scan_raw.ft[scan_raw.ft < 0] + scan_raw.vt.shape[0] + 1
    scan = Mesh(v=scan_raw.v, f=scan_raw.f)
    scan.v = scan.v.dot(cv2.Rodrigues(np.array([np.pi, 0., 0.]))[0])        # OpenDR coordinates

    scan.vt = scan_raw.vt
    scan.ft = scan_raw.ft

    scan = normalize_scan(scan, smpl, change_height=False)

    scan.v = scan.v.dot(cv2.Rodrigues(np.array([np.pi, 0., 0.]))[0])
    return scan


def vis_reg(sub_scan, gender='neutral'):
    sys.path.append(config.global_var.SMPL_PATH)
    from models.smpl4garment import SMPL4Garment
    reg_path = os.path.join(registration_dir, sub_scan, 'singlemesh_{}.npz'.format(gender))
    if not os.path.exists(reg_path):
        print('registration for {} doesnt exists.'.format(sub_scan))
        return
    else:
        reg_data = np.load(reg_path)
        smpl = SMPL4Garment(gender=gender)
        smpl_mesh = smpl.run(beta=reg_data['betas'], theta=reg_data['pose'])  #this doesnt include trans
        mv = MeshViewer()
        mv.set_static_meshes([smpl_mesh])
        print('press c for SMPL+D visualisation')
        ipdb.set_trace()
        mv = MeshViewer()
        mv.set_static_meshes([Mesh(v=reg_data['vh'],f=smpl_mesh.f)])
        print('press c ')



if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Get separate garment for every scan'
    )
    parser.add_argument('--scan', '-s')
    parser.add_argument('--gender', '-g')
    args = parser.parse_args()
    aligned_scan = align_scan(args.scan)   # for comparison for registration(with translation) and scan, first align the scan using this
    vis_reg(args.gender, args.gender)

