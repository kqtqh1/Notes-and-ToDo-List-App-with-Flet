import flet as ft

class Home(ft.UserControl):
    def build(self):
        return ft.ResponsiveRow(
            [
                ft.Container(
                    content=ft.Column(
                        controls=[
                            #top container for greetings
                            ft.Container(
                                content=ft.Column(
                                    controls=[
                                        ft.Text("NOTES & TODO LIST", weight=ft.FontWeight.BOLD, size=30, color="#262f2e",text_align=ft.TextAlign.CENTER),
                                    ],
                                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                                    alignment=ft.MainAxisAlignment.CENTER,
                                ),
                                height=400,
                                padding=20,
                            ),
                            #container for buttons
                            ft.Container(
                                content=ft.Column(
                                    controls=[
                                        ft.ElevatedButton("Add Notes",color="#262f2e", height=50,width=300,bgcolor="#dedede", on_click=self.gotoNotes,
                                                          style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=4))),
                                        ft.ElevatedButton("Add task to To-Do List",color="#262f2e", height=50,width=300,bgcolor="#dedede", on_click=self.gotoToDo,
                                                          style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=4))),
                                    ],
                                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                                    alignment=ft.MainAxisAlignment.CENTER,
                                    spacing=20,
                                ),
                                height=280,
                                width=400,
                                bgcolor="#262f2e",
                                padding=20,
                            )
                        ],
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    ),
                    
                    bgcolor="#dedede",
                    height=680,
                    border_radius=16,
                )
            ]
        )
    def gotoNotes(self, e):
        self.page.go("/notes")

    def gotoToDo(self, e):
        self.page.go("/todo")
    
#ItemList for individual task or notes
class ItemList(ft.UserControl):
    def __init__(self, contentInput,  removeInput, titleInput=None):
        super().__init__()
        self.contentInput= contentInput
        self.removeInput = removeInput
        self.titleInput = titleInput

    def build(self):
        self.task_cb = ft.Checkbox(label=self.contentInput, active_color="#dedede",check_color="#262f2e", expand=True)
        self.title= ft.Text(value=self.titleInput, expand=True, style=ft.TextThemeStyle.HEADLINE_SMALL, weight="bold")
        self.content= ft.Text(value=self.contentInput, expand=True)
        self.edit_title = ft.TextField(value=self.titleInput, border_color="#dedede", expand=True)
        self.edit_content = ft.TextField(value=self.contentInput, border_color="#dedede",expand=True, multiline=True)
        
        if self.titleInput is not None:
            #views for notes
            self.note_view = ft.Column(
                visible=True,
                controls=[
                    self.title,
                    self.content,
                    ft.Row(
                        controls=[
                            ft.IconButton(icon=ft.icons.CREATE_SHARP, icon_color="#858989",on_click=self.edit),
                            ft.IconButton(icon=ft.icons.DELETE_FOREVER_SHARP, icon_color="#C66161",on_click=self.remove),
                        ]
                    )  
                ]
            )
            self.edit_view = ft.Column(
                visible=False,
                controls=[
                    self.edit_title,
                    self.edit_content,
                    ft.IconButton(icon=ft.icons.CHECK_CIRCLE_OUTLINE_SHARP,icon_color="#6A9F6C",on_click=self.save),
                    ft.IconButton(icon=ft.icons.CANCEL_ROUNDED,icon_color="#C66161", on_click=self.cancel),
                ]
            )
            
            return ft.Container(
                content=ft.Column(
                    controls=[self.note_view, self.edit_view],
                ),
                padding=10,
                border_radius=8,
                bgcolor= "#262f2e",
                margin=ft.margin.all(6)
            )
        else:
            #views for ToDo
            self.task_view = ft.Row(
                visible=True,
                controls=[
                    self.task_cb,
                    ft.IconButton(icon=ft.icons.CREATE_SHARP, icon_color="#dedede",on_click=self.edit),
                    ft.IconButton(icon=ft.icons.DELETE_FOREVER_SHARP,icon_color="#C66161",on_click=self.remove),
                ]    
            )
            self.edit_view = ft.Row(
                visible=False,
                controls=[
                    self.edit_content,
                    ft.IconButton(icon=ft.icons.CHECK_CIRCLE_OUTLINE_SHARP,icon_color="#6A9F6C",on_click=self.save),
                    ft.IconButton(icon=ft.icons.CANCEL_ROUNDED,icon_color="#C66161", on_click=self.cancel),
                ]
            )
            return ft.Container(
                content=ft.Column(
                    controls=[self.task_view, self.edit_view],
                ),  
                padding=10,
                bgcolor= "#262f2e",
                border_radius= 4,
                margin=6
            )

    def edit(self, e): 
        if self.titleInput is not None:
            self.note_view.visible = False
        else:
            self.task_view.visible = False
        self.edit_view.visible = True
        self.update()
    #delete an item
    def remove(self, e):
        self.removeInput(self)

    def save(self, e):
        if self.titleInput is not None:
            self.contentInput = self.edit_content.value
            self.titleInput = self.edit_title.value
            self.content.value = self.contentInput 
            self.title.value = self.titleInput  
            self.note_view.visible = True
            self.edit_view.visible = False
            self.update()
        else:
            self.task_cb.label = self.edit_content.value
            self.task_view.visible = True
            self.edit_view.visible = False
            self.update()
    #cancel edit item
    def cancel(self, e):
        if self.titleInput is not None:
            self.note_view.visible = True
        else:
            self.task_view.visible=True
        self.edit_view.visible= False
        self.update()

