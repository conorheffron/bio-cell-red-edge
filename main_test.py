import main
import pytest
import sys


@pytest.mark.parametrize("files", ["original image cropped.png", None])
def test_main(decimals):
  try:
    sys.argv = files
    main = main()
    repr(main)
  except Exception as e:
    pytest.fail(f"An error occurred: {e}")
