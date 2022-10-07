#!/usr/bin/python

from dados import dados_termeletricas, lim_hidro, coef_fcm, coef_fcj
from dados import coef_perda_hidraulica, coef_rend_hidraulico
from dados import dados_afluencias, vazao_por_usina
from dados import dados_velocidade_ventos, dados_geracao_eolica
import numpy as np

print('\n# QUESTÃO 1: Afluências e Geração Eólica')
# USINAS: 0,1,2 (começa no 0 devido ao index da matriz do pandas)
# AFLUENCIAS INICIAIS: 1500,1000,900 (valores fornecidos pelo professor)


def afluenciahidro(usina, afluencia_inicial):
    Y = []

    phi = dados_afluencias.loc[usina, 'phi']
    a = dados_afluencias.loc[usina, 'a']
    b = dados_afluencias.loc[usina, 'b']

    Y0 = afluencia_inicial
    random = np.random.uniform(int(a), int(b))
    Y.append(int(phi*Y0 + random))

    for i in range(11):
        random = np.random.uniform(int(a), int(b))
        y = int(float(phi)*Y[i] + random)
        Y.append(y)

    print(f'afluenciahidro {usina+1}: {Y}')
    return Y

Y = []

Y.append(afluenciahidro(0, 1500))
Y.append(afluenciahidro(1, 1000))
Y.append(afluenciahidro(2, 900))
print(Y)

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

print('# QUESTÃO 2: Volume médio armazenado e a queda bruta')
print('########### HIDRELÉTRICA 1 ###############')

usina = 1
Vmin = lim_hidro.loc[usina-1, 'vol_min']
Vmax = lim_hidro.loc[usina-1, 'vol_max']

V0 = int(Vmin + 0.35 * (Vmax - Vmin))

c = float((2*60*60)/(1e6))
VF = []
VF.append(V0)

Q = list(vazao_por_usina['H1'].values)
q0 = 800  # VAZAO TURBINADA DA HIDRELETRICA 1 NO INSTANTE 0 = 800
Q.insert(q0, 0)
S = []

for i in range(12):
    S.append(0)
    vf = int(VF[i] - c*(Q[i-1] + S[i] - Y[usina-1][i]))
    if vf > Vmax:
        S[i] = Vmax - vf
        vf = int(VF[i] - c*(Q[i] + S[i] - Y[usina-1][i]))
    VF.append(vf)

print("H1: volumes finais:", VF)

Vmed = []
for i in range(1, 13):
    vmed = int((VF[i-1] + VF[i])/2)
    Vmed.append(vmed)

print("H1: volumes médios:", Vmed)

count = 0

fcm_H1 = []
fcj_H1 = []
hb_lista_1 = []
f0 = float(coef_fcm.iloc[0, 1])
f1 = float(coef_fcm.iloc[0, 2])
f2 = float(coef_fcm.iloc[0, 3])
f3 = float(coef_fcm.iloc[0, 4])
f4 = float(coef_fcm.iloc[0, 5])
g0 = float(coef_fcj.iloc[0, 1])
g1 = float(coef_fcj.iloc[0, 2])
g2 = float(coef_fcj.iloc[0, 3])
g3 = float(coef_fcj.iloc[0, 4])
g4 = float(coef_fcj.iloc[0, 5])

for i in range(12):
    f11 = f1*(Vmed[i])
    f22 = f2*(Vmed[i]**2)
    f33 = f3*(Vmed[i]**3)
    f44 = f4*(Vmed[i]**4)
    fcm = f0 + f11 + f22 + f33 + f44
    fcm = round(fcm, 2)
    fcm_H1.append(fcm)

    g11 = g1*(Q[i]+S[i])
    g22 = g2*(Q[i]+S[i])**2
    g33 = g3*(Q[i]+S[i])**3
    g44 = g4*(Q[i]+S[i])**4
    fcj = g0 + g11 + g22 + g33 + g44
    fcj = round(fcj, 2)
    fcj_H1.append(fcj)

    hb = fcm - fcj
    hb = round(hb, 2)
    hb_lista_1.append(hb)

print(f'H1: fcm: {fcm_H1}')
print(f'H1: fcj: {fcj_H1}')
print(f'H1: hb: {hb_lista_1}')

