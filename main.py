import numpy as np
import matplotlib.pyplot as plt
from scipy import interpolate

x = np.linspace(-20,20,50)

y = 2+2*x+2*x**2

maxy = 0.4*np.max(y)
print(maxy)

plt.plot(y,x)


aids = interpolate.interp1d(y,x,'quadratic')

k = aids.__call__(653)

print(k)

plt.show()
