from scipy.integrate import odeint
import numpy as np
import matplotlib.pyplot as plt


def define_equations(S, I, R, beta, gamma, mu):
    dS = -(S * I * beta) - (S * mu)
    dI = (S * I * beta) - (I * gamma) - (I * mu)
    dR = (I * R * gamma) - (R * mu)

    return dS, dI, dR


def run_differentials(beta, gamma, mu_value, S0, I0, R0):
    t = np.linspace(0, 49, 50)
    y0 = S0, I0, R0
    ret = odeint(define_equations, y0, t, args=(beta, gamma, mu_value), mu=None)
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
    beta = float(input("Transmission rate: "))
    gamma = float(input("Recovery rate: "))
    mu = float(input("Death rate: "))

    S0 = int(input("Enter initial susceptible population: "))
    I0 = int(input("Enter initial infected population: "))
    R0 = int(input("Enter initial recovered population: "))

    t, S, I, R = run_differentials(beta, gamma, mu, S0, I0, R0)

    plotsir(t, S, I, R)
