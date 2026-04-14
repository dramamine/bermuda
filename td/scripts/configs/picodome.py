# nosec
import sld_resolume_commands as resolume_commands
from collections import namedtuple
import random

NUM_SECTIONS = 4

LAYER_BG1 = 1
LAYER_TOP = 2
LAYER_POST_EFFECTS = 4


FlowTemplate = namedtuple('FlowTemplate', [
    "initial_clips",
    "section_1_action",
    "section_2_action",
    "section_3_action",
])

ADD_COLOR_FADE = 'ADD_COLOR_FADE'
REMOVE_COLOR_FADE = 'REMOVE_COLOR_FADE'
ADD_TOP_CLIP = 'ADD_TOP_CLIP'
SWAP_BG_CLIP = 'SWAP_BG_CLIP'

template_flow_option_0 = FlowTemplate(
    initial_clips=[LAYER_BG1],
    section_1_action=ADD_COLOR_FADE,
    section_2_action=ADD_TOP_CLIP,
    section_3_action=REMOVE_COLOR_FADE,
)

template_flow_option_1 = FlowTemplate(
    initial_clips=[LAYER_BG1],
    section_1_action=ADD_COLOR_FADE,
    section_2_action=SWAP_BG_CLIP,
    section_3_action=REMOVE_COLOR_FADE,
)

template_flow_option_2 = FlowTemplate(
    initial_clips=[LAYER_BG1, LAYER_TOP],
    section_1_action=ADD_COLOR_FADE,
    section_2_action=SWAP_BG_CLIP,
    section_3_action=REMOVE_COLOR_FADE,
)

template_flow_options = [
    template_flow_option_0,
    template_flow_option_1,
    template_flow_option_2,
]

# trasnsitions that are fun for the bg layer
t = [1, 3, 8, 10, 12, 13, 15, 17, 18, 19, 21, 31, 39, 46, 48]

# these numbers match up with clips in the resolume composition
bg_clips = range(1, 35)

top_clips = range(2, 24)

# list of tuples (intensity, layer, effect_name, is_audio_reactive)
effects = [
    (0, LAYER_BG1, "slide"),
    (0, LAYER_BG1, "slide2"),
    (0, LAYER_BG1, "huerotate2", True),
    (0, LAYER_BG1, "suckr"),
    (0, LAYER_BG1, "threshold", True),
    (0, LAYER_BG1, "vignette", True),
    (0, LAYER_BG1, "blow", True),
    (0, LAYER_BG1, "edgedetection"),
    # (0, LAYER_BG1, "ezradialcloner"),
    # (0, LAYER_BG1, "ezradialcloner2"),
    (0, LAYER_BG1, "goo"),
    (0, LAYER_BG1, "gridcloner"),
    (0, LAYER_BG1, "heat", True),
    (0, LAYER_BG1, "heat2", True),
    (0, LAYER_BG1, "infinitezoom"),
    (0, LAYER_BG1, "infinitezoom2", True),
    # (0, LAYER_BG1, "kaleidoscope"),
    # (0, LAYER_BG1, "kaleidoscope2"),
    # (0, LAYER_BG1, "kaleidoscope3"),
    (0, LAYER_BG1, "linearcloner"),
    (0, LAYER_BG1, "metashape"),
    (0, LAYER_BG1, "mirror"),
    (0, LAYER_BG1, "pointgrid"),
    # (0, LAYER_BG1, "polarkaleido"),
    # (0, LAYER_BG1, "polarkaleido2"),
    # (0, LAYER_BG1, "polarkaleido3"),
    # (0, LAYER_BG1, "polarkaleido4"),
    # (0, LAYER_BG1, "polarkaleido5"),
    (0, LAYER_BG1, "colormorph"),
    # (0, LAYER_BG1, "greenhousevideo"),
]

dashboard_effects = [
    (0, LAYER_POST_EFFECTS, "suckr"),
    (0, LAYER_POST_EFFECTS, "threshold"),
    (0, LAYER_POST_EFFECTS, "vignette"),
    (0, LAYER_POST_EFFECTS, "blow"),
    (0, LAYER_POST_EFFECTS, "edgedetection"),
    (0, LAYER_POST_EFFECTS, "heat"),
    (0, LAYER_POST_EFFECTS, "heat2"),
    (0, LAYER_POST_EFFECTS, "infinitezoom"),
]


