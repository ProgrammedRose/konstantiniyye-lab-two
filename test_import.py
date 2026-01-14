# test_import.py в корне проекта
import sys
sys.path.insert(0, 'src')

try:
    from app.infrastructure.db.base import Base
    print("Import successful!")
except ImportError as e:
    print(f"Import failed: {e}")