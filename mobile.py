import sys
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from scraper import scraper  # Importar a função de raspagem de outra biblioteca

class ProductSearchApp(App):
    def build(self):
        self.title = "Pesquisar suplementos"
        layout = BoxLayout(orientation='vertical')

        self.label = Label(text="Nome do suplemento:")
        self.entry = TextInput()
        self.search_button = Button(text="Pesquisar", background_color=(76/255, 175/255, 80/255, 1))
        self.search_button.bind(on_press=self.search_product)

        # Lista rolável para exibir os resultados
        self.result_list = BoxLayout(orientation='vertical', spacing=5, size_hint_y=None)
        self.result_list.bind(minimum_height=self.result_list.setter('height'))

        layout.add_widget(self.label)
        layout.add_widget(self.entry)
        layout.add_widget(self.result_list)
        layout.add_widget(self.search_button)

        # Cache para armazenar os resultados da pesquisa
        self.cache = {}

        return layout

    def search_product(self, instance):
        product_name = self.entry.text
        result = scraper(product_name)  # Aqui você precisa implementar o método de raspagem da página da web
        self.show_result(result)

    def show_result(self, result):
        self.result_list.clear_widgets()

        # Adiciona os resultados à lista rolável
        for product in result:
            product_label = Label(text=f"{product['Produto']} - {product['Preço']} - {product['Avaliações']}")
            self.result_list.add_widget(product_label)

if __name__ == "__main__":
    ProductSearchApp().run()
