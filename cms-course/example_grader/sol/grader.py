# Import a function from the submission script
import my_script

# Read data from file
with open("input.txt", "r") as rs:
    text = rs.read() # read text string from file including newline at the end

# Run my_function() from the submission script
result = my_script.my_function(text)

# Print out the result
print(result)