# SHORTCUT: just use one intensity of effects
effects_by_intensity = [
    [e for e in effects if e[0] == 0],
    [e for e in effects if e[0] == 0],
    [e for e in effects if e[0] == 0],
]


IntensityTemplate = namedtuple('IntensityTemplate', [
    "active_layers",
    "effect_count_by_intensity",
])

intensity_templates = [
    # 0-4
    [IntensityTemplate(1, (0, 0, 0))],
    [IntensityTemplate(1, (0, 0, 0))],
    [
        IntensityTemplate(1, (0, 0, 0)),
        IntensityTemplate(1, (0, 0, 0)),
        IntensityTemplate(1, (1, 0, 0))
    ],
    [IntensityTemplate(1, (2, 0, 0))],
    [IntensityTemplate(2, (1, 0, 0))],

    # 5
    [
        IntensityTemplate(1, (1, 1, 0)),
        IntensityTemplate(1, (2, 0, 0)),
        IntensityTemplate(2, (2, 0, 0)),
        IntensityTemplate(2, (1, 0, 0)),
    ],

    # 6
    [
        IntensityTemplate(1, (1, 1, 0)),
        IntensityTemplate(1, (2, 0, 0)),
        IntensityTemplate(2, (1, 1, 0)),
        IntensityTemplate(2, (2, 0, 0)),
    ],

    # 7
    [
        IntensityTemplate(2, (1, 1, 0)),
        IntensityTemplate(2, (2, 0, 0)),
        IntensityTemplate(2, (1, 1, 0)),
        IntensityTemplate(2, (2, 0, 0)),
    ],

    # 8
    [
        IntensityTemplate(2, (2, 1, 0)),
        IntensityTemplate(2, (3, 0, 0)),
        IntensityTemplate(2, (1, 1, 0)),
        IntensityTemplate(2, (2, 0, 0)),
    ],

    # 9
    [
        IntensityTemplate(2, (1, 1, 0)),
        IntensityTemplate(2, (2, 0, 0)),
        IntensityTemplate(2, (1, 0, 0)),
        IntensityTemplate(2, (1, 0, 0)),
    ],

    # 10
    [
        IntensityTemplate(2, (1, 0, 0)),
        IntensityTemplate(2, (1, 0, 0)),
    ],

    # 11
    [
        IntensityTemplate(2, (1, 1, 0)),
        IntensityTemplate(2, (2, 0, 0)),
        IntensityTemplate(2, (1, 1, 0)),
        IntensityTemplate(2, (2, 0, 0)),
    ],

    # 12
    [
        IntensityTemplate(2, (1, 1, 1)),
        IntensityTemplate(2, (2, 1, 0)),
        IntensityTemplate(2, (3, 0, 0)),
        IntensityTemplate(2, (1, 1, 1)),
        IntensityTemplate(2, (2, 1, 0)),
        IntensityTemplate(2, (3, 0, 0)),
    ],

    # 13
    [
        IntensityTemplate(2, (2, 1, 1)),
        IntensityTemplate(2, (3, 1, 0)),
        IntensityTemplate(2, (2, 1, 1)),
        IntensityTemplate(2, (3, 1, 0)),
    ],

    # 14
    [
        IntensityTemplate(2, (2, 2, 1)),
        IntensityTemplate(2, (3, 2, 0)),
        IntensityTemplate(2, (2, 2, 1)),
        IntensityTemplate(2, (3, 2, 0)),
    ],

    # 15
    [
        IntensityTemplate(2, (3, 1, 1)),
        IntensityTemplate(2, (3, 2, 1)),
    ],

    # 16
    [
        IntensityTemplate(2, (4, 1, 0)),
        IntensityTemplate(2, (4, 0, 1)),
        IntensityTemplate(2, (3, 1, 1)),
    ],

    # 17
    [
        IntensityTemplate(2, (3, 1, 0)),
        IntensityTemplate(2, (3, 0, 1)),
        IntensityTemplate(2, (2, 1, 1)),
    ],

    # 18
    [
        IntensityTemplate(2, (4, 1, 0)),
        IntensityTemplate(2, (4, 0, 1)),
        IntensityTemplate(2, (3, 1, 1)),
    ],

    # 19
    [
        IntensityTemplate(2, (5, 1, 0)),
        IntensityTemplate(2, (5, 0, 1)),
        IntensityTemplate(2, (4, 1, 1)),
        IntensityTemplate(2, (4, 2, 0)),
        IntensityTemplate(2, (4, 1, 1)),
        IntensityTemplate(2, (3, 2, 1)),
    ],
]


