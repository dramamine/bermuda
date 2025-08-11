# nosec
import sld_resolume_commands as resolume_commands
from collections import namedtuple
import random

###
# considering adding a 4th layer. what would section progress look like?
#
# 1 layer
# 0: activate bg1 clip
# 1: color fade
# 2: activate bg2 clip, transition bg1 to black
# 3: color fade

# 2 layers
# 0: activate bg1 clip
# 1: color fade
# 2: activate bg2 clip
# 3: color fade

# 2 layers
# 0: activate bg1 clip
# 1: color fade
# 2: activate top clip with black mask
# 3: color fade

# 3 layers
# 0: activate bg1 clip with black mask
# 1: color fade
# 2: activate top clip to fill gap
# 3: color fade

# 3 layers
# 0: activate bg1 clip and bg2 clip
# 1: color fade
# 2: activate top clip with black mask
# 3: color fade

# 4 layers
# 0: activate bg1 clip with black mask
# 1: top layer: transition to a clip
# 2: add bg2 clip
# 3: top layer => black


###

NUM_SECTIONS = 4

LAYER_BG1 = 1
LAYER_TOP = 2
LAYER_MASK = 3
LAYER_POST_EFFECTS = 4


FlowTemplate = namedtuple('FlowTemplate', [
    "initial_clips",
    "section_1_action",
    "section_2_action",
    "section_3_action",
])

ADD_COLOR_FADE = 'ADD_COLOR_FADE'
ACTIVATE_TOP_CLIP_FILL_GAP = 'ACTIVATE_TOP_CLIP_FILL_GAP'
REMOVE_COLOR_FADE = 'REMOVE_COLOR_FADE'
ADD_TOP_CLIP = 'ADD_TOP_CLIP'
ADD_MASK_CLIP_WITH_HEAT = 'ADD_MASK_CLIP_WITH_HEAT'
ADD_TOP_AND_MASK_CLIP_WITH_HEAT = 'ADD_TOP_AND_MASK_CLIP_WITH_HEAT'
ACTIVATE_TOP_CLIP_FILL_GAP_WITH_HEAT = 'ACTIVATE_TOP_CLIP_FILL_GAP_WITH_HEAT'
ADD_MASK_CLIP = 'ADD_MASK_CLIP'

template_flow_option_0 = FlowTemplate(
    initial_clips=[LAYER_BG1],
    section_1_action=ADD_COLOR_FADE,
    section_2_action=ADD_MASK_CLIP,
    section_3_action=REMOVE_COLOR_FADE,
)

template_flow_option_1 = FlowTemplate(
    initial_clips=[LAYER_BG1],
    section_1_action=ADD_COLOR_FADE,
    section_2_action=ADD_MASK_CLIP_WITH_HEAT,
    section_3_action=REMOVE_COLOR_FADE,
)

template_flow_option_2 = FlowTemplate(
    initial_clips=[LAYER_BG1],
    section_1_action=ADD_COLOR_FADE,
    section_2_action=ADD_TOP_AND_MASK_CLIP_WITH_HEAT,
    section_3_action=REMOVE_COLOR_FADE,
)

template_flow_option_3 = FlowTemplate(
    initial_clips=[LAYER_BG1, LAYER_MASK],
    section_1_action=ADD_COLOR_FADE,
    section_2_action=ACTIVATE_TOP_CLIP_FILL_GAP_WITH_HEAT,
    section_3_action=REMOVE_COLOR_FADE,
)

template_flow_option_4 = FlowTemplate(
    initial_clips=[LAYER_BG1, LAYER_MASK],
    section_1_action=ADD_COLOR_FADE,
    section_2_action=ACTIVATE_TOP_CLIP_FILL_GAP,
    section_3_action=REMOVE_COLOR_FADE,
)

template_flow_options = [
    template_flow_option_0,
    template_flow_option_1,
    template_flow_option_2,
    template_flow_option_3,
    template_flow_option_4,
]

# trasnsitions that are fun for the bg layer
t = [1, 3, 8, 10, 12, 13, 15, 17, 18, 19, 21, 31, 39, 46, 48]

