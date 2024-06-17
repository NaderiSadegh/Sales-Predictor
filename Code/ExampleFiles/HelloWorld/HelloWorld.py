## @mainpage Hello World Example
#
# @section author Author:
#
# Sadegh Naderi
#
#
# @section intro_sec Introduction
#
# This is an example of a simple Hello World syntax created for explaining how to create a simple virtual environment.
#
# refer to the chapter Environment in the report for more info
#
# @section manual Example manual: Creation and Use of Conda Environments
#
# 1. Create a Conda environment using Anaconda Prompt on your system:
# @code
# conda create --name hello_env python=3.9
# @endcode
# When asked "Proceed ([y]/n)?", press 'y'.
# This command creates a new Conda environment named "hello_env" and specifies Python version 3.9.
#
# 2. Activate the Conda environment:
# @code
# conda activate hello_env
# @endcode
# This command activates the "hello_env" environment, indicating that we want to use this environment for our Python code.
#
# 3. Create a Python file named HelloWorld.py and open it in a text editor. Add the following code:
# @code
# def say_hello():
#
#     print("Hello, World!")
#
# def main():
#
#     say_hello()
#
# # Call the main function to start the program
# if __name__ == "__main__":
#     main()
# @endcode
# This code defines a function say_hello() that prints the "Hello, World!" message to the console.
#
# 4. Save the HelloWorld.py file and close the text editor.
#
# 5. If needed, navigate to the directory where your Python file is located using the cd command. Execute the Python code:
# @code
# python HelloWorld.py
# @endcode
# This command runs the HelloWorld.py script using the Python interpreter in the activated Conda environment.
# You should see the output "Hello, World!" printed to the console, indicating that the code executed successfully.
#
# 6. Deactivate the Conda environment:
# @code
# conda deactivate
# @endcode
# This command deactivates the current Conda environment.
# The Anaconda Prompt should look like Figure 1.
#
# By following these steps, you've created a Conda environment, activated it, written a simple "Hello World" Python code, and executed it within the Conda environment. Conda allows you to manage different environments for different projects, providing isolation and dependency management for your Python applications.

## @file say_hello.py
#  @brief A simple "Hello World" program in Python.
#
#  This program prints the message "Hello, World!" to the console.

def say_hello():
    """! Prints the message "Hello, World!" to the console.
    @brief Processes This function prints the message "Hello, World!" to the console.
    It does not accept any arguments or return any value.
    @return None
    @see say_hello()
    """

    print("Hello, World!")

def main():
    """! The main function of the program.
    @brief Processes This function is the entry point of the program. It calls the say_hello() function to print the
    "Hello, World!" message.
    @return None
    @see say_hello()
    """
    say_hello()

# Call the main function to start the program
if __name__ == "__main__":
    main()