# text representation of what's going on currently with ActiveStuff.
effects_state = ""


class ActiveStuff:
  def __init__(self, mb):
    self.mb = mb

    print("initializing sld_resolume_controller so template flow option is 0")
    self.template_flow_option = template_flow_options[0]

    # fx is a list of tuples (layer, effect_name) which correspond to the OSC
    # commands used to trigger those effects
    # layer is 1-indexed
    self.fx = []

    # clips is a list of tuples (layer, clip_idx) which correspond to the OSC
    # commands used to trigger those clips.
    # layer is 1-indexed
    # clip_idx is 1-indexed
    self.clips = []

    self.section = 0

    self.use_dashboard_over_audio_reactive = True

    self.incremental_section_effect = 0

  def load(self, mb):
    self.mb = mb
    # bias template flow option selection based on intensity
    idx = int((get_intensity() / 19) * (len(template_flow_options) - 1))
    choices = [max(0, idx - 1), idx, min(len(template_flow_options) - 1, idx + 1)]
    choice = random.choice(choices)
    print("using template flow template option:", choice, "of", len(template_flow_options))
    self.template_flow_option = template_flow_options[choice]

  def choose_random_clips(self):
    clips = []
    initial_clips = self.template_flow_option.initial_clips

    if LAYER_BG1 in initial_clips:
      chosen_clip = random.choice(bg_clips)
      clips.append((LAYER_BG1, chosen_clip))
    if LAYER_TOP in initial_clips:
      chosen_clip = random.choice(top_clips)
      clips.append((LAYER_TOP, chosen_clip))

    return clips

  def stringify_my_choices(self, mb, clips, fx):
    global effects_state
    mb_string = "layers: {}, effect_count_by_intensity: {}".format(
        mb.active_layers,
        mb.effect_count_by_intensity,
    )
    clips_string = "  CLIPS:" + \
        ", ".join(["({} L{})".format(c[1], c[0]) for c in clips])
    fx_string = "  FX:" + ", ".join(["({}{} i{} L{})".format(
        f[2], "-aur" if (len(f) >= 4 and f[3]) else "", f[0], f[1]) for f in fx])

    effects_state = "\n".join([mb_string, clips_string, fx_string])
    return effects_state

  def _pick_effects(self):
    fx = []
    effect_count_by_intensity = self.mb.effect_count_by_intensity
    has_reactive_effect = False
    for i in range(3):
      for _ in range(effect_count_by_intensity[i]):
        chosen_effect = random.choice(effects_by_intensity[i])
        fx.append(chosen_effect)
        if len(chosen_effect) > 3 and chosen_effect[3]:
          has_reactive_effect = True

    # add dashboard effect if we didn't get one already.
    if (not has_reactive_effect) and int(op('intensity_chop').rows()[0][0].val) >= 5:
      dashboard_effect = random.choice(dashboard_effects)
      fx.append(dashboard_effect)
      print("forcing use of dashboard effect")
    self.fx = fx
    return

  def prepare(self, transition_time=2):
    # set transition mode
    type = random.choice(t)
    for i in [LAYER_BG1, LAYER_TOP]:
      resolume_commands.update_transition_type(i, type)
      resolume_commands.update_transition_time(i, transition_time)

    # start choosing clips
    self.clips = self.choose_random_clips()

    if len(self.clips) < 1:
      print("ERROR: weird, clips was empty.", self.mb.active_layers)

    self.deactivate_all_fx()
    self._pick_effects()

    # reset section
    self.section = 0
    op('section').par.Value0 = self.section

    return

  def activate(self):
      for c in self.clips:
        resolume_commands.activate_clip(c[0], c[1])

      # clear layers not in use
      if LAYER_TOP not in [c[0] for c in self.clips]:
        resolume_commands.clear_layer(LAYER_TOP)

      # activate fx
      for f in self.fx:
        resolume_commands.activate_effect(f[1], f[2])

      self.start_section_timer()
      print(self.stringify_my_choices(self.mb, self.clips, self.fx))
      resolume_commands.resync()
      return

  def start_section_timer(self):
      bpm = op('/project1/ui_container/resolume_container/bpm').par.Value0
      timer_length = (32 * 60) / bpm
      op('section_timer').par.length = timer_length
      op('section_timer').par.start.pulse()
      return

  def increment_section(self):
    self.section = (self.section + 1) % NUM_SECTIONS
    op('section').par.Value0 = self.section

    if self.section == 0:
      print("sld_resolume_controller::increment_section: section 0 prepare and activate")
      self.prepare()
      self.activate()
      print("done preparing and activating")
    elif self.section == 1:
      if self.template_flow_option.section_1_action == ADD_COLOR_FADE:
        print("sld_resolume_controller::increment_section: section 1 ADD_COLOR_FADE")
        self.fx.append((LAYER_BG1, "huerotate"))
        resolume_commands.activate_effect(LAYER_BG1, "huerotate")
        resolume_commands.send("/composition/layers/1/video/effects/huerotate/effect/huerotate", 0.0)
        resolume_commands.send("/composition/layers/1/video/effects/huerotate/effect/huerotate/behaviour/playdirection", 2)

    elif self.section == 2:
      if len(self.clips) < 1:
        print("sld_resolume_controller::increment_section ERROR: clips was empty, resetting.")
        self.prepare()
        self.activate()
        return

      if self.template_flow_option.section_2_action == ADD_TOP_CLIP:
        print("sld_resolume_controller::increment_section: section 2 ADD_TOP_CLIP")
        chosen_clip = random.choice(top_clips)
        self.clips.append((LAYER_TOP, chosen_clip))
        resolume_commands.activate_clip(LAYER_TOP, chosen_clip)

      elif self.template_flow_option.section_2_action == SWAP_BG_CLIP:
        print("sld_resolume_controller::increment_section: section 2 SWAP_BG_CLIP")
        chosen_clip = random.choice(bg_clips)
        while chosen_clip == self.clips[0][1]:
          chosen_clip = random.choice(bg_clips)
        self.clips[0] = (LAYER_BG1, chosen_clip)
        resolume_commands.activate_clip(LAYER_BG1, chosen_clip)

    elif self.section == 3:
      if self.template_flow_option.section_3_action == REMOVE_COLOR_FADE:
        print("sld_resolume_controller::increment_section: section 3 REMOVE_COLOR_FADE")
        resolume_commands.send("/composition/layers/1/video/effects/huerotate/effect/huerotate/behaviour/playdirection", 0)
    return

  def deactivate_active_fx(self):
    for f in self.fx:
      resolume_commands.deactivate_effect(f[0], f[1])
    resolume_commands.deactivate_effect(LAYER_BG1, "huerotate")
    return

  def deactivate_all_fx(self):
    for f in effects:
      resolume_commands.deactivate_effect(f[1], f[2])
    for f in dashboard_effects:
      resolume_commands.deactivate_effect(f[1], f[2])

    resolume_commands.deactivate_effect(LAYER_BG1, "huerotate")
    return


