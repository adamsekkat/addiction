from matplotlib import pyplot as plt
import numpy as np
from matplotlib.widgets import Button, Slider

#parametres initiaux
d = 0.2
q = 0.8
init_p = 0.6 # varie entre 0.2 et 0.8

S_max = 0.5
R_max = 7
init_E0 = 0.05

init_m_e = 0.0001        
m_lambda = 0
init_lambda_0 = 0.7

N = 260        

init_C0_patient1 = 0.9
init_C0_patient2 = -0.2
init_S0_patient1 = -0.7
init_S0_patient2 = 0.8

init_alpha = 0.001
init_beta = 0.05
init_gamma = 10


def Addiction_groupe(d,q,p,S_max,R_max,E0,m_e,m_lambda,lambda_0,C0_patient1,C0_patient2,S0_patient1,S0_patient2,alpha,beta,gamma,N):
    h = p*S_max
    k = (p/q)*S_max
    b = 2*d/q

    t = np.arange(0,N+1)

    C_patient1 = np.zeros(N+1)
    C_patient2 = np.zeros(N+1)

    S_patient1 = np.zeros(N+1)
    S_patient2 = np.zeros(N+1)

    E = np.zeros(N+1)

    psi_patient1 = np.zeros(N+1)
    psi_patient2 = np.zeros(N+1)

    V_patient1 = np.zeros(N+1)
    V_patient2 = np.zeros(N+1)

    A_patient1 = np.zeros(N+1)
    A_patient2 = np.zeros(N+1)

    P_patient1 = np.zeros(N+1)
    P_patient2 = np.zeros(N+1)

    random_poisson = np.zeros(N+1)

    C_patient1[0] = C0_patient1
    C_patient2[0] = C0_patient2

    S_patient1[0] = S0_patient1
    S_patient2[0] = S0_patient2

    E[0] = E0

    for i in range(N+1):
        psi_patient1[i] = C_patient1[i] - S_patient1[i] - E[i]
        psi_patient2[i] = C_patient2[i] - S_patient2[i] - E[i]
        V_patient1[i] = min(1,max(psi_patient1[i],0))
        V_patient2[i] = min(1,max(psi_patient2[i],0))
        random_poisson[i] = np.random.poisson(lambda_0)
        P_patient1[i] = p + beta*np.exp(-gamma*A_patient1[i])
        P_patient2[i] = p + beta*np.exp(-gamma*A_patient2[i])
        A_patient1[i] = q*V_patient1[i] + (random_poisson[i]/R_max)*q*(1-V_patient1[i])
        A_patient2[i] = q*V_patient2[i] + (random_poisson[i]/R_max)*q*(1-V_patient2[i])
        if i < N :
            C_patient1[i+1] = (1-d)*C_patient1[i] + alpha*A_patient2[i]*C_patient1[i] + b*min(1,1-C_patient1[i])*A_patient1[i]
            C_patient2[i+1] = (1-d)*C_patient2[i] + alpha*A_patient1[i]*C_patient2[i] + b*min(1,1-C_patient2[i])*A_patient2[i]
            S_patient1[i+1] = S_patient1[i] + P_patient2[i]*max(0,S_max - S_patient1[i]) - h*C_patient1[i] - k*A_patient1[i]
            S_patient2[i+1] = S_patient2[i] + P_patient1[i]*max(0,S_max - S_patient2[i]) - h*C_patient2[i] - k*A_patient2[i]
            E[i+1] = E[i] - m_e
    return t,C_patient1,C_patient2,S_patient1,S_patient2,E,V_patient1,V_patient2,A_patient1,A_patient2

t,C_patient1,C_patient2,S_patient1,S_patient2,E,V_patient1,V_patient2,A_patient1,A_patient2 = Addiction_groupe(d,q,init_p,S_max,R_max,init_E0,init_m_e,m_lambda,init_lambda_0,init_C0_patient1,init_C0_patient2,init_S0_patient1,init_S0_patient2,init_alpha,init_beta,init_gamma,N)

