import os

os.environ["DDEBACKEND"] = "tensorflow.compat.v1"  # pytorch tensorflow.compat.v1
import deepxde as dde
import matplotlib.pyplot as plt
import numpy as np
from scipy import io
import time

start_time = time.time()

# dde.config.set_default_float("float64")
stride = 5
elevation = 20
azimuth = -40
dpi = 130

z_lower = -5
z_upper = 5
t_lower = -5
t_upper = 5

# dde.config.set_default_float("float64")
nx = 512
nt = 512
# Creation of the 2D domain (for plotting and input)
x = np.linspace(z_lower, z_upper, nx)[:, None]
t = np.linspace(t_lower, t_upper, nt)[:, None]
X, T = np.meshgrid(x, t)
I = 1j
EExact = (
    -(12 + 16 * I) * np.exp((3 - I / 2) * T + 3 - (1513 / 377 + 73 * I / 116) * X)
    + (-12 + 16 * I) * np.exp((3 + I / 2) * T + 3 - (503 / 377 + 57 * I / 52) * X)
    + 400 * np.exp((1 + I / 2) * T - (29 / 13 + 57 * I / 52) * X + 1)
    + 400 * np.exp((1 - I / 2) * T + (13 / 29 - 73 * I / 116) * X + 1)
) / (
    (48 + 64 * I) * np.exp((2 - I) * T + 2 + (-672 / 377 + 176 * I / 377) * X)
    + (48 - 64 * I) * np.exp((2 + I) * T + 2 - (672 / 377 + 176 * I / 377) * X)
    + 100 * np.exp(2 * T - (58 * X) / 13 + 2)
    + 100 * np.exp(2 * T + (26 * X) / 29 + 2)
    + np.exp(4 * T - (1344 * X) / 377 + 4)
    + 400
)
pExact = (
    16
    * (
        42688 * I * np.exp((2 - I) * T + 2 + (-672 / 377 + 176 * I / 377) * X)
        + 832 * I * np.exp((2 + I) * T + 2 - (672 / 377 + 176 * I / 377) * X)
        + 352 * I * np.exp(4 * T - (1344 * X) / 377 + 4)
        + 26000 * I * np.exp(2 * T + (26 * X) / 29 + 2)
        + 34800 * I * np.exp(2 * T - (58 * X) / 13 + 2)
        - 14384 * np.exp((2 - I) * T + 2 + (-672 / 377 + 176 * I / 377) * X)
        + 20176 * np.exp((2 + I) * T + 2 - (672 / 377 + 176 * I / 377) * X)
        - 135 * np.exp(4 * T - (1344 * X) / 377 + 4)
        + 27300 * np.exp(2 * T + (26 * X) / 29 + 2)
        + 14500 * np.exp(2 * T - (58 * X) / 13 + 2)
        + 150800
    )
    * (
        283 * I * np.exp((3 - I / 2) * T + 3 - (1513 / 377 + 73 * I / 116) * X)
        - 339 * I * np.exp((3 + I / 2) * T + 3 - (503 / 377 + 57 * I / 52) * X)
        - 8700 * I * np.exp((1 + I / 2) * T - (29 / 13 + 57 * I / 52) * X + 1)
        - 6500 * I * np.exp((1 - I / 2) * T + (13 / 29 - 73 * I / 116) * X + 1)
        + 206 * np.exp((3 - I / 2) * T + 3 - (1513 / 377 + 73 * I / 116) * X)
        + 398 * np.exp((3 + I / 2) * T + 3 - (503 / 377 + 57 * I / 52) * X)
        - 5800 * np.exp((1 + I / 2) * T - (29 / 13 + 57 * I / 52) * X + 1)
        - 2600 * np.exp((1 - I / 2) * T + (13 / 29 - 73 * I / 116) * X + 1)
    )
    / (
        142129
        * (
            64 * I * np.exp((2 - I) * T + 2 + (-672 / 377 + 176 * I / 377) * X)
            - 64 * I * np.exp((2 + I) * T + 2 - (672 / 377 + 176 * I / 377) * X)
            + 100 * np.exp(2 * T - (58 * X) / 13 + 2)
            + 48 * np.exp((2 - I) * T + 2 + (-672 / 377 + 176 * I / 377) * X)
            + 48 * np.exp((2 + I) * T + 2 - (672 / 377 + 176 * I / 377) * X)
            + 100 * np.exp(2 * T + (26 * X) / 29 + 2)
            + np.exp(4 * T - (1344 * X) / 377 + 4)
            + 400
        )
        ** 2
    )
)
etaExact = (
    (675584 + 2316288 * I)
    * np.exp((4 + 2 * I) * T + 4 - (1344 / 377 + 352 * I / 377) * X)
    - (3222400 + 6003200 * I)
    * np.exp((4 - I) * T + 4 + (-334 / 377 + 176 * I / 377) * X)
    + (9843200 + 14182400 * I)
    * np.exp((2 + I) * T + 2 - (672 / 377 + 176 * I / 377) * X)
    - (4860800 + 4774400 * I)
    * np.exp((4 - I) * T + 4 + (-2354 / 377 + 176 * I / 377) * X)
    - (40928 + 13696 * I) * np.exp((6 + I) * T + 6 - (2016 / 377 + 176 * I / 377) * X)
    + (-4860800 + 4774400 * I)
    * np.exp((4 + I) * T + 4 - (2354 / 377 + 176 * I / 377) * X)
    + (-3222400 + 6003200 * I)
    * np.exp((4 + I) * T + 4 - (334 / 377 + 176 * I / 377) * X)
    + (675584 - 2316288 * I)
    * np.exp((4 - 2 * I) * T + 4 + (-1344 / 377 + 352 * I / 377) * X)
    + (9843200 - 14182400 * I)
    * np.exp((2 - I) * T + 2 + (-672 / 377 + 176 * I / 377) * X)
    + (-40928 + 13696 * I) * np.exp((6 - I) * T + 6 + (-2016 / 377 + 176 * I / 377) * X)
    - 377 * np.exp(8 * T - (2688 * X) / 377 + 8)
    + 6960000 * np.exp(2 * T - (58 * X) / 13 + 2)
    - 13520000 * np.exp(2 * T + (26 * X) / 29 + 2)
    - 3770000 * np.exp(4 * T + (52 * X) / 29 + 4)
    - 3770000 * np.exp(4 * T - (116 * X) / 13 + 4)
    - 13844800 * np.exp(4 * T - (1344 * X) / 377 + 4)
    - 33800 * np.exp(6 * T - (3026 * X) / 377 + 6)
    + 17400 * np.exp(6 * T - (1006 * X) / 377 + 6)
    - 60320000
) / (
    377
    * (
        64 * I * np.exp((2 - I) * T + 2 + (-672 / 377 + 176 * I / 377) * X)
        - 64 * I * np.exp((2 + I) * T + 2 - (672 / 377 + 176 * I / 377) * X)
        + 100 * np.exp(2 * T - (58 * X) / 13 + 2)
        + 48 * np.exp((2 - I) * T + 2 + (-672 / 377 + 176 * I / 377) * X)
        + 48 * np.exp((2 + I) * T + 2 - (672 / 377 + 176 * I / 377) * X)
        + 100 * np.exp(2 * T + (26 * X) / 29 + 2)
        + np.exp(4 * T - (1344 * X) / 377 + 4)
        + 400
    )
    ** 2
)

