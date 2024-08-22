from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivymd.app import MDApp
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.label import MDLabel
from kivymd.uix.textfield import MDTextField
from kivymd.uix.button import MDRaisedButton
from kivymd.uix.screen import MDScreen

class MenuScreen(MDScreen):
    def __init__(self, **kwargs):
        super(MenuScreen, self).__init__(**kwargs)
        layout = MDBoxLayout(orientation='vertical', spacing=10, padding=20, md_bg_color=(1, 1, 1, 1))  # Branco

        title = MDLabel(
            text='Curso de Inglês',
            halign='center',
            font_style='H3',
            size_hint=(1, 0.3),
            theme_text_color='Custom',
            text_color=(0.6, 0.2, 0.6, 1)  # Roxo
        )
        layout.add_widget(title)

        button_style = {
            'size_hint': (0.8, 0.1),
            'md_bg_color': (0.9, 0.6, 0.8, 1),  # Rosa claro
            'font_style': 'H5',
            'pos_hint': {'center_x': 0.5},
        }

        btn_basic = MDRaisedButton(
            text='Inglês Básico',
            **button_style
        )
        btn_basic.bind(on_press=self.go_to_basic)
        layout.add_widget(btn_basic)

        btn_intermediate = MDRaisedButton(
            text='Inglês Intermediário',
            **button_style
        )
        btn_intermediate.bind(on_press=self.go_to_intermediate)
        layout.add_widget(btn_intermediate)

        btn_advanced = MDRaisedButton(
            text='Inglês Avançado',
            **button_style
        )
        btn_advanced.bind(on_press=self.go_to_advanced)
        layout.add_widget(btn_advanced)

        self.add_widget(layout)

    def go_to_basic(self, instance):
        self.manager.current = 'basic'

    def go_to_intermediate(self, instance):
        self.manager.current = 'intermediate'

    def go_to_advanced(self, instance):
        self.manager.current = 'advanced'


class BaseQuestionScreen(MDScreen):
    def __init__(self, title, questions, **kwargs):
        super(BaseQuestionScreen, self).__init__(**kwargs)
        self.questions = questions
        self.current_question = 0
        self.correct_answers = 0
        self.answer_status = []

        layout = MDBoxLayout(orientation='vertical', spacing=10, padding=20, md_bg_color=(1, 1, 1, 1))  # Branco

        self.title = MDLabel(
            text=title,
            halign='center',
            font_style='H3',
            size_hint=(1, 0.1),
            theme_text_color='Custom',
            text_color=(0.6, 0.2, 0.6, 1)  # Roxo
        )
        layout.add_widget(self.title)

        self.question_label = MDLabel(
            text=self.questions[self.current_question][0],
            halign='center',
            size_hint=(1, 0.2),
            theme_text_color='Custom',
            text_color=(0.6, 0.2, 0.6, 1)  # Roxo
        )
        layout.add_widget(self.question_label)

        self.answer_input = MDTextField(
            hint_text='Insira sua resposta aqui',
            size_hint=(1, 0.2),
            line_color_focus=(0.6, 0.2, 0.6, 1)  # Roxo
        )
        layout.add_widget(self.answer_input)

        self.result_label = MDLabel(
            text='',
            halign='center',
            size_hint=(1, 0.2),
            theme_text_color='Custom',
            text_color=(0.6, 0.2, 0.6, 1)  # Roxo
        )
        layout.add_widget(self.result_label)

        button_style = {
            'size_hint': (0.8, 0.1),
            'md_bg_color': (0.9, 0.6, 0.8, 1),  # Rosa claro
            'font_style': 'H6',
            'pos_hint': {'center_x': 0.5},
        }

        btn_submit = MDRaisedButton(
            text='Enviar',
            **button_style
        )
        btn_submit.bind(on_press=self.check_answer)
        layout.add_widget(btn_submit)

        btn_next = MDRaisedButton(
            text='Próxima Pergunta',
            **button_style
        )
        btn_next.bind(on_press=self.next_question)
        layout.add_widget(btn_next)

        btn_back = MDRaisedButton(
            text='Voltar ao Menu',
            **button_style
        )
        btn_back.bind(on_press=self.go_back)
        layout.add_widget(btn_back)

        self.add_widget(layout)

    def check_answer(self, instance):
        correct_answer = self.questions[self.current_question][1].lower()
        user_answer = self.answer_input.text.lower()

        if user_answer == correct_answer:
            self.result = 'Correto!'
            self.correct_answers += 1
            self.answer_status.append((self.questions[self.current_question][0], 'Correto'))
        else:
            self.result = f'Incorreto. A resposta correta é "{correct_answer}".'
            self.answer_status.append((self.questions[self.current_question][0], 'Incorreto'))

        self.update_result()

    def update_result(self):
        self.result_label.text = self.result

    def next_question(self, instance):
        self.current_question += 1
        if self.current_question < len(self.questions):
            self.update_question()
        else:
            self.result_label.text = 'Você completou todas as perguntas!'
            self.show_results()

    def update_question(self):
        self.question_label.text = self.questions[self.current_question][0]
        self.answer_input.text = ''
        self.result_label.text = ''

    def show_results(self):
        result_text = f'Você acertou {self.correct_answers} de {len(self.questions)} perguntas.\n\n'
        for question, status in self.answer_status:
            result_text += f'Pergunta: "{question}" - {status}\n'
        
        self.result_label.text = result_text

    def go_back(self, instance):
        self.current_question = 0
        self.correct_answers = 0
        self.answer_status = []
        self.update_question()
        self.result_label.text = ''
        
        self.manager.current = 'menu'


