from matplotlib import pyplot as plt
import numpy as np
from matplotlib.widgets import Button, Slider

#parametres initiaux
d = 0.5
q = 0.8
init_p = 0.6 # varie entre 0.2 et 0.8

S_max = 0.7
R_max = 7

C0 = 0
S0 = S_max
E0 = 1
init_lambda_0 = 0.2

lambda_max = 0.5 # maximum du paramètre de la loi de Poisson
init_m_e = 0.01 # pas de l'influence sociale -> doit varier
m_lambda = 0 # pas du parametre de la loi de poisson

N = 250  #nombre de semaines

h = init_p*S_max
k = (init_p/q)*S_max
b = 2*d/q

def Addiction(d,q,p,R_max,C0,S0,E0,lambda_0,m_e,m_lambda,h,k,b,N):
    C = [C0]
    S = [S0]
    E = [E0]
    psi = [C[0]-S[0]-E[0]]
    V = [min(1,max(psi[0],0))]
    lambda_tab = [lambda_0]
    R_lambda = np.random.poisson(lambda_tab[0],1)[0]
    A = [q*V[0] + (R_lambda/R_max)*q*(1-V[0])]
    t = np.arange(0,N+1)
    for i in range(N):
        C.append((1-d)*C[i] + b*min(1,1-C[i])*A[i])
        S.append(S[i] + p*max(0,S_max-S[i]) -h*C[i] -k*A[i])
        E.append(E[i]-m_e)
        psi.append(C[i]-S[i]-E[i])
        V.append(min(1,max(psi[i],0)))
        lambda_tab.append(lambda_tab[i] + m_lambda)
        R_lambda = np.random.poisson(lambda_tab[i],1)[0]
        A.append(q*V[i] + (R_lambda/R_max)*q*(1-V[i]))
    return t,C,S,E,V,A



fig, ax = plt.subplots()
t,C,S,E,V,A = Addiction(d,q,init_p,R_max,C0,S0,E0,init_lambda_0,init_m_e,m_lambda,h,k,b,N)
line_C, = ax.plot(t,C,label="C : Intensité du désir ", lw=2)
line_S, = ax.plot(t,S,label="S : Intensité du self-control", lw=2)
line_E, = ax.plot(t,E,label="E : Influence sociétale", lw=2)
line_V, = ax.plot(t,V,label="V : Niveau de vulnérabilité", lw=2)
line_A, = ax.plot(t,A,label="A : Addiction exercée", lw=2)
ax.set_xlabel("Temps en semaine")
ax.set_ylabel("Intensité")
ax.set_title("Évolution des niveaux et intensités pour les paramètres suivants \n p : " + str(init_p) + " , lambda_0 : " + str(init_lambda_0) + " , me : " + str(init_m_e))
plt.axhline(y=0.85,color='black',linestyle='--')


fig.subplots_adjust(left=0.15, bottom=0.55)

ax_p = fig.add_axes([0.1, 0.1, 0.35, 0.03])
p_slider = Slider(
    ax=ax_p,
    label='p',
    valmin=0.2,
    valmax=0.8,
    valinit=init_p,
)

ax_lambda_0 = fig.add_axes([0.1, 0.2, 0.35, 0.03])
lambda_0_slider = Slider(
    ax=ax_lambda_0,
    label='lambda_0',
    valmin=0.2,
    valmax=0.5,
    valinit=init_lambda_0,
)

ax_m_e = fig.add_axes([0.1, 0.3, 0.35, 0.03])
m_e_slider = Slider(
    ax=ax_m_e,
    label='m_e',
    valmin=0,
    valmax=0.2,
    valinit=init_m_e,
)


def update(val):
    t,C_val,S_val,E_val,V_val,A_val = Addiction(d,q,p_slider.val,R_max,C0,S0,E0,lambda_0_slider.val,m_e_slider.val,m_lambda,h,k,b,N)
    line_C.set_ydata(C_val)
    line_S.set_ydata(S_val)
    line_E.set_ydata(E_val)
    line_V.set_ydata(V_val)
    line_A.set_ydata(A_val)
    ax.set_ylim(E_val[-1], 2)
    ax.set_title("Évolution des niveaux et intensités pour les paramètres suivants \n p : " + str(p_slider.val) + " , lambda_0 : " + str(lambda_0_slider.val) + " , me : " + str(m_e_slider.val))
    fig.canvas.draw_idle()


p_slider.on_changed(update)
lambda_0_slider.on_changed(update)
m_e_slider.on_changed(update)





resetax = fig.add_axes([0.8, 0.95, 0.1, 0.04])
button = Button(resetax, 'Reset', hovercolor='0.975')


def reset(event):
    p_slider.reset()
    lambda_0_slider.reset()
    m_e_slider.reset()
button.on_clicked(reset)

ax.legend()
plt.show()