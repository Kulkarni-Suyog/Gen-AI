
import sys
from pathlib import Path

# Get the main GSTSaral project directory
BASE_DIR = Path(__file__).resolve().parent.parent

# Add project root to Python path
sys.path.insert(0, str(BASE_DIR))

from app.vectorstore import build_vectorstore


if __name__ == "__main__":

    print("===== GSTSARAL VECTOR DATABASE =====")

    build_vectorstore()

    print("Vector database created successfully!")
