from dotenv import load_dotenv
import os


load_dotenv()

def get_env_variable(name: str) -> str:
    env_variable: str = os.environ.get(name)
    if not env_variable:
        raise KeyError("[ERROR] Attribute {} not found".format(name))

    return env_variable
