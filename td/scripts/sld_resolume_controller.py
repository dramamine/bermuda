# me - this DAT
#
# channel - the Channel object which has changed
# sampleIndex - the index of the changed sample
# val - the numeric value of the changed sample
# prev - the previous sample value
#
# Make sure the corresponding toggle is enabled in the CHOP Execute DAT.
import sld_resolume_commands as resolume_commands
from collections import namedtuple
import random

NUM_SECTIONS = 4

LAYER_BG = 1
LAYER_MASK = 2
LAYER_TOP = 3
LAYER_POST_EFFECTS = 5

# trasnsitions that are fun for the bg layer
t = [1, 3, 8, 10, 12, 13, 15, 17, 18, 19, 21, 31, 39, 46, 48]

# these numbers match up with empty clips in the resolume composition
v = [0, 40, 72, 89]
bg_clips_by_intensity = [
  range(v[0]+1, v[1]),
  range(v[0]+1, v[2]),
  range(v[1]+1, v[2]),
  range(v[1]+1, v[3]),
  range(v[2]+1, v[3]),
]

# these numbers match up with empty clips in the resolume composition

m = [0, 16, 27, 39]
mask_clips_by_intensity = [
  range(m[0]+1, m[1]),
  range(m[0]+1, m[2]),
  range(m[1]+1, m[2]),
  range(m[1]+1, m[3]),
  range(m[2]+1, m[3]),
]

top_clips = range(1, 20)

