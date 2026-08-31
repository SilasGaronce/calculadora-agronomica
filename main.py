from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.spinner import Spinner
from kivy.uix.scrollview import ScrollView

FATOR_CO_MO = 1.724
FATOR_K_MG_CMOLC = 391.0

class SistemaSoloApp(App):
    def build(self):
        root = ScrollView()
        layout = BoxLayout(orientation='vertical', padding=15, spacing=10, size_hint_y=None)
        layout.bind(minimum_height=layout.setter('height'))

        layout.add_widget(Label(text="[b]Calculadora Agronômica - Mobile[/b]", markup=True, font_size=20, size_hint_y=None, height=40))

        layout.add_widget(Label(text="Cultura:", size_hint_y=None, height=30))
        self.cultura_sp = Spinner(text='Soja', values=('Soja', 'Milho', 'Café', 'Pastagem'), size_hint_y=None, height=40)
        layout.add_widget(self.cultura_sp)

        self.inputs = {}
        campos = [
            ("prof", "Profundidade (cm):", "20"),
            ("argila", "Argila (%):", "35"),
            ("ph", "pH em H2O:", "5.5"),
            ("co", "C.O. (%):", "1.5"),
            ("p", "Fósforo P (mg/dm³):", "15"),
            ("k", "K (mg/dm³):", "60"),
            ("ca", "Ca (cmolc/dm³):", "2.5"),
            ("mg", "Mg (cmolc/dm³):", "0.8"),
            ("al", "Al³⁺ (cmolc/dm³):", "0.2"),
            ("h_al", "H+Al (cmolc/dm³):", "3.0"),
            ("v2", "V% Alvo:", "60"),
            ("prnt", "PRNT (%):", "90")
        ]

        for key, label_text, default_val in campos:
            layout.add_widget(Label(text=label_text, size_hint_y=None, height=25))
            ti = TextInput(text=default_val, multiline=False, size_hint_y=None, height=40)
            layout.add_widget(ti)
            self.inputs[key] = ti

        btn = Button(text="PROCESSAR CÁLCULOS", size_hint_y=None, height=50, background_color=(0.1, 0.6, 0.2, 1))
        btn.bind(on_press=self.calcular)
        layout.add_widget(btn)

        self.resultado_lbl = Label(text="", markup=True, size_hint_y=None, height=300)
        self.resultado_lbl.bind(texture_size=lambda _, size: setattr(self.resultado_lbl, 'height', size[1]))
        layout.add_widget(self.resultado_lbl)

        root.add_widget(layout)
        return root

    def parse(self, val_str, default=0.0):
        try:
            return float(val_str.strip().replace(',', '.'))
        except:
            return default

    def calcular(self, instance):
        argila = self.parse(self.inputs['argila'].text, 20.0)
        pH = self.parse(self.inputs['ph'].text, 5.5)
        CO = self.parse(self.inputs['co'].text, 1.0)
        K_cmolc = self.parse(self.inputs['k'].text, 0.0) / FATOR_K_MG_CMOLC
        Ca = self.parse(self.inputs['ca'].text, 0.0)
        Mg = self.parse(self.inputs['mg'].text, 0.0)
        Al = self.parse(self.inputs['al'].text, 0.0)
        H_Al = self.parse(self.inputs['h_al'].text, 0.0)
        V2 = self.parse(self.inputs['v2'].text, 60.0)
        PRNT = self.parse(self.inputs['prnt'].text, 90.0)

        MO = CO * FATOR_CO_MO
        SB = Ca + Mg + K_cmolc
        T_potencial = SB + H_Al
        V1 = (SB / T_potencial) * 100.0 if T_potencial > 0 else 0.0

        fator_Y = 1.5 if argila < 35 else 2.0
        NC = (((V2 - V1) * T_potencial) / PRNT) if V2 > V1 else 0.0

        res = f"[b]Resultados:[/b]\n" \
              f"pH: {pH} | MO: {MO:.2f}%\n" \
              f"SB: {SB:.2f} | CTC (T): {T_potencial:.2f}\n" \
              f"V%: {V1:.1f}% (Alvo: {V2}%)\n" \
              f"[b]Calcário Recomendado:[/b] {NC:.2f} t/ha"

        self.resultado_lbl.text = res

if __name__ == '__main__':
    SistemaSoloApp().run()
