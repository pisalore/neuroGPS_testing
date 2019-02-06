## NeuroGPS_testing
### An application of NeuroGPS on light sheet microscopic images (degree thesis at UNIFI).

This code repository contains all the necessary to test NeuroGPS with the F1-score metric.

- Project structure:
	* files: This folder contains the original dataset. The initial 2D images of all the stacks are located in the folder named substack and there is also the corresponding original ground truth marker file. 
	* STACKS: This folder contains the 3D original dataset, created with Fiji from 2D images (website: [Fiji](https://fiji.sc/)). These files are those used as input in NeuroGPS software.
	* codice_F1: This folder contain all the necessary to calculate F1 score. There are:
		* gt folder: this folder contains the modified ground truth for the F1-score calculation.
		* scripts folder: this folder contains all the scripts used to adapt the NeuroGPS output to the ground truth for the F1-score                calculation.
		* treshold folder: this folder contains all the NeuroGPS outputs for each 3D stack of images in the dataset, for each possibile              treshold-minimum radius couple of values. These files are compared with the gt for the F1-score calculation.
		* F1_ORACLE_LOSO: this is the python file where the function Oracle and Leave-One-Stack-Out are implemented.
		* All the necessary code for the implementation of F1-calculation and the process of markers file containing neurons'                        annotations.

It is also included a text file were are saved test results (RESULTS.rtf).
The experiments have been done using a computer with these features:
- Memory: GB DDR4 2400MHz SDRAM, 16 GB SDRAM;-
- Processor: IntelR©CoreTMi7 8550U/7500U Processor; 
- Graphic card: NVIDIA GeForce GTX 1050;
- OS: Windows 10 Pro;

For reproduce the results:
1. Download the repository.
2. Make sure your computer is equipped with Python 3.7.
3. Open the project and install all the requirements.
4. Unzip the treshold.zip file, then drag and drop the folder treshold in the folder "codice_F1.
5. Run `F1_ORACLE_LOSO.py`

For the visualization of the 3D images it's recommended to use the Vaa3D software-suite. Websites: [Vaa3D official site](http://home.penglab.com/proj/vaa3d/home/index.html) - [Vaa3D on GitHub](https://github.com/Vaa3D) .

For more details on this project, visit the [wiki pages](https://github.com/pisalore/neuroGPS_testing/wiki) of NeuroGPS testing.
