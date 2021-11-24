


### NeuralGIF
 
Code for  Sizer Dataset

<img src="https://virtualhumans.mpi-inf.mpg.de/sizer/sizer_teaser.jpg" alt="" width="88%"/>

While models of 3D clothing learned from real data exist, no method can predict clothing deformation as a function of garment size. In this paper, we introduce SizerNet to predict 3D clothing conditioned on human body shape and garment size parameters, and ParserNet to infer garment meshes and shape under clothing with personal details in a single pass from an input mesh. SizerNet allows to estimate and visualize the dressing effect of a garment in various sizes, and ParserNet allows to edit clothing of an input mesh directly, removing the need for scan segmentation, which is a challenging problem in itself. To learn these models, we introduce the SIZER dataset of clothing size variation which includes 100 different subjects wearing casual clothing items in various sizes, totaling to approximately 2000 scans. This dataset includes the scans, registrations to the SMPL model, scans segmented in clothing parts, garment category and size labels. Our experiments show better parsing accuracy and size prediction than baseline methods trained on SIZER. The code, model and dataset will be released for research purposes.
### Download Dataset 
    https://nextcloud.mpi-klsb.mpg.de/index.php/s/nx6wK6BJFZCTF8C/authenticate/showShare

### For dataset access
    1. Fill this form [https://docs.google.com/forms/d/e/1FAIpQLSddBep3Eif1gI-6IhaZybBDoR-_H_QW1NST0JV5vviauvPNTA/viewform]
    2. For password, send an email to: gtiwari@mpi-inf.mpg.de

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

    1.MPI-IS psbody mesh library [https://github.com/MPI-IS/mesh]

    2.OpenDR

    3.SMPL class from(https://github.com/chaitanya100100/TailorNet/models), but you can use others

### Visualise scan and clean floor noise
    python scan_visualise.py --scan=<subjectid>_<scanid> --process remove_floor

This script only visualises original scan and cleaned scan. If you need clean scan for further processing then save clean_mesh in obj file
subjectid = {10001, 10005 ....... }
scanid = {1937.....} (for 10001)

### Visualise segmented garment layers

    python get_garment.py --scan=<subjectid>_<scanid>

This script only visualises original scan and 3 layers of segmented scan, namely upper garment, lower garment and other.

### Visualise registration

    python visualise_registration.py --scan=<subjectid>_<scanid>

#### SMPL model
    We currently use SMPL4GARMENT from TailorNet, change the SMPL_PATH in global_var.py
#### Using scans and registrations

    Align scan, using visualise_registration/align_scan, before comparing scan and corresponding registrations.

### Citation:
    @inproceedings{tiwari20sizer,
        title = {SIZER: A Dataset and Model for Parsing 3D Clothing and Learning Size Sensitive 3D Clothing},
        author = {Tiwari, Garvita and Bhatnagar, Bharat Lal and Tung, Tony and Pons-Moll, Gerard},
        booktitle = {European Conference on Computer Vision ({ECCV})},
        month = {August},
        organization = {{Springer}},
        year = {2020},
        }
