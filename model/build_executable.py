"""Build executable for inference CLI.

Usage:
  pyinstaller --onefile --name sign_infer model/build_executable.py
"""

from model_pipeline.cli import main

if __name__ == "__main__":
    main()