# EExact = data1['q1']  # (201,256)
EExact_u = np.real(EExact)  # (201,256)
EExact_v = np.imag(EExact)
# EExact_h = np.sqrt(EExact_u ** 2 + EExact_v ** 2)

# pExact = data1['q2']  # (201,256)
pExact_u = np.real(pExact)
pExact_v = np.imag(pExact)
# pExact_h = np.sqrt(pExact_u ** 2 + pExact_v ** 2)

# etaExact = data1['q3']  # (201,256)
etaExact_u = np.real(etaExact)  # (201,256)
etaExact_v = np.imag(etaExact)
# etaExact_h = np.sqrt(etaExact_u ** 2 + etaExact_v ** 2)
# z_lower = np.min(x)
# z_upper = np.max(x)
# t_lower = np.min(t)
# t_upper = np.max(t)
# nx = x.shape[0]; nt = t.shape[0]
"""matlab要从底部看，初始（第一行）"""
idx_x = np.random.choice(nx, 200, replace=False)  # 输出数组x的行数输出为(0——256-1)，False无放回抽样
x0 = x[idx_x, :]  # 取对应列的数据,(100,1)
# 精确解，第idx_x行，第一列的数据
# Eu0 = EExact_u[idx_x, 0:1]  # 因为t=t0，所以去取第一列
# print(np.shape(Eu0))
Eu0 = EExact_u[0:1, idx_x]  # (1,100)     写成[0, idx_x]会变成(100,)
Ev0 = EExact_v[0:1, idx_x]  # 之所以要写成0:1是因为要确保它是个矩阵
pu0 = pExact_u[0:1, idx_x]
pv0 = pExact_v[0:1, idx_x]
etau0 = etaExact_u[0:1, idx_x]
etav0 = etaExact_v[0:1, idx_x]

