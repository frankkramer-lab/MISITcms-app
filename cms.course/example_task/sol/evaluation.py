#-----------------------------------------------------#
#                  Evaluation methods                 #
#-----------------------------------------------------#
def confusion_matrix(pred, truth):
    # Transform panda dataframe to numpy arra
    truth = truth.values
    # Count classes
    tp = fp = fn = tn = 0
    for i in range(0, len(pred)):
        if pred[i] == 1 and truth[i] == 1:
            tp += 1
        elif pred[i] == 1 and truth[i] == 0:
            fp += 1
        elif pred[i] == 0 and truth[i] == 1:
            fn += 1
        elif pred[i] == 0 and truth[i] == 0:
            tn += 1
    # Return confusion matrix
    return tp, fp, fn, tn

def compute_scores(con_mat):
    tp, fp, fn, tn = con_mat
    # Calculate scores
    accuracy = (tp + tn) / (tp + fp + fn + tn)
    f1 = 2*tp / (2*tp + fp + fn)
    precision = tp / (tp + fp)
    sensitivity = tp / (tp + fn)
    specificity = tn / (tn + fp)
    # Return scores
    return accuracy, f1, precision, sensitivity, specificity
