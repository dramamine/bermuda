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

# trasnsitions that are fun for the bg layer
t = [1, 3, 8, 10, 12, 13, 15, 17, 18, 19, 21, 31, 39, 46, 48]

# these numbers match up with empty clips in the resolume composition
v = [0, 17, 26, 29]
bg_clips_by_intensity = [
  range(v[0]+1, v[1]),
  range(v[0]+1, v[2]),
  range(v[1]+1, v[2]),
  range(v[1]+1, v[3]),
  range(v[2]+1, v[3]),
]

# these numbers match up with empty clips in the resolume composition

m = [0, 6, 16, 24]
mask_clips_by_intensity = [
  range(m[0]+1, m[1]),
  range(m[0]+1, m[2]),
  range(m[1]+1, m[2]),
  range(m[1]+1, m[3]),
  range(m[2]+1, m[3]),
]

top_clips_by_intensity = [
  range(1, 6),
  range(1, 11),
  range(6, 11),
  range(6, 16),
  range(11, 16),
]

# def triple(str):
#   return [str, str+"2", str+"3"]

# bg_layer_effects = [
#   "slide",
#   "slide2",
#   "slide3",
#   "huerotate",
#   "suckr"
# ]

# mask_layer_effects = [
#   "slide",
#   "slide2",
#   "slide3",
#   # TODO radialmask needs to be paired with one of kaleidoscope(0-2)
#   # "radialmask",
#   # triple("displace"),
#   # triple("distortion"),
#   "trails",
#   "ezradialcloner",
# ]

# top_layer_effects = [
#   "huerotate",
# ]

# effects_by_layer = [
#   bg_layer_effects,
#   mask_layer_effects,
#   top_layer_effects
# ]