fig, ax = plt.subplots(6)
line_C1, = ax[0].plot(t,C_patient1,label="C1 : Intensité du désir du patient 1",lw=2)
line_C2, = ax[0].plot(t,C_patient2,label="C2 : Intensité du désir du patient 2",lw=2)
line_E0, = ax[0].plot(t,E,label="E : Influence Sociétale",lw=2)
line_S1, = ax[1].plot(t,S_patient1,label="S1 : Intensité du self-control du patient 1",lw=2)
line_S2, = ax[1].plot(t,S_patient2,label="S2 : Intensité du self-control du patient 2",lw=2)
line_E1, = ax[1].plot(t,E,label="E : Influence Sociétale",lw=2)
line_V1, = ax[2].plot(t,V_patient1,label="V1 : Niveau de Vulnérabilité du patient 1",lw=2)
line_V2, = ax[2].plot(t,V_patient2,label="V2 : Niveau de Vulnérabilité du patient 2",lw=2)
line_E2, = ax[2].plot(t,E,label="E : Influence Sociétale",lw=2)
line_A1, = ax[3].plot(t,A_patient1,label="A1 : Addiction exercée au patient 1",lw=2)
line_A2, = ax[3].plot(t,A_patient2,label="A2 : Addiction exercée au  patient 2",lw=2)
line_E3, = ax[3].plot(t,E,label="E : Influence Sociétale",lw=2)
line_C1_global,= ax[4].plot(t,C_patient1,label="C1",lw=2,color="red")
line_C2_global, = ax[5].plot(t,C_patient2,label="C2",lw=1,color="red",linestyle="--")
line_S1_global, = ax[4].plot(t,S_patient1,label="S1",lw=2,color="green")
line_S2_global, = ax[5].plot(t,S_patient2,label="S2",lw=1,color="green",linestyle="--")
line_E1_global, = ax[4].plot(t,E,label="E",lw=2,color="yellow")
line_E2_global, = ax[5].plot(t,E,label="E",lw=2,color="yellow")
line_V1_global, = ax[4].plot(t,V_patient1,label="V1",lw=2,color="black")
line_V2_global, = ax[5].plot(t,V_patient2,label="V2",lw=1,color="black",linestyle="--")
line_A1_global, = ax[4].plot(t,A_patient1,label="A1",lw=2,color="blue")
line_A2_global, = ax[5].plot(t,A_patient2,label="A2",lw=1,color="blue",linestyle="--")
ax[5].set_xlabel("Temps en semaine")
ax[5].set_ylabel("Intensité")


ax_p = fig.add_axes([0.02, 0.02, 0.07, 0.015])
p_slider = Slider(
    ax=ax_p,
    label='p',
    valmin=-1,
    valmax=1,
    valinit=init_p,
)

ax_E0 = fig.add_axes([0.15, 0.02, 0.07, 0.015])
E0_slider = Slider(
    ax=ax_E0,
    label='E0',
    valmin=-1,
    valmax=1,
    valinit=init_E0,
)

ax_m_e = fig.add_axes([0.28, 0.02, 0.07, 0.015])
m_e_slider = Slider(
    ax=ax_m_e,
    label='m_e',
    valmin=-0.003,
    valmax=0.003,
    valinit=init_m_e,
)

ax_lambda_0 = fig.add_axes([0.455, 0.02, 0.07, 0.015])
lambda_0_slider = Slider(
    ax=ax_lambda_0,
    label='lambda_0',
    valmin=0,
    valmax=1,
    valinit=init_lambda_0,
)

ax_C0_1 = fig.add_axes([0.05, 0.95, 0.1, 0.015])
C0_1_slider = Slider(
    ax=ax_C0_1,
    label='C0_1',
    valmin=-2,
    valmax=2,
    valinit=init_C0_patient1,
)

ax_C0_2 = fig.add_axes([0.25, 0.95, 0.1, 0.015])
C0_2_slider = Slider(
    ax=ax_C0_2,
    label='C0_2',
    valmin=-2,
    valmax=2,
    valinit=init_C0_patient2,
)

ax_S0_1 = fig.add_axes([0.45, 0.95, 0.1, 0.015])
S0_1_slider = Slider(
    ax=ax_S0_1,
    label='S0_1',
    valmin=-2,
    valmax=2,
    valinit=init_S0_patient1,
)

