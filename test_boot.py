import sys
try:
    from app.main import app
    print("Successfully imported app.main.app")
    sys.exit(0)
except Exception as e:
    import traceback
    traceback.print_exc()
    sys.exit(1)