# these numbers match up with empty clips in the resolume composition
v = [0, 35, 66, 84]
bg_clips_by_intensity = [
    range(v[0]+1, v[1]),
    range(v[0]+1, v[2]),
    range(v[1]+1, v[2]),
    range(v[1]+1, v[3]),
    range(v[2]+1, v[3]),
]

# these numbers match up with empty clips in the resolume composition

m = [0, 16, 27, 38]
mask_clips_by_intensity = [
    range(m[0]+1, m[1]),
    range(m[0]+1, m[2]),
    range(m[1]+1, m[2]),
    range(m[1]+1, m[3]),
    range(m[2]+1, m[3]),
]

top_clips = range(2, 23)

# list of tuples (intensity, layer, effect_name, is_audio_reactive)
effects = [
    (0, LAYER_BG1, "slide"),
    (0, LAYER_BG1, "slide2"),
    # placeholder: note that huerotate is special and is not in this list
    (0, LAYER_BG1, "huerotate2", True),
    (0, LAYER_BG1, "suckr"),
    (0, LAYER_BG1, "threshold", True),
    (0, LAYER_BG1, "vignette", True),
    (0, LAYER_BG1, "blow", True),
    (0, LAYER_BG1, "edgedetection"),
    (0, LAYER_BG1, "ezradialcloner"),
    (0, LAYER_BG1, "ezradialcloner2"),
    (0, LAYER_BG1, "goo"),
    (0, LAYER_BG1, "gridcloner"),
    (0, LAYER_BG1, "heat", True),
    (0, LAYER_BG1, "heat2", True),
    (0, LAYER_BG1, "infinitezoom"),
    (0, LAYER_BG1, "infinitezoom2", True),
    (0, LAYER_BG1, "kaleidoscope"),
    (0, LAYER_BG1, "kaleidoscope2"),
    (0, LAYER_BG1, "kaleidoscope3"),
    (0, LAYER_BG1, "linearcloner"),
    (0, LAYER_BG1, "metashape"),
    (0, LAYER_BG1, "mirror"),
    (0, LAYER_BG1, "pointgrid"),
    (0, LAYER_BG1, "polarkaleido"),
    (0, LAYER_BG1, "polarkaleido2"),
    (0, LAYER_BG1, "polarkaleido3"),
    (0, LAYER_BG1, "polarkaleido4"),
    (0, LAYER_BG1, "polarkaleido5"),
    (0, LAYER_BG1, "colormorph"),
    (0, LAYER_BG1, "greenhousevideo"),

    (0, LAYER_MASK, "slide", True),
    (0, LAYER_MASK, "slide2"),
    (0, LAYER_MASK, "slide3"),
    (0, LAYER_MASK, "radialmask"),
    (0, LAYER_MASK, "kaleidoscope"),
    (1, LAYER_MASK, "kaleidoscope2"),
    (2, LAYER_MASK, "kaleidoscope3"),
    (0, LAYER_MASK, "ezradialcloner"),
    (0, LAYER_MASK, "displace", True),
    (1, LAYER_MASK, "displace2", True),
    (2, LAYER_MASK, "displace3", True),
    (0, LAYER_MASK, "distortion", True),
    (1, LAYER_MASK, "distortion2", True),
    (2, LAYER_MASK, "distortion3", True),
    (2, LAYER_MASK, "trails"),
    (1, LAYER_MASK, "greenhousevideo"),
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


# get the effects above where the intensity is 0
effects_by_intensity = [
    [e for e in effects if e[0] == 0],
    [e for e in effects if e[0] == 1],
    [e for e in effects if e[0] == 2],
]


IntensityTemplate = namedtuple('IntensityTemplate', [
    "active_layers",
    "clip_intensity",
    "effect_count_by_intensity",
])

intensity_templates = [
    # 0-4
    [IntensityTemplate(1, 0, (0, 0, 0))],
    [IntensityTemplate(1, 0, (0, 0, 0))],
    [  # 0 or 1 simple effect
        IntensityTemplate(1, 0, (0, 0, 0)),
        IntensityTemplate(1, 0, (0, 0, 0)),
        IntensityTemplate(1, 0, (1, 0, 0))
    ],
    [IntensityTemplate(1, 1, (2, 0, 0))],
    [IntensityTemplate(2, 0, (1, 0, 0))],

    # 5
    [
        IntensityTemplate(1, 1, (1, 1, 0)),
        IntensityTemplate(1, 1, (2, 0, 0)),
        IntensityTemplate(2, 1, (2, 0, 0)),
        IntensityTemplate(2, 1, (1, 0, 0)),
    ],

    # 6
    [
        IntensityTemplate(1, 2, (1, 1, 0)),
        IntensityTemplate(1, 2, (2, 0, 0)),
        IntensityTemplate(2, 1, (1, 1, 0)),
        IntensityTemplate(2, 1, (2, 0, 0)),
    ],

    # 7
    [
        IntensityTemplate(2, 2, (1, 1, 0)),
        IntensityTemplate(2, 2, (2, 0, 0)),
        IntensityTemplate(2, 3, (1, 1, 0)),
        IntensityTemplate(2, 3, (2, 0, 0)),
    ],

    # 8
    [
        IntensityTemplate(2, 2, (2, 1, 0)),
        IntensityTemplate(2, 2, (3, 0, 0)),
        IntensityTemplate(2, 3, (1, 1, 0)),
        IntensityTemplate(2, 3, (2, 0, 0)),
    ],

    # 9
    [
        IntensityTemplate(3, 2, (1, 1, 0)),
        IntensityTemplate(3, 2, (2, 0, 0)),
        IntensityTemplate(3, 3, (1, 0, 0)),
        IntensityTemplate(3, 3, (1, 0, 0)),
    ],

    # 10
    [
        IntensityTemplate(2, 4, (1, 0, 0)),
        IntensityTemplate(3, 3, (1, 0, 0)),
    ],

    # 11
    [
        IntensityTemplate(2, 4, (1, 1, 0)),
        IntensityTemplate(2, 4, (2, 0, 0)),
        IntensityTemplate(3, 3, (1, 1, 0)),
        IntensityTemplate(3, 3, (2, 0, 0)),
    ],

    # 12
    [
        IntensityTemplate(2, 4, (1, 1, 1)),
        IntensityTemplate(2, 4, (2, 1, 0)),
        IntensityTemplate(2, 4, (3, 0, 0)),
        IntensityTemplate(3, 3, (1, 1, 1)),
        IntensityTemplate(3, 3, (2, 1, 0)),
        IntensityTemplate(3, 3, (3, 0, 0)),
    ],

    # 13
    [
        IntensityTemplate(2, 4, (2, 1, 1)),
        IntensityTemplate(2, 4, (3, 1, 0)),
        IntensityTemplate(3, 3, (2, 1, 1)),
        IntensityTemplate(3, 3, (3, 1, 0)),
    ],

    # 14
    [
        IntensityTemplate(2, 4, (2, 2, 1)),
        IntensityTemplate(2, 4, (3, 2, 0)),
        IntensityTemplate(3, 3, (2, 2, 1)),
        IntensityTemplate(3, 3, (3, 2, 0)),
    ],

    # 15
    [
        IntensityTemplate(3, 3,  (3, 1, 1)),
        IntensityTemplate(3, 3,  (3, 2, 1))
    ],

    # 16
    [
        IntensityTemplate(3, 3,  (4, 1, 0)),
        IntensityTemplate(3, 3,  (4, 0, 1)),
        IntensityTemplate(3, 3,  (3, 1, 1)),
    ],

    # 17
    [
        IntensityTemplate(3, 4,  (3, 1, 0)),
        IntensityTemplate(3, 4,  (3, 0, 1)),
        IntensityTemplate(3, 4,  (2, 1, 1)),
    ],

    # 18
    [
        IntensityTemplate(3, 4,  (4, 1, 0)),
        IntensityTemplate(3, 4,  (4, 0, 1)),
        IntensityTemplate(3, 4,  (3, 1, 1)),
    ],

    # 19
    [
        IntensityTemplate(3, 4,  (5, 1, 0)),
        IntensityTemplate(3, 4,  (5, 0, 1)),
        IntensityTemplate(3, 4,  (4, 1, 1)),
        IntensityTemplate(3, 4,  (4, 2, 0)),
        IntensityTemplate(3, 4,  (4, 1, 1)),
        IntensityTemplate(3, 4,  (3, 2, 1)),
    ],
]


def get_clips_intensity(active_layers, clip_intensity):
  if active_layers == 1:
    return [clip_intensity]
  if active_layers == 2:
    return [clip_intensity, clip_intensity]
  if active_layers == 3:
    return [clip_intensity, clip_intensity, clip_intensity]


# text representation of what's going on currently with ActiveStuff.
# TODO maybe just call an op() and update its value
effects_state = ""


class ActiveStuff:
  def __init__(self, mb):
    # intensity template
    self.mb = mb

    print("initializing sld_resolume_controller so template flow option is 0")
    # TODO make this dynamic, maybe by adding to intensity templates
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

    # TODO reconsider, right now it's just true always
    self.use_dashboard_over_audio_reactive = True

    # some random number to decide what to do with the section changes
    # TODO hardcoded to 0 for now for huerotate on BG layer
    self.incremental_section_effect = 0

  def load(self, mb):
    # print("sld_resolume_controller::load called with mb:", mb)
    self.mb = mb
    # bias template flow option selection based on mb.intensity
    # earlier options for low intensity, later options for high intensity
    idx = int((get_intensity() / 19) * (len(template_flow_options) - 1))
    # add some randomness around the biased index
    choices = [max(0, idx - 1), idx, min(len(template_flow_options) - 1, idx + 1)]
    choice = random.choice(choices)
    print("using template flow template option:", choice, "of", len(template_flow_options))
    self.template_flow_option = template_flow_options[choice]


  def choose_random_clips(self):
    clips = []
    initial_clips = self.template_flow_option.initial_clips
    clip_intensity = self.mb.clip_intensity

    # print("initial_clips:", initial_clips, "clip_intensity:", clip_intensity)

    if LAYER_BG1 in initial_clips:
      chosen_clip = random.choice(bg_clips_by_intensity[clip_intensity])
      clips.append((LAYER_BG1, chosen_clip))
    if LAYER_MASK in initial_clips:
      chosen_clip = random.choice(mask_clips_by_intensity[clip_intensity])
      clips.append((LAYER_MASK, chosen_clip))
    if LAYER_TOP in initial_clips:
      chosen_clip = random.choice(top_clips)
      clips.append((LAYER_TOP, chosen_clip))
    # special case where we show black top clip when LAYER_MASK is present but LAYER_TOP is not
    elif LAYER_MASK in initial_clips:
      clips.append([LAYER_TOP, 1]) # black top clip
    # print("using clips:", clips)
    return clips

  def stringify_my_choices(self, mb, clips, fx):
    global effects_state
    mb_string = "layers: {}, clip_intensity (0-4): {}, effect_count_by_intensity: {}".format(
        mb.active_layers,
        mb.clip_intensity,
        mb.effect_count_by_intensity,
    )
    clips_string = "  CLIPS:" + \
        ", ".join(["({} i{})".format(c[1], c[0]) for c in clips])
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
    # TODO consider adding something like this for audio-reactive effects
    if (not has_reactive_effect) and int(op('intensity_chop').rows()[0][0].val) >= 5:
      dashboard_effect = random.choice(dashboard_effects)
      fx.append(dashboard_effect)
      print("forcing use of dashboard effect")
    self.fx = fx
    return

  def prepare(self, transition_time=2):
    # set transition mode
    type = random.choice(t)
    for i in range(1, 4): # # of layers
      resolume_commands.update_transition_type(i, type)
      resolume_commands.update_transition_time(i, transition_time)

    # start choosing clips
    self.clips = self.choose_random_clips()

    if len(self.clips) < 1:
      print("ERROR: weird, clips was empty.",
        self.mb.active_layers, self.mb.clip_intensity)

    self.deactivate_all_fx()
    self._pick_effects()

    # reset section
    self.section = 0
    op('section').par.Value0 = self.section

    return

  def activate(self):
      for c in self.clips:
        # print("sld_resolume_controller::activate layer {} clip {}".format(c[0], c[1]))
        resolume_commands.activate_clip(c[0], c[1])

      # check clips, if none of the clips[0] prperties are LAYER_MASK, then clear that layer
      if LAYER_MASK not in [c[0] for c in self.clips]:
        # print("sld_resolume_controller::activate: clearing layer {}".format(LAYER_MASK))
        resolume_commands.clear_layer(LAYER_MASK)
      if LAYER_TOP not in [c[0] for c in self.clips]:
        # print("sld_resolume_controller::activate: clearing layer {}".format(LAYER_TOP))
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
      # print("TODO WORKING?? sld_resolume_controller::resetting timer with bpm", bpm)
      timer_length = (32 * 60) / bpm
      op('section_timer').par.length = timer_length
      op('section_timer').par.start.pulse()
      return

  def increment_section(self):
    self.section = (self.section + 1) % NUM_SECTIONS
    op('section').par.Value0 = self.section

    # switch statement based on section
    if self.section == 0:
      print("sld_resolume_controller::increment_section: section 0 prepare and activate")
      self.prepare()
      self.activate()
      print("done preparing and activating")
    elif self.section == 1:
      # add a variation
      if self.template_flow_option.section_1_action == ADD_COLOR_FADE:
        print("sld_resolume_controller::increment_section: section 1 ADD_COLOR_FADE")
        self.fx.append((LAYER_BG1, "huerotate"))
        resolume_commands.activate_effect(LAYER_BG1, "huerotate")
        resolume_commands.send("/composition/layers/1/video/effects/huerotate/effect/huerotate", 0.0)
        resolume_commands.send("/composition/layers/1/video/effects/huerotate/effect/huerotate/behaviour/playdirection", 2)
        # FUN INFO: in Resolume, set the effect Start Settings -> Clip Trigger OFF to prevent re-animation when switching clips
        # print("sld_resolume_controller::added huerotate to top layer since we incremented section")

    elif self.section == 2:

      # TODO could delete this block maybe
      # update bg clip
      if len(self.clips) < 1:
        print(
            "sld_resolume_controller::increment_section ERROR: clips was empty, resetting. ")
        self.prepare()
        self.activate()
        return

      if self.template_flow_option.section_2_action == ACTIVATE_TOP_CLIP_FILL_GAP:
        print("sld_resolume_controller::increment_section: section 2 ACTIVATE_TOP_CLIP_FILL_GAP")
        # print("sld_resolume_controller::section 2: activating top clip to fill gap")
        # activate a top clip to fill the gap
        chosen_clip = random.choice(top_clips)
        self.clips.append((LAYER_TOP, chosen_clip))
        resolume_commands.activate_clip(LAYER_TOP, chosen_clip)

      elif self.template_flow_option.section_2_action == 'DEPRECATED_SECTION_2_ACTION':
        print("sld_resolume_controller::increment_section: section 2 DEPRECATED_SECTION_2_ACTION")
        clips_intensity = get_clips_intensity(
            self.mb.active_layers, self.mb.clip_intensity)
        # print("DEBUG: section 2:", clips_intensity, clips_intensity[0])
        bg_clip_intensity = clips_intensity[0]
        # get a random choice that is not the current choice
        chosen_clip = random.choice(bg_clips_by_intensity[bg_clip_intensity])
        while chosen_clip == self.clips[0][1]:
          chosen_clip = random.choice(bg_clips_by_intensity[bg_clip_intensity])

        self.clips[0] = (LAYER_BG1, chosen_clip)
        resolume_commands.activate_clip(LAYER_BG1, chosen_clip)

      elif self.template_flow_option.section_2_action == ADD_TOP_CLIP:
        print("sld_resolume_controller::increment_section: section 2 ADD_TOP_CLIP")
        # activate a top clip to fill the gap
        chosen_clip = random.choice(top_clips)
        self.clips.append((LAYER_TOP, chosen_clip))
        resolume_commands.activate_clip(LAYER_TOP, chosen_clip)

      elif self.template_flow_option.section_2_action == ADD_MASK_CLIP_WITH_HEAT:
        print("sld_resolume_controller::increment_section: section 2 ADD_MASK_CLIP_WITH_HEAT")
        # activate a mask clip with heat
        chosen_clip = random.choice(mask_clips_by_intensity[self.mb.clip_intensity])
        self.clips.append((LAYER_MASK, chosen_clip))
        resolume_commands.activate_clip(LAYER_MASK, chosen_clip)

        self.clips.append((LAYER_TOP, 1))  # black top clip
        resolume_commands.activate_clip(LAYER_TOP, 1)  # black top clip

        self.fx.append((LAYER_MASK, "heat"))
        resolume_commands.activate_effect(LAYER_MASK, "heat")

      elif self.template_flow_option.section_2_action == ADD_TOP_AND_MASK_CLIP_WITH_HEAT:
        print("sld_resolume_controller::increment_section: section 2 ADD_TOP_AND_MASK_CLIP_WITH_HEAT")
        # activate a top clip and a mask clip with heat
        chosen_top_clip = random.choice(top_clips)
        self.clips.append((LAYER_TOP, chosen_top_clip))
        resolume_commands.activate_clip(LAYER_TOP, chosen_top_clip)

        chosen_mask_clip = random.choice(mask_clips_by_intensity[self.mb.clip_intensity])
        self.clips.append((LAYER_MASK, chosen_mask_clip))
        resolume_commands.activate_clip(LAYER_MASK, chosen_mask_clip)
        self.fx.append((LAYER_MASK, "heat"))
        resolume_commands.activate_effect(LAYER_MASK, "heat")
      elif self.template_flow_option.section_2_action == ACTIVATE_TOP_CLIP_FILL_GAP_WITH_HEAT:
        print("sld_resolume_controller::increment_section: section 2 ACTIVATE_TOP_CLIP_FILL_GAP_WITH_HEAT")
        # activate a top clip to fill the gap with heat
        chosen_clip = random.choice(top_clips)
        self.clips.append((LAYER_TOP, chosen_clip))
        resolume_commands.activate_clip(LAYER_TOP, chosen_clip)
        self.fx.append((LAYER_MASK, "heat"))
        resolume_commands.activate_effect(LAYER_TOP, "heat")
      elif self.template_flow_option.section_2_action == ADD_MASK_CLIP:
        print("sld_resolume_controller::increment_section: section 2 ADD_MASK_CLIP")
        # activate a mask clip
        chosen_clip = random.choice(mask_clips_by_intensity[self.mb.clip_intensity])
        self.clips.append((LAYER_MASK, chosen_clip))
        resolume_commands.activate_clip(LAYER_MASK, chosen_clip)

    elif self.section == 3:
      if self.template_flow_option.section_3_action == REMOVE_COLOR_FADE:
        print("sld_resolume_controller::increment_section: section 3 REMOVE_COLOR_FADE")
        resolume_commands.send("/composition/layers/1/video/effects/huerotate/effect/huerotate/behaviour/playdirection", 0)
    return

  # TODO see if this is working as intended or if its just overkill
  def deactivate_active_fx(self):
    # deactivate fx
    for f in self.fx:
      # print("sld_resolume_controller::deactivate fx {} on layer {}".format(f[1], f[0]))
      resolume_commands.deactivate_effect(f[0], f[1])
    # print("deactivating huerotate")
    resolume_commands.deactivate_effect(LAYER_BG1, "huerotate")
    return

  def deactivate_all_fx(self):
    # print("sld_resolume_controller::deactivate_all_fx called")
    for f in effects:
      resolume_commands.deactivate_effect(f[1], f[2])
    for f in dashboard_effects:
      resolume_commands.deactivate_effect(f[1], f[2])

    resolume_commands.deactivate_effect(LAYER_MASK, "heat")
    resolume_commands.deactivate_effect(LAYER_BG1, "huerotate")
    return


ast = ActiveStuff(IntensityTemplate(2, 0, (1, 0, 0)))


def load_pattern_and_play(transition_time=2):
  # TODO better reset?
  # full_reset()
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
  resolume_commands.update_transition_time(LAYER_MASK, transition_time)
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
  # TODO now that dashboard effects and audio effects aren't any different,
  # you can use this fn to decide if you want to show any audio-reactive effects
  # or you want to run in 'silent' mode
  # ast.use_dashboard_over_audio_reactive = val
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

# handler for the button to increment section


def increment_section():
  ast.increment_section()
  return
