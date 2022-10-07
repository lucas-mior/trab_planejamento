#!/usr/bin/python

import pandas as pd
import numpy as np

dados_termeletricas = pd.DataFrame({
    'usina': [1, 2, 3],
    'GTmin': [100, 50, 0],
    'GTmax': [500, 500, 'infinito'],
    'A(R$/MWh)': [15, 250, 3000],
    'B(R$)': [1000, 100, 0],
    'T(on)': [8,    6,   0],
    'T(off)': [4, 6, 0],
    'C(MW/h)': [50, 75, 'infinito']})

lim_hidro = pd.DataFrame({
    'usina': [1, 2, 3],
    'montante': [0, 1, 2],
    'vol_min': [2300, 4300, 1420],
    'vol_max': [3340, 5100, 1500],
    'unidades': [3, 5, 4],
    'faixa_oper_min': [300, 200, 150],
    'faixa_oper_max': [430, 300, 210]})

coef_fcm = pd.DataFrame({
    'usina': [1, 2, 3],
    'F0': [401.217, 331.649, 244.787],
    'F1': [0.0500965, 0.0075202, 0.0134591],
    'F2': [-0.0000157, 0, 0],
    'F3': [3.30e-09, 0, 0],
    'F4': [-2.88e-13, 0, 0]})

coef_fcj = pd.DataFrame({
    'usina': [1, 2, 3],
    'G0':  [371.936,  261.363,  210.708],
    'G1':  [0.00193242,  0.00301186,  0.00154505],
    'G2':  [-8.530000e-8,  -0.000000564,  -0.000000159],
    'G3':  [2.38e-12,  6.79e-11,  1.22e-11],
    'G4':  [-2.62e-17,  -3.03e-15,  -3.69e-16]})

print(dados_termeletricas.head())

coef_perda_hidraulica = pd.DataFrame({
    'usina': [1, 2, 3],
    'perda': [7.5e-6, 2.2e-5, 5.0e-6]})

coef_rend_hidraulico = pd.DataFrame({
    'usina': [1, 2, 3],
    'I0': [0.3587300, 0.2518621, -6.65554162],
    'I1': [0.0023513, 0.0028912, 0.03689946],
    'I2': [0.0036111, 0.0065000, 0],
    'I3': [0.0000081, 0.0000186, 0],
    'I4': [-0.0000049, -0.0000092, -0.00004493],
    'I5': [-0.00003120, -0.00005650, 0]})

dados_afluencias = pd.DataFrame({
    'usina': [1, 2, 3],
    'phi': [1.15,  0.80,  1.10],
    'a': [-300,  150,  -200],
    'b': [300,  500,  100]})

dados_velocidade_ventos = {
    'phi': 0.15,
    'eta_media': 20,
    'eta_desvio': 5
}

dados_geracao_eolica = {
    'Cp': 0.55,
    'AR': 1000,
}

demanda = [2750, 3200, 2800, 2400,
           2100, 1900, 2300, 2450,
           2700, 3300, 3200, 3350]

vazao_por_usina = pd.DataFrame({
    'estagio': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12],
    'H1': [1050, 1100, 900, 800, 1025, 700, 750, 430, 360, 690, 750, 1100],
    'H2': [850, 1100, 1200, 1050, 800, 800, 700, 620, 550, 900, 1050, 1150],
    'H3': [1150, 1275, 880, 760, 375, 390, 780, 1500, 1800, 1650, 1300, 1100]})

print(vazao_por_usina)

# QUESTÃO 1 ###################################
print('######################## QUESTÃO 1 #######################')
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


afluencia_1 = afluenciahidro(0, 1500)
afluencia_2 = afluenciahidro(1, 1000)
afluencia_3 = afluenciahidro(2, 900)

exit()

velocidadeventolista = []  # VELOCIDADE DO VENTO INICIAL: 25 (fornecido)
ro = 1225  # massa especifica do ar: 1225
phi = dados_velocidade_ventos['phi']
media = dados_velocidade_ventos['eta_media']
desviopadrao = dados_velocidade_ventos['eta_desvio']
coefpotencia = dados_geracao_eolica['Cp']
areacaptacao = dados_geracao_eolica['AR']
zeta = np.random.normal(20, 5, 12)
sw_0 = int(phi*25+zeta[0])
if sw_0 > 25:
    sw_0 = 0
