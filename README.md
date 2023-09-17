# Solar System Animation

This project provides an OpenGL-based 3D animation of the Solar System. The animation includes rotating planets and a variety of celestial features. It uses the Python programming language, along with several libraries to achieve its goals.

# OpenGL and PIL code
# Functionality for drawing a solar system simulation.
# Includes code for drawing the sun, mercury, venus, earth, mars, jupiter, saturn, and uranus.
# Uses texture mapping for each planet and stars.
# Allows toggling of lighting with the 'l' key.
# Utilizes GLUT for the rendering loop and keyboard inputs.
# Manages OpenGL textures and handles different light sources.
# Uses GLU for quadrics and GL functions for 3D transformations and shading.
# Assumes the images are available in the current directory for texture mapping.

## Table of Contents

- [Installation](#installation)
- [Dependencies](#dependencies)
- [Usage](#usage)
- [How to Run](#how-to-run)
- [Contributing](#contributing)
- [License](#license)

## Installation

To install the project, you can clone it using Git:

```bash
git clone https://github.com/your-username/your-solar-system-repo.git
```

## Dependencies

This project uses several Python libraries which must be installed beforehand. You can install them via pip:

```bash
pip install PyOpenGL
pip install pillow
```

Or using the `requirements.txt` file (if available):

```bash
pip install -r requirements.txt
```

## Usage

Once installed, navigate to the project directory and run the main Python file to start the animation.

## How to Run

Open your terminal, navigate to the directory where the code resides and run the following command:

```bash
python main.py
```

### Keyboard Controls

- `l`: Toggle lighting on/off

## Contributing

If you would like to contribute to this project, please fork the repository, create a new branch, and submit a pull request.

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details.
