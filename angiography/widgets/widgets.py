import solara
from ..modules.modules import Module
from ..meta.segment_definitions import segment_definitions_dict, segment_definitions_markdown
from ..meta.module_pages import get_landing_pages
from ..meta.utils import load_data
from ..meta.styles import start_button_style, n_items_style, slider_style, select_style, return_button_style, markdown_style, text_corpus_style, text_header_style, background_style, widget_within_style, tab_style, theme_style, locate_slider_style
from pathlib import Path


@solara.component
def Page():
    set_theme()
    with solara.lab.Tabs(color=tab_style["color"], background_color=tab_style["background_color"], slider_color=tab_style["slider_color"]):
        with solara.lab.Tab("main"):
            MainPage()
        with solara.lab.Tab("about"):
            MetaPage()
        with solara.lab.Tab("syntax"):
            SyntaxPage()

def set_theme():
  solara.lab.theme.themes.light.primary = theme_style["primary"]
  solara.lab.theme.themes.light.secondary = theme_style["secondary"]

@solara.component
def StartOrSelect(module_select, start_module, module_dict, n_syllables_reactive, use_syntax_scores):
  if start_module.value is None:
    SelectModule(module_select, start_module, module_dict, n_syllables_reactive, use_syntax_scores)
  else:
    StartModule(start_module.value, module_dict, start_module, n_syllables_reactive.value, use_syntax_scores.value)


@solara.component
def SelectModule(module_select, start_module, module_dict, n_syllables_reactive, use_syntax_scores):
  solara.Title("LearnAngiography Main")
  def on_start_click():
    if module_select.value != "Choose":
      start_module.value = module_select.value
  with solara.Row(gap="5vw"):
    with solara.Column(gap="0vw"):
      with solara.Column(gap="0vw", style=select_style):
        s = solara.Select(
            label="Select module", 
            values=list(module_dict.keys()), 
            value=module_select,
            style=select_style,
        ) 
      min = 1
      max = 20
      with solara.Column(gap="2vw", style=slider_style):
          solara.Switch(label="Use syntax scores instead of full name", value=use_syntax_scores, disabled=module_select.value not in ["Choose artery name", "Locate artery"])
          solara.SliderInt(f"Choose number of items (range {min} to {max})", value=n_syllables_reactive, min=min, max=max)
      solara.InputInt(f"Number of items: ", value=n_syllables_reactive, style=n_items_style)
    local_path = Path.cwd().joinpath("angiography/media/favicon.png")
    if local_path.exists():
        image_path = str(local_path)
    else:
        image_path = "https://github.com/KonKob/LearnAngiography/blob/6ce22964b262d5cb6e8dd4d388467f4f95dae27c/angiography/media/favicon.png"
    solara.Image(image_path, width="30vw")
  solara.Button("Start", on_click=on_start_click, style=start_button_style)
  

@solara.component
def MainPage():
    module_dict = load_data()
    module_select = solara.reactive("Choose")
    start_module = solara.reactive(None)
    n_syllables_reactive = solara.reactive(3)
    use_syntax_scores = solara.reactive(False)
    StartOrSelect(module_select, start_module, module_dict, n_syllables_reactive, use_syntax_scores)

@solara.component
def StartModule(key, module_dict, start_module=None, n_syllables=3, use_syntax_scores=True):
    m = Module(images_annotations = module_dict[key]["images"],
          syllable = module_dict[key]["syllable"],
          name = key,
          segment_definitions_dict = segment_definitions_dict,
          user_stats = None,
          module_stats = None,
          print = False,
          n_syllables=n_syllables,
          use_syntax_scores = use_syntax_scores)
    ex_syll = solara.reactive(-1)
    View(m, ex_syll, start_module, n_syllables)

@solara.component
def LandingPage(m, ex_syll, start_module):
  solara.Title(f"LearnAngiography {m.module_name}")
  solara.Markdown(get_landing_pages(m), style=markdown_style)
  def start():
    ex_syll.value += 1
  solara.Button("Start", on_click=start, style=start_button_style)
  def return_to_main():
    start_module.value = None
  solara.Button("Back to main menu", on_click=return_to_main, style=return_button_style)

@solara.component
def create_widgets(options, widget, value):  
  func = widget_select_dict[str(widget)]
  func(options, widget, value)

@solara.component
def create_tooltip(options, widget, value):
  with widget(options["tooltip"]):
    options["widget_within"](options["widget_within_label"], style=widget_within_style)

@solara.component
def create_text_widget(options, widget, value):
  widget(label=options["label"], value=options["value"], style=text_corpus_style)

@solara.component
def create_toggle_buttons_single(options, widget, value):
  widget(value=value, values=options["options"], style=text_corpus_style)

@solara.component
def create_vboxes(options, widget, value):
  with widget():
    for text, value, tooltip, tooltip_description in zip(options["text"], options["values"], options["tooltips"], options["tooltip_descriptions"]):
      with tooltip(tooltip_description):
        text(value)

@solara.component
def create_float_slider(options, widget, value):
  with solara.Column(gap="0vw", style=locate_slider_style):
    widget(label=options["label"], value=value, min=options["min"], max=options["max"])

