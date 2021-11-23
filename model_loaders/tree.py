from object_reader import read_obj, load_obj

def load_trees(ctx):
    """Load tree objects that are placed on the pavement."""

    trees = []
    x_spacer = 3.75
    y_spacer = 8

    tree_obj = read_obj('assets/models/tree.obj')

    for i in range(0, 2):
        for j in range(-20, 28, y_spacer):
            # Prevent trees being placed too near the cross roads.
            if j < -8 or j > 8:
                left = True
                for _ in range(0, 2):
                    # Decides which road the trees are being placed on.
                    if i > 0:
                        position = [-x_spacer if left else x_spacer, 0, j]
                    else:
                        position = [j, 0, -x_spacer if left else x_spacer]

                    tree = load_obj(ctx              = ctx,
                                    obj_file         = tree_obj,
                                    texture_filepath = 'assets/textures/tree.png',
                                    position         = (position))

                    trees.append(tree)
                    left = not left

    return trees
