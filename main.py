import flet as ft

# ==========================================================
# CONSTANTES / FATORES
# ==========================================================
FATOR_CO_MO = 1.724
FATOR_K_MG_CMOLC = 391.0
FATOR_K_K2O = 940.0
FATOR_CA_CAO = 7.146
FATOR_MG_MGO = 6.031
FATOR_N_MIN = 18.0

def main(page: ft.Page):
    page.title = "Sistema de Interpretação de Solo - V5.2"
    page.vertical_alignment = ft.MainAxisAlignment.START
    page.scroll = ft.ScrollMode.AUTO
    page.window_width = 650
    page.window_height = 720

    # Variáveis / Inputs
    cultura_var = ft.Dropdown(
        label="Cultura",
        value="Soja",
        options=[
            ft.dropdown.Option("Soja"),
            ft.dropdown.Option("Milho"),
            ft.dropdown.Option("Café"),
            ft.dropdown.Option("Feijão"),
            ft.dropdown.Option("Cana-de-açúcar"),
            ft.dropdown.Option("Pastagem"),
            ft.dropdown.Option("Outra"),
        ]
    )
    
    prof_amostra = ft.TextField(label="Profundidade da amostra (cm)", value="20")
    argila = ft.TextField(label="Teor de argila (%)", value="35")
    p_rem = ft.TextField(label="P-rem (mg/L) [n se n/a]", value="n")
    
    pH = ft.TextField(label="pH em H2O", value="5.5")
    CO = ft.TextField(label="C.O. (%)", value="1.5")
    P = ft.TextField(label="Fósforo - P (mg/dm³)", value="15")
    
    unid_K = ft.RadioGroup(content=ft.Row([
        ft.Radio(value="1", label="mg/dm³"),
        ft.Radio(value="2", label="cmolc/dm³")
    ]), value="1")
    K_lido = ft.TextField(label="Valor de K", value="60")
    
    unid_CaMg = ft.RadioGroup(content=ft.Row([
        ft.Radio(value="1", label="cmolc/dm³"),
        ft.Radio(value="2", label="mmolc/dm³")
    ]), value="1")
    Ca_lido = ft.TextField(label="Valor de Ca", value="2.5")
    Mg_lido = ft.TextField(label="Valor de Mg", value="0.8")
    
    Na = ft.TextField(label="Sódio - Na (cmolc/dm³)", value="n")
    Al = ft.TextField(label="Alumínio - Al³⁺ (cmolc/dm³)", value="0.2")
    H_Al = ft.TextField(label="Acidez potencial - H+Al", value="3.0")
    S_SO4 = ft.TextField(label="Enxofre - S-SO4 (mg/dm³)", value="n")
    CEe = ft.TextField(label="CEe (dS/m)", value="n")
    
    val_B = ft.TextField(label="Boro (B)", value="n")
    val_Cu = ft.TextField(label="Cobre (Cu)", value="n")
    val_Fe = ft.TextField(label="Ferro (Fe)", value="n")
    val_Mn = ft.TextField(label="Manganês (Mn)", value="n")
    val_Zn = ft.TextField(label="Zinco (Zn)", value="n")
    
    Ca_sub = ft.TextField(label="Ca (Subsolo)", value="n")
    Mg_sub = ft.TextField(label="Mg (Subsolo)", value="n")
    K_sub = ft.TextField(label="K (Subsolo)", value="n")
    Al_sub = ft.TextField(label="Al (Subsolo)", value="n")
    
    V2 = ft.TextField(label="V% Alvo (V2)", value="60.0")
    K_alvo = ft.TextField(label="Meta de K na CTC (%)", value="3.0")
    PRNT = ft.TextField(label="PRNT do Calcário (%)", value="90.0")
    CaO_gar = ft.TextField(label="Garantia CaO (%)", value="35.0")
    MgO_gar = ft.TextField(label="Garantia MgO (%)", value="15.0")
    prof_inc = ft.TextField(label="Prof. Incorporação (cm)", value="20.0")
    area_aplic = ft.TextField(label="Área de Aplicação (%)", value="100.0")
    
    metodo_calagem = ft.RadioGroup(content=ft.Column([
        ft.Radio(value="1", label="Saturação por Bases"),
        ft.Radio(value="2", label="Neutralização Al+Ca+Mg")
    ]), value="1")
    exig_CaMg_cult = ft.TextField(label="Exig. mín Ca+Mg (se método 2)", value="0.0")

    txt_resultado = ft.Text(selectable=True, font_family="monospace")

    def parse_val(val_str, default=0.0):
        if val_str is None:
            return default
        val_clean = str(val_str).strip().lower()
        if val_clean in ['', 'n', 'nao', 'não', '-', 'na']:
            return None
        try:
            return float(val_clean.replace(',', '.'))
        except ValueError:
            return default

    def processar_calculos(e):
        try:
            argila_v = parse_val(argila.value, 20.0)
            pH_v = parse_val(pH.value, 5.5)
            CO_v = parse_val(CO.value, 1.0)
            
            K_lido_val = parse_val(K_lido.value, 0.0)
            K_cmolc = K_lido_val / FATOR_K_MG_CMOLC if int(unid_K.value) == 1 else K_lido_val
            
            Ca_lido_val = parse_val(Ca_lido.value, 0.0)
            Mg_lido_val = parse_val(Mg_lido.value, 0.0)
            
            if int(unid_CaMg.value) == 2:
                Ca = Ca_lido_val / 10.0
                Mg = Mg_lido_val / 10.0
            else:
                Ca = Ca_lido_val
                Mg = Mg_lido_val

            Na_val = parse_val(Na.value, 0.0)
            Na_v = Na_val if Na_val is not None else 0.0
            
            Al_v = parse_val(Al.value, 0.0)
            if Al_v is None: Al_v = 0.0
            
            H_Al_v = parse_val(H_Al.value, 0.0)
            if H_Al_v is None: H_Al_v = 0.0

            MO = CO_v * FATOR_CO_MO if CO_v is not None else 0.0
            N_est_kg = MO * FATOR_N_MIN
            
            SB = Ca + Mg + K_cmolc + Na_v
            t_efetiva = SB + Al_v
            T_potencial = SB + H_Al_v

            if T_potencial > 0:
                V1 = (SB / T_potencial) * 100.0
                perc_Ca = (Ca / T_potencial) * 100.0
                perc_Mg = (Mg / T_potencial) * 100.0
                perc_K = (K_cmolc / T_potencial) * 100.0
            else:
                V1 = perc_Ca = perc_Mg = perc_K = 0.0

            m_sat = (Al_v / t_efetiva) * 100.0 if t_efetiva > 0 else 0.0
            rel_CaMg = Ca / Mg if Mg > 0 else 999.0

            if pH_v < 5.0: classe_acidez = "Acidez muito alta"
            elif pH_v < 5.5: classe_acidez = "Acidez alta"
            elif pH_v < 6.0: classe_acidez = "Acidez moderada"
            elif pH_v <= 6.5: classe_acidez = "Faixa geralmente adequada"
            else: classe_acidez = "pH elevado"

            if argila_v < 15.0: fator_Y = 1.0
            elif argila_v < 35.0: fator_Y = 1.5
            elif argila_v < 60.0: fator_Y = 2.0
            else: fator_Y = 3.0

            PRNT_v = parse_val(PRNT.value, 90.0)
            V2_v = parse_val(V2.value, 60.0)
            
            NC_V = ((V2_v - V1) * T_potencial) / PRNT_v if V2_v > V1 else 0.0
            
            exig_CaMg = parse_val(exig_CaMg_cult.value, 0.0)
            if exig_CaMg is None: exig_CaMg = 0.0
            soma_CaMg = Ca + Mg
            
            if soma_CaMg < exig_CaMg:
                NC_Al = (fator_Y * Al_v) + (exig_CaMg - soma_CaMg)
            else:
                NC_Al = fator_Y * Al_v
                
            NC_Al = max(0.0, (NC_Al * 100.0) / PRNT_v)
            NC_final = NC_Al if int(metodo_calagem.value) == 2 else NC_V

            prof_inc_val = parse_val(prof_inc.value, 20.0)
            area_aplic_val = parse_val(area_aplic.value, 100.0)
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
                "Boro (B)": parse_val(val_B.value),
                "Cobre (Cu)": parse_val(val_Cu.value),
                "Ferro (Fe)": parse_val(val_Fe.value),
                "Manganês (Mn)": parse_val(val_Mn.value),
                "Zinco (Zn)": parse_val(val_Zn.value)
            }

            sub_Ca_v = parse_val(Ca_sub.value)
            sub_Al_v = parse_val(Al_sub.value)

            relatorio = f"""========================================================
                 LAUDO DE INTERPRETAÇÃO                 
========================================================

CULTURA: {cultura_var.value}
DIAGNÓSTICO DO pH: {classe_acidez} (pH {pH_v})
MATÉRIA ORGÂNICA: {MO:.2f} %  | N Estimado: {N_est_kg:.2f} kg/ha

--- COMPLEXO SORTIVO ---
Soma de Bases (SB): {SB:.2f} cmolc/dm³
CTC Efetiva (t): {t_efetiva:.2f} cmolc/dm³
CTC Potencial (T): {T_potencial:.2f} cmolc/dm³
Saturação por Bases (V%): {V1:.2f}% (Alvo: {V2_v}%)
Saturação por Alumínio (m%): {m_sat:.2f}%
Relação Ca/Mg: {rel_CaMg:.2f}

--- RECOMENDAÇÃO DE CALAGEM ---
Método escolhido: {'Neutralização Al' if int(metodo_calagem.value)==2 else 'Saturação Bases'}
Dose calculada: {NC_final:.2f} t/ha
Tipo de Calcário sugerido: {tipo_calcario}
{rec_acidez}

--- MICRONUTRIENTES ---
"""
            for k, v in micros.items():
                val_txt = f"{v} mg/dm³" if v is not None else "Não analisado (n)"
                relatorio += f"{k}: {val_txt}\n"

            relatorio += "\n--- AVALIAÇÃO DE SUBSOLO / GESSAGEM ---\n"
            if sub_Ca_v is not None:
                relatorio += f"Ca Subsolo: {sub_Ca_v} cmolc/dm³\n"
                if sub_Al_v is not None:
                    relatorio += f"Al Subsolo: {sub_Al_v} cmolc/dm³\n"
                if sub_Ca_v < 0.5 or (sub_Al_v is not None and sub_Al_v > 0.5):
                    relatorio += "Recomendação: Indicado uso de gesso agrícola.\n"
                else:
                    relatorio += "Perfil do subsolo em condições favoráveis.\n"
            else:
                relatorio += "Análise de subsolo não informada (n).\n"

            txt_resultado.value = relatorio
            tabela_abas.selected_index = 4
            page.update()
        except Exception as ex:
            page.dialog = ft.AlertDialog(title=ft.Text(f"Erro nos dados: {str(ex)}"))
            page.dialog.open = True
            page.update()

    # Estrutura de Abas
    tabela_abas = ft.Tabs(
        selected_index=0,
        animation_duration=300,
        tabs=[
            ft.Tab(
                text="1. Física",
                content=ft.Column([cultura_var, prof_amostra, argila, p_rem], scroll=ft.ScrollMode.AUTO)
            ),
            ft.Tab(
                text="2. Química",
                content=ft.Column([pH, CO, P, ft.Text("Unidade do K:"), unid_K, K_lido, ft.Text("Unidade Ca/Mg:"), unid_CaMg, Ca_lido, Mg_lido, Na, Al, H_Al, S_SO4, CEe], scroll=ft.ScrollMode.AUTO)
            ),
            ft.Tab(
                text="3. Micros",
                content=ft.Column([val_B, val_Cu, val_Fe, val_Mn, val_Zn, Ca_sub, Mg_sub, K_sub, Al_sub], scroll=ft.ScrollMode.AUTO)
            ),
            ft.Tab(
                text="4. Manejo",
                content=ft.Column([V2, K_alvo, PRNT, CaO_gar, MgO_gar, prof_inc, area_aplic, ft.Text("Método de Calagem:"), metodo_calagem, exig_CaMg_cult, ft.ElevatedButton("PROCESSAR CÁLCULOS", on_click=processar_calculos)], scroll=ft.ScrollMode.AUTO)
            ),
            ft.Tab(
                text="5. Resultados",
                content=ft.Column([txt_resultado, ft.ElevatedButton("Recalcular", on_click=processar_calculos)], scroll=ft.ScrollMode.AUTO)
            ),
        ],
        expand=1
    )
    
    page.add(tabela_abas)

ft.app(target=main)
