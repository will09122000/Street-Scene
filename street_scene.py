from scene import Scene
from model_loaders.model_loader import load_models

if __name__ == '__main__':

    # initialises the scene object
    print('Initialising Scene')
    scene = Scene(width=1280, height=720)

    # load here the 3d meshes
    print('Loading Models')
    scene.add_models(load_models(scene.ctx))

    # Load the scene's lighting.
    print('Adding Lighting')
    scene.add_lighting()

    # starts drawing the scene
    scene.run()
