from scene import Scene
from model_loaders.model_loader import load_models

if __name__ == '__main__':

    # Initialises the scene object.
    scene = Scene(width=1280, height=720)

    # Create day and night skyboxes.
    scene.add_skyboxes()

    # load all 3D models in the scene.
    scene.add_models(load_models(scene.ctx))

    # Load the scene's local lighting.
    scene.add_lighting()

    # Prints the user's input controls for navigating and exiting the scene.
    scene.display_controls()

    # Start drawing the scene.
    scene.run()
