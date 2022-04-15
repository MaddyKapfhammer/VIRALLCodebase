"""A practice program with SIR modeling in Python."""

from scipy.integrate import odeint
import numpy as np
import matplotlib.pyplot as plt

# matplotlib inline
# import mpld3
# mpld3.enable_notebook()


def deriv(compartment, t, N, beta, gamma):
    S, I, R = compartment
    dSdt = -beta * S * I / N
    dIdt = beta * S * I / N - gamma * I
    dRdt = gamma * I

    return dSdt, dIdt, dRdt


def vector_deriv(compartment, t, N, beta, gamma, vector):
    S, I, R = compartment
    dS = -beta * S * vector / N
    dI = beta * S * I / N - gamma * I
    dR = gamma * I

    return dS, dI, dR


def specify_compartments(N, beta, D, S0, I0, R0):
    gamma = 1.0 / D
    t = np.linspace(0, 50, 51)
    y0 = S0, I0, R0
    ret = odeint(deriv, y0, t, args=(N, beta, gamma))
    S, I, R = ret.T

    return t, S, I, R


def plotsir(t, S, I, R):
    f, ax = plt.subplots(1, 1, figsize=(10, 4))
    ax.plot(t, S, "b", alpha=0.7, linewidth=2, label="Susceptible")
    ax.plot(t, I, "y", alpha=0.7, linewidth=2, label="Infected")
    ax.plot(t, R, "g", alpha=0.7, linewidth=2, label="Recovered")

    ax.set_xlabel("Time (weeks)")

    ax.yaxis.set_tick_params(length=0)
    ax.xaxis.set_tick_params(length=0)
    ax.grid(b=True, which="major", c="w", lw=2, ls="-")
    legend = ax.legend()
    legend.get_frame().set_alpha(0.5)
    for spine in ("top", "right", "bottom", "left"):
        ax.spines[spine].set_visible(False)

    plt.show()


if __name__ == "__main__":
    # N = int(input("Enter size of population: "))
    # beta = float(input("How many people does an infected individual infect per day?: "))
    # D = float(input("How long does infection last?: "))

    # S0 = int(input("Enter initial susceptible population: "))
    # I0 = int(input("Enter initial infected population: "))
    # R0 = int(input("Enter initial recovered population: "))

    N = 9500
    beta = 0.4
    D = 8.26
    S0 = 9000
    I0 = 200
    R0 = 300

    t, S, I, R = specify_compartments(N, beta, D, S0, I0, R0)
    print("day=0")
    print(S[0])
    print(I[0])
    print(R[0])
    print("")
    print("day=25")
    print(S[25])
    print(I[25])
    print(R[25])
    print("")
    print("day=50")
    print(S[50])
    print(I[50])
    print(R[50])
    # print(t, S, I, R)

    plotsir(t, S, I, R)
