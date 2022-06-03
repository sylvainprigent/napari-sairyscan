This plugin implements various methods to reconstruct high resolution images for the Airyscan 
microscope raw data 

## Description

Airyscan raw images are confocal images obtained from 32 sub-detectors. Several methods can be used
to reconstruct a high resolution image from these 32 sub-detectors images. This plugin implements
the following methods:
- **Pseudo-confocal**: creates a pseudo confocal image by summing 7, 19 or 19 detectors
- **ISM**: creates a higher resolution image by summing the images from the 32 sub-detectors after 
co-registering all the images to the central detector. A deconvolution algorithm can be applied in 
post-processing to gain more resolution
- **IFED**: reconstructs a high resolution image by subtracting the outer ring detector to the central 
detector. This method can be interpreted as a 'virtual STED'
- **ISFED**: reconstructs a high resolution image by combining the co-registered detectors images and the
raw detectors images     
- **Join deconvolution**: reconstructs a high resolution image by jointly deblurring all 32 detectors 
with a variational approach.

![Example image](https://raw.githubusercontent.com/sylvainprigent/napari-sairyscan/main/docs/images/screenshot.png)

## Intended Audience & Supported Data

Supported data are raw images from the Airyscan microscope. These images must be stacks of 32 
layers corresponding to the 32 detectors. The Airyscan reader plugin can open .czi raw files. Data
can also be stored in any format that napari can open. 

## Quickstart

- Open the sample image from the menu *File > Open samples > napari-sairyscan > SAiryscan*

![Open image](https://raw.githubusercontent.com/sylvainprigent/napari-sairyscan/main/docs/images/open_sample.png)
![Open image](https://raw.githubusercontent.com/sylvainprigent/napari-sairyscan/main/docs/images/samples.png)


- Open the SAiryscan plugin from the menu *Plugins > napari-sairyscan: Airyscan reconstruction*

![Open image](https://raw.githubusercontent.com/sylvainprigent/napari-sairyscan/main/docs/images/open_plugin.png)
![Open image](https://raw.githubusercontent.com/sylvainprigent/napari-sairyscan/main/docs/images/join_deconv_plugin.png)

- We select the `join deconvolution` method and run it with the default parameters. Default parameters
are optimized for the sample image:

![Open image](https://raw.githubusercontent.com/sylvainprigent/napari-sairyscan/main/docs/images/join_deconv_result.png)


## Getting Help

For any bug report or feature request please [file an issue]

## How to Cite

If you use this plugin please cite the [paper](https://ieeexplore.ieee.org/document/9054640):
    
    @INPROCEEDINGS{9054640,
    author={Prigent, Sylvain and Dutertre, Stephanie and Kervrann, Charles},
    booktitle={ICASSP 2020 - 2020 IEEE International Conference on Acoustics, Speech and Signal Processing (ICASSP)}, 
    title={Empirical Sure-Guided Microscopy Super-Resolution Image Reconstruction from Confocal Multi-Array Detectors}, 
    year={2020},
    volume={},
    number={},
    pages={1075-1079},
    doi={10.1109/ICASSP40776.2020.9054640}}



[file an issue]: https://github.com/sylvainprigent/napari-sairyscan/issues