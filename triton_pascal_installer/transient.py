import os
import shutil
import tempfile
import wheel.wheelfile

def create_transient_package(name, version, tag, output):
  """
    Create a transient wheel package.

    Parameters
    ----------
    name    : str
              The name of the package.
    version : str
              The version of the package.
    tag     : str
              The wheel tag (e.g., "py3-none-any").
    output  : str
              The output path for the wheel file.
  """

  with tempfile.TemporaryDirectory() as directory:
    # Define source directory path
    input = os.path.join(directory, "src")

    # Define the path for the wheel file to be created
    wheel_file = os.path.join(directory, f"{name}-{version}-{tag}.whl")

    # Create the .dist-info directory
    dist_info = os.path.join(input, f"{name}-{version}.dist-info")
    os.makedirs(dist_info)

    # Write the METADATA file
    with open(os.path.join(dist_info, "METADATA"), "w") as file:
      file.write("Metadata-Version: 2.1\n")
      file.write(f"Name: {name}\n")
      file.write(f"Version: {version}\n")
      file.write(f"Requires-Dist: {name}-pascal\n")
      file.write("\n")

    # Write the top_level.txt file
    with open(os.path.join(dist_info, "top_level.txt"), "w") as file:
      file.write("\n")

    # Write the WHEEL file
    with open(os.path.join(dist_info, "WHEEL"), "w") as file:
      file.write("Wheel-Version: 1.0\n")
      file.write("Generator: setuptools (72.1.0)\n")
      file.write("Root-Is-Purelib: true\n")
      file.write(f"Tag: {tag}\n")
      file.write("\n")

    # Create the wheel file
    with wheel.wheelfile.WheelFile(wheel_file, "w") as wf:
      wf.write_files(input)

    # Copy the created wheel file to the specified output
    shutil.copy(wheel_file, output)