"""边界"""
idx_t = np.random.choice(nt, 200, replace=False)  # 从t中随机抽样50个数据
tb = t[idx_t, :]  # （50，1）
"""lower boundry是第1列（最左边一列），upper boundry是第256列（最右边一列）"""
Eu_lb = EExact_u[idx_t, 0:1]  # (100,1)     写成[idx_t, 0]会变成(100,)
Ev_lb = EExact_v[idx_t, 0:1]
pu_lb = pExact_u[idx_t, 0:1]
pv_lb = pExact_v[idx_t, 0:1]
etau_lb = etaExact_u[idx_t, 0:1]
etav_lb = etaExact_v[idx_t, 0:1]

Eu_ub = EExact_u[idx_t, nx - 1 : nx]
Ev_ub = EExact_v[idx_t, nx - 1 : nx]
pu_ub = pExact_u[idx_t, nx - 1 : nx]
pv_ub = pExact_v[idx_t, nx - 1 : nx]
etau_ub = etaExact_u[idx_t, nx - 1 : nx]
etav_ub = etaExact_v[idx_t, nx - 1 : nx]

X0 = np.concatenate((x0, 0 * x0 + t_lower), axis=1)  # (x0, 0)，axis=0竖直拼接，1水平拼接，（50，2）
X_lb = np.concatenate((0 * tb + z_lower, tb), 1)  # (lb[0], tb)
X_ub = np.concatenate((0 * tb + z_upper, tb), 1)  # (ub[0], tb)
X_u_train = np.vstack([X_lb, X0, X_ub])  # (300,2)
# print(np.shape(X_u_train))
# exit()
Eu_icbc = np.vstack([Eu_lb, Eu0.T, Eu_ub])  # (300,1)
Ev_icbc = np.vstack([Ev_lb, Ev0.T, Ev_ub])
pu_icbc = np.vstack([pu_lb, pu0.T, pu_ub])
pv_icbc = np.vstack([pv_lb, pv0.T, pv_ub])
etau_icbc = np.vstack([etau_lb, etau0.T, etau_ub])
etav_icbc = np.vstack([etav_lb, etav0.T, etav_ub])
# print(X_u_train,'\n', etau_icbc)
# exit()

# The whole domain flattened
X_star = np.hstack((X.flatten()[:, None], T.flatten()[:, None]))

# Space and time domains/geometry (for the deepxde model)
space_domain = dde.geometry.Interval(z_lower, z_upper)  # 先定义空间
time_domain = dde.geometry.TimeDomain(t_lower, t_upper)  # 再定义时间
geomtime = dde.geometry.GeometryXTime(space_domain, time_domain)  # 结合一下，变成时空区域


