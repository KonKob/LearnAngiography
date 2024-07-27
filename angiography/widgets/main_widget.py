import solara
from .module_widget import StartModule

@solara.component
def Page(module_dict):
  module_select = solara.reactive("Choose")
  start_module = solara.reactive(None)
  StartOrSelect(module_select, start_module, module_dict)


@solara.component
def StartOrSelect(module_select, start_module, module_dict):
  if start_module.value is None:
    SelectModule(module_select, start_module, module_dict)
  else:
    StartModule(start_module.value, module_dict, start_module)


@solara.component
def SelectModule(module_select, start_module, module_dict):
  def on_start_click():
    if module_select.value != "Choose":
      start_module.value = module_select.value
  solara.Select(
      label="Select module", 
      values=["Choose"] + list(module_dict.keys()), 
      value=module_select
  )
  solara.Button("Start", on_click=on_start_click)