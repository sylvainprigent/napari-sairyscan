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

![Open image](https://raw.githubusercontent.com/sylvainprigent/napari-sairyscan/main/docs/images/screenshot.png)
![Open image](https://raw.githubusercontent.com/sylvainprigent/napari-sairyscan/main/docs/images/screenshot.png)


- Open the SAiryscan plugin from the menu *Plugins > napari-sairyscan: Airyscan reconstruction*

![Open image](https://raw.githubusercontent.com/sylvainprigent/napari-sairyscan/main/docs/images/screenshot.png)
![Open image](https://raw.githubusercontent.com/sylvainprigent/napari-sairyscan/main/docs/images/screenshot.png)



## Getting Help

This section should point users to your preferred support tools, whether this be raising
an issue on GitHub, asking a question on image.sc, or using some other method of contact.
If you distinguish between usage support and bug/feature support, you should state that
here.

## How to Cite

Many plugins may be used in the course of published (or publishable) research, as well as
during conference talks and other public facing events. If you'd like to be cited in
a particular format, or have a DOI you'd like used, you should provide that information here. 
