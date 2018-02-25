The classifying system has been developed in Matlab. 
A Matlab library is provided with the following modules:

- extract_features.m is the Matlab function that obtains the ENF and then the discriminative features of the signal given as input.

- obtain_X_Y.m and obtain_Xtest.m are the functions that load the training or the practice/testing files,
 respectively, and call extract_features.m to build the data matrices and label vectors.

- predict_test.m is the function that builds a classifier from a training dataset and performs classification on a test set.

- get_file_prediction.m is the function that combines per-segment predictions to obtain per-file estimations.

- crossValidation.m partitions the data into disjoint training and validation sets to obtain an estimation of the classification error. 
It is used for model and feature selection.

- main.m is the executable script that calls the previous function in order to read data from the files, 
get cross-validation estimations, and apply the classification models to the practice and testing datasets. 
The execution of the different parts can be enabled and disabled through flags located at the beginning of the file.

-------------------------------------------------------------------------------------------------------------------
EXECUTION OF THE CODE
-------------------------------------------------------------------------------------------------------------------

In order to be able to reproduce the results of the classifying system the next steps have to be followed:

1- Copy the Training, Practice and Test folders into this folder "Code". The Matlab code assumes that the input files 
are located in the same folder as the code. For the training samples, all grid folders A-I must be inside the same folder " "

2- Execute the file "main.m" inside this folder. It contains 6 flags used to control the reading of the input files, the 
execution of the crossvalidation and the obtaining of the output of the Practice and Test sets. These flags are initially set to 1,
which means all the operations described above will be performed and 2 files will be created as output:

• output_test.txt: File containing the predictions for the test set
• output_practice.txt: File containing the predictions for the practice test.






