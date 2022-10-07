#!/usr/bin/python

from dados import dados_termeletricas, lim_hidro, coef_fcm, coef_fcj
from dados import coef_perda_hidraulica, coef_rend_hidraulico
from dados import dados_afluencias, vazao_por_usina
from dados import dados_velocidade_ventos, dados_geracao_eolica
import numpy as np

print('\n# QUESTÃO 1: Afluências e Geração Eólica')
# USINAS: 0,1,2 (começa no 0 devido ao index da matriz do pandas)
# AFLUENCIAS INICIAIS: 1500,1000,900 (valores fornecidos pelo professor)


def afluencia_hidro(usina, afluencia_inicial):
    Y = []

    phi = dados_afluencias.loc[usina-1, 'phi']
    a = dados_afluencias.loc[usina-1, 'a']
    b = dados_afluencias.loc[usina-1, 'b']

    Y0 = afluencia_inicial
    random = np.random.uniform(int(a), int(b))
    Y.append(int(phi*Y0 + random))

    for i in range(11):
        random = np.random.uniform(int(a), int(b))
        y = int(float(phi)*Y[i] + random)
        Y.append(y)

    print(f'afluencia_hidro {usina}: {Y}')
    return Y


Y = []
Y.append(afluencia_hidro(1, 1500))
Y.append(afluencia_hidro(2, 1000))
Y.append(afluencia_hidro(3, 900))

ro = 1225  # massa especifica do ar: 1225
phi = dados_velocidade_ventos['phi']
media = dados_velocidade_ventos['eta_media']
desviopadrao = dados_velocidade_ventos['eta_desvio']
Cp = dados_geracao_eolica['Cp']
AR = dados_geracao_eolica['AR']

SW = []  # VELOCIDADE DO VENTO INICIAL: 25 (fornecido)
SW.append(phi*25)
zeta = np.random.normal(media, desviopadrao, 12)

for i in range(12):
    sw = int(phi*SW[i]+float(zeta[i]))
    if sw > 25:
        sw = 0
    elif sw < 3:
        sw = 0
    SW.append(sw)

SW.pop(0)

print(f'velocidade do vento: {SW}')

GW = []
for i in range(12):
    gw = int((ro*AR*(SW[i]**3)*Cp)/2)
    gw = int(1e-6*gw)  # convertendo de W para MW
    GW.append(gw)

print(f'potencia do aero: {GW}')
GW = [gw * 40 for gw in GW]
print(f'potencia total do parque: {GW}')

print('\n# QUESTÃO 2: Volume médio armazenado e a queda bruta')
c = float((2*60*60)/(1e6))


def Vmed_HB_Q_S(usina, Qmon, Smon):
    Vmin = lim_hidro.loc[usina-1, 'vol_min']
    Vmax = lim_hidro.loc[usina-1, 'vol_max']

    V0 = int(Vmin + 0.35 * (Vmax - Vmin))
    VF = []
    VF.append(V0)

    Q = list(vazao_por_usina[f'H{usina}'].values)
    if usina == 1:
        q0 = 800  # VAZAO TURBINADA DA HIDRELETRICA 1 NO INSTANTE 0 = 800
    else:
        q0 = 0
    Q.insert(0, q0)
    S = []
    S.append(0)

    for i in range(1, 13):
        S.append(0)
        vf = int(VF[i-1] - c*(Q[i-1] + S[i-1] - Y[usina-1][i-1]))
        if Qmon is not None:
            vf += c*(Qmon[i-1] + Smon[i-1])

        if vf > Vmax:
            S[i-1] = round(Vmax - vf, 2)
            vf += S[i-1]
        VF.append(vf)

    Vmed = []
    for i in range(1, 13):
        vmed = int((VF[i-1] + VF[i])/2)
        Vmed.append(vmed)

    FCM = []
    FCJ = []
    HB = []
    f0 = coef_fcm.loc[usina-1, 'F0']
    f1 = coef_fcm.loc[usina-1, 'F1']
    f2 = coef_fcm.loc[usina-1, 'F2']
    f3 = coef_fcm.loc[usina-1, 'F3']
    f4 = coef_fcm.loc[usina-1, 'F4']
    g0 = coef_fcj.loc[usina-1, 'G0']
    g1 = coef_fcj.loc[usina-1, 'G1']
    g2 = coef_fcj.loc[usina-1, 'G2']
    g3 = coef_fcj.loc[usina-1, 'G3']
    g4 = coef_fcj.loc[usina-1, 'G4']

    for i in range(12):
        f11 = f1*(Vmed[i])
        f22 = f2*(Vmed[i]**2)
        f33 = f3*(Vmed[i]**3)
        f44 = f4*(Vmed[i]**4)
        fcm = f0 + f11 + f22 + f33 + f44
        fcm = round(fcm, 2)
        FCM.append(fcm)

        g11 = g1*(Q[i]+S[i])
        g22 = g2*(Q[i]+S[i])**2
        g33 = g3*(Q[i]+S[i])**3
        g44 = g4*(Q[i]+S[i])**4
        fcj = g0 + g11 + g22 + g33 + g44
        fcj = round(fcj, 2)
        FCJ.append(fcj)

        hb = fcm - fcj
        hb = round(hb, 2)
        HB.append(hb)

    return Vmed, Q, S, HB


