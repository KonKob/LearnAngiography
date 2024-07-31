import solara
from ..modules.modules import Module
from ..meta.segment_definitions import segment_definitions
from ..meta.module_pages import get_landing_pages
from ..meta.utils import load_data


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

@solara.component
def StartModule(key, module_dict, start_module=None, n_syllables=3):
    m = Module(images_annotations = module_dict[key]["images"],
          syllable = module_dict[key]["syllable"],
          name = key,
          segment_definitions = segment_definitions,
          user_stats = None,
          module_stats = None,
          print = False,
          n_syllables=n_syllables)
    ex_syll = solara.reactive(-1)
    View(m, ex_syll, start_module, n_syllables)

@solara.component
def LandingPage(m, ex_syll, start_module):
  solara.Markdown(get_landing_pages(m))
  def start():
    ex_syll.value += 1
  solara.Button("Start", on_click=start)
  def return_to_main():
    start_module.value = None
  solara.Button("Back to main menu", on_click=return_to_main)

@solara.component
def create_widgets(options, widget, value):  
  func = widget_select_dict[str(widget)]
  func(options, widget, value)

@solara.component
def create_tooltip(options, widget, value):
  with widget(options["tooltip"]):
    options["widget_within"](options["widget_within_label"], style=options["widget_within_style"])

@solara.component
def create_text_widget(options, widget, value):
  widget(label=options["label"], value=options["value"])

@solara.component
def create_toggle_buttons_single(options, widget, value):
  widget(value=value, values=options["options"])

@solara.component
def create_vboxes(options, widget, value):
  with widget():
    for text, value, tooltip, tooltip_description in zip(options["text"], options["values"], options["tooltips"], options["tooltip_descriptions"]):
      with tooltip(tooltip_description):
        text(value)

@solara.component
def create_float_slider(options, widget, value):
  widget(label=options["label"], value=value, min=options["min"], max=options["max"])

widget_select_dict = {'react.component(solara.components.misc.Text)': create_text_widget,
                      'react.component(solara.components.togglebuttons.ToggleButtonsSingle)': create_toggle_buttons_single,
                      'react.component(solara.components.slider.SliderFloat)': create_float_slider,
                      'react.component(solara.components.tooltip.Tooltip)': create_tooltip,
                      'react.component(solara.components.misc.VBox)': create_vboxes}

@solara.component
def ModulePage(m, ex_syll, n_syllables):
  m.executed_syllables = ex_syll.value
  solara.Text(f"{ex_syll.value+1}/{n_syllables}")
  m.syllables[m.executed_syllables].start()
  solara.Text(m.syllables[m.executed_syllables].task_description)

  solara_dict = m.syllables[m.executed_syllables].solara_dict 
  answer_list = []
  for i, widget in enumerate(solara_dict["widgets"]):
    answer_value = solara_dict["answer_value"][i]
    create_widgets(solara_dict["widget_options"][i], widget, answer_value)
    if answer_value is not None:
      answer_list.append(answer_value.value)
  if len(answer_list) == 1:
    answer = answer_list[0]
  else:
    answer = answer_list
  
  def next():
    m.answer(answer)
    ex_syll.value += 1 

  solara.Button("Next", on_click=next)


@solara.component
def ResultsPage(m, start_module=None):
  m.result()
  solara.Text(f"Results:")
  solara.Text(f"{m.total_score}/{m.n_syllables}")
  solara.Text(f"{round(m.relative_score*100, 2)}%")
  if start_module is not None:
    def back_to_menu():
      start_module.value = None
    solara.Button("Back to main menu", on_click=back_to_menu)


@solara.component
def View(m, ex_syll, start_module, n_syllables=3):
  if ex_syll.value == -1:
    LandingPage(m, ex_syll, start_module)
  elif ex_syll.value >= 0 and ex_syll.value < n_syllables:
    ModulePage(m, ex_syll, n_syllables)
  elif ex_syll.value == n_syllables:
    ResultsPage(m, start_module)