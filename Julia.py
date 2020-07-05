import numpy as np
import matplotlib.pyplot as plt

times = 200
step = 2000
julia = np.ones((step, step))

x = np.linspace(-2, 2, step)
y = np.linspace(-2, 2, step)

def func(z):
	constant = -0.8 + 0.156j
	return z**2 + constant

for i in range(len(x)):
	for j in range(len(y)):
		temp = complex(x[i], y[j])
		for n in range(times):
			if abs(temp) > 2:
				julia[i,j] = -1
				break;
			temp = func(temp)

plt.imshow(julia)
plt.show()