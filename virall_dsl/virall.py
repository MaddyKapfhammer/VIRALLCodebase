from scipy.integrate import odeint
import numpy as np
import matplotlib.pyplot as plt
from os.path import join, dirname

from textx import metamodel_from_file
from textx.export import metamodel_export, model_export

def create_differential_equations(compartment, N, beta, gamma):
    S, I, R = compartment
    dSdt = -beta * S * I / N
    dIdt = beta * S * I / N - gamma * I
    dRdt = gamma * I
    
    return dSdt, dIdt, dRdt


def differentiate(N, beta, D, S0, I0, R0, time_frame):
    gamma = 1.0 / D
    t = np.linspace(0, time_frame, 50)
    y0 = S0, I0, R0
    ret = odeint(create_differential_equations, y0, t, args=(N, beta, gamma))
    S, I, R = ret.T

    return t, S, I, R


def plot_model(t, S, I, R, susceptible_color, infected_color, recovered_color):
    f, ax = plt.subplots(1,1,figsize=(10,4))
    ax.plot(t, S, susceptible_color, alpha=0.7, linewidth=2, label='Susceptible')
    ax.plot(t, I, infected_color, alpha=0.7, linewidth=2, label='Infected')
    ax.plot(t, R, recovered_color, alpha=0.7, linewidth=2, label='Recovered')

    ax.set_xlabel('Time (days)')

    ax.yaxis.set_tick_params(length=0)
    ax.xaxis.set_tick_params(length=0)
    ax.grid(b=True, which='major', c='w', lw=2, ls='-')
    legend = ax.legend()
    legend.get_frame().set_alpha(0.5)
    for spine in ('top', 'right', 'bottom', 'left'):
        ax.spines[spine].set_visible(False)
    
    plt.show()


class Virall(object):

    def __init__(self):
        self.susceptible = 1000
        self.infected = 1
        self.recovered = 0
        self.beta = 1
        self.gamma = 4
        self.d = 1
        self.time_frame = 50
        self.susceptible_color = "blue"
        self.infected_color = "green"
        self.recovered_color = "yellow"

    def interpret(self, virall_model):
        for c in virall_model.commands:
            if c.__class__.__name__ == "CreateModel":
                "Creating differential equations"
                model_type = c.model_type
                print(model_type)
            elif c.__class__.__name__ == "Calculate":
                "Differentiating"
                population_size = c.population_size
                beta = c.beta
                d = c.D
                susceptible = c.susceptible
                infected = c.infected
                recovered = c.recovered
                time_frame = c.time_frame

                t, S, I, R = differentiate(population_size, beta, d, susceptible, infected, recovered, time_frame)
            elif c.__class__.__name__ == "Plot":
                susceptible_color = c.susceptible_color
                infected_color = c.infected_color
                recovered_color = c.recovered_color

                plot_model(t, S, I, R, susceptible_color, infected_color, recovered_color)


def main(debug=False):
    this_folder = dirname(__file__)

    virall_meta = metamodel_from_file(join(this_folder, "new_virall.tx"), debug=False)
    metamodel_export(virall_meta, join(this_folder, "virall_meta.dot"))

    virall_model = virall_meta.model_from_file(join(this_folder, 'SIR_model.virall'))
    model_export(virall_model, join(this_folder, 'program.dot'))

    virall = Virall()
    virall.interpret(virall_model)


if __name__ == "__main__":
    main()