# list of tuples (intensity, layer, effect_name, is_audio_reactive)
effects = [
  (0, LAYER_BG, "slide"),
  (0, LAYER_BG, "slide2"),
  (0, LAYER_BG, "huerotate", True),
  # placeholder: note that huerotate2 is special and is not in this list
  (0, LAYER_BG, "suckr"),
  (0, LAYER_BG, "threshold", True),
  (0, LAYER_BG, "vignette", True),
  (0, LAYER_BG, "blow", True),
  (0, LAYER_BG, "edgedetection"),
  (0, LAYER_BG, "ezradialcloner"),
  (0, LAYER_BG, "ezradialcloner2"),
  (0, LAYER_BG, "goo"),
  (0, LAYER_BG, "gridcloner"),
  (0, LAYER_BG, "heat", True),
  (0, LAYER_BG, "heat2", True),
  (0, LAYER_BG, "infinitezoom"),
  (0, LAYER_BG, "infinitezoom2", True),
  (0, LAYER_BG, "kaleidoscope"),
  (0, LAYER_BG, "kaleidoscope2"),
  (0, LAYER_BG, "kaleidoscope3"),
  (0, LAYER_BG, "linearcloner"),
  (0, LAYER_BG, "metashape"),
  (0, LAYER_BG, "mirror"),
  (0, LAYER_BG, "pointgrid"),
  (0, LAYER_BG, "polarkaleido"),
  (0, LAYER_BG, "polarkaleido2"),
  (0, LAYER_BG, "polarkaleido3"),
  (0, LAYER_BG, "polarkaleido4"),
  (0, LAYER_BG, "polarkaleido5"),

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

# TODO need more intesnisities with just the first layer. maybe 0-4?
# TODO intensity_templates still unused
intensity_templates = [
  # 0-4
  [IntensityTemplate(1, 0, (0, 0, 0))],
  [IntensityTemplate(1, 0, (0, 0, 0))],
  [IntensityTemplate(1, 0, (1, 0, 0))],
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


def divide_into_twos(num):
  if num <= 0:
    return [0, 0]
  numbers = sorted(random.sample(range(num), 1))
  bob1 = numbers[0]
  bob2 = num - numbers[0]
  return random.choice( [[bob1, bob2], [bob2, bob1]] )

def divide_into_threes(num):
  if num <= 0:
    return [0, 0, 0]
  numbers = sorted(random.sample(range(num), 2))
  bob1 = numbers[0]
  bob2 = numbers[1] - numbers[0]
  bob3 = num - numbers[1]
  return random.choice([ [bob1, bob2, bob3], [bob3, bob2, bob1] ])

def get_array_with_total(len, val, cap = None):
  res = [0] * len
  while val > 0:
    idx = random.randint(0, len - 1)
    if cap and res[idx] >= cap:
        val -=1
        continue
    res[idx] += 1
    val -= 1
  return res

def reduce_fx(fx, num):
  while (sum(fx) > num):
    idx = random.randint(0, len(fx) - 1)
    if fx[idx] > 0:
      fx[idx] -= 1
  return fx


def get_clips_intensity(active_layers, clip_intensity):
  if active_layers == 1:
    return [clip_intensity]
  if active_layers == 2:
    return [clip_intensity, clip_intensity]# divide_into_twos(clip_intensity)
  if active_layers == 3:
    return [clip_intensity, clip_intensity, clip_intensity] # divide_into_threes(clip_intensity)

# text representation of what's going on currently with ActiveStuff.
# TODO maybe just call an op() and update its value
effects_state = ""

class ActiveStuff:
  def __init__(self, mb):
    self.mb = mb

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
    self.mb = mb

  def choose_random_clips(self, active_layers, clip_intensity):
    clips = []
    if active_layers >= 1:
      # get range for BG layer
      bg_possibilities = bg_clips_by_intensity[clip_intensity]
      chosen_clip = random.choice(bg_possibilities)
      clips.append( (LAYER_BG, chosen_clip) )

    if active_layers >= 2:
      # get range for MASK layer
      mask_possibilities = mask_clips_by_intensity[clip_intensity]
      chosen_clip = random.choice(mask_possibilities)
      clips.append( (LAYER_MASK, chosen_clip) )

    if active_layers >= 3:
      # get range for TOP layer
      chosen_clip = random.choice(top_clips)
      clips.append( (LAYER_TOP, chosen_clip) )

    return clips

  def stringify_my_choices(self, mb, clips, fx):
    global effects_state
    mb_string = "layers: {}, clip_intensity (0-4): {}, effect_count_by_intensity: {}".format(
      mb.active_layers,
      mb.clip_intensity,
      mb.effect_count_by_intensity,
    )
    clips_string = "  CLIPS:" + ", ".join(["({} i{})".format(c[1], c[0]) for c in clips])
    fx_string = "  FX:" + ", ".join(["({}{} i{} L{})".format(f[2], "-aur" if (len(f)>=4 and f[3]) else "", f[0], f[1]) for f in fx])

    effects_state = "\n".join([mb_string, clips_string, fx_string])
    return effects_state

  def prepare(self, transition_time = 2):
    # set transition mode
    type = random.choice(t)
    for i in range(1,4):
      resolume_commands.update_transition_type(i, type)
      resolume_commands.update_transition_time(i, transition_time)

    ## start choosing clips
    self.clips = self.choose_random_clips(self.mb.active_layers, self.mb.clip_intensity)

    if len(self.clips) < 1:
      print("ERROR: weird, clips was empty.", self.mb.active_layers, self.mb.clip_intensity)

    self.deactivate_all_fx()
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

    # reset section
    self.section = 0
    op('section').par.Value0 = self.section

    return

  def activate(self):
      for c in self.clips:
        # print("sld_resolume_controller::activate layer {} clip {}".format(c[0], c[1]))
        resolume_commands.activate_clip(c[0], c[1])

      # clearing out old clips
      if (self.mb.active_layers < 3):
        resolume_commands.clear_layer(3)
      if (self.mb.active_layers < 2):
        resolume_commands.clear_layer(2)

      # activate fx
      for f in self.fx:
        # TODO call resolume about this
        #print("sld_resolume_controller::activate layer {} fx {}".format(f[1], f[2]))
        resolume_commands.activate_effect(f[1], f[2])

      # @TODO set a timer based on BPM to increment the section.
      self.start_section_timer()
      print( self.stringify_my_choices(self.mb, self.clips, self.fx) )
      return
  def start_section_timer(self):
      bpm = op('/project1/ui_container/resolume_container/bpm').par.Value0
      # print("sld_resolume_controller::resetting timer with bpm", bpm)
      timer_length = (32 * 60) / bpm
      op('section_timer').par.length = timer_length
      op('section_timer').par.start.pulse()

  def increment_section(self):
    # print("sld_resolume_controller::increment_section called, it was:", self.section, self.section % NUM_SECTIONS)
    self.section = (self.section + 1) % NUM_SECTIONS
    # print("sld_resolume_controller::increment_section called, its now:", self.section)
    op('section').par.Value0 = self.section

    # switch statement based on section
    if self.section == 0:
      self.prepare()
      self.activate()
    elif self.section == 1:
      # add a variation
      self.fx.append( (LAYER_BG, "huerotate2") )
      resolume_commands.activate_effect(LAYER_BG, "huerotate2")
      resolume_commands.send("/composition/layers/1/video/effects/huerotate2/effect/huerotate", 0.0)
        # FUN INFO: in Resolume, set the effect Start Settings -> Clip Trigger OFF to prevent re-animation when switching clips
        # print("sld_resolume_controller::added huerotate2 to top layer since we incremented section")
    elif self.section == 2:
      # update bg clip
      if len(self.clips) < 1:
        print("sld_resolume_controller::increment_section ERROR: clips was empty, resetting. ")
        self.prepare()
        self.activate()
        return

      clips_intensity = get_clips_intensity(self.mb.active_layers, self.mb.clip_intensity)
      # print("DEBUG: section 2:", clips_intensity, clips_intensity[0])
      bg_clip_intensity = clips_intensity[0]
      # get a random choice that is not the current choice
      chosen_clip = random.choice(bg_clips_by_intensity[bg_clip_intensity])
      while chosen_clip == self.clips[0][1]:
        chosen_clip = random.choice(bg_clips_by_intensity[bg_clip_intensity])

      self.clips[0] = (LAYER_BG, chosen_clip)
      resolume_commands.activate_clip(LAYER_BG, chosen_clip)

      # print("sld_resolume_controller::clips now:", self.clips[0])
      pass
    elif self.section == 3:
      # turn off the variation
        self.fx.append((LAYER_BG, "huerotate3"))
        resolume_commands.activate_effect(LAYER_BG, "huerotate3")
        resolume_commands.send(
            "/composition/layers/1/video/effects/huerotate3/effect/huerotate", 0.0
        )
    return

  def deactivate_active_fx(self):
    # deactivate fx
    for f in self.fx:
      # print("sld_resolume_controller::deactivate fx {} on layer {}".format(f[1], f[0]))
      resolume_commands.deactivate_effect(f[0], f[1])
    # print("deactivating huerotate2")
    # resolume_commands.deactivate_effect(LAYER_BG, "huerotate2")
    return
  def deactivate_all_fx(self):
    # print("sld_resolume_controller::deactivate_all_fx called")
    for f in effects:
      resolume_commands.deactivate_effect(f[1], f[2])
    for f in dashboard_effects:
      resolume_commands.deactivate_effect(f[1], f[2])

    resolume_commands.deactivate_effect(LAYER_BG, "huerotate2")
    resolume_commands.deactivate_effect(LAYER_BG, "huerotate3")
    return

ast = ActiveStuff(IntensityTemplate(2, 0, (1, 0, 0)))

def load_pattern_and_play(transition_time = 2):
  # TODO better reset?
  # full_reset()

  i = int( op('intensity_chop').rows()[0][0].val )
  print("sld_resolume_controller::load_pattern_and_play with intensity: ", i)

  # pick a template
  ast.load( random.choice(intensity_templates[i]) )

  ast.prepare(transition_time)
  ast.activate()
  return

def full_reset(deactivate_all = False):
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
  resolume_commands.update_transition_time(LAYER_BG, transition_time)
  resolume_commands.update_transition_time(LAYER_MASK, transition_time)
  resolume_commands.update_transition_time(LAYER_TOP, transition_time)
  resolume_commands.clear()

def on_bpm_change(bpm, restart_section = True, resync = False):
  print("resolume_controller::update_bpm called", restart_section, bpm)
  resolume_commands.update_bpm(bpm)
  if resync:
    resolume_commands.resync()
  if restart_section:
    print("bpm change load pattern and play")
    load_pattern_and_play()

  return

def set_is_playlist_audio(val):
  #TODO now that dashboard effects and audio effects aren't any different,
  # you can use this fn to decide if you want to show any audio-reactive effects
  # or you want to run in 'silent' mode
  # ast.use_dashboard_over_audio_reactive = val
  return

def on_section_timer_complete():
  ast.increment_section()
  return

def set_intensity(num):
  global intensity
  intensity = num
  return

def choose_intensity(num):
  set_intensity(num)
  op('/project1/ui_container/resolume_container/knobFixed').par.Value0 = num/19
  ast.load( random.choice( intensity_templates[num] ))
  ast.prepare()
  return

def activate():
  ast.activate()
  return

# handler for the button to increment section
def increment_section():
  ast.increment_section()
  return