if sw_0 < 3:
    sw_0 = 0
velocidadeventolista.append(sw_0)

for i in range(11):
    sw = int(phi*velocidadeventolista[i]+float(zeta[i+1]))
    if sw > 25:
        sw = 0
    if sw < 3:
        sw = 0
    velocidadeventolista.append(sw)

print(f'velocidade do vento: {velocidadeventolista}')
potenciaventolista = []
potenciatotalventolista = []

for i in range(12):
    gw = int((ro*areacaptacao*(velocidadeventolista[i]**3)*coefpotencia)/2)
    gw = int(1e-6*gw)  # convertendo de W para MW
    potenciaventolista.append(gw)
    gw = 40*gw
    potenciatotalventolista.append(gw)

print(f'potencia do aero: {potenciaventolista}')
print(f'potencia total do parque: {potenciatotalventolista}')

# QUESTÃO 2 ###################################
print('######################### QUESTÃO 2 ###########################')
print('########### HIDRELÉTRICA 1 ###############')
# AFLUENCIAS INICIAIS: 1500,1000,900 (valores fornecidos pelo professor)
vol_min = int(lim_hidro.iloc[0, 2])
vol_max = int(lim_hidro.iloc[0, 3])
volume_final_1 = []
vazao_vertida_1 = []
c = float((2*60*60)/(1e6))
vol_0 = float(vol_min + 0.35*(vol_max-vol_min))
q_0 = 800  # VAZAO TURBINADA DA HIDRELETRICA 1 NO INSTANTE 0 = 800
s_0 = 0  # VERTIMENTO DA HIDRELETRICA 1 NO INSTANTE 0 =  0
vol_final = float(vol_0-c*(q_0+s_0-1500))
vol_final = round(vol_final, 2)
volume_final_1.append(vol_final)

if vol_final > vol_max:
    s = vol_max-vol_final
    vazao_vertida_1.append(s)
    vol_final = vol_max
else:
    s = 0
    vazao_vertida_1.append(s)
    vol_final = vol_final

count = 0

for i in range(12):
    q = int(dados_termeletricas1.iloc[i, 1])
    vol_final = float(vol_final-c*(q+vazao_vertida_1[i]-int(afluencia_1[i])))
    count += 1
    if vol_final > vol_max:
        s = vol_max-vol_final
        vazao_vertida_1.append(s)
        print(f'vertimento de {s} no estágio: {count}')
        vol_final = vol_max
    else:
        s = 0
        vazao_vertida_1.append(s)
        vol_final = vol_final
    vol_final = round(vol_final, 2)
    volume_final_1.append(vol_final)

print(f'vazao_vertida_1: {vazao_vertida_1}')
print(f'volumes_finais_1: {volume_final_1}')
volume_medio_lista_1 = []

for i in range(12):
    volume_medio = (volume_final_1[i]+volume_final_1[i+1])/2
    volume_medio = round(volume_medio, 2)
    volume_medio_lista_1.append(volume_medio)

print(f'volume_medio_1: {volume_medio_lista_1}')
fcm_lista_1 = []
fcj_lista_1 = []
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
    q = int(dados_termeletricas1.iloc[i, 1])
    f11 = f1*volume_medio_lista_1[i]
    f22 = f2*(volume_medio_lista_1[i])**2
    f33 = f3*(volume_medio_lista_1[i])**3
    f44 = f4*(volume_medio_lista_1[i])**4
    fcm = f0 + f11 + f22 + f33 + f44
    fcm = round(fcm, 2)
    fcm_lista_1.append(fcm)

    g11 = g1*(q+vazao_vertida_1[i])
    g22 = g2*(q+vazao_vertida_1[i])**2
    g33 = g3*(q+vazao_vertida_1[i])**3
    g44 = g4*(q+vazao_vertida_1[i])**4
    fcj = g0 + g11 + g22 + g33 + g44
    fcj = round(fcj, 2)
    fcj_lista_1.append(fcj)

    hb = fcm - fcj
    hb = round(hb, 2)
    hb_lista_1.append(hb)

