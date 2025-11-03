import pytest
import subprocess

def test_main():
  try:
    subprocess.run(["python", "main.py", "original image cropped.png"])
  except Exception as e:
    pytest.fail(f"An error occurred: {e}")
