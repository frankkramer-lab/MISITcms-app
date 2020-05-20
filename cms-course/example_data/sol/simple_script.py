import argparse
import csv

# Implement an Argument Parser
parser = argparse.ArgumentParser()
# Add arguments to the Argument Parser
parser.add_argument("-i", "--input", action="store", dest="input", type=str)
parser.add_argument("--modus", action="store", dest="modus", type=str)

# Parse arguments
args = parser.parse_args()

# Do some stuff
if args.modus == "txt":
    with open(args.input, "r") as txt_reader:
        output = txt_reader.read()
elif args.modus == "csv":
    with open(args.input) as csv_reader:
        spamreader = csv.reader(csv_reader)
        output = ""
        for row in spamreader:
            output += " ".join(row) + "\n"
else:
    output = ":O"

# Output to sys.out
print(output.rstrip())
