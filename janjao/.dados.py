import pandas as pd

dados_termeletricas = [['GT(mín/máx)(MW)', '100/500', '50/500', '0/infinito'],
            ['A(R$/MWh)', '15', '150', '2500'],
            ['B(R$)', '1000', '100', '0'],
            ['T(on/off)', '8/4', '6/6', '0/0'],
            ['C(MW/h)', '50', '75', 'infinito']]

limites = [['1', '0', '2300', '3340','3', '300', '430'],
            ['2', '1', '4300', '5100','5', '200', '300'],
            ['3', '2', '1420', '1500','4', '150', '210']]

coeficientes_da_fcm = [['1', '401,217', '0,0500965', '-0,0000157','3,30e-09', '-2,88e-13'],
            ['2', '331,649', '0,0075202', '0','0', '0'],
            ['3', '244,787', '0,0134591', '0','0', '0']]

coeficientes_da_fcj = [['1', '371,936', '0,00193242', '-8,530000e-8','2,38e-12', '-2,62e-17'],
            ['2', '261,363', '0,00301186', '-0,000000564','6,79e-11', '-3,03e-15'],
            ['3', '210,708', '0,00154505', '-0,000000159','1,22e-11', '-3,69e-16']]

coeficientes_de_perda_hidraulica = [['H', '7,5⋅10-6', '2,2⋅10-5', '5,0⋅10-6']]

coeficientes_da_funcao_rendimento_hidraulico = [['1', '0,3587300', '0,0023513', '0,0036111','0,0000081', '-0,0000049', '-0,00003120'],
            ['2', '0,2518621', '0,0028912', '0,0065000','0,0000186', '-0,0000092', '-0,00005650'],
            ['3', '-6,65554162', '0,03689946', '0','0', '-0,00004493', '0']]

dados_das_afluencias = [['1', '1,15', '-300', '300'],
            ['2', '0,80', '150', '500'],
            ['3', '1,10', '-400', '100']]

dados_de_velocidade_dos_ventos = [['0,15', '20', '5']]

dados_de_geracao_eolica = [['0,55', '1000']]

dados_de_demanda_em_cada_estagio = [['1', '2750'],
            ['2', '3300'],
            ['3', '2800'],
            ['4', '2400'],
            ['5', '2100'],
            ['6', '1900'],
            ['7', '2250'],
            ['8', '2450'],
            ['9', '2700'],
            ['10', '3400'],
            ['11', '3200'],
            ['12', '3300'],]

vazao_turbinada_para_cada_usina = [['1', '1050', '850', '1150'],
            ['2', '1100', '1.100', '1275'],
            ['3', '900', '1.200', '880'],
            ['4', '800', '1.050', '760'],
            ['5', '1025', '800', '375'],
            ['6', '700', '800', '390'],
            ['7', '750', '700', '780'],
            ['8', '430', '620', '1500'],
            ['9', '360', '550', '1800'],
            ['10', '690', '900', '1650'],
            ['11', '750', '1050', '1300'],
            ['12', '1100', '1150', '1100'],]

df1 = pd.DataFrame(dados_termeletricas, columns=['Usina', '1', '2','3'])
df2 = pd.DataFrame(limites, columns=['Usina','Montante','Volume Mínimo','Volume Máximo','Unidades','Faixa Operativa Mínima','Faixa Operativa Máxima'])
df3 = pd.DataFrame(coeficientes_da_fcm, columns=['Usina','F0','F1','F2','F3','F4'])
df4 = pd.DataFrame(coeficientes_da_fcj, columns=['Usina','G0','G1','G2','F3','F4'])
df5 = pd.DataFrame(coeficientes_de_perda_hidraulica, columns=['Usina','1','2','3'])
df6 = pd.DataFrame(coeficientes_da_funcao_rendimento_hidraulico, columns=['Usina','I0','I1','I2','I3','I4','I5'])
df7 = pd.DataFrame(dados_das_afluencias, columns=['Usina','phi','a','b'])
df8 = pd.DataFrame(dados_de_velocidade_dos_ventos, columns=['phi','(média)','(Desvio Padrão)'])
df9 = pd.DataFrame(dados_de_geracao_eolica, columns=['Cp','AR(m^2)'])
df10 = pd.DataFrame(dados_de_demanda_em_cada_estagio, columns=['t','Lt'])
df11 = pd.DataFrame(vazao_turbinada_para_cada_usina, columns=['Estágio','H1','H2','H3'])
print(df1)
print(df2)
print(df3)
print(df4)
print(df5)
print(df6)
print(df7)
print(df8)
print(df9)
print(df10)
print(df11)