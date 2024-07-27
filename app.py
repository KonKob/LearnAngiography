import solara
from angiography.meta.utils import load_data
from angiography.widgets.main_widget import StartOrSelect

@solara.component
def Page():
    module_dict = load_data()
    module_select = solara.reactive("Choose")
    start_module = solara.reactive(None)
    StartOrSelect(module_select, start_module, module_dict)