#todo list page
class Todo(ft.UserControl):
    def build(self):
        self.input = ft.TextField(hint_text='What should be done?', color="#262f2e",border_color="#262f2e",expand=True,multiline=True)
        self.tasks = ft.Column()  

        view = ft.ResponsiveRow(
            [
                ft.Container(
                    bgcolor = "#dedede",
                    width= 400,
                    height=680,
                    border_radius=16,
                    padding= 10,
                    content=ft.Column(
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                        controls=[
                            ft.Text(value='ToDo', weight="bold", size=20, color="#262f2e"),
                            ft.Row(
                                controls=[
                                    self.input,
                                    ft.FloatingActionButton(icon=ft.icons.ADD, foreground_color="#dedede",bgcolor="#262f2e",on_click=self.addTask)
                                ]
                            ),
                            ft.Text(value='List of todo items', weight="bold", color="#262f2e"),
                            self.tasks,
                            ft.ElevatedButton(text="Back",color="#dedede", bgcolor="#262f2e",on_click=self.gotoHome),
                        ]
                    )
                )      
            ]
        )
        return view
    
    def addTask(self, e):
        if self.input.value != '':
            task = ItemList(self.input.value, self.remove_task)
            self.tasks.controls.append(task)
            self.input.value = ''
            self.update()

    def remove_task(self, task):
        self.tasks.controls.remove(task)
        self.update()

    def gotoHome(self, e):
        self.page.go("/")

#note page
class Notes(ft.UserControl):
    def build(self):
        self.title = ft.TextField(hint_text='title', border_color="#262f2e",expand=True)
        self.content= ft.TextField(hint_text='content',border_color="#262f2e", expand=True,multiline=True)
        self.tasks = ft.ListView(expand=1, spacing=10, padding=15, auto_scroll=True)

        view = ft.ResponsiveRow(
            [
                ft.Container(
                    bgcolor="#dedede",
                    width=400,
                    height= 680, 
                    border_radius=16,
                    padding = 20,
                    content=ft.Column(
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                        controls=[ 
                            ft.Text(value='Notes',color="#262f2e",size= 20, weight="bold"),
                            #container for new notes
                            ft.Container(
                                content= ft.Column(
                                    [
                                        self.title,
                                        self.content,
                                        ft.FloatingActionButton(icon=ft.icons.ADD,foreground_color="#dedede",bgcolor="#262f2e", on_click=self.addNote),
                                    ]
                                ),
                                padding=12,
                                border_radius=5,
                                bgcolor= "#858989",
                                margin=ft.margin.all(10),
                                alignment=ft.alignment.center,
                            ),
                            ft.Text(value='Note List', color="#262f2e", weight="bold"),
                            self.tasks,
                            ft.ElevatedButton("Back",color="#dedede", bgcolor="#262f2e", on_click=self.gotoHome),
                        ]
                    )
                )
            ]
        )
        return view

    def addNote(self, e):
        if self.title.value != '' and self.content.value != '':
            note = ItemList(self.content.value, self.remove_note, self.title.value,)
            self.tasks.controls.append(note)
            self.title.value = ''
            self.content.value = ''
            self.update()

    def remove_note(self, note):
        self.tasks.controls.remove(note)
        self.update()

    def gotoHome(self, e):
        self.page.go("/")

def main(page: ft.Page):
    page.window_height = 738
    page.window_width = 400

    #function to manage page views based on the URL route
    def route_change(route):
        page.views.clear()
        if page.route == "/":
            page.views.append(ft.View( route, [Home()], scroll="auto"))
        elif page.route == "/notes":
            page.views.append(ft.View(route, [Notes()], scroll="auto"))
        elif page.route == "/todo":
            page.views.append(ft.View( route, [Todo()] ) )
        page.update()

    page.on_route_change = route_change
    page.go("/")

ft.app(target=main)