def pde(x, y):  # 这里x其实是x和t，y其实是u和v
    Eu = y[:, 0:1]
    Ev = y[:, 1:2]
    pu = y[:, 2:3]
    pv = y[:, 3:4]
    etau = y[:, 4:5]

    # In 'jacobian', i is the output component and j is the input component
    pu_t = dde.grad.jacobian(y, x, i=2, j=1)  # 一阶导用jacobian，二阶导用hessian
    pv_t = dde.grad.jacobian(y, x, i=3, j=1)
    etau_t = dde.grad.jacobian(y, x, i=4, j=1)

    Eu_z = dde.grad.jacobian(y, x, i=0, j=0)  # 一阶导用jacobian，二阶导用hessian
    Ev_z = dde.grad.jacobian(y, x, i=1, j=0)

    # In 'hessian', i and j are both input components. (The Hessian could be in principle something like d^2y/dxdt, d^2y/d^2x etc)
    # The output component is selected by "component"
    Eu_tt = dde.grad.hessian(y, x, component=0, i=1, j=1)
    Ev_tt = dde.grad.hessian(y, x, component=1, i=1, j=1)

    f1_u = Eu_tt + 2 * Eu * (Eu**2 + Ev**2) + 2 * pv - Ev_z
    f1_v = Ev_tt + 2 * Ev * (Eu**2 + Ev**2) - 2 * pu + Eu_z
    f2_u = 2 * Ev * etau - pv_t + 2 * pu
    f2_v = -2 * Eu * etau + pu_t + 2 * pv
    f3_u = 2 * pv * Ev + 2 * pu * Eu + etau_t

    return [f1_u, f1_v, f2_u, f2_v, f3_u]


"""这里检查一下，有可能坐标与值对应不上"""
# def gen_traindata():
#
#
#     return X_u_train, Eu_icbc, Ev_icbc, pu_icbc, pv_icbc, etau_icbc, etav_icbc
# '''精确解'''
# X_u_train, Eu_icbc, Ev_icbc, pu_icbc, pv_icbc, etau_icbc, etav_icbc = gen_traindata()

observe_y = dde.icbc.PointSetBC(X_u_train, Eu_icbc, component=0)
observe_y1 = dde.icbc.PointSetBC(X_u_train, Ev_icbc, component=1)
observe_y2 = dde.icbc.PointSetBC(X_u_train, pu_icbc, component=2)
observe_y3 = dde.icbc.PointSetBC(X_u_train, pv_icbc, component=3)
observe_y4 = dde.icbc.PointSetBC(X_u_train, etau_icbc, component=4)

data = dde.data.TimePDE(
    geomtime,
    pde,
    [
        # bc,bc1,bc2,bc3,bc4, ic,ic1,ic2,ic3,ic4,
        observe_y,
        observe_y1,
        observe_y2,
        observe_y3,
        observe_y4,
    ],
    num_domain=25000,
    # num_boundary=20,
    # num_initial=10,
    anchors=X_u_train,
    # solution=func,
    # num_test=10000,
)

net = dde.nn.FNN([2] + [128] * 6 + [5], "tanh", "Glorot normal")

model = dde.Model(data, net)

resampler = dde.callbacks.PDEPointResampler(period=5000)

model.compile(
    "adam",
    lr=0.001,
    loss="MSE",
    decay=("inverse time", 8000, 0.5),
    loss_weights=[1, 1, 1, 1, 1, 100, 100, 100, 100, 100],
)
losshistory, train_state = model.train(
    iterations=30000, display_every=100, callbacks=[resampler]
)
# dde.optimizers.config.set_LBFGS_options(
#     maxcor=50,
#     ftol=1.0 * np.finfo(float).eps,
#     gtol=1e-08,
#     maxiter=50000,
#     maxfun=50000,
#     maxls=50,
# )
model.compile(
    "L-BFGS",
    # loss_weights=[1, 1, 1, 1, 1, 1, 100, 100, 100, 100, 100, 100]
)
losshistory, train_state = model.train(
    display_every=100,
    # callbacks=[resampler]
)

