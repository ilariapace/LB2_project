# LB2_sspred_project

This project had the main intention of compare two machine learning methods as prediction method for the JPred4 protein family. First, a statistic analysis is performed to count the SS present in the used datasets (the JPred4 training set and the blindset). Then, the GOR approach is implemented, in first place the training phase and then the prediction set. The SVM was launched by libsvm, using the inputs from the DSSP and FASTA files originated through the svm_input.py script. Some evaluation metrics are implemented to compare the two approaches and decide which is the most efficient one, such as accuracy, TPR, SOV evaluation indexes.

### Content of the folder
#### LB2_sspred/
* __Script/__ 

    Python codes used 
* __Supplementary Materials/__
    
    Plots about traning and blind test sets
    * Blindset/
    * Training/ 
