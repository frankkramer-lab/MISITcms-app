# Import a function from the submission script
import my_script1
import my_script2

# Read data from file
with open("input.txt", "r") as rs:
    text = rs.read() # read text string from file including newline at the end

# Run my_function() from the submission script
text = my_script1.my_function(text)
text = my_script2.my_function(text)

# Print out the result
print(text)
