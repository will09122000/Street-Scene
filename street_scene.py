from scene import Scene
from model_loaders.model_loader import load_models

if __name__ == '__main__':

    # initialises the scene object
    scene = Scene(width=1280, height=720)

    # Create day and night skyboxes
    scene.add_skyboxes()

    # load here the 3d meshes
    scene.add_models(load_models(scene.ctx))

    # Load the scene's lighting.
    scene.add_lighting()

    # starts drawing the scene
    scene.run()
