import solara
from .module_widget import StartModule
from angiography.meta.utils import load_data


@solara.component
def StartOrSelect(module_select, start_module, module_dict, n_syllables_reactive):
  if start_module.value is None:
    SelectModule(module_select, start_module, module_dict, n_syllables_reactive)
  else:
    StartModule(start_module.value, module_dict, start_module, n_syllables_reactive.value)


@solara.component
def SelectModule(module_select, start_module, module_dict, n_syllables_reactive):
  def on_start_click():
    if module_select.value != "Choose":
      start_module.value = module_select.value
  solara.Select(
      label="Select module", 
      values=["Choose"] + list(module_dict.keys()), 
      value=module_select
  )
  solara.SliderInt("Choose number of items", value=n_syllables_reactive, min=1, max=20)
  solara.InputInt(f"Number of items: ", value=n_syllables_reactive)
  solara.Button("Start", on_click=on_start_click)


@solara.component
def Page():
    module_dict = load_data()
    module_select = solara.reactive("Choose")
    start_module = solara.reactive(None)
    n_syllables_reactive = solara.reactive(3)
    StartOrSelect(module_select, start_module, module_dict, n_syllables_reactive)