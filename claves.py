from dotenv import load_dotenv
import os
load_dotenv()
print("El administrador es:" ,os.getenv("administrador"))