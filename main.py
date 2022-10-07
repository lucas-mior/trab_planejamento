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
# AFLUENCIAS INICIAIS: 1500,1000,900 (valores fornecidos pelo professor)
usina = 1
Vmin = lim_hidro.loc[usina, 'vol_min']
Vmax = lim_hidro.loc[usina, 'vol_max']

volume_final_1 = []
vazao_vertida_1 = []
c = float((2*60*60)/(1e6))
vol_0 = float(Vmin + 0.35*(Vmax-Vmin))
q_0 = 800  # VAZAO TURBINADA DA HIDRELETRICA 1 NO INSTANTE 0 = 800
s_0 = 0  # VERTIMENTO DA HIDRELETRICA 1 NO INSTANTE 0 =  0
vol_final = float(vol_0-c*(q_0+s_0-1500))
vol_final = round(vol_final, 2)
volume_final_1.append(vol_final)

if vol_final > Vmax:
    s = Vmax-vol_final
    vazao_vertida_1.append(s)
    vol_final = Vmax
else:
    s = 0
    vazao_vertida_1.append(s)
    vol_final = vol_final

count = 0

for i in range(12):
    q = int(dados_termeletricas1.iloc[i, 1])
    vol_final = float(vol_final-c*(q+vazao_vertida_1[i]-int(afluencia_1[i])))
    count += 1
    if vol_final > Vmax:
        s = Vmax-vol_final
        vazao_vertida_1.append(s)
        print(f'vertimento de {s} no estágio: {count}')
        vol_final = Vmax
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

exit()

# HIDRELÉTRICA 2 ###############
print('########### HIDRELÉTRICA 2 ###############')
Vmin = int(lim_hidro.iloc[1, 2])
Vmax = int(lim_hidro.iloc[1, 3])
volume_final_2 = []
vazao_vertida_2 = []
c = float((2*60*60)/(1e6))
vol_0 = float(Vmin + 0.35*(Vmax-Vmin))
q_0 = 800  # VAZAO TURBINADA DA HIDRELETRICA 1 NO INSTANTE 0 = 800
s_0 = 0  # VERTIMENTO DA HIDRELETRICA 1 NO INSTANTE 0 =  0
vol_final = float(vol_0-c*(0+0-1000))+c*(q_0+s_0)
vol_final = round(vol_final, 2)
volume_final_2.append(vol_final)
if vol_final > Vmax:
    s = Vmax-vol_final
    s = round(s, 2)
    vazao_vertida_2.append(s)
    vol_final = Vmax
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
    if vol_final > Vmax:
        s = Vmax-vol_final
        s = round(s, 2)
        vazao_vertida_2.append(s)
        vol_final = Vmax
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
Vmin = int(lim_hidro.iloc[2, 2])
Vmax = int(lim_hidro.iloc[2, 3])
volume_final_3 = []
vazao_vertida_3 = []
c = float((2*60*60)/(1e6))
vol_0 = float(Vmin + 0.35*(Vmax-Vmin))
q_0 = 800  # VAZAO TURBINADA DA HIDRELETRICA 1 NO INSTANTE 0 = 800
s_0 = 0  # VERTIMENTO DA HIDRELETRICA 1 NO INSTANTE 0 =  0
vol_final = float(vol_0-c*(0+0-900))+c*(q_0+s_0)
vol_final = round(vol_final, 2)
volume_final_3.append(vol_final)
if vol_final > Vmax:
    s = Vmax-vol_final
    s = round(s, 2)
    vazao_vertida_3.append(s)
    vol_final = Vmax
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
    if vol_final > Vmax:
        s = Vmax-vol_final
        s = round(s, 2)
        vazao_vertida_3.append(s)
        vol_final = Vmax
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
