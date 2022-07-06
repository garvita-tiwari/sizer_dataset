
#### Dataset and folder path
    1. sizer_dataset/scans/dataset/{subjectid}/{scan_id} : contains raw scans, corresponding texture image and segmentation of scans
    e.g. 10001/1937 -> model_0.8.obj (scan mesh), model_0.8.jpg(UV texture), seg_0.8_new.png (UV segmentation)

    2. sizer_dataset/registrations/registration_upload.zip contains registration in same folder structure.
        a. For every scan, we have neutral, female and male SMPL registrations file in 'singlemesh_{gender}.npz' file,
        where each npz file contains:  betas, pose, trans, gar_class, sub_scan, vh.
        betas, pose, trans: SMPL betas, pose and translation
        gar_class: ['g1', 'g2', 'g3', 'g4', 'g5', 'g6', 'g7', 'l1', 'l2', 'l3'] for male garments 
            and ['g8', 'g9', 'g10', 'g11', 'g12', 'g13', 'g14', 'l4', 'l5', 'l6', 'l7'] for female garments
        b. Each folder also includes 'singlemesh_{gender}.jpg', which SMPL registered texture UV.
    3. change global_var.scan_dir to '{root_dir}sizer_dataset/scans/dataset'
        and global_var.registration_dir {root_dir}sizer_dataset/scans/registrations/{unzipped folder}'
### Dependencies:

    1. MPI-IS psbody mesh library [https://github.com/MPI-IS/mesh]
    2. OpenDR
    3. SMPL class from(https://github.com/chaitanya100100/TailorNet/models), but you can use others
    4. Pytorch3D

#### SMPL model
    We currently use SMPL4GARMENT from TailorNet, change the SMPL_PATH in global_var.py