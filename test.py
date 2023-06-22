import numpy as np
import mayavi.mlab as mlab

# Fake data from:
# http://docs.enthought.com/mayavi/mayavi/auto/mlab_helper_functions.html#points3d
t = np.linspace(0, 2 * np.pi, 200000)

x = np.sin(2 * t)
y = np.cos(t)
z = np.cos(2 * t)

# Create a [0..len(t)) index that we'll pass as 's'
s = np.arange(len(t))

# Create and populate lookup table (the integer index in s corresponding
#   to the point will be used as the row in the lookup table
lut = np.zeros((len(s), 4))

# A simple lookup table that transitions from red (at index 0) to
#   blue (at index len(data)-1)
for row in s:
    f = (row/len(s))
    lut[row,:] = [255*(1-f),0,255*f,255]

# Plot the points, update its lookup table
p3d = mlab.points3d(x, y, z, s, scale_mode='none')
p3d.module_manager.scalar_lut_manager.lut.number_of_colors = len(s)
p3d.module_manager.scalar_lut_manager.lut.table = lut

mlab.draw()
mlab.show()