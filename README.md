


## SIZER Dataset Repository
 

<p align="center"><img src="https://virtualhumans.mpi-inf.mpg.de/sizer/sizer_teaser.jpg" alt="" width="88%"/></p>


### Download Dataset 
    https://nextcloud.mpi-klsb.mpg.de/index.php/s/nx6wK6BJFZCTF8C/authenticate/showShare
Fill this [form](https://docs.google.com/forms/d/e/1FAIpQLSddBep3Eif1gI-6IhaZybBDoR-_H_QW1NST0JV5vviauvPNTA/viewform)
### For dataset access

1. Fill this [form](https://docs.google.com/forms/d/e/1FAIpQLSddBep3Eif1gI-6IhaZybBDoR-_H_QW1NST0JV5vviauvPNTA/viewform)
2. For password, send an email to: gtiwari@mpi-inf.mpg.de

### Installation and Datafiles:
    Check INSTALL.MD


## Dataset Details

A dataset of clothing size variation of approximately 2000  scans including 100 subjects wearing 10 garment classes in different sizes,
where we make available, scans, clothing segmentation, SMPL+G registrations, body shape under clothing, garment class and size labels


### Data and Annotations

We compare SIZER dataset with existing real world 3D datasets

| Data  | Number of Scans | Registrations        | Segmentation          | Minimal Clothing/Body under clothing             | Multiview images                  | Labels                          | Demographics|
|-------|-----------------|----------------------|-----------------------|--------------------------------------------------|-----------------------------------|---------------------------------| --------------|
| SIZER | ~2000           | SMPL, SMPL+D, SMPL+G | Upper, Lower and body | yes | code or scanner images on request | clothing style, size and gender | Yes(on request)|
| CAPE  | Dynamic scans   | SMPL , SMPL+D        | No | Yes | No*                               | Gender                          | No |
| THUman2.0  | ~500            | SMPL , SMPL+X        | No | Yes | No*                               | -                               | No |




| Clothing Style     | Number of scans |  
|--------------------|-----------------| 
| TShirt, Shorts     | 889         |  
| Shirt, Pants       | 655             | 
| Shirt, Shorts      | 182             | 
| Shirt +Coat, Pants | 252             | 
| Hoodies, Pants     | 255             |
| Vest, Short        | 226             | 
| Vest, Pants        | 23              | 


= {'g1': 'ShirtNoCoat_Pants', 165
'g2' : 'ShirtNoCoat_Pants'  157 
'g9' : 'ShirtNoCoat_Pants' , 96
'l1' : 'ShirtNoCoat_Pants', 135
'l4' : 'ShirtNoCoat_Pants',  94 



'g8': 'ShirtNoCoat_ShortPants', 95
'l5':  'ShirtNoCoat_ShortPants', 87



'g3' : 'Coat_Pants', 155
'g10' : 'Coat_Pants', 97

'g4' : 'Hoodies',158
'g11' : 'Hoodie Pants', 97


'g5' : 'TShirtNoCoat_ShortPants',  131
'g6' :'TShirtNoCoat_ShortPants',  154
'g12': 'TShirtNoCoat_ShortPants', 98
'g13': 'TShirtNoCoat_ShortPants', 101
'l2' : 'TShirtNoCoat_ShortPants',  130
'l3' : 'TShirtNoCoat_ShortPants', 123
'l6' : 'TShirtNoCoat_ShortPants', 76 
'l7' : 'TShirtNoCoat_ShortPants'} 76


'g7' : 'Vest_ShortPants' , 134
'g14': 'Vest_ShortPants', 92

'g15' : 'Vest_Pants', 23

## Visualize and process data


### Visualize scan and clean floor noise
    python vis_data/scan_visualise.py --scan=<subjectid>/<scanid> --process remove_floor

This script only visualises original scan and cleaned scan and saves the clean mesh in the same data directory
subjectid = {10001, 10005 ....... }
scanid = {1937.....} (for 10001)

<p align="center">
Output
</p>

<p align="center">

  <img alt="org_scan" src="data/org_scan.png" width="10%">
&nbsp; &nbsp; &nbsp; &nbsp;
  <img alt="seg_labels" src="data/seg_labels.png" width="10%">
&nbsp; &nbsp; &nbsp; &nbsp;
  <img alt="clean_scan" src="data/clean_scan.png" width="10%">
</p>
<p align="center">
  Original Scan
&nbsp; &nbsp; &nbsp; &nbsp;
  Segmentation Labels
&nbsp; &nbsp; &nbsp; &nbsp;
  Clean Scan
</p>

### Visualize segmented garment layers

    python vis_data/get_garment.py --scan=<subjectid>/<scanid>

<p align="center">
Output
</p>
<p align="center">
  <img alt="org_scan" src="data/shirt.png" width="13%">
&nbsp; &nbsp; &nbsp; &nbsp;
  <img alt="seg_labels" src="data/pants.png" width="11%">
&nbsp; &nbsp; &nbsp; &nbsp;
  <img alt="clean_scan" src="data/skin.png" width="9%">
</p>
<p align="center">
  Original Scan
&nbsp; &nbsp; &nbsp; &nbsp;
  Segmentation Labels
&nbsp; &nbsp; &nbsp; &nbsp;
  Clean Scan
</p>

This script only visualises original scan and 3 layers of segmented scan, namely upper garment, lower garment and other.

### Visualize registration

    python vis_data/visualise_registration.py --scan=<subjectid>/<scanid>

Note: Before using/comparing scans and registrations, align scan, using align_scan() in visualise_registration.py 

### Evaluate registration

    python vis_data/visualise_registration.py --scan=<subjectid>/<scanid>

If you have your own code/method for scan registrations, we here provide a code to evaluate the quality of registration. 
## Others

We here provide code for using/evaluating SIZER dataset for various tasks such as 3D reconstruction from images, scan fitting etc.

### Image based reconstruction
For image based reconstruction, SIZER scans can be rendered and data pair of {image, scans, SMPL params} can be generated for training or evaluation.

#### Rendering using fixed camera views:
    python image_recon/pytorch_renderer.py --mesh_path=<obj_file> --out_dir=<out_dir>


#### Rendering image, depth and normal
    python image_recon/image_renderer.py --mesh_path=<obj_file> --out_dir=<out_dir>

<obj_file> should contain <>.obj and <>.jpg in the same folder with same name. Currently we render from 72 fixed views, This can be changed in create_rotmat() function in image_recon/render_utils.py


<p align="center">
Output
</p>
<p align="center">
  <img alt="org_scan" src="data/9.jpg" width="12%">
&nbsp; &nbsp; &nbsp; &nbsp;
  <img alt="org_scan" src="data/9_depth.jpg" width="12%">
&nbsp; &nbsp; &nbsp; &nbsp;
  <img alt="clean_scan" src="data/9_normal.jpg" width="12%">
</p>
<p align="center">
  RGB render
&nbsp; &nbsp; &nbsp; &nbsp;
  Depth
&nbsp; &nbsp; &nbsp; &nbsp;
  Normal
</p>

#### Creating data pairs:
    Coming Soon





### Citation:
    @inproceedings{tiwari20sizer,
        title = {SIZER: A Dataset and Model for Parsing 3D Clothing and Learning Size Sensitive 3D Clothing},
        author = {Tiwari, Garvita and Bhatnagar, Bharat Lal and Tung, Tony and Pons-Moll, Gerard},
        booktitle = {European Conference on Computer Vision ({ECCV})},
        month = {August},
        organization = {{Springer}},
        year = {2020},
        }
