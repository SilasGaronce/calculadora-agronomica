import kivy
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.spinner import Spinner
from kivy.uix.togglebutton import ToggleButton
from kivy.uix.tabbedpanel import TabbedPanel, TabbedPanelHeader
from kivy.core.window import Window

Window.softinput_mode = "below_target"

# ==========================================================
# CONSTANTES / FATORES
# ==========================================================
FATOR_CO_MO = 1.724
FATOR_K_MG_CMOLC = 391.0
FATOR_K_K2O = 940.0
FATOR_CA_CAO = 7.146
FATOR_MG_MGO = 6.031
FATOR_N_MIN = 18.0

class CalculadoraAgronomicaApp(App):
    def build(self):
        self.title = "Sistema de Interpretação de Solo"
        
        self.panel = TabbedPanel(do_default_tab=False)
        self.panel.tab_width = 130
        
        self.tab1 = TabbedPanelHeader(text="1. Físico")
        self.tab2 = TabbedPanelHeader(text="2. Química")
        self.tab3 = TabbedPanelHeader(text="3. Micros/Sub")
        self.tab4 = TabbedPanelHeader(text="4. Manejo")
        self.tab5 = TabbedPanelHeader(text="5. Laudo")
        
        self.panel.add_widget(self.tab1)
        self.panel.add_widget(self.tab2)
        self.panel.add_widget(self.tab3)
        self.panel.add_widget(self.tab4)
        self.panel.add_widget(self.tab5)
        
        self.inputs = {}
        
        self.build_tab1()
        self.build_tab2()
        self.build_tab3()
        self.build_tab4()
        self.build_tab5()
        
        self.panel.default_tab = self.tab1
        return self.panel

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

    def add_row(self, layout, label_text, input_key, default_val=""):
        lbl = Label(text=label_text, size_hint_y=None, height=40, halign='left', valign='middle')
        lbl.bind(size=lbl.setter('text_size'))
        inp = TextInput(text=str(default_val), multiline=False, size_hint_y=None, height=40)
        self.inputs[input_key] = inp
        layout.add_widget(lbl)
        layout.add_widget(inp)

    # ------------------------------------------------------
    # TAB 1: CULTURA E FÍSICO
    # ------------------------------------------------------
    def build_tab1(self):
        scroll = ScrollView()
        layout = GridLayout(cols=2, spacing=10, padding=10, size_hint_y=None)
        layout.bind(minimum_height=layout.setter('height'))
        
        layout.add_widget(Label(text="Cultura:", size_hint_y=None, height=40))
        self.cultura_spinner = Spinner(
            text="Soja",
            values=["Soja", "Milho", "Café", "Feijão", "Cana-de-açúcar", "Pastagem", "Outra"],
            size_hint_y=None, height=40
        )
        self.cultura_spinner.bind(text=self.atualizar_v2_padrao)
        layout.add_widget(self.cultura_spinner)
        
        self.add_row(layout, "Profundidade amostra (cm):", "prof_amostra", "20")
        self.add_row(layout, "Teor de argila (%):", "argila", "35")
        self.add_row(layout, "P-rem (mg/L) [n se n/a]:", "p_rem", "n")
        
        scroll.add_widget(layout)
        self.tab1.content = scroll

    def atualizar_v2_padrao(self, spinner, text):
        if hasattr(self, 'inputs') and "V2" in self.inputs:
            if text == "Café":
                self.inputs["V2"].text = "70.0"
            elif text == "Pastagem":
                self.inputs["V2"].text = "50.0"
            else:
                self.inputs["V2"].text = "60.0"

    # ------------------------------------------------------
    # TAB 2: QUÍMICA
    # ------------------------------------------------------
    def build_tab2(self):
        scroll = ScrollView()
        layout = GridLayout(cols=2, spacing=10, padding=10, size_hint_y=None)
        layout.bind(minimum_height=layout.setter('height'))
        
        self.add_row(layout, "pH em H2O:", "pH", "5.5")
        self.add_row(layout, "C.O. (%):", "CO", "1.5")
        self.add_row(layout, "Fósforo - P (mg/dm³):", "P", "15")
        
        layout.add_widget(Label(text="Unidade do K:", size_hint_y=None, height=40))
        k_box = BoxLayout(orientation='horizontal', size_hint_y=None, height=40)
        self.btn_k_mg = ToggleButton(text="mg/dm³", group="unid_k", state="down")
        self.btn_k_cmol = ToggleButton(text="cmolc/dm³", group="unid_k")
        k_box.add_widget(self.btn_k_mg)
        k_box.add_widget(self.btn_k_cmol)
        layout.add_widget(k_box)
        
        self.add_row(layout, "Valor de K:", "K_lido", "60")
        
        layout.add_widget(Label(text="Unidade Ca/Mg:", size_hint_y=None, height=40))
        camg_box = BoxLayout(orientation='horizontal', size_hint_y=None, height=40)
        self.btn_camg_cmol = ToggleButton(text="cmolc/dm³", group="unid_camg", state="down")
        self.btn_camg_mmol = ToggleButton(text="mmolc/dm³", group="unid_camg")
        camg_box.add_widget(self.btn_camg_cmol)
        camg_box.add_widget(self.btn_camg_mmol)
        layout.add_widget(camg_box)
        
        self.add_row(layout, "Valor de Ca:", "Ca_lido", "2.5")
        self.add_row(layout, "Valor de Mg:", "Mg_lido", "0.8")
        self.add_row(layout, "Sódio - Na (cmolc/dm³):", "Na", "n")
        self.add_row(layout, "Alumínio - Al³⁺ (cmolc/dm³):", "Al", "0.2")
        self.add_row(layout, "Acidez potencial - H+Al:", "H_Al", "3.0")
        self.add_row(layout, "Enxofre - S-SO4 (mg/dm³):", "S_SO4", "n")
        self.add_row(layout, "CEe (dS/m):", "CEe", "n")
        
        scroll.add_widget(layout)
        self.tab2.content = scroll

    # ------------------------------------------------------
    # TAB 3: MICROS E SUBSOLO
    # ------------------------------------------------------
    def build_tab3(self):
        scroll = ScrollView()
        layout = GridLayout(cols=2, spacing=10, padding=10, size_hint_y=None)
        layout.bind(minimum_height=layout.setter('height'))
        
        lbl_micros = Label(text="-- MICRONUTRIENTES --", size_hint_y=None, height=30, bold=True)
        layout.add_widget(lbl_micros)
        layout.add_widget(Label(text="", size_hint_y=None, height=30))
        
        self.add_row(layout, "Boro (B):", "val_B", "n")
        self.add_row(layout, "Cobre (Cu):", "val_Cu", "n")
        self.add_row(layout, "Ferro (Fe):", "val_Fe", "n")
        self.add_row(layout, "Manganês (Mn):", "val_Mn", "n")
        self.add_row(layout, "Zinco (Zn):", "val_Zn", "n")
        
        lbl_sub = Label(text="-- SUBSOLO --", size_hint_y=None, height=30, bold=True)
        layout.add_widget(lbl_sub)
        layout.add_widget(Label(text="", size_hint_y=None, height=30))
        
        self.add_row(layout, "Ca (Subsolo):", "Ca_sub", "n")
        self.add_row(layout, "Mg (Subsolo):", "Mg_sub", "n")
        self.add_row(layout, "K (Subsolo):", "K_sub", "n")
        self.add_row(layout, "Al (Subsolo):", "Al_sub", "n")
        
        scroll.add_widget(layout)
        self.tab3.content = scroll

    # ------------------------------------------------------
    # TAB 4: MANEJO
    # ------------------------------------------------------
    def build_tab4(self):
        scroll = ScrollView()
        layout = GridLayout(cols=2, spacing=10, padding=10, size_hint_y=None)
        layout.bind(minimum_height=layout.setter('height'))
        
        self.add_row(layout, "V% Alvo (V2):", "V2", "60.0")
        self.add_row(layout, "Meta de K na CTC (%):", "K_alvo", "3.0")
        self.add_row(layout, "PRNT do Calcário (%):", "PRNT", "90.0")
        self.add_row(layout, "Garantia CaO (%):", "CaO_gar", "35.0")
        self.add_row(layout, "Garantia MgO (%):", "MgO_gar", "15.0")
        self.add_row(layout, "Prof. Incorporação (cm):", "prof_inc", "20.0")
        self.add_row(layout, "Área de Aplicação (%):", "area_aplic", "100.0")
        
        layout.add_widget(Label(text="Método Calagem:", size_hint_y=None, height=40))
        met_box = BoxLayout(orientation='vertical', size_hint_y=None, height=80)
        self.btn_met_v = ToggleButton(text="Saturação por Bases", group="metodo_cal", state="down", height=40)
        self.btn_met_al = ToggleButton(text="Neutralização Al+Ca+Mg", group="metodo_cal", height=40)
        met_box.add_widget(self.btn_met_v)
        met_box.add_widget(self.btn_met_al)
        layout.add_widget(met_box)
        
        self.add_row(layout, "Exig. mín Ca+Mg (Método 2):", "exig_CaMg_cult", "0.0")
        
        btn_calc = Button(text="PROCESSAR CÁLCULOS", size_hint_y=None, height=50, background_color=(0.2, 0.7, 0.3, 1))
        btn_calc.bind(on_press=self.processar_calculos)
        
        layout.add_widget(Label(text="", size_hint_y=None, height=50))
        layout.add_widget(btn_calc)
        
        scroll.add_widget(layout)
        self.tab4.content = scroll

    # ------------------------------------------------------
    # TAB 5: LAUDO / RESULTADOS
    # ------------------------------------------------------
    def build_tab5(self):
        box = BoxLayout(orientation='vertical', padding=10, spacing=10)
        scroll = ScrollView()
        
        self.txt_resultado = Label(
            text="Preencha os dados e clique em 'PROCESSAR CÁLCULOS'.",
            size_hint_y=None,
            halign='left',
            valign='top',
            font_name='Roboto',
            font_size='14sp'
        )
        self.txt_resultado.bind(size=lambda s, w: setattr(s, 'text_size', (s.width, None)))
        self.txt_resultado.bind(texture_size=lambda s, w: setattr(s, 'height', w[1]))
        
        scroll.add_widget(self.txt_resultado)
        box.add_widget(scroll)
        
        btn_recalc = Button(text="Recalcular", size_hint_y=None, height=45)
        btn_recalc.bind(on_press=self.processar_calculos)
        box.add_widget(btn_recalc)
        
        self.tab5.content = box

    # ------------------------------------------------------
    # LÓGICA DE CÁLCULO
    # ------------------------------------------------------
    def processar_calculos(self, instance=None):
        try:
            argila = self.parse_val(self.inputs["argila"].text, 35.0) or 35.0
            pH = self.parse_val(self.inputs["pH"].text, 5.5) or 5.5
            CO = self.parse_val(self.inputs["CO"].text, 0.0) or 0.0
            P = self.parse_val(self.inputs["P"].text, 0.0) or 0.0
            
            K_lido_val = self.parse_val(self.inputs["K_lido"].text, 0.0) or 0.0
            is_k_mg = self.btn_k_mg.state == "down"
            K_cmolc = K_lido_val / FATOR_K_MG_CMOLC if is_k_mg else K_lido_val
            
            Ca_lido_val = self.parse_val(self.inputs["Ca_lido"].text, 0.0) or 0.0
            Mg_lido_val = self.parse_val(self.inputs["Mg_lido"].text, 0.0) or 0.0
            is_camg_mmol = self.btn_camg_mmol.state == "down"
            
            if is_camg_mmol:
                Ca = Ca_lido_val / 10.0
                Mg = Mg_lido_val / 10.0
            else:
                Ca = Ca_lido_val
                Mg = Mg_lido_val

            Na_val = self.parse_val(self.inputs["Na"].text, 0.0)
            Na = Na_val if Na_val is not None else 0.0
            
            Al = self.parse_val(self.inputs["Al"].text, 0.0) or 0.0
            H_Al = self.parse_val(self.inputs["H_Al"].text, 0.0) or 0.0

            MO = CO * FATOR_CO_MO
            N_est_kg = MO * FATOR_N_MIN
            
            SB = Ca + Mg + K_cmolc + Na
            t_efetiva = SB + Al
            T_potencial = SB + H_Al

            if T_potencial > 0:
                V1 = (SB / T_potencial) * 100.0
                perc_Ca = (Ca / T_potencial) * 100.0
                perc_Mg = (Mg / T_potencial) * 100.0
                perc_K = (K_cmolc / T_potencial) * 100.0
                PST = (Na / T_potencial) * 100.0
            else:
                V1 = perc_Ca = perc_Mg = perc_K = PST = 0.0

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

            PRNT = self.parse_val(self.inputs["PRNT"].text, 90.0) or 90.0
            V2 = self.parse_val(self.inputs["V2"].text, 60.0) or 60.0
            
            NC_V = ((V2 - V1) * T_potencial) / PRNT if V2 > V1 else 0.0
            
            exig_CaMg = self.parse_val(self.inputs["exig_CaMg_cult"].text, 0.0) or 0.0
            soma_CaMg = Ca + Mg
            
            if soma_CaMg < exig_CaMg:
                NC_Al = (fator_Y * Al) + (exig_CaMg - soma_CaMg)
            else:
                NC_Al = fator_Y * Al
                
            NC_Al = max(0.0, (NC_Al * 100.0) / PRNT)

            is_metodo_al = self.btn_met_al.state == "down"
            NC_final = NC_Al if is_metodo_al else NC_V

            prof_inc_val = self.parse_val(self.inputs["prof_inc"].text, 20.0) or 20.0
            area_aplic_val = self.parse_val(self.inputs["area_aplic"].text, 100.0) or 100.0
            
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
                "Boro (B)": self.parse_val(self.inputs["val_B"].text),
                "Cobre (Cu)": self.parse_val(self.inputs["val_Cu"].text),
                "Ferro (Fe)": self.parse_val(self.inputs["val_Fe"].text),
                "Manganês (Mn)": self.parse_val(self.inputs["val_Mn"].text),
                "Zinco (Zn)": self.parse_val(self.inputs["val_Zn"].text)
            }

            sub_Ca = self.parse_val(self.inputs["Ca_sub"].text)
            sub_Al = self.parse_val(self.inputs["Al_sub"].text)

            relatorio = "========================================\n"
            relatorio += "        LAUDO DE INTERPRETAÇÃO          \n"
            relatorio += "========================================\n\n"
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
            relatorio += f"Método escolhido: {'Neutralização Al' if is_metodo_al else 'Saturação Bases'}\n"
            relatorio += f"Dose calculada: {NC_final:.2f} t/ha\n"
            relatorio += f"Tipo de Calcário sugerido: {tipo_calcario}\n"
            relatorio += f"{rec_acidez}\n\n"

            relatorio += "--- MICRONUTRIENTES ---\n"
            for k, v in micros.items():
                val_txt = f"{v} mg/dm³" if v is not None else "Não analisado (n)"
                relatorio += f"{k}: {val_txt}\n"

            relatorio += "\n--- SUBSOLO / GESSAGEM ---\n"
            if sub_Ca is not None:
                relatorio += f"Ca Subsolo: {sub_Ca} cmolc/dm³\n"
                if sub_Al is not None:
                    relatorio += f"Al Subsolo: {sub_Al} cmolc/dm³\n"
                if sub_Ca < 0.5 or (sub_Al is not None and sub_Al > 0.5):
                    relatorio += "Recomendação: Indicado uso de gesso agrícola para melhoria do perfil do solo.\n"
                else:
                    relatorio += "Perfil do subsolo em condições favoráveis.\n"
            else:
                relatorio += "Análise de subsolo não informada (n).\n"

            self.txt_resultado.text = relatorio
            self.panel.switch_to(self.tab5)

        except Exception as e:
            self.txt_resultado.text = f"Erro nos dados inseridos: {str(e)}"
            self.panel.switch_to(self.tab5)

if __name__ == "__main__":
    CalculadoraAgronomicaApp().run()