# lala=X.flatten()[:, None]#(51456,1) ，改成[:]和 都会是(51456,)，flatten要变成矩阵只能是None，0:1之类的会报错

"""精确解"""
EExact_h = np.abs(EExact)  # （201，256）
Eh_true = EExact_h.flatten()  # (51456,)
pExact_h = np.abs(pExact)
ph_true = pExact_h.flatten()
etaExact_h = np.abs(etaExact)
etah_true = etaExact_h.flatten()
# Make prediction
"""预测解"""
prediction = model.predict(
    X_star, operator=None
)  # 如果 `operator` 为 `None`，则返回网络输出，否则返回 `operator` 的输出
Eu_pred = prediction[:, 0]  # (51456,)
Ev_pred = prediction[:, 1]
Eh_pred = np.sqrt(Eu_pred**2 + Ev_pred**2)
pu_pred = prediction[:, 2]
pv_pred = prediction[:, 3]
ph_pred = np.sqrt(pu_pred**2 + pv_pred**2)
etau_pred = prediction[:, 4]
etah_pred = np.abs(etau_pred)
E_L2_relative_error = dde.metrics.l2_relative_error(Eh_true, Eh_pred)
p_L2_relative_error = dde.metrics.l2_relative_error(ph_true, ph_pred)
eta_L2_relative_error = dde.metrics.l2_relative_error(etah_true, etah_pred)
print("E L2 relative error: %e" % E_L2_relative_error)
print("p L2 relative error: %e" % p_L2_relative_error)
print("eta L2 relative error: %e" % eta_L2_relative_error)
elapsed = time.time() - start_time
"""预测解"""
EH_pred = Eh_pred.reshape(nt, nx)
pH_pred = ph_pred.reshape(nt, nx)
etaH_pred = etah_pred.reshape(nt, nx)

A = t_upper - t_lower

fig101 = plt.figure("E对比图", dpi=dpi)
ax = plt.subplot(2, 1, 1)
tt = -2
index = round(
    (tt - t_lower) / A * (nt - 1)
)  # index只能是0-200（总共有201行,=0时索引第1个数,=200时索引第201）
plt.plot(x, EExact_h[index, :], "b-", linewidth=2, label="Exact")
plt.plot(x, EH_pred[index, :], "r--", linewidth=2, label="Prediction")
ax.set_ylabel("$|E(t,z)|$")
ax.set_xlabel("$z$")
plt.title("t=%s" % tt)
plt.legend()
ax = plt.subplot(2, 1, 2)
tt = 2
index = round((tt - t_lower) / A * (nt - 1))  # 只能是0-200（总共有201行）
plt.plot(x, EExact_h[index, :], "b-", linewidth=2, label="Exact")
plt.plot(x, EH_pred[index, :], "r--", linewidth=2, label="Prediction")
ax.set_ylabel("$|E(t,z)|$")
ax.set_xlabel("$z$")
plt.title("t=%s" % tt)
plt.legend()
plt.tight_layout()

fig102 = plt.figure("p对比图", dpi=dpi)
ax = plt.subplot(2, 1, 1)
tt = -2
index = round((tt - t_lower) / A * (nt - 1))  # 只能是0-200（总共有201行）
plt.plot(x, pExact_h[index, :], "b-", linewidth=2, label="Exact")
plt.plot(x, pH_pred[index, :], "r--", linewidth=2, label="Prediction")
ax.set_ylabel("$|p(t,z)|$")
ax.set_xlabel("$z$")
plt.title("t=%s" % tt)
plt.legend()
ax = plt.subplot(2, 1, 2)
tt = 2
index = round((tt - t_lower) / A * (nt - 1))  # 只能是0-200（总共有201行）
plt.plot(x, pExact_h[index, :], "b-", linewidth=2, label="Exact")
plt.plot(x, pH_pred[index, :], "r--", linewidth=2, label="Prediction")
ax.set_ylabel("$|p(t,z)|$")
ax.set_xlabel("$z$")
plt.title("t=%s" % tt)
plt.legend()
plt.tight_layout()

