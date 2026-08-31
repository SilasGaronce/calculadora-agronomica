import kivy
from kivy.app import App
from kivy.uix.tabbedpanel import TabbedPanel, TabbedPanelItem
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.spinner import Spinner
from kivy.uix.scrollview import ScrollView

kivy.require('2.1.0')

FATOR_CO_MO = 1.724
FATOR_K_MG_CMOLC = 391.0
FATOR_K_K2O = 940.0
FATOR_CA_CAO = 7.146
FATOR_MG_MGO = 6.031
FATOR_N_MIN = 18.0

class SoloAppUI(TabbedPanel):
    def __init__(self, **kwargs):
        super(SoloAppUI, self).__init__(**kwargs)
        self.do_default_tab = False
        
        self.cultura_spinner = Spinner(text='Soja', values=('Soja', 'Milho', 'Café', 'Feijão', 'Cana-de-açúcar', 'Pastagem', 'Outra'))
        self.prof_amostra_input = TextInput(text='20', multiline=False)
        self.argila_input = TextInput(text='35', multiline=False)
        self.p_rem_input = TextInput(text='n', multiline=False)
        
        self.pH_input = TextInput(text='5.5', multiline=False)
        self.CO_input = TextInput(text='1.5', multiline=False)
        self.P_input = TextInput(text='15', multiline=False)
        
        self.unid_K_spinner = Spinner(text='mg/dm³', values=('mg/dm³', 'cmolc/dm³'))
        self.K_lido_input = TextInput(text='60', multiline=False)
        
        self.unid_CaMg_spinner = Spinner(text='cmolc/dm³', values=('cmolc/dm³', 'mmolc/dm³'))
        self.Ca_lido_input = TextInput(text='2.5', multiline=False)
        self.Mg_lido_input = TextInput(text='0.8', multiline=False)
        
        self.Na_input = TextInput(text='n', multiline=False)
        self.Al_input = TextInput(text='0.2', multiline=False)
        self.H_Al_input = TextInput(text='3.0', multiline=False)
        self.S_SO4_input = TextInput(text='n', multiline=False)
        self.CEe_input = TextInput(text='n', multiline=False)
        
        self.val_B_input = TextInput(text='n', multiline=False)
        self.val_Cu_input = TextInput(text='n', multiline=False)
        self.val_Fe_input = TextInput(text='n', multiline=False)
        self.val_Mn_input = TextInput(text='n', multiline=False)
        self.val_Zn_input = TextInput(text='n', multiline=False)
        
        self.Ca_sub_input = TextInput(text='n', multiline=False)
        self.Mg_sub_input = TextInput(text='n', multiline=False)
        self.K_sub_input = TextInput(text='n', multiline=False)
        self.Al_sub_input = TextInput(text='n', multiline=False)
        
        self.V2_input = TextInput(text='60.0', multiline=False)
        self.K_alvo_input = TextInput(text='3.0', multiline=False)
        self.PRNT_input = TextInput(text='90.0', multiline=False)
        self.CaO_gar_input = TextInput(text='35.0', multiline=False)
        self.MgO_gar_input = TextInput(text='15.0', multiline=False)
        self.prof_inc_input = TextInput(text='20.0', multiline=False)
        self.area_aplic_input = TextInput(text='100.0', multiline=False)
        
        self.metodo_spinner = Spinner(text='Saturação por Bases', values=('Saturação por Bases', 'Neutralização Al+Ca+Mg'))
        self.exig_CaMg_cult_input = TextInput(text='0.0', multiline=False)
        
        self.txt_resultado = Label(text='Preencha os dados e processe.', size_hint_y=None, height=800, text_size=(500, None))
        self.txt_resultado.bind(texture_size=lambda l, s: setattr(l, 'height', s[1]))

        self.add_widget(self.cria_aba_fisica())
        self.add_widget(self.cria_aba_quimica())
        self.add_widget(self.cria_aba_micros())
        self.add_widget(self.cria_aba_manejo())
        self.add_widget(self.cria_aba_resultados())

    def cria_aba_fisica(self):
        th = TabbedPanelItem(text='1. Física')
        layout = GridLayout(cols=2, spacing=10, padding=10, size_hint_y=None)
        layout.bind(minimum_height=layout.setter('height'))
        
        layout.add_widget(Label(text='Cultura:'))
        layout.add_widget(self.cultura_spinner)
        layout.add_widget(Label(text='Profundidade da amostra (cm):'))
        layout.add_widget(self.prof_amostra_input)
        layout.add_widget(Label(text='Teor de argila (%):'))
        layout.add_widget(self.argila_input)
        layout.add_widget(Label(text='P-rem (mg/L) [n se n/a]:'))
        layout.add_widget(self.p_rem_input)
        
        root = ScrollView()
        root.add_widget(layout)
        th.add_widget(root)
        return th

    def cria_aba_quimica(self):
        th = TabbedPanelItem(text='2. Química')
        layout = GridLayout(cols=2, spacing=10, padding=10, size_hint_y=None)
        layout.bind(minimum_height=layout.setter('height'))
        
        items = [
            ('pH em H2O:', self.pH_input),
            ('C.O. (%):', self.CO_input),
            ('Fósforo - P (mg/dm³):', self.P_input),
            ('Unidade do K:', self.unid_K_spinner),
            ('Valor de K:', self.K_lido_input),
            ('Unidade Ca/Mg:', self.unid_CaMg_spinner),
            ('Valor de Ca:', self.Ca_lido_input),
            ('Valor de Mg:', self.Mg_lido_input),
            ('Sódio - Na (cmolc/dm³):', self.Na_input),
            ('Alumínio - Al³⁺ (cmolc/dm³):', self.Al_input),
            ('Acidez potencial - H+Al:', self.H_Al_input),
            ('Enxofre - S-SO4 (mg/dm³):', self.S_SO4_input),
            ('CEe (dS/m):', self.CEe_input)
        ]
        for label, widget in items:
            layout.add_widget(Label(text=label))
            layout.add_widget(widget)
            
        root = ScrollView()
        root.add_widget(layout)
        th.add_widget(root)
        return th

    def cria_aba_micros(self):
        th = TabbedPanelItem(text='3. Micros')
        layout = GridLayout(cols=2, spacing=10, padding=10, size_hint_y=None)
        layout.bind(minimum_height=layout.setter('height'))
        
        items = [
            ('Boro (B):', self.val_B_input),
            ('Cobre (Cu):', self.val_Cu_input),
            ('Ferro (Fe):', self.val_Fe_input),
            ('Manganês (Mn):', self.val_Mn_input),
            ('Zinco (Zn):', self.val_Zn_input),
            ('Ca (Subsolo):', self.Ca_sub_input),
            ('Mg (Subsolo):', self.Mg_sub_input),
            ('K (Subsolo):', self.K_sub_input),
            ('Al (Subsolo):', self.Al_sub_input)
        ]
        for label, widget in items:
            layout.add_widget(Label(text=label))
            layout.add_widget(widget)
            
        root = ScrollView()
        root.add_widget(layout)
        th.add_widget(root)
        return th

    def cria_aba_manejo(self):
        th = TabbedPanelItem(text='4. Manejo')
        layout = GridLayout(cols=2, spacing=10, padding=10, size_hint_y=None)
        layout.bind(minimum_height=layout.setter('height'))
        
        items = [
            ('V% Alvo (V2):', self.V2_input),
            ('Meta de K na CTC (%):', self.K_alvo_input),
            ('PRNT do Calcário (%):', self.PRNT_input),
            ('Garantia CaO (%):', self.CaO_gar_input),
            ('Garantia MgO (%):', self.MgO_gar_input),
            ('Prof. Incorporação (cm):', self.prof_inc_input),
            ('Área de Aplicação (%):', self.area_aplic_input),
            ('Método de Calagem:', self.metodo_spinner),
            ('Exig. mín Ca+Mg:', self.exig_CaMg_cult_input)
        ]
        for label, widget in items:
            layout.add_widget(Label(text=label))
            layout.add_widget(widget)
            
        btn = Button(text='PROCESSAR CÁLCULOS', size_hint_y=None, height=50)
        btn.bind(on_press=self.processar_calculos)
        layout.add_widget(btn)
        layout.add_widget(Label(text=''))
        
        root = ScrollView()
        root.add_widget(layout)
        th.add_widget(root)
        return th

    def cria_aba_resultados(self):
        th = TabbedPanelItem(text='5. Resultados')
        layout = BoxLayout(orientation='vertical', spacing=10, padding=10, size_hint_y=None)
        layout.bind(minimum_height=layout.setter('height'))
        
        layout.add_widget(self.txt_resultado)
        btn = Button(text='Recalcular', size_hint_y=None, height=50)
        btn.bind(on_press=self.processar_calculos)
        layout.add_widget(btn)
        
        root = ScrollView()
        root.add_widget(layout)
        th.add_widget(root)
        return th

    def parse_val(self, val_str, default=0.0):
        if val_str is None:
            return default
        val_clean = str(val_str).strip().lower()
        if val_clean in ['', 'n', 'nao', 'não', '-', 'na']:
            return None
        try:
            return float(val_clean.replace(',', '.'))
        except ValueError:
            return default

    def processar_calculos(self, instance):
        try:
            argila = self.parse_val(self.argila_input.text, 20.0)
            pH = self.parse_val(self.pH_input.text, 5.5)
            CO = self.parse_val(self.CO_input.text, 1.0)
            
            K_lido_val = self.parse_val(self.K_lido_input.text, 0.0)
            unid_k_val = 1 if self.unid_K_spinner.text == 'mg/dm³' else 2
            K_cmolc = K_lido_val / FATOR_K_MG_CMOLC if unid_k_val == 1 else K_lido_val
            
            Ca_lido_val = self.parse_val(self.Ca_lido_input.text, 0.0)
            Mg_lido_val = self.parse_val(self.Mg_lido_input.text, 0.0)
            unid_camg_val = 1 if self.unid_CaMg_spinner.text == 'cmolc/dm³' else 2
            
            if unid_camg_val == 2:
                Ca = Ca_lido_val / 10.0
                Mg = Mg_lido_val / 10.0
            else:
                Ca = Ca_lido_val
                Mg = Mg_lido_val

            Na_val = self.parse_val(self.Na_input.text, 0.0)
            Na = Na_val if Na_val is not None else 0.0
            
            Al = self.parse_val(self.Al_input.text, 0.0)
            if Al is None: Al = 0.0
            
            H_Al = self.parse_val(self.H_Al_input.text, 0.0)
            if H_Al is None: H_Al = 0.0

            MO = CO * FATOR_CO_MO if CO is not None else 0.0
            N_est_kg = MO * FATOR_N_MIN
            
            SB = Ca + Mg + K_cmolc + Na
            t_efetiva = SB + Al
            T_potencial = SB + H_Al

            if T_potencial > 0:
                V1 = (SB / T_potencial) * 100.0
                perc_Ca = (Ca / T_potencial) * 100.0
                perc_Mg = (Mg / T_potencial) * 100.0
                perc_K = (K_cmolc / T_potencial) * 100.0
            else:
                V1 = perc_Ca = perc_Mg = perc_K = 0.0

            m_sat = (Al / t_efetiva) * 100.0 if t_efetiva > 0 else 0.0
            rel_CaMg = Ca / Mg if Mg > 0 else 999.0

            if pH < 5.0: classe_acidez = "Acidez muito alta"
            elif pH < 5.5: classe_acidez = "Acidez alta"
            elif pH < 6.0: classe_acidez = "Acidez moderada"
            elif pH <= 6.5: classe_acidez = "Faixa geralmente adequada"
            else: classe_acidez = "pH elevado"

            if argila < 15.0: fator_Y = 1.0
            elif argila < 35.0: fator_Y = 1.5
            elif argila < 60.0: fator_Y = 2.0
            else: fator_Y = 3.0

            PRNT = self.parse_val(self.PRNT_input.text, 90.0)
            V2 = self.parse_val(self.V2_input.text, 60.0)
            
            NC_V = ((V2 - V1) * T_potencial) / PRNT if V2 > V1 else 0.0
            
            exig_CaMg = self.parse_val(self.exig_CaMg_cult_input.text, 0.0)
            if exig_CaMg is None: exig_CaMg = 0.0
            soma_CaMg = Ca + Mg
            
            if soma_CaMg < exig_CaMg:
                NC_Al = (fator_Y * Al) + (exig_CaMg - soma_CaMg)
            else:
                NC_Al = fator_Y * Al
                
            NC_Al = max(0.0, (NC_Al * 100.0) / PRNT)

            metodo_val = 2 if self.metodo_spinner.text == 'Neutralização Al+Ca+Mg' else 1
            NC_final = NC_Al if metodo_val == 2 else NC_V

            prof_inc_val = self.parse_val(self.prof_inc_input.text, 20.0)
            area_aplic_val = self.parse_val(self.area_aplic_input.text, 100.0)
            NC_final = NC_final * (prof_inc_val / 20.0) * (area_aplic_val / 100.0)

            if NC_final > 0:
                rec_acidez = f"Aplicar {NC_final:.2f} t/ha de calcário."
                if Mg < 0.8 or perc_Mg < 10.0 or rel_CaMg > 4.5:
                    tipo_calcario = "Dolomítico (Fornecer Mg)"
                elif Mg > 1.5 or perc_Mg > 20.0 or rel_CaMg < 2.0:
                    tipo_calcario = "Calcítico (Fornecer Ca)"
                else:
                    tipo_calcario = "Magnesiano pode ser utilizado"
            else:
                rec_acidez = "Não há necessidade de calagem."
                tipo_calcario = "N/A"

            micros = {
                "Boro (B)": self.parse_val(self.val_B_input.text),
                "Cobre (Cu)": self.parse_val(self.val_Cu_input.text),
                "Ferro (Fe)": self.parse_val(self.val_Fe_input.text),
                "Manganês (Mn)": self.parse_val(self.val_Mn_input.text),
                "Zinco (Zn)": self.parse_val(self.val_Zn_input.text)
            }

            sub_Ca = self.parse_val(self.Ca_sub_input.text)
            sub_Al = self.parse_val(self.Al_sub_input.text)

            relatorio = "========================================================\n"
            relatorio += "                 LAUDO DE INTERPRETAÇÃO                 \n"
            relatorio += "========================================================\n\n"
            relatorio += f"CULTURA: {self.cultura_spinner.text}\n"
            relatorio += f"DIAGNÓSTICO DO pH: {classe_acidez} (pH {pH})\n"
            relatorio += f"MATÉRIA ORGÂNICA: {MO:.2f} %  | N Estimado: {N_est_kg:.2f} kg/ha\n\n"
            
            relatorio += "--- COMPLEXO SORTIVO ---\n"
            relatorio += f"Soma de Bases (SB): {SB:.2f} cmolc/dm³\n"
            relatorio += f"CTC Efetiva (t): {t_efetiva:.2f} cmolc/dm³\n"
            relatorio += f"CTC Potencial (T): {T_potencial:.2f} cmolc/dm³\n"
            relatorio += f"Saturação por Bases (V%): {V1:.2f}% (Alvo: {V2}%)\n"
            relatorio += f"Saturação por Alumínio (m%): {m_sat:.2f}%\n"
            relatorio += f"Relação Ca/Mg: {rel_CaMg:.2f}\n\n"
            
            relatorio += "--- RECOMENDAÇÃO DE CALAGEM ---\n"
            relatorio += f"Método escolhido: {'Neutralização Al' if metodo_val==2 else 'Saturação Bases'}\n"
            relatorio += f"Dose calculada: {NC_final:.2f} t/ha\n"
            relatorio += f"Tipo de Calcário sugerido: {tipo_calcario}\n"
            relatorio += f"{rec_acidez}\n\n"

            relatorio += "--- MICRONUTRIENTES ---\n"
            for k, v in micros.items():
                val_txt = f"{v} mg/dm³" if v is not None else "Não analisado (n)"
                relatorio += f"{k}: {val_txt}\n"

            relatorio += "\n--- AVALIAÇÃO DE SUBSOLO / GESSAGEM ---\n"
            if sub_Ca is not None:
                relatorio += f"Ca Subsolo: {sub_Ca} cmolc/dm³\n"
                if sub_Al is not None:
                    relatorio += f"Al Subsolo: {sub_Al} cmolc/dm³\n"
                if sub_Ca < 0.5 or (sub_Al is not None and sub_Al > 0.5):
                    relatorio += "Recomendação: Indicado uso de gesso agrícola.\n"
                else:
                    relatorio += "Perfil do subsolo em condições favoráveis.\n"
            else:
                relatorio += "Análise de subsolo não informada (n).\n"

            self.txt_resultado.text = relatorio
            self.current = self.tab_list[4].name
        except Exception as e:
            self.txt_resultado.text = f"Erro de Cálculo: {str(e)}"
            self.current = self.tab_list[4].name

class SistemaSoloApp(App):
    def build(self):
        return SoloAppUI()

if __name__ == '__main__':
    SistemaSoloApp().run()