widget_select_dict = {'react.component(solara.components.misc.Text)': create_text_widget,
                      'react.component(solara.components.togglebuttons.ToggleButtonsSingle)': create_toggle_buttons_single,
                      'react.component(solara.components.slider.SliderFloat)': create_float_slider,
                      'react.component(solara.components.tooltip.Tooltip)': create_tooltip,
                      'react.component(solara.components.misc.VBox)': create_vboxes}

@solara.component
def ModulePage(m, ex_syll, n_syllables):
  m.executed_syllables = ex_syll.value
  solara.Title(f"LearnAngiography {m.module_name}")
  m.syllables[m.executed_syllables].start()
  solara.Text(m.syllables[m.executed_syllables].task_description, style=text_header_style)
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
  solara.Button("Next", on_click=next, style=start_button_style)
  solara.Text(f"{ex_syll.value+1}/{n_syllables}", style=text_corpus_style)


@solara.component
def ResultsPage(m, start_module=None):
  solara.Title(f"LearnAngiography {m.module_name}")
  m.result()
  solara.Markdown(rf"""
  # Results:
  
  > {m.total_score}/{m.n_syllables} = {round(m.relative_score*100, 2)}%
  """,
  style = markdown_style)
  if start_module is not None:
    def back_to_menu():
      start_module.value = None
    solara.Button("Back to main menu", on_click=back_to_menu, style=return_button_style)
  with solara.Column(gap="4vw"):
    for syllable in m.syllables:
      with solara.Row(gap="2vw", style=background_style):
        syllable.result()
        with solara.Column(gap="0vw"):
          solara.Text(f"{syllable.task_description}", style=text_header_style)
          solara.Text(f"Your answer: {syllable.result_answer}", style=text_corpus_style)
          solara.Text(f"Correct answer: {syllable.result_solution}", style=text_corpus_style)


@solara.component
def View(m, ex_syll, start_module, n_syllables=3):
  if ex_syll.value == -1:
    LandingPage(m, ex_syll, start_module)
  elif ex_syll.value >= 0 and ex_syll.value < n_syllables:
    ModulePage(m, ex_syll, n_syllables)
  elif ex_syll.value == n_syllables:
    ResultsPage(m, start_module)


@solara.component
def MetaPage():
  solara.Markdown(r"""
  ## About
  
  <a href="https://github.com/KonKob/LearnAngiography">
    <img align="right" src="https://github.githubassets.com/images/modules/logos_page/GitHub-Mark.png" alt="GitHub" style="width:40px;height:40px;">
  </a>
  This application is meant for learning purposes. It is based on the data and annotations of the publicly available [ARCADE Dataset](https://zenodo.org/badge/DOI/10.5281/zenodo.10390295.svg) published in 2024 [[1]](https://doi.org/10.1038/s41597-023-02871-z)). Check out my [github repository]("https://github.com/KonKob/LearnAngiography") for detailed information!  
                  
  ## Data
  The dataset targets the two purposes syntax and stenosis detection with 1500 images each. 1000 training images of each category are used in this application.
  The data was acquired from 1500 patients with clinical suspicion of coronary heart disease from the Research Institute of Cardiology and Internal Diseases in Almaty (Kazakhstan).
  0 to 2 images per each of the six different angulations were recorded per patient resulting in 0 to 12 images per patient in the final dataset. Two different angiographs were used for acquisitation: Philips Azurion 3 (Philips, Amsterdam, Netherlands) and Siemens Artis Zee (Siemens Medical Solutions, Erlangen, Germany).
  The different angulations contain 4 views for the left coronary artery (Left Anterior Oblique (LAO) and Right Anterior Oblique (RAO) caudal views, Postero-Anterior (PA) and RAO cranial views) and 2 views for the right coronary artery (LAO and RAO cranial views). The authors of the ARCADE dataset [1], used the syntax score [2], to define stenosis as >= 50% degree of constriction  in coronary arteries of at least 1.5 _mm_ diameter.

  ## References

  > [1] Popov, M., Amanturdieva, A., Zhaksylyk, N., Alkanov, A., Saniyazbekov, A., Aimyshev, T., Ismailov, E., Bulegenov, A., Kuzhukeyev, A., Kulanbayeva, A., Kalzhanov, A., Temenov, N., Kolesnikov, A., Sakhov, O., & Fazli, S. (2024). Dataset for Automatic Region-based Coronary Artery Disease Diagnostics Using X-Ray Angiography Images. Scientific data, 11(1), 20.

  > [2] Sianos, G., Morel, M. A., Kappetein, A. P., Morice, M. C., Colombo, A., Dawkins, K., van den Brand, M., Van Dyck, N., Russell, M. E., Mohr, F. W., & Serruys, P. W. (2005). The SYNTAX Score: an angiographic tool grading the complexity of coronary artery disease. EuroIntervention : journal of EuroPCR in collaboration with the Working Group on Interventional Cardiology of the European Society of Cardiology, 1(2), 219–227.""",
  style = markdown_style)

@solara.component
def SyntaxPage():
  solara.Markdown(segment_definitions_markdown, style=markdown_style)
