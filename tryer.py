import subprocess

# Define the command as a list of strings
command = ["kitty", "+kitten", "icat", "./output.gif"]

# Execute the command
result = subprocess.run(command, capture_output=True, text=True)

# Check the result
if result.returncode == 0:
    print("Command executed successfully.")
    # Optionally, print the output if needed
    print(result.stdout)
else:
    print(f"Command failed with return code {result.returncode}.")
    # Optionally, print the error message
    print(result.stderr)
