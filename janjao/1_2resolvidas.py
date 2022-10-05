import pandas as pd
import numpy as np

dados_termeletricas = [['GT(mín/máx)(MW)', '100/500', '50/500', '0/infinito'],
                       ['A(R$/MWh)', '15', '250', '3000'],
                       ['B(R$)', '1000', '100', '0'],
                       ['T(on/off)', '8/4', '6/6', '0/0'],
                       ['C(MW/h)', '50', '75', 'infinito']]

limites = [['1', '0', '2300', '3340', '3', '300', '430'],
           ['2', '1', '4300', '5100', '5', '200', '300'],
           ['3', '2', '1420', '1500', '4', '150', '210']]

coef_fcm = [['1', '401.217', '0.0500965', '-0.0000157', '3.30e-09', '-2.88e-13'],
            ['2', '331.649', '0.0075202', '0', '0', '0'],
            ['3', '244.787', '0.0134591', '0', '0', '0']]

coef_fcj = [['1', '371.936', '0.00193242', '-8.530000e-8', '2.38e-12', '-2.62e-17'],
            ['2', '261.363', '0.00301186', '-0.000000564', '6.79e-11', '-3.03e-15'],
            ['3', '210.708', '0.00154505', '-0.000000159', '1.22e-11', '-3.69e-16']]

coef_perda_hidraulica = [['H', '7.5e-6', '2.2e-5', '5.0e-6']]

coef_funcao_rendimento_hidraulico = [['1', '0.3587300', '0.0023513', '0.0036111', '0.0000081', '-0.0000049', '-0.00003120'],
                                     ['2', '0.2518621', '0.0028912', '0.0065000','0.0000186', '-0.0000092', '-0.00005650'],
                                     ['3', '-6.65554162', '0.03689946', '0', '0', '-0.00004493', '0']]

dados_afluencias = [['1', '1.15', '-300', '300'],
                    ['2', '0.80', '150', '500'],
                    ['3', '1.10', '-200', '100']]

dados_velocidade_ventos = [['0.15', '20', '5']]

dados_geracao_eolica = [['0.55', '1000']]

dados_demanda_em_cada_estagio = [['1', '2750'],
                                 ['2', '3200'],
                                 ['3', '2800'],
                                 ['4', '2400'],
                                 ['5', '2100'],
                                 ['6', '1900'],
                                 ['7', '2300'],
                                 ['8', '2450'],
                                 ['9', '2700'],
                                 ['10', '3300'],
                                 ['11', '3200'],
                                 ['12', '3350']]

vazao_turbinada_para_cada_usina = [['1', '1050', '850', '1150'],
                                   ['2', '1100', '1100', '1275'],
                                   ['3', '900', '1200', '880'],
                                   ['4', '800', '1050', '760'],
                                   ['5', '1025', '800', '375'],
                                   ['6', '700', '800', '390'],
                                   ['7', '750', '700', '780'],
                                   ['8', '430', '620', '1500'],
                                   ['9', '360', '550', '1800'],
                                   ['10', '690', '900', '1650'],
                                   ['11', '750', '1050', '1300'],
                                   ['12', '1100', '1150', '1100']]

df1 = pd.DataFrame(dados_termeletricas, columns=['Usina', '1', '2', '3'])
df2 = pd.DataFrame(limites, columns=['Usina', 'Montante', 'Volume Mínimo', 'Volume Máximo', 'Unidades', 'Faixa Operativa Mínima', 'Faixa Operativa Máxima'])
df3 = pd.DataFrame(coef_fcm, columns=['Usina', 'F0', 'F1', 'F2', 'F3', 'F4'])
df4 = pd.DataFrame(coef_fcj, columns=['Usina', 'G0', 'G1', 'G2', 'F3', 'F4'])
df5 = pd.DataFrame(coef_perda_hidraulica, columns=['Usina', '1', '2', '3'])
df6 = pd.DataFrame(coef_funcao_rendimento_hidraulico, columns=['Usina', 'I0', 'I1', 'I2', 'I3', 'I4', 'I5'])
df7 = pd.DataFrame(dados_afluencias, columns=['Usina', 'phi', 'a', 'b'])
df8 = pd.DataFrame(dados_velocidade_ventos, columns=['phi', '(média)', '(Desvio Padrão)'])
df9 = pd.DataFrame(dados_geracao_eolica, columns=['Cp', 'AR(m^2)'])
df10 = pd.DataFrame(dados_demanda_em_cada_estagio, columns=['t', 'Lt'])
df11 = pd.DataFrame(vazao_turbinada_para_cada_usina, columns=['Estágio', 'H1', 'H2', 'H3'])

