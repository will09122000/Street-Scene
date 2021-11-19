
def compile_shaders(ctx):
    """
    Compiles shaders into a dictionary.
    """
    print('Compiling Shaders')

    shaders = {}

    shaders.clear()

    shaders['BaseModel'] = ctx.program(vertex_shader = open('shaders/BaseModelVertex.glsl').read(),
                                        fragment_shader = open('shaders/BaseModelFragment.glsl').read())

    shaders['LightModel'] = ctx.program(vertex_shader = open('shaders/LightModelVertex.glsl').read(),
                                         fragment_shader = open('shaders/LightModelFragment.glsl').read())

    shaders['Skybox'] = ctx.program(vertex_shader = open('shaders/SkyboxVertex.glsl').read(),
                                     fragment_shader = open('shaders/SkyboxFragment.glsl').read())

    shaders['EnviroMapModel'] = ctx.program(vertex_shader = open('shaders/EnviroMapVertex.glsl').read(),
                                             fragment_shader = open('shaders/EnviroMapFragment.glsl').read())
