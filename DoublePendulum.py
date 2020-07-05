from scipy.integrate import solve_ivp
import matplotlib.pyplot as plt
import numpy as np


class DoublePendulum(object):
    """
    system_arg为系统参数，需传递一个array_like的对象，该对象的第一个值为l1的的长度，第二个
    参数为l2的长度，第三个值为小球m1的质量，第四个值为小球m2的质量

    init为系统初始值，需要传递一个array_like的对象，该对象的第一个值为l1与竖直方向的夹角，
    第二个值为l2与竖直方向的夹角，第三个值为l1的角速度，第四个值为l2的角速度

    第三个参数为求解的时间范围
    """
    def __init__(self, system_arg, init, t_span):
    	# 动画的总帧数
        total_frame = 500
        self.l1 = system_arg[0]
        self.l2 = system_arg[1]
        self.m1 = system_arg[2]
        self.m2 = system_arg[3]
        self.init_theta = init[0]
        self.init_psi = init[1]
        self.init_theta_1 = init[2]
        self.init_psi_1 = init[3]
        self.t_span = t_span
        self.t_eval = np.linspace(t_span[0], t_span[1], total_frame)

    def get_coefficient(self, theta, psi, theta_1, psi_1):
        g = 9.8
        a11 = (self.m1+self.m2) * self.l1
        a12 = self.m2 * self.l2 * np.cos(psi-theta)
        b1 = -self.m2 * self.l2 * np.sin(theta-psi) * psi_1**2 - (self.m1+self.m2) * g * np.sin(theta)
        a21 = self.l1 * np.cos(psi - theta)
        a22 = self.l2
        b2 = -self.l1 * np.sin(psi - theta) * theta_1**2 - g * np.sin(psi)
        matrix_A = ((a11, a12), (a21, a22))
        array_b = (b1, b2)
        coefficient = np.linalg.solve(matrix_A, array_b)
        return coefficient

    def func(self, t, y):
        theta = y[0]
        psi = y[1]
        theta_1 = y[2]
        psi_1 = y[3]
        theta_2, psi_2 = self.get_coefficient(theta, psi, theta_1, psi_1)
        return [theta_1, psi_1, theta_2, psi_2]

    def solve_ode(self):
        init = (self.init_theta, self.init_psi, self.init_theta_1, self.init_psi_1)
        sol = solve_ivp(self.func, self.t_span, init, t_eval=self.t_eval)
        return sol

    # 展示双摆运动的动画。若需显示小球轨迹，is_track=True，若不显示，则is_track=False
    def show(self, is_track=False):
        track_x = list()
        track_y = list()
        sol = self.solve_ode()
        for (theta, psi) in zip(sol.y[0], sol.y[1]):
            x1 = self.l1 * np.sin(theta)
            y1 = -self.l1 * np.cos(theta)
            x2 = self.l1 * np.sin(theta) + self.l2 * np.sin(psi)
            y2 = -self.l1 * np.cos(theta) - self.l2 * np.cos(psi)
            plt.scatter(x1, y1)
            plt.plot((0, x1), (0, y1))
            plt.scatter(x2, y2)
            plt.plot((x1, x2), (y1, y2))
            track_x.append(x2)
            track_y.append(y2)
            if is_track is True:
                plt.plot(track_x, track_y)
            plt.xlim(-(self.l1 + self.l2), +(self.l1 + self.l2))
            plt.ylim(-(self.l1 + self.l2), +(self.l1 + self.l2))
            # 每一帧停留的时间
            plt.pause(0.001)
            plt.draw()
            plt.clf()

system1 = DoublePendulum((10.000, 7, 10, 10), (1, 0, 1, 0), [0, 50])
system2 = DoublePendulum((10.001, 7, 10, 10), (1, 0, 1, 0), [0, 50])
sol1 = system1.solve_ode()
sol2 = system2.solve_ode()
plt.plot(sol1.t, sol1.y[0])
plt.plot(sol2.t, sol2.y[0])
plt.show()