################################### QUESTÃO 1 ###################################
print('################################### QUESTÃO 1 ###################################')
#USINAS: 0,1,2 (começa no 0 devido ao index da matriz do pandas)
#AFLUENCIAS INICIAIS: 1500,1000,900 (valores fornecidos pelo professor)
def afluenciahidro(usina,afluencia_inicial):
    afluencialista = []
    phi = df7.iloc[usina, 1]
    a = df7.iloc[usina, 2]
    b = df7.iloc[usina, 3]
    afluencia_0 = afluencia_inicial
    random = np.random.uniform(int(a), int(b))
    afluencia_1 = int(float(phi)*afluencia_0 + random)
    afluencialista.append(afluencia_1)
    for i in range(11):
        random = np.random.uniform(int(a), int(b))
        afluencia = int(float(phi)*afluencialista[i] + random)
        afluencialista.append(afluencia)
    print(f'afluenciahidro {usina+1}: {afluencialista}')
    return afluencialista

afluencia_1 = afluenciahidro(0, 1500)
afluencia_2 = afluenciahidro(1, 1000)
afluencia_3 = afluenciahidro(2, 900)

#VELOCIDADE DO VENTO INICIAL: 25 (valor fornecido pelo professor)
#massa especifica do ar: 1225
velocidadeventolista = []
ro = 1225
phi = float(df8.iloc[0, 0])
media = int(df8.iloc[0, 1])
desviopadrao = int(df8.iloc[0, 2])
coefpotencia = float(df9.iloc[0, 0])
areacaptacao = int(df9.iloc[0, 1])
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

################################### QUESTÃO 2 ###################################
print('################################### QUESTÃO 2 ###################################')
print('########### HIDRELÉTRICA 1 ###############')
# AFLUENCIAS INICIAIS: 1500,1000,900 (valores fornecidos pelo professor)
vol_min = int(df2.iloc[0, 2])
vol_max = int(df2.iloc[0, 3])
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
    q = int(df11.iloc[i, 1])
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
f0 = float(df3.iloc[0, 1])
f1 = float(df3.iloc[0, 2])
f2 = float(df3.iloc[0, 3])
f3 = float(df3.iloc[0, 4])
f4 = float(df3.iloc[0, 5])
g0 = float(df4.iloc[0, 1])
g1 = float(df4.iloc[0, 2])
g2 = float(df4.iloc[0, 3])
g3 = float(df4.iloc[0, 4])
g4 = float(df4.iloc[0, 5])

for i in range(12):
    q = int(df11.iloc[i, 1])
    fcm = f0 + f1*volume_medio_lista_1[i] + (f2*(volume_medio_lista_1[i])**2) + (f3*(volume_medio_lista_1[i])**3) + (f4*(volume_medio_lista_1[i])**4)
    fcm = round(fcm, 2)
    fcm_lista_1.append(fcm)
    fcj = g0 + g1*(q+vazao_vertida_1[i]) + (g2*(q+vazao_vertida_1[i])**2) + (g3*(q+vazao_vertida_1[i])**3) + (g4*(q+vazao_vertida_1[i])**4)
    fcj = round(fcj, 2)
    fcj_lista_1.append(fcj)
    hb = fcm - fcj
    hb = round(hb, 2)
    hb_lista_1.append(hb)
print(f'fcm_lista_1: {fcm_lista_1}')
print(f'fcj_lista_1: {fcj_lista_1}')
print(f'hb_lista_1: {hb_lista_1}')

########### HIDRELÉTRICA 2 ###############
print('########### HIDRELÉTRICA 2 ###############')
vol_min = int(df2.iloc[1, 2])
vol_max = int(df2.iloc[1, 3])
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
    q_1 = int(df11.iloc[i, 1])
    q = int(df11.iloc[i, 2])
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
f0 = float(df3.iloc[1, 1])
f1 = float(df3.iloc[1, 2])
f2 = float(df3.iloc[1, 3])
f3 = float(df3.iloc[1, 4])
f4 = float(df3.iloc[1, 5])
g0 = float(df4.iloc[1, 1])
g1 = float(df4.iloc[1, 2])
g2 = float(df4.iloc[1, 3])
g3 = float(df4.iloc[1, 4])
g4 = float(df4.iloc[1, 5])