fig103 = plt.figure("eta对比图", dpi=dpi)
ax = plt.subplot(2, 1, 1)
tt = -2
index = round((tt - t_lower) / A * (nt - 1))  # 只能是0-200（总共有201行）
plt.plot(x, etaExact_h[index, :], "b-", linewidth=2, label="Exact")
plt.plot(x, etaH_pred[index, :], "r--", linewidth=2, label="Prediction")
ax.set_ylabel("$|\eta(t,z)|$")
ax.set_xlabel("$z$")
plt.title("t=%s" % tt)
plt.legend()
ax = plt.subplot(2, 1, 2)
tt = 2
index = round((tt - t_lower) / A * (nt - 1))  # 只能是0-200（总共有201行）
plt.plot(x, etaExact_h[index, :], "b-", linewidth=2, label="Exact")
plt.plot(x, etaH_pred[index, :], "r--", linewidth=2, label="Prediction")
ax.set_ylabel("$|\eta(t,z)|$")
ax.set_xlabel("$z$")
plt.title("t=%s" % tt)
plt.legend()
plt.tight_layout()

fig5 = plt.figure("3d预测演化图E", dpi=dpi)
ax = fig5.add_subplot(projection="3d")
surf = ax.plot_surface(
    X,
    T,
    EH_pred,
    rstride=stride,  # 指定行的跨度
    cstride=stride,  # 指定列的跨度
    cmap="Spectral",  # 设置颜色映射 还可以设置成YlGnBu_r和viridis
    linewidth=0,
    antialiased=False,
)  # 抗锯齿
# ax.grid(False)#关闭背景的网格线
ax.set_xlabel("$z$")
ax.set_ylabel("$t$")
ax.set_zlabel("$|E(t,z)|$")
# fig5.colorbar(surf, shrink=0.5, aspect=5)
ax.view_init(elevation, azimuth)
plt.tight_layout()  # 自动调整大小和间距，使各个子图标签不重叠


fig6 = plt.figure("3d预测演化图p", dpi=dpi)
ax = fig6.add_subplot(projection="3d")
surf = ax.plot_surface(
    X,
    T,
    pH_pred,
    rstride=stride,  # 指定行的跨度
    cstride=stride,  # 指定列的跨度
    cmap="Spectral",  # 设置颜色映射
    linewidth=0,
    antialiased=False,
)  # 抗锯齿
# ax.grid(False)#关闭背景的网格线
ax.set_xlabel("$z$")
ax.set_ylabel("$t$")
ax.set_zlabel("$|p(t,z)|$")
# fig6.colorbar(surf, shrink=0.5, aspect=5)
ax.view_init(elevation, azimuth)
plt.tight_layout()  # 自动调整大小和间距，使各个子图标签不重叠


fig7 = plt.figure("3d预测演化图eta", dpi=dpi)
ax = fig7.add_subplot(projection="3d")
surf = ax.plot_surface(
    X,
    T,
    etaH_pred,
    rstride=stride,  # 指定行的跨度
    cstride=stride,  # 指定列的跨度
    cmap="Spectral",  # 设置颜色映射
    linewidth=0,
    antialiased=False,
)  # 抗锯齿
# ax.grid(False)#关闭背景的网格线
ax.set_xlabel("$z$")
ax.set_ylabel("$t$")
ax.set_zlabel("$|\eta(t,z)|$")
# fig7.colorbar(surf, shrink=0.5, aspect=5)
ax.view_init(elevation, azimuth)
plt.tight_layout()  # 自动调整大小和间距，使各个子图标签不重叠

