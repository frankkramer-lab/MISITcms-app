#-----------------------------------------------------#
#                   Library imports                   #
#-----------------------------------------------------#
# Import external libraries
import argparse
# Import student libraries
from data_processing import read_dataset, exploration, preprocessing, split_dataset
from algorithms import *
from evaluation import confusion_matrix, compute_scores

#-----------------------------------------------------#
#                      Argparser                      #
#-----------------------------------------------------#
# Implement Argument Parser
parser = argparse.ArgumentParser(description="Autism Spectrum Disorder (ASD) classification")
# Add arguments to the Argument Parser
parser.add_argument("-i", "--input", action="store", dest="input",
                    type=str, required=True,
                    help="Path to the Autism_Screening.Data.csv file.")
parser.add_argument("-a", "--algorithm", action="store", dest="algorithm",
                    type=str, default="lr",
                    help="Option which classification algorithm is used.\
                    Possible algorithm: [explore, lr, nb, knn, svm, rf, compare]")
# Parse arguments
args = parser.parse_args()

#-----------------------------------------------------#
#                 Data Set Exploration                #
#-----------------------------------------------------#
if args.algorithm == "explore":
	# Load data set from file
	data_set = read_dataset(args.input)
	# Run Data Set Exploration
	exploration(data_set)

#-----------------------------------------------------#
#               Classification Pipeline               #
#-----------------------------------------------------#
elif args.algorithm in ["lr", "nb", "knn", "svm", "rf"]:
	# Load data set from file
	data_set = read_dataset(args.input)

    # Preprocess data set
	cat_var_list = ["Age_Range", "Ethnicity", "Residence", "Entry_Person"]
	bol_var_list = ["ASD", "Gender", "Test_Jundice", "Test_Family_PDD", "Used_App_Before"]
	num_var_list = ["Age"]
	data_set_preprocessed = preprocessing(data_set,
                                          categorical_variables=cat_var_list,
                                          binary_variables=bol_var_list,
                                          numeric_variables=num_var_list)

    # Split data set into train and test data sets
	train_x, test_x, train_y, test_y = split_dataset(data_set_preprocessed,
                                                     y_var="ASD",
                                                     test_size=0.2)

    # Initialize algorithm
	model = None
	if args.algorithm == "lr":
		model = Logistic_Regression()
	elif args.algorithm == "nb":
		model = Naive_Bayes()
	elif args.algorithm == "knn":
		model = k_Nearest_Neighbors()
	elif args.algorithm == "svm":
		model = Support_Vector_Machine()
	elif args.algorithm == "rf":
		model = Random_Forest()

    # Train model
	model.train(train_x, train_y)

    # Predict the testing data with the
	pred = model.predict(test_x)

    # Evaluate results
	confusion_mat = confusion_matrix(pred, test_y)
	scores = compute_scores(confusion_mat)
	accuracy, f1, precision, sensitivity, specificity = scores

    # Output results
	print("Algorithm: " + args.algorithm)
	print("Accuracy: " + str(accuracy))
	print("F1: " + str(f1))
	print("Precision: " + str(precision))
	print("Sensitivity: " + str(sensitivity))
	print("Specificity: " + str(specificity))

#-----------------------------------------------------#
#                 Comparison Pipeline                 #
#-----------------------------------------------------#
elif args.algorithm == "compare":
	# Load data set from file
	data_set = read_dataset(args.input)

    # Preprocess data set
	cat_var_list = ["Age_Range", "Ethnicity", "Residence", "Entry_Person"]
	bol_var_list = ["ASD", "Gender", "Test_Jundice", "Test_Family_PDD", "Used_App_Before"]
	num_var_list = ["Age"]
	data_set_preprocessed = preprocessing(data_set,
                                          categorical_variables=cat_var_list,
                                          binary_variables=bol_var_list,
                                          numeric_variables=num_var_list)

    # Split data set into train and test data sets
	train_x, test_x, train_y, test_y = split_dataset(data_set_preprocessed,
                                                     y_var="ASD",
                                                     test_size=0.2)

    # Run each algorithm and calculate the accuracy
	algorithms = ["lr", "nb", "knn", "svm", "rf"]
	for alg in algorithms:
		# Create model
		model = None
		if alg == "lr":
			model = Logistic_Regression()
		elif alg == "nb":
			model = Naive_Bayes()
		elif alg == "knn":
			model = k_Nearest_Neighbors()
		elif alg == "svm":
			model = Support_Vector_Machine()
		elif alg == "rf":
			model = Random_Forest()
		# Train model
		model.train(train_x, train_y)
		# Predict the testing data with the
		pred = model.predict(test_x)
        # Evaluate results
		confusion_mat = confusion_matrix(pred, test_y)
		scores = compute_scores(confusion_mat)
		accuracy, f1, precision, sensitivity, specificity = scores
        # Print out result
		print(alg + ": " + str(accuracy))
