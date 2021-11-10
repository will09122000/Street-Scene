from scene import Scene
from model_loader import load_models
import moderngl

if __name__ == '__main__':

    # initialises the scene object
    print('Initialising Scene')
    scene = Scene(width=1920, height=1080)

    # load here the 3d meshes
    print('Loading Models')
    scene.add_models(load_models(scene.ctx))

    print('Adding Lighting')
    scene.add_lighting()

    # starts drawing the scene
    scene.run()