print(f'fcm_lista_1: {fcm_lista_1}')
print(f'fcj_lista_1: {fcj_lista_1}')
print(f'hb_lista_1: {hb_lista_1}')

# HIDRELÉTRICA 2 ###############
print('########### HIDRELÉTRICA 2 ###############')
vol_min = int(lim_hidro.iloc[1, 2])
vol_max = int(lim_hidro.iloc[1, 3])
volume_final_2 = []
vazao_vertida_2 = []
c = float((2*60*60)/(1e6))
vol_0 = float(vol_min + 0.35*(vol_max-vol_min))
q_0 = 800  # VAZAO TURBINADA DA HIDRELETRICA 1 NO INSTANTE 0 = 800
s_0 = 0  # VERTIMENTO DA HIDRELETRICA 1 NO INSTANTE 0 =  0
vol_final = float(vol_0-c*(0+0-1000))+c*(q_0+s_0)
vol_final = round(vol_final, 2)
volume_final_2.append(vol_final)
if vol_final > vol_max:
    s = vol_max-vol_final
    s = round(s, 2)
    vazao_vertida_2.append(s)
    vol_final = vol_max
else:
    s = 0
    vazao_vertida_2.append(s)
    vol_final = vol_final
count = 0

for i in range(12):
    q_1 = int(dados_termeletricas1.iloc[i, 1])
    q = int(dados_termeletricas1.iloc[i, 2])
    vol_final = float(vol_final-c*(q+vazao_vertida_2[i]-int(afluencia_2[i]))) + c*(q_1+vazao_vertida_1[i])
    count += 1
    if vol_final > vol_max:
        s = vol_max-vol_final
        s = round(s, 2)
        vazao_vertida_2.append(s)
        vol_final = vol_max
    else:
        s = 0
        vazao_vertida_2.append(s)
        vol_final = vol_final
    vol_final = round(vol_final, 2)
    volume_final_2.append(vol_final)

print(f'vazao_vertida_2: {vazao_vertida_2}')
print(f'volumes_finais_2: {volume_final_2}')
volume_medio_lista_2 = []

for i in range(12):
    volume_medio = (volume_final_2[i]+volume_final_2[i+1])/2
    volume_medio = round(volume_medio, 2)
    volume_medio_lista_2.append(volume_medio)

print(f'volume_medio_2: {volume_medio_lista_2}')
fcm_lista_2 = []
fcj_lista_2 = []
hb_lista_2 = []
f0 = float(coef_fcm.iloc[1, 1])
f1 = float(coef_fcm.iloc[1, 2])
f2 = float(coef_fcm.iloc[1, 3])
f3 = float(coef_fcm.iloc[1, 4])
f4 = float(coef_fcm.iloc[1, 5])
g0 = float(coef_fcj.iloc[1, 1])
g1 = float(coef_fcj.iloc[1, 2])
g2 = float(coef_fcj.iloc[1, 3])
g3 = float(coef_fcj.iloc[1, 4])
g4 = float(coef_fcj.iloc[1, 5])

for i in range(12):
    q = int(dados_termeletricas1.iloc[i, 2])
    f11 = f1*volume_medio_lista_2[i]
    f22 = f2*(volume_medio_lista_2[i])**2
    f33 = f3*(volume_medio_lista_2[i])**3
    f44 = f4*(volume_medio_lista_2[i])**4
    fcm = f0 + f11 + f22 + f33 + f44
    fcm = round(fcm, 2)
    fcm_lista_2.append(fcm)

    g11 = g1*(q+vazao_vertida_2[i])
    g22 = g2*(q+vazao_vertida_2[i])**2
    g33 = g3*(q+vazao_vertida_2[i])**3
    g44 = g4*(q+vazao_vertida_2[i])**4
    fcj = g0 + g11 + g22 + g33 + g44
    fcj = round(fcj, 2)
    fcj_lista_2.append(fcj)

    hb = fcm - fcj
    hb = round(hb, 2)
    hb_lista_2.append(hb)