fig8 = plt.figure("3d真解E", dpi=dpi, facecolor=None, edgecolor=None)
ax = fig8.add_subplot(projection="3d")
surf = ax.plot_surface(
    X,
    T,
    EExact_h,
    rstride=stride,  # 指定行的跨度
    cstride=stride,  # 指定列的跨度
    cmap="coolwarm",  # 设置颜色映射 还可以设置成YlGnBu_r和viridis
    linewidth=0,
    antialiased=False,
)  # 抗锯齿
# ax.grid(False)#关闭背景的网格线
ax.set_xlabel("$z$")
ax.set_ylabel("$t$")
ax.set_zlabel("$|E(t,z)|$")
# fig8.colorbar(surf, shrink=0.5, aspect=5)
ax.view_init(elevation, azimuth)
plt.tight_layout()  # 自动调整大小和间距，使各个子图标签不重叠

fig9 = plt.figure("3d真解p", dpi=dpi, facecolor=None, edgecolor=None)
ax = fig9.add_subplot(projection="3d")
surf = ax.plot_surface(
    X,
    T,
    pExact_h,
    rstride=stride,  # 指定行的跨度
    cstride=stride,  # 指定列的跨度
    cmap="coolwarm",  # 设置颜色映射
    linewidth=0,
    antialiased=False,
)  # 抗锯齿
# ax.grid(False)#关闭背景的网格线
ax.set_xlabel("$z$")
ax.set_ylabel("$t$")
ax.set_zlabel("$|p(t,z)|$")
# fig9.colorbar(surf, shrink=0.5, aspect=5)
ax.view_init(elevation, azimuth)
plt.tight_layout()  # 自动调整大小和间距，使各个子图标签不重叠


fig10 = plt.figure("3d真解eta", dpi=dpi, facecolor=None, edgecolor=None)
ax = fig10.add_subplot(projection="3d")
surf = ax.plot_surface(
    X,
    T,
    etaExact_h,
    rstride=stride,  # 指定行的跨度
    cstride=stride,  # 指定列的跨度
    cmap="coolwarm",  # 设置颜色映射
    linewidth=0,
    antialiased=False,
)  # 抗锯齿
# ax.grid(False)#关闭背景的网格线
ax.set_xlabel("$z$")
ax.set_ylabel("$t$")
ax.set_zlabel("$|\eta(t,z)|$")
# fig10.colorbar(surf, shrink=0.5, aspect=5)
ax.view_init(elevation, azimuth)
plt.tight_layout()  # 自动调整大小和间距，使各个子图标签不重叠

# dde薛定谔里的图
fig15 = plt.figure("平面预测演化图", dpi=dpi)
plt.suptitle("Prediction Dynamics")
ax0 = plt.subplot(3, 1, 1)
ax0.set_ylabel("$E$")
h = ax0.imshow(
    EH_pred.T,
    interpolation="nearest",
    cmap="viridis",
    extent=[t_lower, t_upper, z_lower, z_upper],
    origin="lower",
    aspect="auto",
)
plt.colorbar(h, ax=ax0)
ax0.plot(
    X_u_train[:, 1],
    X_u_train[:, 0],
    "kx",
    label="Data (%d points)" % (X_u_train.shape[0]),
    markersize=4,
    clip_on=False,
)

ax1 = plt.subplot(3, 1, 2)
ax1.set_ylabel("$p$")
h = ax1.imshow(
    pH_pred.T,
    interpolation="nearest",
    cmap="viridis",
    extent=[t_lower, t_upper, z_lower, z_upper],
    origin="lower",
    aspect="auto",
)
plt.colorbar(h, ax=ax1)
ax1.plot(
    X_u_train[:, 1],
    X_u_train[:, 0],
    "kx",
    label="Data (%d points)" % (X_u_train.shape[0]),
    markersize=4,
    clip_on=False,
)

ax2 = plt.subplot(3, 1, 3)
ax2.set_ylabel("$\eta$")
h = ax2.imshow(
    etaH_pred.T,
    interpolation="nearest",
    cmap="viridis",
    extent=[t_lower, t_upper, z_lower, z_upper],
    origin="lower",
    aspect="auto",
)
plt.colorbar(h, ax=ax2)
ax2.plot(
    X_u_train[:, 1],
    X_u_train[:, 0],
    "kx",
    label="Data (%d points)" % (X_u_train.shape[0]),
    markersize=4,
    clip_on=False,
)