ast = ActiveStuff(IntensityTemplate(2, (1, 0, 0)))


def load_pattern_and_play(transition_time=2):
  i = int(op('intensity_chop').rows()[0][0].val)
  print("sld_resolume_controller::load_pattern_and_play with intensity: ", i)

  # pick a template
  ast.load(random.choice(intensity_templates[i]))

  ast.prepare(transition_time)
  ast.activate()
  return


def full_reset(deactivate_all=False):
  global ast
  print("sld_resolume_controller::full_reset called.")
  if deactivate_all:
    ast.deactivate_all_fx()
  else:
    ast.deactivate_active_fx()

  resolume_commands.clear()
  op('section_timer').par.initialize.pulse()

  return


def fadeout(transition_time):
  resolume_commands.update_transition_time(LAYER_BG1, transition_time)
  resolume_commands.update_transition_time(LAYER_TOP, transition_time)
  resolume_commands.clear()


def on_bpm_change(bpm, restart_section=True, resync=False):
  print("resolume_controller::update_bpm called", restart_section, bpm)

  resolume_commands.update_bpm(bpm)
  if resync:
    resolume_commands.resync()

  if restart_section:
    print("bpm change load pattern and play")
    load_pattern_and_play()

  return


def set_is_playlist_audio(val):
  return


def on_section_timer_complete():
  ast.increment_section()
  return


def get_intensity():
  return int(op('intensity_chop')[0, 0])

def set_intensity(num):
  global intensity
  intensity = num
  return


def choose_intensity(num):
  set_intensity(num)
  op('/project1/ui_container/resolume_container/knobFixed').par.Value0 = num/19
  ast.load(random.choice(intensity_templates[num]))
  ast.prepare()
  return


def activate():
  ast.activate()
  return


def increment_section():
  ast.increment_section()
  return