print(f'fcm_lista_2: {fcm_lista_2}')
print(f'fcj_lista_2: {fcj_lista_2}')
print(f'hb_lista_2: {hb_lista_2}')

# HIDRELÉTRICA 3 ###############
print('########### HIDRELÉTRICA 3 ###############')
vol_min = int(lim_hidro.iloc[2, 2])
vol_max = int(lim_hidro.iloc[2, 3])
volume_final_3 = []
vazao_vertida_3 = []
c = float((2*60*60)/(1e6))
vol_0 = float(vol_min + 0.35*(vol_max-vol_min))
q_0 = 800  # VAZAO TURBINADA DA HIDRELETRICA 1 NO INSTANTE 0 = 800
s_0 = 0  # VERTIMENTO DA HIDRELETRICA 1 NO INSTANTE 0 =  0
vol_final = float(vol_0-c*(0+0-900))+c*(q_0+s_0)
vol_final = round(vol_final, 2)
volume_final_3.append(vol_final)
if vol_final > vol_max:
    s = vol_max-vol_final
    s = round(s, 2)
    vazao_vertida_3.append(s)
    vol_final = vol_max
else:
    s = 0
    vazao_vertida_3.append(s)
    vol_final = vol_final
count = 0

for i in range(12):
    q_2 = int(dados_termeletricas1.iloc[i, 2])
    q = int(dados_termeletricas1.iloc[i, 3])
    vol_final = float(vol_final-c*(q+vazao_vertida_3[i]-int(afluencia_3[i]))) + c*(q_1+vazao_vertida_1[i])
    count += 1
    if vol_final > vol_max:
        s = vol_max-vol_final
        s = round(s, 2)
        vazao_vertida_3.append(s)
        vol_final = vol_max
    else:
        s = 0
        vazao_vertida_3.append(s)
        vol_final = vol_final
    vol_final = round(vol_final, 2)
    volume_final_3.append(vol_final)

print(f'vazao_vertida_3: {vazao_vertida_3}')
print(f'volumes_finais_3: {volume_final_3}')
volume_medio_lista_3 = []

for i in range(12):
    volume_medio = (volume_final_3[i]+volume_final_3[i+1])/2
    volume_medio = round(volume_medio, 2)
    volume_medio_lista_3.append(volume_medio)

print(f'volume_medio_3: {volume_medio_lista_3}')
fcm_lista_3 = []
fcj_lista_3 = []
hb_lista_3 = []
f0 = float(coef_fcm.iloc[2, 1])
f1 = float(coef_fcm.iloc[2, 2])
f2 = float(coef_fcm.iloc[2, 3])
f3 = float(coef_fcm.iloc[2, 4])
f4 = float(coef_fcm.iloc[2, 5])
g0 = float(coef_fcj.iloc[2, 1])
g1 = float(coef_fcj.iloc[2, 2])
g2 = float(coef_fcj.iloc[2, 3])
g3 = float(coef_fcj.iloc[2, 4])
g4 = float(coef_fcj.iloc[2, 5])

for i in range(12):
    q = int(dados_termeletricas1.iloc[i, 3])
    f11 = f1*(volume_medio_lista_3[i])
    f22 = f2*(volume_medio_lista_3[i])**2
    f33 = f3*(volume_medio_lista_3[i])**3
    f44 = f4*(volume_medio_lista_3[i])**4
    fcm = f0 + f11 + f22 + f33 + f44
    fcm = round(fcm, 2)
    fcm_lista_3.append(fcm)

    g11 = g1*(q+vazao_vertida_3[i])
    g22 = g2*(q+vazao_vertida_3[i])**2
    g33 = g3*(q+vazao_vertida_3[i])**3
    g44 = g4*(q+vazao_vertida_3[i])**4
    fcj = g0 + g11 + g22 + g33 + g44
    fcj = round(fcj, 2)
    fcj_lista_3.append(fcj)

    hb = fcm - fcj
    hb = round(hb, 2)
    hb_lista_3.append(hb)

print(f'fcm_lista_3: {fcm_lista_3}')
print(f'fcj_lista_3: {fcj_lista_3}')
print(f'hb_lista_3: {hb_lista_3}')

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
