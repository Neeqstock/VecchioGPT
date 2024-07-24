import os
import platform


def set_environment_variable(variable_name, variable_value):
    # Determine the platform (Linux or Windows)
    current_platform = platform.system()

    try:
        # Set the environment variable based on the platform
        if current_platform == "Linux":
            os.environ[variable_name] = variable_value
            print(f"Environment variable {variable_name} set successfully.")
        elif current_platform == "Windows":
            os.system(f'setx {variable_name} "{variable_value}"')
            print(f"Environment variable {variable_name} set successfully.")
        else:
            print("Unsupported platform. Environment variable not set.")
    except Exception as e:
        print(f"Error setting environment variable: {e}")


# if __name__ == "__main__":
#     variable_value = input(f"Enter the value for {variable_name}: ")

#     set_environment_variable("VECCHIOGPT_KEY", variable_value)
