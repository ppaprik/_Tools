import os
import sys
import subprocess
import traceback


#================================================================================
# Class for environment manager (Creation and installation of requirements)
class EnvMain:
    def __init__(self, _env_folder_path: str = ".", _requirements_and_installed_file_path: str = ".", _env_name: str = ".env") -> None:
        """
            By Default the env will be created in the directory from where the script is executed,
            and the requirements.txt and installed.txt files will be created in the directory where script is located

            :env_folder_path: path to the folder where the environment is located
            if env_folder_path is None, the current directory from where the script is executed will be used

            :requirements_file_and_installed_file_path: path to the requirements.txt and installed.txt files
            if requirements_file_and_installed_file_path is None, the current directory from where the script is executed will be used
        """
        self.env_name = _env_name

        # Set path for [env_folder_path]
        if _env_folder_path == ".":
            self.env_folder_path: str = self.env_name
        else:
            self.env_folder_path: str = os.path.join(_env_folder_path, self.env_name)

        # Set path for [requirements_file_and_installed_file_path]
        if _requirements_and_installed_file_path == ".":
            self.requirements_and_installed_file_path: str = os.path.dirname(__file__)
        else:
            self.requirements_and_installed_file_path: str = _requirements_and_installed_file_path

        self.requirements_file = os.path.join(self.requirements_and_installed_file_path, "requirements.txt")
        self.installed_file = os.path.join(self.requirements_and_installed_file_path, "installed.txt")


    def run(self):
        self.createEnv()
        self.createRequirementsFile()
        self.createInstalledFile()
        self.upgradePip()
        self.installRequirements()

        # print(self.getEnvPythonPath())


    def createEnv(self) -> None:
        if os.path.exists(self.env_folder_path):
            print("<< Environment already exists")
        else:
            print("<< Creating environment...")
            try:
                subprocess.run([sys.executable, "-m", "venv", self.env_folder_path], check=True)
                print("<< Success: Environment created")
            except subprocess.CalledProcessError as error:
                print(f"<< Failed: to create virtual environment. Error: {error}")
                traceback.print_exc()

    
    def upgradePip(self) -> None:
        print("<< Upgrading pip...")
        try:
            subprocess.run([self.getEnvPythonPath(), "-m", "pip", "install", "--upgrade", "pip"], check=True)
            print("<< Success: Pip upgraded")
        except subprocess.CalledProcessError as error:
            print(f"<< Failed: to upgrade pip. Error: {error}")
            traceback.print_exc()


    def installRequirements(self) -> None:
        print("<< Installing requirements...")
        try:
            subprocess.run([self.getEnvPythonPath(), "-m", "pip", "install", "-r", self.requirements_file], check=True)
            print("<< Success: Requirements installed")
            self.setStateOfInstalledFile(1)
        except subprocess.CalledProcessError as error:
            print(f"<< Failed: to install requirements. Error: {error}")
            traceback.print_exc()
            sys.exit(1)
    

    #==================================================
    # Creators
    def createRequirementsFile(self) -> None:
        if os.path.exists(self.requirements_file):
            print("<< Requirements file already exists")
        else:
            print("<< Creating requirements file...")
            try:
                with open(self.requirements_file, "w") as file:
                    file.write("")
                print("<< Success: Requirements file created")
            except Exception as error:
                print(f"<< Failed: to create requirements file. Error: {error}")
            traceback.print_exc()


    def createInstalledFile(self) -> None:
        if os.path.exists(self.installed_file):
            print("<< Installed file already exists")
        else:
            print("<< Creating installed file...")
            try:
                with open(self.installed_file, "w") as file:
                    file.write("0")
                print("<< Success: Installed file created")
            except Exception as error:
                print(f"<< Failed: to create installed file. Error: {error}")
                traceback.print_exc()
    

    #==================================================
    # Getters
    def getEnvPythonPath(self) -> str:
        if os.name == "nt":
            return os.path.join(self.env_folder_path, "Scripts", "python.exe")
        else:
            return os.path.join(self.env_folder_path, "bin", "python")
    

    #==================================================
    # Setters
    def setStateOfInstalledFile(self, _state: int) -> None:
        try:
            with open(self.installed_file, "w") as file:
                file.write(str(_state))
            print("<< Success: State of installed file changed")
        except Exception as error:
            print(f"<< Failed: to change state of installed file. Error: {error}")
            traceback.print_exc()


#================================================================================
# Start
if __name__ == "__main__":
    env_main = EnvMain()
    env_main.run()