# plt.subplots_adjust(left=0.15, right=1-0.01,bottom=0.08, top=1-0.08,wspace=None, hspace=0.25)
plt.tight_layout()  # 自动调整大小和间距，使各个子图标签不重叠


fig16 = plt.figure("平面实际演化图", dpi=dpi)
plt.suptitle("Exact Dynamics")
ax0 = plt.subplot(3, 1, 1)
ax0.set_ylabel("$E$")
h = ax0.imshow(
    EExact_h.T,
    interpolation="nearest",
    cmap="viridis",
    extent=[t_lower, t_upper, z_lower, z_upper],
    origin="lower",
    aspect="auto",
)
# plt.colorbar(h, ax=ax0)

ax1 = plt.subplot(3, 1, 2)
ax1.set_ylabel("$p$")
h = ax1.imshow(
    pExact_h.T,
    interpolation="nearest",
    cmap="viridis",
    extent=[t_lower, t_upper, z_lower, z_upper],
    origin="lower",
    aspect="auto",
)
# plt.colorbar(h, ax=ax1)

ax2 = plt.subplot(3, 1, 3)
ax2.set_ylabel("$\eta$")
h = ax2.imshow(
    etaExact_h.T,
    interpolation="nearest",
    cmap="viridis",
    extent=[t_lower, t_upper, z_lower, z_upper],
    origin="lower",
    aspect="auto",
)
plt.colorbar(h, ax=[ax0, ax1, ax2], location="right")
# plt.subplots_adjust(left=0.15, right=1-0.01,bottom=0.08, top=1-0.08,wspace=None, hspace=0.25)
# plt.tight_layout()#自动调整大小和间距，使各个子图标签不重叠

fig17 = plt.figure("平面绝对误差演化图", dpi=dpi)
plt.suptitle("Absolute error dynamics")
ax0 = plt.subplot(3, 1, 1)
# ax0.set_title("Absolute error dynamics")
ax0.set_ylabel("$E$")
h = ax0.imshow(
    np.abs(EExact_h - EH_pred).T,
    interpolation="nearest",
    cmap="summer",  # PuOr
    extent=[t_lower, t_upper, z_lower, z_upper],
    origin="lower",
    aspect="auto",
)
plt.colorbar(h, ax=ax0)
ax1 = plt.subplot(3, 1, 2)
ax1.set_ylabel("$p$")
h = ax1.imshow(
    np.abs(pExact_h - pH_pred).T,
    interpolation="nearest",
    cmap="spring",
    extent=[t_lower, t_upper, z_lower, z_upper],
    origin="lower",
    aspect="auto",
)
plt.colorbar(h, ax=ax1)
ax2 = plt.subplot(3, 1, 3)
ax2.set_ylabel("$\eta$")
h = ax2.imshow(
    np.abs(etaExact_h - etaH_pred).T,
    interpolation="nearest",
    cmap="cool",  # seismic
    extent=[t_lower, t_upper, z_lower, z_upper],
    origin="lower",
    aspect="auto",
)
plt.colorbar(h, ax=ax2)
# plt.subplots_adjust(left=0.15, right=1-0.01,bottom=0.08, top=1-0.08,wspace=None, hspace=0.25)
plt.tight_layout()  # 自动调整大小和间距，使各个子图标签不重叠

dde.saveplot(losshistory, train_state, issave=True, isplot=True)

io.savemat(
    "预测结果_双孤子etav0.mat",
    {
        "x": x,
        "t": t,
        "elapsed": elapsed,
        "X_u_train": X_u_train,
        "E_L2_relative_error": E_L2_relative_error,
        "p_L2_relative_error": p_L2_relative_error,
        "eta_L2_relative_error": eta_L2_relative_error,
        "EH_pred": EH_pred,
        "pH_pred": pH_pred,
        "etaH_pred": etaH_pred,
        "EExact_h": EExact_h,
        "pExact_h": pExact_h,
        "etaExact_h": etaExact_h,
    },
)

plt.show()