# list of tuples (intensity, layer, effect_name)
effects = [
  (0, LAYER_BG, "slide"),
  (0, LAYER_BG, "slide2"),
  (0, LAYER_BG, "slide3"),
  (0, LAYER_BG, "huerotate"),
  (0, LAYER_BG, "suckr"),
  # placeholder: note that huerotate2 is special and is not in this list
  (0, LAYER_MASK, "slide"),
  (0, LAYER_MASK, "slide2"),
  (0, LAYER_MASK, "slide3"),
  (0, LAYER_MASK, "radialmask"),
  (0, LAYER_MASK, "kaleidoscope"),
  (1, LAYER_MASK, "kaleidoscope2"),
  (2, LAYER_MASK, "kaleidoscope3"),
  (0, LAYER_MASK, "ezradialcloner"),
  (0, LAYER_MASK, "displace"),
  (1, LAYER_MASK, "displace2"),
  (2, LAYER_MASK, "displace3"),
  (0, LAYER_MASK, "distortion"),
  (1, LAYER_MASK, "distortion2"),
  (2, LAYER_MASK, "distortion3"),
  (2, LAYER_MASK, "trails"),
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
  [IntensityTemplate(1, 0, (0, 0, 0))],
  [IntensityTemplate(2, 0, (0, 0, 0))],
  [IntensityTemplate(2, 1, (0, 0, 0))],
  [IntensityTemplate(2, 1, (1, 0, 0))],

  [
    IntensityTemplate(2, 1, (0, 1, 0)),
    IntensityTemplate(2, 1, (2, 0, 0)),
    IntensityTemplate(2, 2, (1, 0, 0)),
  ],

  [
    IntensityTemplate(2, 1, (1, 1, 0)),
    IntensityTemplate(2, 2, (0, 1, 0)),
    IntensityTemplate(2, 2, (2, 0, 0)),
  ],

  [
    IntensityTemplate(2, 2, (1, 1, 0)),
  ],

  [
    IntensityTemplate(2, 2, (0, 2, 0)),
    IntensityTemplate(2, 2, (0, 0, 1)),
  ],

  [
    IntensityTemplate(3, 0, (1, 0, 0)),
  ],

  [
    IntensityTemplate(3, 1, (1, 0, 0)),
    IntensityTemplate(3, 0, (0, 1, 0)),
  ],

  [
    IntensityTemplate(3, 1, (2, 0, 0)),
    IntensityTemplate(3, 1, (2, 1, 0)),
  ],

  [
    IntensityTemplate(3, 2, (1, 1, 0))
  ],

  [
    IntensityTemplate(3, 3, (1, 1, 0))
  ],

  [
    IntensityTemplate(3, 3, (2, 1, 0))
  ],

  [
    IntensityTemplate(3, 3,  (3, 1, 0))
  ],

  [
      IntensityTemplate(3, 3,  (4, 1, 0)),
      IntensityTemplate(3, 3,  (4, 0, 1)),
      IntensityTemplate(3, 3,  (3, 1, 1)),
  ],

  [
      IntensityTemplate(3, 4,  (3, 1, 0)),
      IntensityTemplate(3, 4,  (3, 0, 1)),
      IntensityTemplate(3, 4,  (2, 1, 1)),
  ],

  [
      IntensityTemplate(3, 4,  (4, 1, 0)),
      IntensityTemplate(3, 4,  (4, 0, 1)),
      IntensityTemplate(3, 4,  (3, 1, 1)),
  ],

  [
      IntensityTemplate(3, 4,  (5, 1, 0)),
      IntensityTemplate(3, 4,  (5, 0, 1)),
      IntensityTemplate(3, 4,  (4, 1, 1)),
      IntensityTemplate(3, 4,  (4, 2, 0)),
      IntensityTemplate(3, 4,  (4, 1, 1)),
      IntensityTemplate(3, 4,  (3, 2, 1)),
  ],

  [
      IntensityTemplate(3, 5,  (3, 1, 0)),
      IntensityTemplate(3, 5,  (3, 0, 1)),
      IntensityTemplate(3, 5,  (2, 1, 1)),
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
    return divide_into_twos(clip_intensity)
  if active_layers == 3:
    return divide_into_threes(clip_intensity)

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

    # some random number to decide what to do with the section changes
    # TODO hardcoded to 0 for now for huerotate on BG layer
    self.incremental_section_effect = 0

  def load(self, mb):
    self.mb = mb

  def prepare(self):
    print("using template:", self.mb)

    # set transition mode
    resolume_commands.update_transition_type(LAYER_BG, random.choice(t))

    clips_intensity = get_clips_intensity(self.mb.active_layers, self.mb.clip_intensity)
    clips = []
    for i in range(self.mb.active_layers):
      idx = clips_intensity[i]
      chosen_clip = random.choice(bg_clips_by_intensity[idx])
      clips.append( (i+1, chosen_clip) )
    self.clips = clips

    # TODO intensity
    # effect_intensities = get_array_with_total(self.mb.effect_count, self.mb.effect_intensity, 2)

    fx = []
    # for i in range(self.mb.effect_count):
    #   layer = random.randint(0, self.mb.active_layers-1)
    #   options = effects_by_layer[layer]
    #   chosen_effect = random.choice(options)
    #   fx.append( (layer+1, chosen_effect) )
    effect_count_by_intensity = self.mb.effect_count_by_intensity
    for i in range(3):
      for j in range(effect_count_by_intensity[i]):
        chosen_effect = random.choice(effects_by_intensity[i])
        fx.append(chosen_effect)


    self.fx = fx

    self.section = 0
    op('section').par.Value0 = self.section

    return

  def activate(self):
      print("activating...")
      for c in self.clips:
        print("activate layer {} clip {}".format(c[0], c[1]))
        resolume_commands.activate_clip(c[0], c[1])
      # activate fx
      for f in self.fx:
        # TODO call resolume about this
        print("activate layer {} fx {}".format(f[1], f[2]))
        resolume_commands.activate_effect(f[1], f[2])

      self.pretty_print()
      return

  def increment_section(self):
    self.section = (self.section + 1) % NUM_SECTIONS
    op('section').par.Value0 = self.section

    # switch statement based on section
    if self.section == 0:
      self.prepare()
      self.activate()
    elif self.section == 1:
      # add a variation
      if self.incremental_section_effect == 0:
        self.fx.append( (LAYER_BG, "huerotate2") )
        resolume_commands.activate_effect(LAYER_BG, "huerotate2")
        resolume_commands.send(
            "/composition/layers/1/video/effects/huerotate2/effect/huerotate", 0.0
          )
        # FUN INFO: in Resolume, set the effect Start Settings -> Clip Trigger OFF to prevent re-animation when switching clips
        print("added huerotate2 to top layer since we incremented section")
    elif self.section == 2:
      # update bg clip
      print("clips was:", self.clips[0])

      clips_intensity = get_clips_intensity(self.mb.active_layers, self.mb.clip_intensity)
      bg_clip_intensity = clips_intensity[0]
      # get a random choice that is not the current choice
      chosen_clip = random.choice(bg_clips_by_intensity[bg_clip_intensity])
      while chosen_clip == self.clips[0][1]:
        chosen_clip = random.choice(bg_clips_by_intensity[bg_clip_intensity])

      self.clips[0] = (LAYER_BG, chosen_clip)
      resolume_commands.activate_clip(LAYER_BG, chosen_clip)


      print("clips now:", self.clips[0])
      pass
    elif self.section == 3:
      # turn off the variation
      if self.incremental_section_effect == 0:
        self.fx.append( (LAYER_BG, "huerotate2") )
        resolume_commands.deactivate_effect(LAYER_BG, "huerotate2")
        print("turned off huerotate2 cuz of section 3")
    return

  # debug string about current state of ActiveStuff
  def pretty_print(self):
    global effects_state

    mb_string = "active_layers: {}, clip_intensity: {}, effect_count_by_intensity: {}".format(
      self.mb.active_layers,
      self.mb.clip_intensity,
      self.mb.effect_count_by_intensity,
    )
    clips_string = "CLIPS:" + ", ".join(["({}, {})".format(c[0], c[1]) for c in self.clips])
    fx_string = "FX:" + ", ".join(["({}, {}, {})".format(f[0], f[1], f[2]) for f in self.fx])

    effects_state = "\n".join([mb_string, clips_string, fx_string])
    return effects_state


  def deactivate(self):
    # deactivate fx
    for f in self.fx:
      # TODO call resolume about this
      print("deactivate fx {} on layer {}".format(f[1], f[0]))
      resolume_commands.deactivate_effect(f[0], f[1])
    return

ast = ActiveStuff(IntensityTemplate(2, 0, (1, 0, 0)))

def demo_update():
  global ast
  print("demo_update called")
  # ast.load(intensity_templates[0])
  ast.deactivate()

  # read intensity
  i = int( op('intensity_chop').rows()[0][0].val )
  print(i)

  # pick a template
  ast.load( random.choice(intensity_templates[i]) )

  ast.prepare()
  ast.activate()
  return

def full_reset():
  global ast
  print("full_reset called")
  ast.deactivate()

  resolume_commands.clear()

  for f in effects:
    resolume_commands.deactivate_effect(f[1], f[2])
  # for effect_name in effects_by_layer[i]:
  #   resolume_commands.deactivate_effect(i+1, effect_name)

  return

# def choose_and_activate_template(intensity):
#   print("using intensity", intensity)
#   # choose a pattern
#   assert intensity < len(intensity_templates), "intensity out of range"
#   ast.deactivate()

#   pattern = random.choice(intensity_templates[intensity])
#   ast.load(pattern)
#   ast.prepare()
#   ast.activate()
#   return


# # some range
# intensity = 0

# # section of song; 0-3
# section = 0

# active_template_fn = None

# # first_layer_ranges = {
# #   'light': range(1, 5)
# # }

# transitions = []

# def gradually_add_mask():
#   print("gradually_add_mask called")
#   if section == 0:
#     # update transition
#     resolume_commands.update_transition_time(LAYER_BG, 2.0)
#     resolume_commands.update_blend_mode(LAYER_BG, 10)

#     range = first_layer_ranges['light']
#     idx = random.choice(range)
#     resolume_commands.first_layer_only_instant_fadeout_others(idx)
#   return



# allowed_templates_by_intensity = [
#   [gradually_add_mask]
# ]

def set_intensity(num):
  print("intensity updated:", num)
  global intensity
  intensity = num
  return


# old
# def update_section(num):
#   global section
#   section = num
#   op('section').par.Value0 = section
#   return

# handler for the button to increment section
def increment_section():
  ast.increment_section()

  # old
  # update_section((section + 1) % NUM_SECTIONS)
  return




def choose_template():
  global active_template_fn
  choices = allowed_templates_by_intensity[intensity]
  next = random.choice(choices)
  active_template_fn = next
  op('active_template_display').par.Value0 = active_template_fn.__name__
  return

# TODO rethink what "next" does.
def next():
  print("not sure what NEXT does yet")
  # increment_section()
  # if section == 0:
  #   choose_template()
  # if active_template_fn:
  #   active_template_fn()
  return

def flush():
  print("flush called. not sure what flush does yet")
  # update_section(0)
  # if active_template_fn:
  #   active_template_fn()

  return













print("sld_resolume_controller.py loaded.")