for i in range(12):
    q = int(df11.iloc[i, 2])
    fcm = f0 + f1*volume_medio_lista_2[i] + (f2*(volume_medio_lista_2[i])**2) + (f3*(volume_medio_lista_2[i])**3) + (f4*(volume_medio_lista_2[i])**4)
    fcm = round(fcm, 2)
    fcm_lista_2.append(fcm)
    fcj = g0 + g1*(q+vazao_vertida_2[i]) + (g2*(q+vazao_vertida_2[i])**2) + (g3*(q+vazao_vertida_2[i])**3) + (g4*(q+vazao_vertida_2[i])**4)
    fcj = round(fcj, 2)
    fcj_lista_2.append(fcj)
    hb = fcm - fcj
    hb = round(hb, 2)
    hb_lista_2.append(hb)
print(f'fcm_lista_2: {fcm_lista_2}')
print(f'fcj_lista_2: {fcj_lista_2}')
print(f'hb_lista_2: {hb_lista_2}')

########### HIDRELÉTRICA 3 ###############
print('########### HIDRELÉTRICA 3 ###############')
vol_min = int(df2.iloc[2, 2])
vol_max = int(df2.iloc[2, 3])
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
    q_2 = int(df11.iloc[i, 2])
    q = int(df11.iloc[i, 3])
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
f0 = float(df3.iloc[2, 1])
f1 = float(df3.iloc[2, 2])
f2 = float(df3.iloc[2, 3])
f3 = float(df3.iloc[2, 4])
f4 = float(df3.iloc[2, 5])
g0 = float(df4.iloc[2, 1])
g1 = float(df4.iloc[2, 2])
g2 = float(df4.iloc[2, 3])
g3 = float(df4.iloc[2, 4])
g4 = float(df4.iloc[2, 5])

for i in range(12):
    q = int(df11.iloc[i, 3])
    fcm = f0 +(f1*(volume_medio_lista_3[i]))+(f2*(volume_medio_lista_3[i])**2)+(f3*(volume_medio_lista_3[i])**3)+(f4*(volume_medio_lista_3[i])**4)
    fcm = round(fcm, 2)
    fcm_lista_3.append(fcm)
    fcj = g0 + (g1*(q+vazao_vertida_3[i]))+(g2*(q+vazao_vertida_3[i])**2)+(g3*(q+vazao_vertida_3[i])**3)+(g4*(q+vazao_vertida_3[i])**4)
    fcj = round(fcj, 2)
    fcj_lista_3.append(fcj)
    hb = fcm - fcj
    hb = round(hb, 2)
    hb_lista_3.append(hb)

print(f'fcm_lista_3: {fcm_lista_3}')
print(f'fcj_lista_3: {fcj_lista_3}')
print(f'hb_lista_3: {hb_lista_3}')

################################### QUESTÃO 3 ###################################
print('################################### QUESTÃO 3 ###################################')
unidades_1 = int(df2.iloc[0, 5])
unidades_2 = int(df2.iloc[1, 5])
unidades_3 = int(df2.iloc[2, 5])
h_1 = float(df5.iloc[0, 1])
h_2 = float(df5.iloc[0, 2])
h_3 = float(df5.iloc[0, 3])
i0 = float(df6.iloc[0, 1])
i1 = float(df6.iloc[0, 2])
i2 = float(df6.iloc[0, 3])
i3 = float(df6.iloc[0, 4])
i4 = float(df6.iloc[0, 5])
i5 = float(df6.iloc[0, 6])
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
    q = int(df11.iloc[i, 3])
    w_itn_1 = q/unidades_1
    hl_itn_1 = hb_lista_1[i] - h_1*w_itn_1
    r_itn_1 = i0 + (i1*w_itn_1) + (i2*hl_itn_1) + (i3**w_itn_1*hl_itn_1) + (i4*(w_itn_1**2)) + (i5*(hl_itn_1**2))
    gh_itn = 0.00981*r_itn_1*hl_itn_1*w_itn_1
