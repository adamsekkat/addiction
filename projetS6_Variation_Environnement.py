from matplotlib import pyplot as plt
import numpy as np
from matplotlib.widgets import Button, Slider


#parametres initiaux
d = 0.2
q = 0.8
p = 0.6 # varie entre 0.2 et 0.8

S_max = 0.5
R_max = 7

C0 = 0.7
S_0 = -0.35
init_E0 = 1
lambda_0 = 0.9

init_m_e = 0.03        
m_lambda = 0.0

h = p*S_max
k = (p/q)*S_max
b = 2*d/q

N = 260  


def Addiction_Variation_Environnement(d,q,p,h,k,b,S_max,S_0,R_max,lambda_0,C0,E0,m_e,m_lambda,N):
    S0 = S_0
    h = p*S_max
    k = (p/q)*S_max
    b = 2*d/q
    t = np.arange(0,N+1)
    C = np.zeros(N+1)
    S = np.zeros(N+1)
    E = np.zeros(N+1)
    psi = np.zeros(N+1)
    V = np.zeros(N+1)
    A = np.zeros(N+1)
    lambda_tab = np.zeros(N+1)
    random_poisson = np.zeros(N+1)
    C[0] = C0
    S[0] = S0
    E[0] = E0
    lambda_tab[0] = lambda_0
    #random_poisson = np.random.poisson(lambda_0)
    for i in range(N+1):
        psi[i] = C[i] - S[i] - E[i]
        V[i] = min(1,max(psi[i],0))
        random_poisson[i] = np.random.poisson(lambda_0)
        A[i] = q*V[i] + (random_poisson[i]/R_max)*q*(1-V[i])
        if i < N :
            C[i+1] = (1-d)*C[i] + b*min(1,1-C[i])*A[i]
            S[i+1] = S[i] + p*max(0,S_max - S[i]) -h*C[i] -k*A[i]
            E[i+1] = E[i] - m_e
            lambda_tab[i+1] = lambda_tab[i] + m_lambda
    return t,C,S,E,V,A



fig, ax = plt.subplots()
t,C,S,E,V,A = Addiction_Variation_Environnement(d,q,p,h,k,b,S_max,S_0,R_max,lambda_0,C0,init_E0,init_m_e,m_lambda,N)
line_C, = ax.plot(t,C,label="C : Intensité du désir ", lw=2)
line_S, = ax.plot(t,S,label="S : Intensité du self-control", lw=2)
line_E, = ax.plot(t,E,label="E : Influence sociétale", lw=2)
line_V, = ax.plot(t,V,label="V : Niveau de vulnérabilité", lw=2)
line_A, = ax.plot(t,A,label="A : Addiction exercée", lw=2)
ax.set_xlabel("Temps en semaine")
ax.set_ylabel("Intensité")
ax.set_title("Variations des intensités en fonction de l'environnement pour les paramètres suivants \n p : " + str(p) + " , lambda_0 : " + str(lambda_0) + " , E0 : " + str(init_E0) + " , m_e : " + str(init_m_e))
plt.axhline(y=0.85,color='black',linestyle='--')



fig.subplots_adjust(left=0.15, bottom=0.55)

ax_m_e = fig.add_axes([0.1, 0.1, 0.35, 0.03])
m_e_slider = Slider(
    ax=ax_m_e,
    label='m_e',
    valmin=-0.003,
    valmax=0.003,
    valinit=init_m_e,
)
ax_E0 = fig.add_axes([0.1, 0.2, 0.35, 0.03])
E0_slider = Slider(
    ax=ax_E0,
    label='E0',
    valmin=-1,
    valmax=1,
    valinit=init_E0,
)

def update(val):
    t,C_val,S_val,E_val,V_val,A_val = Addiction_Variation_Environnement(d,q,p,h,k,b,S_max,S_0,R_max,lambda_0,C0,E0_slider.val,m_e_slider.val,m_lambda,N)
    line_C.set_ydata(C_val)
    line_S.set_ydata(S_val)
    line_E.set_ydata(E_val)
    line_V.set_ydata(V_val)
    line_A.set_ydata(A_val)
    ax.set_ylim(-2, 2)
    ax.set_title("Variations des intensités en fonction de l'environnement pour les paramètres suivants \n p : " + str(p) + " , lambda_0 : " + str(lambda_0) + " , E0 : " + str(E0_slider.val) + " , m_e : " + str(m_e_slider.val)) 
    fig.canvas.draw_idle()


m_e_slider.on_changed(update)
E0_slider.on_changed(update)



resetax = fig.add_axes([0.8, 0.95, 0.1, 0.04])
button = Button(resetax, 'Reset', hovercolor='0.975')


