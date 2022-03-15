# Local Binary Pattern

Local binary pattern (LBP) is a method used to extract statistical features from and grey-scale* image.
It was first introduced by 

> Ojala et al., “A comparative study of texture 
measures with classification based on feature distributions”. Pattern 
Recognition. 29(1), 51–59 (1996) 

It transforms the image into a histogram which describes the frequency of occurence of local patterns. 


*It has been extended to color/multi channel images.



# Dataset

>Dengxin Dai, Hayko Riemenschneider, and Luc Van Gool.. The Synthesizability of Texture Examples. In CVPR 2014.


# Run the code

To download the data type the following commands in the console:

    cd data

    #eth data
    wget http://data.vision.ee.ethz.ch/daid/Synthesizability/ETH_Synthesizability.zip
    unzip ETH_Synthesizability.zip 
    
    #brodatz
    wget https://sipi.usc.edu/database/textures.zip
    unzip textures.zip

Install the dependencies by running:

    pip install requirements.txt

