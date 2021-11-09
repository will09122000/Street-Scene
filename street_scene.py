from scene import Scene
from model_loader import load_models
import moderngl

if __name__ == '__main__':

    # initialises the scene object
    scene = Scene()

    # load here the 3d meshes
    scene.add_models(load_models(scene.ctx))

    scene.add_lighting()

    # starts drawing the scene
    scene.run()