class BasicEnglishScreen(BaseQuestionScreen):
    def __init__(self, **kwargs):
        questions = [
            ('Como se diz "Bom dia" em Inglês?', 'good morning'),
            ('Como se diz "Obrigado" em Inglês?', 'thank you'),
            ('Como se diz "Desculpe" em Inglês?', 'sorry'),
            ('Como se diz "Por favor" em Inglês?', 'please'),
            ('Como se diz "Sim" em Inglês?', 'yes'),
            ('Como se diz "Não" em Inglês?', 'no'),
            ('Como se diz "Eu não entendo" em Inglês?', 'I don’t understand'),
            ('Como se diz "Qual é o seu nome?" em Inglês?', 'What is your name?'),
            ('Como se diz "Eu gosto de aprender inglês" em Inglês?', 'I like to learn English'),
            ('Como se diz "Onde fica o banheiro?" em Inglês?', 'Where is the bathroom?')
        ]
        super(BasicEnglishScreen, self).__init__(title='Inglês Básico', questions=questions, **kwargs)


class IntermediateEnglishScreen(BaseQuestionScreen):
    def __init__(self, **kwargs):
        questions = [
            ('Como se diz "Eu gostaria de um café" em Inglês?', 'I would like a coffee'),
            ('Como se diz "Quanto custa?" em Inglês?', 'How much does it cost?'),
            ('Como se diz "Eu não falo inglês muito bem" em Inglês?', 'I don’t speak English very well'),
            ('Como se diz "Você pode me ajudar?" em Inglês?', 'Can you help me?'),
            ('Como se diz "Eu estou perdido" em Inglês?', 'I am lost'),
            ('Como se diz "Qual é o seu número de telefone?" em Inglês?', 'What is your phone number?'),
            ('Como se diz "Eu gostaria de fazer uma reserva" em Inglês?', 'I would like to make a reservation'),
            ('Como se diz "Eu não sei" em Inglês?', 'I don’t know'),
            ('Como se diz "Qual é o horário de funcionamento?" em Inglês?', 'What are the opening hours?'),
            ('Como se diz "Você pode repetir isso, por favor?" em Inglês?', 'Can you repeat that, please?')
        ]
        super(IntermediateEnglishScreen, self).__init__(title='Inglês Intermediário', questions=questions, **kwargs)


class AdvancedEnglishScreen(BaseQuestionScreen):
    def __init__(self, **kwargs):
        questions = [
            ('Como se diz "Eu gostaria de discutir um projeto com você" em Inglês?', 'I would like to discuss a project with you'),
            ('Como se diz "Eu vou fazer uma apresentação amanhã" em Inglês?', 'I will give a presentation tomorrow'),
            ('Como se diz "Posso ter uma cópia do relatório?" em Inglês?', 'Can I have a copy of the report?'),
            ('Como se diz "Eu preciso de mais tempo para terminar isso" em Inglês?', 'I need more time to finish this'),
            ('Como se diz "Você pode me dar um feedback?" em Inglês?', 'Can you give me feedback?'),
            ('Como se diz "Eu gostaria de marcar uma reunião" em Inglês?', 'I would like to schedule a meeting'),
            ('Como se diz "Você tem alguma sugestão?" em Inglês?', 'Do you have any suggestions?'),
            ('Como se diz "Eu vou revisar o material e retornar para você" em Inglês?', 'I will review the material and get back to you'),
            ('Como se diz "Estou ansioso para trabalhar com você" em Inglês?', 'I am looking forward to working with you'),
            ('Como se diz "Por favor, mantenha-me informado" em Inglês?', 'Please keep me informed')
        ]
        super(AdvancedEnglishScreen, self).__init__(title='Inglês Avançado', questions=questions, **kwargs)


class MyApp(MDApp):
    def build(self):
        sm = ScreenManager()

        sm.add_widget(MenuScreen(name='menu'))
        sm.add_widget(BasicEnglishScreen(name='basic'))
        sm.add_widget(IntermediateEnglishScreen(name='intermediate'))
        sm.add_widget(AdvancedEnglishScreen(name='advanced'))

        return sm

MyApp().run()