ax_S0_2 = fig.add_axes([0.65, 0.95, 0.1, 0.015])
S0_2_slider = Slider(
    ax=ax_S0_2,
    label='S0_2',
    valmin=-2,
    valmax=2,
    valinit=init_S0_patient2,
)

ax_alpha = fig.add_axes([0.585, 0.02, 0.07, 0.015])
alpha_slider = Slider(
    ax=ax_alpha,
    label='alpha',
    valmin=0.0001,
    valmax=0.01,
    valinit=init_alpha,
)

ax_beta = fig.add_axes([0.73, 0.02, 0.07, 0.015])
beta_slider = Slider(
    ax=ax_beta,
    label='beta',
    valmin=0.0001,
    valmax=0.01,
    valinit=init_beta,
)

ax_gamma = fig.add_axes([0.9, 0.02, 0.07, 0.015])
gamma_slider = Slider(
    ax=ax_gamma,
    label='gamma',
    valmin=10,
    valmax=100,
    valinit=init_gamma,
)

def update(val):
    t,C_patient1_val,C_patient2_val,S_patient1_val,S_patient2_val,E_val,V_patient1_val,V_patient2_val,A_patient1_val,A_patient2_val = Addiction_groupe(d,q,p_slider.val,S_max,R_max,E0_slider.val,m_e_slider.val,m_lambda,lambda_0_slider.val,C0_1_slider.val,C0_2_slider.val,S0_1_slider.val,S0_2_slider.val,alpha_slider.val,beta_slider.val,gamma_slider.val,N)
    line_C1.set_ydata(C_patient1_val)
    line_C2.set_ydata(C_patient2_val)
    line_E0.set_ydata(E_val)
    line_S1.set_ydata(S_patient1_val)
    line_S2.set_ydata(S_patient2_val)
    line_E1.set_ydata(E_val)
    line_V1.set_ydata(V_patient1_val)
    line_V2.set_ydata(V_patient2_val)
    line_E2.set_ydata(E_val)
    line_A1.set_ydata(A_patient1_val)
    line_A2.set_ydata(A_patient2_val)
    line_E3.set_ydata(E_val)
    line_C1_global.set_ydata(C_patient1_val)
    line_C2_global.set_ydata(C_patient2_val)
    line_E1_global.set_ydata(E_val)
    line_E2_global.set_ydata(E_val)
    line_S1_global.set_ydata(S_patient1_val)
    line_S2_global.set_ydata(S_patient2_val)
    line_V1_global.set_ydata(V_patient1_val)
    line_V2_global.set_ydata(V_patient2_val)
    line_A1_global.set_ydata(A_patient1_val)
    line_A2_global.set_ydata(A_patient2_val)
    plt.title("Variations des intensités pour les deux patients  avec \n p : " + str(p_slider.val) + " , lambda_0 : " + str(lambda_0_slider.val) + " , alpha : " + str(alpha_slider.val) + " , beta : " + str(beta_slider.val) + " , gamma : " + str(gamma_slider.val))
    fig.canvas.draw_idle()

p_slider.on_changed(update)
E0_slider.on_changed(update)
m_e_slider.on_changed(update)
lambda_0_slider.on_changed(update)
C0_1_slider.on_changed(update)
C0_2_slider.on_changed(update)
S0_1_slider.on_changed(update)
S0_2_slider.on_changed(update)
alpha_slider.on_changed(update)
beta_slider.on_changed(update)
gamma_slider.on_changed(update)

resetax = fig.add_axes([0.8, 0.95, 0.1, 0.04])
button = Button(resetax, 'Reset', hovercolor='0.975')

def reset(event):
    p_slider.reset()
    E0_slider.reset()
    m_e_slider.reset()
    lambda_0_slider.reset()
    C0_1_slider.reset()
    C0_2_slider.reset()
    S0_1_slider.reset()
    S0_2_slider.reset()
    alpha_slider.reset()
    beta_slider.reset()
    gamma_slider.reset()

button.on_clicked(reset)

ax[0].legend(fontsize=7)
ax[1].legend(fontsize=7)
ax[2].legend(fontsize=7)
ax[3].legend(fontsize=7)
ax[4].legend(fontsize=7)
ax[5].legend(fontsize=7)
plt.show()