print('# HIDRELÉTRICA 2 e 3 ###############')
for usina in [2, 3]:
    Vmin = lim_hidro.loc[usina-1, 'vol_min']
    Vmax = lim_hidro.loc[usina-1, 'vol_max']

    V0 = int(Vmin + 0.35 * (Vmax - Vmin))

    c = float((2*60*60)/(1e6))
    VF = []
    VF.append(V0)

    Q = list(vazao_por_usina[f'H{usina}'].values)
    q0 = 800  # VAZAO TURBINADA DA HIDRELETRICA 1 NO INSTANTE 0 = 800
    Q.insert(q0, 0)
    S = []

    for i in range(12):
        S.append(0)
        vf = int(VF[i] - c*(Q[i-1] + S[i] - Y[usina-1][i]))
        if vf > Vmax:
            S[i] = Vmax - vf
            vf = int(VF[i] - c*(Q[i] + S[i] - Y[usina-1][i]))
        VF.append(vf)

    print(f"H{usina}: volumes finais: {VF}")

    Vmed = []
    for i in range(1, 13):
        vmed = int((VF[i-1] + VF[i])/2)
        Vmed.append(vmed)

    print(f"H{usina}: volumes médios: {Vmed}")

    count = 0

    fcm_H1 = []
    fcj_H1 = []
    hb_lista_1 = []
    f0 = float(coef_fcm.iloc[0, 1])
    f1 = float(coef_fcm.iloc[0, 2])
    f2 = float(coef_fcm.iloc[0, 3])
    f3 = float(coef_fcm.iloc[0, 4])
    f4 = float(coef_fcm.iloc[0, 5])
    g0 = float(coef_fcj.iloc[0, 1])
    g1 = float(coef_fcj.iloc[0, 2])
    g2 = float(coef_fcj.iloc[0, 3])
    g3 = float(coef_fcj.iloc[0, 4])
    g4 = float(coef_fcj.iloc[0, 5])

    for i in range(12):
        f11 = f1*(Vmed[i])
        f22 = f2*(Vmed[i]**2)
        f33 = f3*(Vmed[i]**3)
        f44 = f4*(Vmed[i]**4)
        fcm = f0 + f11 + f22 + f33 + f44
        fcm = round(fcm, 2)
        fcm_H1.append(fcm)

        g11 = g1*(Q[i]+S[i])
        g22 = g2*(Q[i]+S[i])**2
        g33 = g3*(Q[i]+S[i])**3
        g44 = g4*(Q[i]+S[i])**4
        fcj = g0 + g11 + g22 + g33 + g44
        fcj = round(fcj, 2)
        fcj_H1.append(fcj)

        hb = fcm - fcj
        hb = round(hb, 2)
        hb_lista_1.append(hb)

    print(f'H{usina}: fcm: {fcm_H1}')
    print(f'H{usina}: fcj: {fcj_H1}')
    print(f'H{usina}: hb: {hb_lista_1}')
    Vmin = int(lim_hidro.iloc[usina-1, 2])
    Vmax = int(lim_hidro.iloc[usina-1, 3])

exit()
# QUESTÃO 3 ###################################
print('####################### QUESTÃO 3 ##########################')
unidades_1 = int(lim_hidro.iloc[0, 5])
unidades_2 = int(lim_hidro.iloc[1, 5])
unidades_3 = int(lim_hidro.iloc[2, 5])
h_1 = float(coef_perda_hidraulica.iloc[0, 1])
h_2 = float(coef_perda_hidraulica.iloc[0, 2])
h_3 = float(coef_perda_hidraulica.iloc[0, 3])
i0 = float(coef_rend_hidraulico.iloc[0, 1])
i1 = float(coef_rend_hidraulico.iloc[0, 2])
i2 = float(coef_rend_hidraulico.iloc[0, 3])
i3 = float(coef_rend_hidraulico.iloc[0, 4])
i4 = float(coef_rend_hidraulico.iloc[0, 5])
i5 = float(coef_rend_hidraulico.iloc[0, 6])
print(unidades_1)
print(unidades_2)
print(unidades_3)
print(h_1)
print(h_2)
print(h_3)
print(i0)
print(i1)
print(i2)
print(i3)
print(i4)
print(i5)

for i in range(12):
    q = int(dados_termeletricas1.iloc[i, 3])
    w_itn_1 = q/unidades_1
    hl_itn_1 = hb_lista_1[i] - h_1*w_itn_1
    i11 = (i1*w_itn_1)
    i22 = (i2*hl_itn_1)
    i33 = (i3*w_itn_1*hl_itn_1)
    i44 = (i4*(w_itn_1**2))
    i55 = (i5*(hl_itn_1**2))
    r_itn_1 = i0 + i11 + i22 + i33 + i44 + i55
    gh_itn = 0.00981*r_itn_1*hl_itn_1*w_itn_1