Vmed1, Q1, S1, HB1 = Vmed_HB_Q_S(1, Qmon=None, Smon=None)
Vmed2, Q2, S2, HB2 = Vmed_HB_Q_S(2, Qmon=Q1, Smon=S1)
Vmed3, Q3, S3, HB3 = Vmed_HB_Q_S(3, Qmon=Q2, Smon=S2)

Q1.pop(0)
S1.pop(0)
Q2.pop(0)
S2.pop(0)
Q3.pop(0)
S3.pop(0)

Vmed = [Vmed1, Vmed2, Vmed3]
Q = [Q1, Q2, Q3]
S = [S1, S2, S3]
HB = [HB1, HB2, HB3]

for usina in [1, 2, 3]:
    print("Usina H{}:".format(usina))
    print("Vmed:", Vmed[usina-1])
    # print("Q:", Q[usina-1])
    # print("S:", S[usina-1])
    print("HB:", HB[usina-1])
    print("")

nUG = [3, 5, 4]

print("\n# QUESTÃO 3 ##########################")
gravity = 0.00981


def geracao_hidro(usina, n, i):
    w = Q[usina-1][i] / n
    H = coef_perda_hidraulica['perda']
    hl = HB[usina-1][i] - H[usina-1]*w
    Ir = coef_rend_hidraulico.iloc[usina-1, 1:].values

    r = Ir[0] + Ir[1]*w + Ir[2]*hl
    r += (Ir[3]*w*hl + Ir[4]*w*w + Ir[5]*hl*hl)

    GHmin = lim_hidro.loc[usina-1, 'GHmin']
    GHmax = lim_hidro.loc[usina-1, 'GHmax']
    gh = round(gravity*r*hl*w)
    if gh < GHmin or gh > GHmax:
        gh = 0
    return gh


def max_pot(usina, i):
    GH = []
    for n in range(nUG[usina-1]):
        GH.append(geracao_hidro(usina, n+1, i))

    return max(GH)


GH = []
for usina in [1, 2, 3]:
    gh = []
    for i in range(12):
        gh.append(max_pot(usina=usina, i=i))
    GH.append(gh)

print("GH[0]", GH[0])
print("GH[1]", GH[1])
print("GH[2]", GH[2])

print("\n# Questão 4: Rendimento global e produtibilidade ############")
NG = []
for usina in [1, 2, 3]:
    ng = []
    for i in range(12):
        ngit = round(GH[usina-1][i]/(gravity*HB[usina-1][i]*Q[usina-1][i]), 2)
        ng.append(ngit)
    NG.append(ng)

print("NG[0] = ", NG[0])
print("NG[1] = ", NG[1])
print("NG[2] = ", NG[2])

P = []
pcit = []
for usina in [1, 2, 3]:
    p = []
    for i in range(12):
        pit = round(GH[usina-1][i]/Q[usina-1][i], 2)
        p.append(pit)
    pcit.append(round(np.mean(p), 2))
    P.append(p)

print("pcit: ", pcit)
print("P[0] = ", P[0])
print("P[1] = ", P[1])
print("P[2] = ", P[2])



print("\n# Questão 5 ###########")
