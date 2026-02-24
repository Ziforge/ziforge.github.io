#!/usr/bin/env python3
"""Generate architecture diagrams for ziforge.github.io portfolio."""

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch
import numpy as np
import os

# -- Theme --
BG = '#111111'
AMBER = '#e8a835'
AMBER_DIM = '#e8a83540'
AMBER_BORDER = '#e8a83580'
CYAN = '#5bc0be'
CYAN_DIM = '#5bc0be40'
CYAN_BORDER = '#5bc0be80'
TEXT = '#cccccc'
TEXT_DIM = '#999999'
TEXT_DARK = '#666666'
GREY = '#555555'
BORDER = '#333333'

OUT_DIR = 'diagrams'
os.makedirs(OUT_DIR, exist_ok=True)

plt.rcParams.update({
    'figure.facecolor': BG,
    'axes.facecolor': BG,
    'text.color': TEXT,
    'font.family': 'monospace',
    'font.size': 9,
})


def new_fig(w=10, h=2.2):
    fig, ax = plt.subplots(figsize=(w, h))
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 2.2)
    ax.set_aspect('equal')
    ax.axis('off')
    return fig, ax


def box(ax, x, y, w, h, label, sublabels=None, color=AMBER, lw=1.5, style='round,pad=0.1'):
    rect = FancyBboxPatch((x, y), w, h, boxstyle=style,
                          facecolor=color.replace('#', '#') + '12',
                          edgecolor=color, linewidth=lw)
    ax.add_patch(rect)
    cy = y + h
    ax.text(x + w/2, cy - 0.22, label, ha='center', va='center',
            fontsize=9, fontweight='bold', color=color)
    if sublabels:
        for i, sl in enumerate(sublabels):
            ax.text(x + w/2, cy - 0.48 - i*0.2, sl, ha='center', va='center',
                    fontsize=7, color=TEXT_DIM)


def arrow(ax, x1, y1, x2, y2, color=GREY, style='->', lw=1.5, dashed=False):
    ls = '--' if dashed else '-'
    ax.annotate('', xy=(x2, y2), xytext=(x1, y1),
                arrowprops=dict(arrowstyle=style, color=color, lw=lw, ls=ls))


def label_bottom(ax, text, y=0.08):
    ax.text(5, y, text, ha='center', va='center', fontsize=7,
            color='#444444', style='normal', fontweight='normal')


def save(fig, name):
    fig.savefig(os.path.join(OUT_DIR, f'{name}.png'), dpi=200,
                bbox_inches='tight', pad_inches=0.15, facecolor=BG)
    plt.close(fig)
    print(f'  saved {name}.png')


# ============================================================
# 1. Gateless Gate
# ============================================================
def diagram_gateless_gate():
    fig, ax = new_fig(10, 2.8)
    ax.set_ylim(0, 2.8)
    # Analog front end
    box(ax, 0.2, 1.3, 1.6, 1.0, 'ANALOG FRONT END',
        ['Precision Op-Amps', 'DC-Coupled I/O', '±12V / ±5V'], color=CYAN)
    # FPGA Core
    box(ax, 2.6, 0.8, 2.2, 1.6, 'FPGA CORE',
        ['DSP Engine', 'Routing Matrix', 'Novel Architecture', '', 'PATENT PENDING'], color=AMBER, lw=2)
    # DAC / Codec
    box(ax, 5.6, 1.3, 1.6, 1.0, 'DAC / CODEC',
        ['Audio Conversion', 'Output Stage'], color=CYAN)
    # Total Recall
    box(ax, 5.6, 0.1, 1.6, 0.85, 'TOTAL RECALL',
        ['Novel Approach'], color=AMBER, lw=1)
    # Case / Physical
    box(ax, 7.8, 0.8, 1.9, 1.6, 'PHYSICAL',
        ['3D Print (OpenSCAD)', 'Custom PSU', 'Panel + Knobs', 'LEDs'], color=CYAN)
    # Arrows
    arrow(ax, 1.85, 1.8, 2.55, 1.8)
    arrow(ax, 4.85, 1.8, 5.55, 1.8)
    arrow(ax, 4.85, 1.2, 5.55, 0.55, dashed=True, color=AMBER)
    arrow(ax, 7.25, 1.6, 7.75, 1.6)
    label_bottom(ax, 'FPGA MODULAR SYNTH · SYSTEMVERILOG · 3U 104HP EURORACK · CUSTOM PCB · OPENSCAD · 3D PRINT')
    save(fig, 'gateless-gate')

# ============================================================
# 2. Physical Tape
# ============================================================
def diagram_physical_tape():
    fig, ax = new_fig()
    box(ax, 0.1, 0.5, 1.2, 1.2, 'AUDIO IN', color=CYAN)
    box(ax, 1.8, 0.3, 2.2, 1.5, '3D TAPE GRID',
        ['64×256×4', '65,536 points', 'Jiles-Atherton', '7-pt Stencil'], color=AMBER, lw=2)
    box(ax, 4.5, 0.3, 2.0, 1.5, 'METAL GPU',
        ['65,536 Threads', 'Compute Shaders', 'Real-time 48kHz'], color=AMBER, lw=2)
    box(ax, 7.0, 0.5, 1.4, 1.2, 'SATURATED OUT',
        ['Tape FX'], color=CYAN)
    box(ax, 8.7, 0.6, 1.1, 1.0, 'OUT', color=CYAN)
    arrow(ax, 1.35, 1.1, 1.75, 1.1)
    arrow(ax, 4.05, 1.1, 4.45, 1.1, color=AMBER, dashed=True)
    arrow(ax, 6.55, 1.1, 6.95, 1.1)
    arrow(ax, 8.45, 1.1, 8.65, 1.1)
    label_bottom(ax, 'TAPE WIDTH 6mm · BUFFER 5cm · OXIDE 10μm · JILES-ATHERTON · METAL GPU · C++/JUCE')
    save(fig, 'physical-tape')

# ============================================================
# 3. Piobaire
# ============================================================
def diagram_piobaire():
    fig, ax = new_fig(10, 2.6)
    ax.set_ylim(0, 2.6)
    box(ax, 0.1, 0.8, 1.2, 1.2, 'REED',
        ['Bernoulli', 'Nonlinear'], color=AMBER)
    box(ax, 1.8, 0.6, 1.8, 1.5, 'WAVEGUIDE',
        ['Bidirectional', '5 Bore Profiles', 'Material Damping'], color=AMBER, lw=2)
    box(ax, 4.1, 0.6, 1.8, 1.5, 'TONE HOLES',
        ['9 Chanter', '13 Regulator Keys', 'Kelly-Lochbaum'], color=CYAN)
    box(ax, 6.4, 0.8, 1.2, 1.2, 'BELL',
        ['Radiation', 'Flared Horn'], color=CYAN)
    box(ax, 8.1, 0.7, 1.4, 1.3, 'METAL GPU',
        ['7 Pipes', '96kHz'], color=AMBER, lw=2)
    arrow(ax, 1.35, 1.4, 1.75, 1.4)
    arrow(ax, 3.65, 1.4, 4.05, 1.4)
    arrow(ax, 5.95, 1.4, 6.35, 1.4)
    arrow(ax, 7.65, 1.4, 8.05, 1.4, color=AMBER, dashed=True)
    label_bottom(ax, 'CHANTER · 3 DRONES · 3 REGULATORS · PARAPHONIC · 7 WAVEGUIDE PAIRS · METAL GPU', y=0.35)
    save(fig, 'piobaire')

# ============================================================
# 4. MLEMS Synthi
# ============================================================
def diagram_mlems_synthi():
    fig, ax = new_fig(10, 2.6)
    ax.set_ylim(0, 2.6)
    box(ax, 0.1, 0.8, 1.2, 1.2, 'INPUT', color=CYAN)
    box(ax, 1.8, 0.6, 2.0, 1.5, 'VA FILTER',
        ['4-Pole Diode Ladder', 'Bilinear Transform', 'tanh Saturation'], color=AMBER, lw=2)
    box(ax, 4.5, 0.6, 2.0, 1.5, 'WAVENET',
        ['Residual Learning', 'ONNX Runtime', '~700KB Model'], color=AMBER, lw=2)
    # Sum node
    circle = plt.Circle((7.2, 1.35), 0.2, fill=False, edgecolor=AMBER, lw=1.5)
    ax.add_patch(circle)
    ax.text(7.2, 1.35, '+', ha='center', va='center', fontsize=12, color=AMBER)
    box(ax, 7.8, 0.8, 1.2, 1.2, 'OUTPUT',
        ['VST3/AU'], color=CYAN)
    arrow(ax, 1.35, 1.4, 1.75, 1.4)
    arrow(ax, 3.85, 1.35, 4.45, 1.35, color=AMBER, dashed=True)
    arrow(ax, 6.55, 1.35, 6.98, 1.35)
    arrow(ax, 7.42, 1.35, 7.75, 1.35)
    # VA direct path
    arrow(ax, 3.85, 0.9, 7.0, 0.9, color=GREY, dashed=True)
    arrow(ax, 7.0, 0.9, 7.15, 1.13, color=GREY, dashed=True)
    label_bottom(ax, 'HYBRID VA + NEURAL · RESIDUAL LEARNING · ONNX RUNTIME · C++/JUCE · PYTORCH', y=0.35)
    save(fig, 'mlems-synthi')

# ============================================================
# 5. teorainn
# ============================================================
def diagram_teorainn():
    fig, ax = new_fig(10, 2.6)
    ax.set_ylim(0, 2.6)
    box(ax, 0.1, 0.8, 1.2, 1.2, 'INPUT', color=CYAN)
    box(ax, 1.7, 0.8, 1.4, 1.2, 'PRE-DIFF',
        ['4× Allpass', 'Modulated'], color=AMBER)
    box(ax, 3.5, 1.2, 1.6, 0.9, 'FDN TANK A',
        ['8 Delays', 'Hadamard'], color=AMBER, lw=2)
    box(ax, 3.5, 0.15, 1.6, 0.9, 'FDN TANK B',
        ['8 Delays', 'Hadamard'], color=AMBER, lw=2)
    box(ax, 5.6, 0.6, 1.4, 1.4, 'TIME FX',
        ['Shimmer', 'Chorus', 'Delay'], color=CYAN)
    box(ax, 7.5, 0.8, 1.2, 1.2, 'OUTPUT',
        ['Stereo'], color=CYAN)
    arrow(ax, 1.35, 1.4, 1.65, 1.4)
    arrow(ax, 3.15, 1.6, 3.45, 1.6)
    arrow(ax, 3.15, 1.0, 3.45, 0.65, color=GREY)
    arrow(ax, 5.15, 1.6, 5.55, 1.4)
    arrow(ax, 5.15, 0.65, 5.55, 1.0)
    arrow(ax, 7.05, 1.3, 7.45, 1.4)
    # Feedback loops
    ax.annotate('', xy=(3.5, 1.95), xytext=(5.1, 1.95),
                arrowprops=dict(arrowstyle='->', color=AMBER_BORDER, lw=1, ls='--',
                                connectionstyle='arc3,rad=0.3'))
    ax.annotate('', xy=(3.5, 0.0), xytext=(5.1, 0.0),
                arrowprops=dict(arrowstyle='->', color=AMBER_BORDER, lw=1, ls='--',
                                connectionstyle='arc3,rad=-0.3'))
    label_bottom(ax, 'LEXICON-INSPIRED · DUAL 8-DELAY FDN · HADAMARD MIXING · RT60 SABINE · C++/JUCE', y=0.35)
    save(fig, 'teorainn')

# ============================================================
# 6. EKS Extended
# ============================================================
def diagram_eks():
    fig, ax = new_fig()
    box(ax, 0.1, 0.5, 1.4, 1.2, 'EXCITATION',
        ['Burst Noise', 'Pick Position'], color=AMBER)
    box(ax, 2.0, 0.4, 1.6, 1.3, 'DELAY LINE',
        ['Fractional Interp', 'P = SR/freq'], color=AMBER, lw=2)
    box(ax, 4.1, 0.4, 1.6, 1.3, 'FIR3 DAMP',
        ['Brightness S', 'T60 Decay'], color=AMBER, lw=2)
    box(ax, 6.2, 0.5, 1.3, 1.2, 'DYN LP',
        ['Level Comp'], color=CYAN)
    box(ax, 8.0, 0.5, 1.2, 1.2, 'OUT',
        ['Stereo'], color=CYAN)
    arrow(ax, 1.55, 1.1, 1.95, 1.1)
    arrow(ax, 3.65, 1.1, 4.05, 1.1, color=AMBER, dashed=True)
    arrow(ax, 5.75, 1.1, 6.15, 1.1)
    arrow(ax, 7.55, 1.1, 7.95, 1.1)
    # Feedback loop
    ax.annotate('', xy=(2.0, 1.85), xytext=(5.7, 1.85),
                arrowprops=dict(arrowstyle='->', color=AMBER_BORDER, lw=1.5, ls='--',
                                connectionstyle='arc3,rad=0.25'))
    ax.text(3.85, 2.0, 'loop gain ρ', ha='center', fontsize=7, color=AMBER)
    label_bottom(ax, 'EXTENDED KARPLUS-STRONG · FAUST DSP · WEB / JACK / VST / BELA / DAISY')
    save(fig, 'eks')

# ============================================================
# 7. EmotionToCV
# ============================================================
def diagram_emotion_to_cv():
    fig, ax = new_fig(10, 2.8)
    ax.set_ylim(0, 2.8)
    box(ax, 0.1, 1.0, 1.0, 1.0, 'CAMERA',
        ['Webcam'], color=CYAN)
    box(ax, 1.5, 0.8, 1.4, 1.3, 'FACE DETECT',
        ['68 Landmarks', 'Haar / dlib'], color=CYAN)
    box(ax, 3.3, 0.6, 1.6, 1.6, 'EMOTION CNN',
        ['Mini-Xception', 'ONNX Runtime', 'Kalman Filter'], color=AMBER, lw=2)
    # Physics models
    models = ['Lorenz → angry', 'Duffing → disgust', 'Mass-Spr → fear',
              'Modal → happy', 'Breath → sad', 'Membrane → surprise']
    box(ax, 5.4, 0.3, 2.2, 2.2, '7 PHYSICS MODELS', color=AMBER, lw=2)
    for i, m in enumerate(models):
        ax.text(6.5, 2.15 - i*0.28, m, ha='center', fontsize=6.5, color=TEXT_DIM)
    box(ax, 8.1, 0.6, 1.5, 1.6, '7× CV',
        ['Expert Sleepers', 'ES-9', 'DC ±5V'], color=CYAN)
    arrow(ax, 1.15, 1.5, 1.45, 1.5)
    arrow(ax, 2.95, 1.4, 3.25, 1.4)
    arrow(ax, 4.95, 1.4, 5.35, 1.4, color=AMBER, dashed=True)
    arrow(ax, 7.65, 1.4, 8.05, 1.4)
    label_bottom(ax, 'FACE → EMOTION → PHYSICS → CV · C++/PYTHON · OPENCV · ONNX · EURORACK')
    save(fig, 'emotion-to-cv')

# ============================================================
# 8. Neuroverse
# ============================================================
def diagram_neuroverse():
    fig, ax = new_fig(10, 2.8)
    ax.set_ylim(0, 2.8)
    # Phenotypes
    box(ax, 0.2, 1.0, 1.6, 1.2, 'PHENOTYPES',
        ['Avoider', 'Low Reg', 'Seeker / Max'], color=CYAN)
    # Core
    box(ax, 2.5, 0.9, 3.2, 1.4, 'NEUROVERSE CORE',
        ['Sensory Phenotype Adaptation', "Dunn's Framework", 'Markov + Coprime Loops'], color=AMBER, lw=2)
    # Modes
    box(ax, 6.4, 1.0, 1.6, 1.2, 'MODES',
        ['Sanctuary', 'Explorer', 'Assessment'], color=CYAN)
    # DSP strip
    modules = ['Bioacoustic', 'Guitar KS', 'teorainn', 'Phys.Tape', 'Neural', 'Binaural', 'Mixer']
    box(ax, 0.2, 0.05, 9.4, 0.65, 'INTEGRATED DSP MODULES (C++ Audio Engine)', color=CYAN, lw=1)
    for i, m in enumerate(modules):
        mx = 0.5 + i * 1.32
        rect = FancyBboxPatch((mx, 0.12), 1.1, 0.35, boxstyle='round,pad=0.05',
                              facecolor=AMBER_DIM, edgecolor=AMBER_BORDER, lw=0.5)
        ax.add_patch(rect)
        ax.text(mx + 0.55, 0.3, m, ha='center', va='center', fontsize=6.5, color=TEXT)
    arrow(ax, 1.85, 1.6, 2.45, 1.6, color=CYAN_BORDER)
    arrow(ax, 5.75, 1.6, 6.35, 1.6, color=CYAN_BORDER)
    arrow(ax, 4.1, 0.85, 4.1, 0.72, color=AMBER_BORDER, dashed=True)
    label_bottom(ax, 'ADAPTIVE SENSORY PLATFORM · UNITY / GODOT · C++ GDEXTENSION · RTNEURAL · META QUEST 3', y=0.55)
    ax.text(5, 2.55, '', ha='center')
    save(fig, 'neuroverse')

# ============================================================
# 9. Binaural HRTF
# ============================================================
def diagram_binaural_hrtf():
    fig, ax = new_fig(10, 2.6)
    ax.set_ylim(0, 2.6)
    box(ax, 0.1, 0.8, 1.2, 1.2, 'SOURCE', color=CYAN)
    # HRTF Processing
    box(ax, 1.8, 0.4, 3.0, 1.8, 'HRTF PROCESSING', color=AMBER, lw=2)
    box(ax, 1.95, 0.95, 1.2, 0.5, 'Left HRIR',
        ['ITD + ILD'], color=AMBER, lw=0.5)
    box(ax, 1.95, 0.45, 1.2, 0.45, 'Right HRIR',
        ['ITD + ILD'], color=AMBER, lw=0.5)
    box(ax, 3.3, 0.55, 1.3, 1.0, 'Woodworth',
        ['Spherical Head', 'Brown-Duda', 'Frac. Delay'], color=AMBER, lw=0.5)
    # Head Tracker
    box(ax, 5.3, 0.6, 1.6, 1.4, 'HEAD TRACKER',
        ['MediaPipe', 'Real-time', 'Orientation'], color=CYAN, lw=1.5)
    # Output
    box(ax, 7.5, 0.6, 2.2, 1.4, 'BINAURAL OUT',
        ['Left    Right', 'Immersive 3D Audio'], color=CYAN)
    arrow(ax, 1.35, 1.4, 1.75, 1.4)
    arrow(ax, 4.85, 1.4, 5.25, 1.4)
    arrow(ax, 6.95, 1.3, 7.45, 1.3)
    # Feedback
    ax.annotate('', xy=(3.3, 0.3), xytext=(6.1, 0.3),
                arrowprops=dict(arrowstyle='->', color=CYAN_BORDER, lw=1, ls='--',
                                connectionstyle='arc3,rad=-0.3'))
    ax.text(4.7, 0.05, 'updates azimuth / elevation', ha='center', fontsize=6, color=CYAN_BORDER)
    label_bottom(ax, 'HEAD-TRACKABLE HRTF · WOODWORTH ITD · BROWN-DUDA ILD · MEDIAPIPE · PYTHON', y=0.35)
    save(fig, 'binaural-hrtf')

# ============================================================
# 10. USB Audio STM32
# ============================================================
def diagram_usb_audio_stm32():
    fig, ax = new_fig()
    box(ax, 0.1, 0.5, 1.2, 1.2, 'USB HOST',
        ['Full Speed', '12 Mbps'], color=CYAN)
    box(ax, 1.7, 0.4, 1.5, 1.3, 'TinyUSB',
        ['UAC 2.0', 'Adaptive', '48kHz/16-bit'], color=AMBER, lw=1.5)
    box(ax, 3.6, 0.4, 1.6, 1.3, 'RING BUFFER',
        ['SRAM2 Bank', 'Dedicated 32KB'], color=AMBER, lw=1.5)
    box(ax, 5.6, 0.5, 1.1, 1.1, 'DMA',
        ['Callbacks'], color=CYAN)
    box(ax, 7.1, 0.4, 1.5, 1.3, 'SAI / CODEC',
        ['PLLSAI2 Clock', 'Audio I/O', 'Stereo PCM'], color=CYAN)
    box(ax, 8.9, 0.6, 0.8, 0.9, 'OUT', color=CYAN)
    arrow(ax, 1.35, 1.1, 1.65, 1.1)
    arrow(ax, 3.25, 1.1, 3.55, 1.1, color=AMBER, dashed=True)
    arrow(ax, 5.25, 1.1, 5.55, 1.1)
    arrow(ax, 6.75, 1.1, 7.05, 1.1)
    arrow(ax, 8.65, 1.1, 8.85, 1.1)
    label_bottom(ax, 'STM32L476 · USB AUDIO CLASS 2.0 · TINYUSB · DUAL PLL CLOCKING · DMA')
    save(fig, 'usb-audio-stm32')

# ============================================================
# 11. windgrain
# ============================================================
def diagram_windgrain():
    fig, ax = new_fig()
    box(ax, 0.1, 0.4, 1.6, 1.3, 'PARTICLE SYS',
        ['N Grains', 'Position (x,y,z)', 'Velocity'], color=AMBER)
    box(ax, 2.2, 0.4, 1.8, 1.3, 'COLLISION',
        ['Hertzian Contact', 'Impact Force', 'Restitution'], color=AMBER, lw=2)
    box(ax, 4.5, 0.4, 1.8, 1.3, 'MODAL SYNTH',
        ['Resonant Modes', 'Grain Material', 'Size-Dep F0'], color=AMBER)
    box(ax, 6.8, 0.5, 1.3, 1.1, 'SPATIAL MIX',
        ['3D Position', 'Attenuation'], color=CYAN)
    box(ax, 8.6, 0.6, 1.0, 0.9, 'OUT', color=CYAN)
    arrow(ax, 1.75, 1.05, 2.15, 1.05)
    arrow(ax, 4.05, 1.05, 4.45, 1.05, color=AMBER, dashed=True)
    arrow(ax, 6.35, 1.05, 6.75, 1.05)
    arrow(ax, 8.15, 1.05, 8.55, 1.05)
    label_bottom(ax, 'GRANULAR COLLISION PHYSICS · HERTZIAN CONTACT · MODAL SYNTHESIS · MATLAB')
    save(fig, 'windgrain')

# ============================================================
# 12. Bela Serge ResEQ
# ============================================================
def diagram_bela_serge():
    fig, ax = new_fig()
    box(ax, 0.1, 0.6, 1.0, 0.9, 'AUDIO IN', color=CYAN)
    # Filter bank
    box(ax, 1.5, 0.3, 5.0, 1.5, 'RESONANT FILTER BANK', color=AMBER, lw=2)
    bands = ['Band 1', 'Band 2', 'Band 3', '...', 'Band N']
    for i, b in enumerate(bands):
        bx = 1.7 + i * 0.95
        rect = FancyBboxPatch((bx, 0.6), 0.8, 0.5, boxstyle='round,pad=0.05',
                              facecolor=AMBER_DIM, edgecolor=AMBER_BORDER, lw=0.5)
        ax.add_patch(rect)
        ax.text(bx + 0.4, 0.85, b, ha='center', va='center', fontsize=6.5, color=TEXT)
    ax.text(4.0, 1.4, 'Variable Q · Per-Band Gain · Self-Oscillation',
            ha='center', fontsize=7, color=TEXT_DIM)
    box(ax, 7.0, 0.4, 2.6, 1.3, 'BELA',
        ['Embedded Linux', 'Ultra-Low Latency', 'Analog I/O'], color=CYAN, lw=1.5)
    arrow(ax, 1.15, 1.05, 1.45, 1.05)
    arrow(ax, 6.55, 1.05, 6.95, 1.05)
    label_bottom(ax, 'SERGE RESONANT EQUALISER · BELA EMBEDDED AUDIO · VARIABLE-Q BANDPASS · C++')
    save(fig, 'bela-serge-reseq')

# ============================================================
# 13. OTO Biscuit
# ============================================================
def diagram_oto_biscuit():
    fig, ax = new_fig()
    box(ax, 0.1, 0.5, 1.0, 1.1, 'AUDIO IN', color=CYAN)
    box(ax, 1.5, 0.4, 1.6, 1.3, 'OTA VCA',
        ['LM13700', 'Linearization', 'Darlington'], color=AMBER)
    box(ax, 3.5, 0.4, 1.6, 1.3, 'OTA FILTER',
        ['LM13700', 'State Variable', 'Nonlinear Gm'], color=AMBER, lw=2)
    box(ax, 5.5, 0.4, 1.6, 1.3, 'WAVESHAPER',
        ['Diode Clip', 'Bit Reduction', 'Sample Rate ↓'], color=AMBER)
    box(ax, 7.6, 0.4, 2.0, 1.3, 'OUTPUT',
        ['SPICE Verified', 'PCB Layout'], color=CYAN)
    arrow(ax, 1.15, 1.05, 1.45, 1.05)
    arrow(ax, 3.15, 1.05, 3.45, 1.05, color=AMBER)
    arrow(ax, 5.15, 1.05, 5.45, 1.05, color=AMBER)
    arrow(ax, 7.15, 1.05, 7.55, 1.05)
    label_bottom(ax, 'OTO BISCUIT RECREATION · LM13700 OTA · ANALOG CIRCUIT DESIGN · SPICE · PCB')
    save(fig, 'oto-biscuit')

# ============================================================
# 14. Harman Spatial
# ============================================================
def diagram_harman_spatial():
    fig, ax = new_fig()
    box(ax, 0.1, 0.5, 1.2, 1.1, 'SOURCE',
        ['Multichannel'], color=CYAN)
    box(ax, 1.7, 0.3, 4.0, 1.5, 'SPATIAL AUDIO PROCESSING', color=AMBER, lw=2)
    items = ['Binaural HRTF', 'Stereo Widening', 'Virtualisation']
    for i, item in enumerate(items):
        ix = 1.9 + i * 1.3
        rect = FancyBboxPatch((ix, 0.65), 1.1, 0.5, boxstyle='round,pad=0.05',
                              facecolor=AMBER_DIM, edgecolor=AMBER_BORDER, lw=0.5)
        ax.add_patch(rect)
        ax.text(ix + 0.55, 0.9, item, ha='center', va='center', fontsize=6.5, color=TEXT)
    ax.text(3.7, 1.4, 'R&D for Consumer & Professional Audio', ha='center', fontsize=7, color=TEXT_DIM)
    box(ax, 6.2, 0.3, 3.4, 1.5, 'HARMAN CORPORATION',
        ['Industry Collaboration', 'Consumer Audio', 'Professional Systems'], color=CYAN, lw=1.5)
    arrow(ax, 1.35, 1.05, 1.65, 1.05)
    arrow(ax, 5.75, 1.05, 6.15, 1.05)
    label_bottom(ax, 'BINAURAL · STEREO PROCESSING · VIRTUALISATION · HARMAN CORPORATION')
    save(fig, 'harman-spatial')

# ============================================================
# 15. WaveNet Filter
# ============================================================
def diagram_wavenet_filter():
    fig, ax = new_fig(10, 2.6)
    ax.set_ylim(0, 2.6)
    box(ax, 0.1, 1.2, 1.6, 1.0, 'EMS HARDWARE',
        ['Buchla / Serge', 'Synthi VCS3'], color=CYAN)
    box(ax, 2.2, 1.2, 1.5, 1.0, 'TRAINING DATA',
        ['Sweep Captures', 'Param Space'], color=AMBER)
    box(ax, 4.2, 0.6, 3.0, 1.7, 'NEURAL ARCHITECTURE', color=AMBER, lw=2)
    items = ['WaveNet\nDilated Causal', 'CNN\nResidual Blocks']
    for i, item in enumerate(items):
        ix = 4.4 + i * 1.5
        rect = FancyBboxPatch((ix, 1.15), 1.2, 0.65, boxstyle='round,pad=0.05',
                              facecolor=AMBER_DIM, edgecolor=AMBER_BORDER, lw=0.5)
        ax.add_patch(rect)
        ax.text(ix + 0.6, 1.47, item, ha='center', va='center', fontsize=6.5, color=TEXT)
    ax.text(5.7, 0.85, 'PyTorch · Nonlinear Behaviour Capture', ha='center', fontsize=7, color=TEXT_DIM)
    box(ax, 7.7, 1.0, 1.8, 1.2, 'EMULATION',
        ['Digital Filter', 'Real-time'], color=CYAN)
    box(ax, 0.1, 0.3, 1.6, 0.65, 'EMS STOCKHOLM',
        ['Guest Composer'], color=CYAN, lw=1)
    arrow(ax, 1.75, 1.7, 2.15, 1.7)
    arrow(ax, 3.75, 1.7, 4.15, 1.7, color=AMBER, dashed=True)
    arrow(ax, 7.25, 1.4, 7.65, 1.4)
    label_bottom(ax, 'WAVENET / CNN · ANALOG FILTER EMULATION · PYTORCH · EMS STOCKHOLM RESIDENCY')
    save(fig, 'wavenet-filter')

# ============================================================
# 16. ERAE Polytone
# ============================================================
def diagram_erae_polytone():
    fig, ax = new_fig(10, 2.6)
    ax.set_ylim(0, 2.6)
    box(ax, 0.1, 0.7, 1.6, 1.5, 'ERAE II',
        ['Hex Touch', 'Surface', 'SysEx API', 'LED Feedback'], color=CYAN)
    box(ax, 2.3, 0.5, 3.0, 1.8, 'POLYTONE ENGINE', color=AMBER, lw=2)
    items = [('Tuning System', 'N-TET (12..106)'), ('Isomorphic', 'Wicki-Hayden'),
             ('Colour Scheme', 'Polychromatic'), ('Hex Grid', '42×24 px')]
    for i, (title, sub) in enumerate(items):
        row, col = divmod(i, 2)
        ix = 2.5 + col * 1.4
        iy = 1.55 - row * 0.7
        rect = FancyBboxPatch((ix, iy), 1.2, 0.5, boxstyle='round,pad=0.05',
                              facecolor=AMBER_DIM, edgecolor=AMBER_BORDER, lw=0.5)
        ax.add_patch(rect)
        ax.text(ix + 0.6, iy + 0.32, title, ha='center', fontsize=6.5, color=TEXT)
        ax.text(ix + 0.6, iy + 0.15, sub, ha='center', fontsize=5.5, color=TEXT_DIM)
    box(ax, 5.8, 1.2, 1.6, 1.0, 'MPE MIDI',
        ['Per-Note Pitch', 'Pressure · Slide'], color=CYAN)
    box(ax, 5.8, 0.3, 1.6, 0.65, 'OSC',
        ['UDP Broadcast'], color=CYAN, lw=1)
    box(ax, 8.0, 1.0, 1.6, 1.3, 'SYNTH',
        ['Any MPE', 'Instrument'], color=CYAN)
    # Bidirectional arrow to ERAE
    arrow(ax, 1.75, 1.45, 2.25, 1.45, color=AMBER)
    arrow(ax, 2.25, 1.25, 1.75, 1.25, color=AMBER)
    arrow(ax, 5.35, 1.7, 5.75, 1.7)
    arrow(ax, 5.35, 0.6, 5.75, 0.6)
    arrow(ax, 7.45, 1.7, 7.95, 1.65)
    label_bottom(ax, 'MICROTONAL ISOMORPHIC · N-TET · MPE MIDI · SYSEX LED · POLYCHROMATIC · PYTHON')
    save(fig, 'erae-polytone')

# ============================================================
# 17. Guitar Physical Model
# ============================================================
def diagram_guitar():
    fig, ax = new_fig(10, 2.4)
    ax.set_ylim(0, 2.4)
    box(ax, 0.1, 0.6, 1.3, 1.2, 'EXCITATION',
        ['Pluck Model', 'Pick Position', 'Velocity'], color=AMBER)
    box(ax, 1.9, 0.5, 2.0, 1.4, 'STRING MODEL',
        ['Waveguide Pair', 'Stiffness Allpass', 'Freq-Dep Damping'], color=AMBER, lw=2)
    box(ax, 4.4, 0.5, 2.0, 1.4, 'BODY RESONANCE',
        ['Modal Coupling', 'Top/Back Plate', 'Air Cavity'], color=AMBER, lw=2)
    box(ax, 6.9, 0.6, 1.3, 1.2, 'JUCE',
        ['Real-time C++', 'VST3 / AU'], color=CYAN)
    box(ax, 8.6, 0.7, 1.0, 1.0, 'OUT', color=CYAN)
    arrow(ax, 1.45, 1.2, 1.85, 1.2)
    arrow(ax, 3.95, 1.2, 4.35, 1.2, color=AMBER, dashed=True)
    arrow(ax, 6.45, 1.2, 6.85, 1.2)
    arrow(ax, 8.25, 1.2, 8.55, 1.2)
    # Python research strip
    rect = FancyBboxPatch((0.1, 0.15), 8.0, 0.3, boxstyle='round,pad=0.05',
                          facecolor='#5bc0be08', edgecolor=CYAN_BORDER, lw=0.5)
    ax.add_patch(rect)
    ax.text(4.1, 0.3, 'Python Research · Parameter Extraction · Prototyping → C++ Implementation',
            ha='center', fontsize=6, color=CYAN_BORDER)
    label_bottom(ax, 'GUITAR PHYSICAL MODEL · WAVEGUIDE STRING · MODAL BODY · PYTHON + C++ / JUCE', y=0.0)
    save(fig, 'guitar-physical-model')

# ============================================================
# 18. Bioacoustics
# ============================================================
def diagram_bioacoustics():
    fig, ax = new_fig()
    box(ax, 0.1, 0.4, 1.4, 1.3, 'FIELD',
        ['Gaulossen', 'Nature Reserve', 'Multi-Channel'], color=CYAN)
    box(ax, 1.9, 0.4, 1.7, 1.3, 'BirdNET',
        ['Species ID', 'CNN Classifier', 'Batch Process'], color=AMBER, lw=1.5)
    box(ax, 4.0, 0.4, 1.7, 1.3, 'ANALYSIS',
        ['F0 (YIN)', 'LPC Formants', 'Spectrogram'], color=AMBER, lw=2)
    box(ax, 6.1, 0.4, 2.5, 1.3, 'PRAVEN PRO',
        ['Raven Pro Integration', 'Selection Tables', 'Annotation Export'], color=CYAN)
    box(ax, 8.9, 0.5, 0.8, 1.0, 'WEB',
        color=CYAN)
    arrow(ax, 1.55, 1.05, 1.85, 1.05)
    arrow(ax, 3.65, 1.05, 3.95, 1.05, color=AMBER, dashed=True)
    arrow(ax, 5.75, 1.05, 6.05, 1.05)
    arrow(ax, 8.65, 1.05, 8.85, 1.05)
    label_bottom(ax, 'FIELD RECORDING · BIRDNET CNN · YIN F0 · LPC FORMANTS · RAVEN PRO · PYTHON')
    save(fig, 'bioacoustics')

# ============================================================
# 19. IR Capture
# ============================================================
def diagram_ir_capture():
    fig, ax = new_fig()
    box(ax, 0.1, 0.4, 1.4, 1.3, 'SWEEP GEN',
        ['Log Sine', 'Automated', 'Calibrated'], color=AMBER)
    box(ax, 1.9, 0.4, 1.6, 1.3, 'ANALOG FILTER',
        ['Device Under Test', 'EMS Synthi'], color=CYAN)
    box(ax, 3.9, 0.3, 1.8, 1.5, 'IR CAPTURE',
        ['JUCE Plugin', 'Deconvolution', 'Cataloguing', '750 IR Files'], color=AMBER, lw=2)
    box(ax, 6.1, 0.4, 1.6, 1.3, 'ML TRAINING',
        ['Training Dataset', 'WaveNet Input', '→ MLEMS Filter'], color=AMBER)
    box(ax, 8.1, 0.5, 1.4, 1.1, 'ONNX MODEL',
        color=CYAN)
    arrow(ax, 1.55, 1.05, 1.85, 1.05)
    arrow(ax, 3.55, 1.05, 3.85, 1.05)
    arrow(ax, 5.75, 1.05, 6.05, 1.05, color=AMBER, dashed=True)
    arrow(ax, 7.75, 1.05, 8.05, 1.05)
    label_bottom(ax, 'IR CAPTURE PIPELINE · SWEEP → ANALOG → DECONVOLUTION → ML TRAINING · C++/JUCE')
    save(fig, 'ir-capture')

# ============================================================
# 20. Verdant Drift
# ============================================================
def diagram_verdant_drift():
    fig, ax = new_fig()
    box(ax, 0.1, 0.4, 1.8, 1.3, 'PROC. WORLD',
        ['Terrain Gen', 'Flora Placement', 'Day/Night'], color=CYAN)
    box(ax, 2.4, 0.3, 2.2, 1.5, 'ECOSYSTEM SIM',
        ['Agent Behaviour', 'Species Populations', 'Activity Patterns'], color=AMBER, lw=2)
    box(ax, 5.1, 0.3, 2.2, 1.5, 'GENERATIVE MUSIC',
        ['Bioacoustic Synth', 'Cricket Stridulation', 'Avian Syrinx'], color=AMBER, lw=2)
    box(ax, 7.8, 0.5, 1.6, 1.1, '3D AUDIO',
        ['Spatial'], color=CYAN)
    arrow(ax, 1.95, 1.05, 2.35, 1.05)
    arrow(ax, 4.65, 1.05, 5.05, 1.05, color=AMBER, dashed=True)
    arrow(ax, 7.35, 1.05, 7.75, 1.05)
    label_bottom(ax, 'PROTEUS-STYLE EXPLORATION · PROCEDURAL WORLD · BIOACOUSTIC MUSIC · GODOT 4.5')
    save(fig, 'verdant-drift')

# ============================================================
# 21. HW Preset Managers
# ============================================================
def diagram_hw_presets():
    fig, ax = new_fig()
    box(ax, 0.1, 0.5, 1.3, 1.2, 'DAW',
        ['VST3/AU/AAX'], color=CYAN)
    box(ax, 1.8, 0.3, 2.6, 1.5, 'JUCE PLUGIN SUITE', color=AMBER, lw=2)
    items = ['OTOInterface', 'PlinkyInterface', 'PlinkyBridge', 'Plinky-VST']
    for i, item in enumerate(items):
        row, col = divmod(i, 2)
        ix = 2.0 + col * 1.2
        iy = 1.15 - row * 0.5
        rect = FancyBboxPatch((ix, iy), 1.0, 0.35, boxstyle='round,pad=0.05',
                              facecolor=AMBER_DIM, edgecolor=AMBER_BORDER, lw=0.5)
        ax.add_patch(rect)
        ax.text(ix + 0.5, iy + 0.18, item, ha='center', fontsize=6, color=TEXT)
    box(ax, 4.8, 0.4, 1.8, 1.3, 'MIDI SYSEX',
        ['Preset Transfer', 'Bank Mgmt', 'Param Sync'], color=AMBER)
    box(ax, 7.0, 0.4, 2.6, 1.3, 'HARDWARE',
        ['OTO Biscuit/BIM/BAM', 'Plinky Synth'], color=CYAN)
    arrow(ax, 1.45, 1.1, 1.75, 1.1)
    arrow(ax, 4.45, 1.1, 4.75, 1.1, color=AMBER, dashed=True)
    arrow(ax, 4.75, 0.9, 4.45, 0.9, color=AMBER, dashed=True)
    arrow(ax, 6.65, 1.1, 6.95, 1.1)
    label_bottom(ax, 'HARDWARE PRESET MANAGERS · MIDI SYSEX · JUCE · VST3/AU/AAX · CROSS-PLATFORM')
    save(fig, 'hw-preset-managers')

# ============================================================
# 22. Ableton LiveAPI
# ============================================================
def diagram_ableton():
    fig, ax = new_fig()
    box(ax, 0.1, 0.4, 1.5, 1.3, 'EXTERNAL',
        ['Control Surfaces', 'Automation', 'Scripts'], color=CYAN)
    box(ax, 2.1, 0.3, 2.8, 1.5, 'REMOTE SCRIPT',
        ['220+ LiveAPI Tools', 'Thread Safety Locks', 'Event Callbacks'], color=AMBER, lw=2)
    box(ax, 5.4, 0.3, 4.2, 1.5, 'ABLETON LIVE', color=CYAN, lw=1.5)
    items = ['Tracks', 'Clips', 'Devices', 'Mixer', 'Transport', 'Scenes']
    for i, item in enumerate(items):
        row, col = divmod(i, 3)
        ix = 5.6 + col * 1.3
        iy = 1.15 - row * 0.5
        rect = FancyBboxPatch((ix, iy), 1.1, 0.35, boxstyle='round,pad=0.05',
                              facecolor=CYAN_DIM, edgecolor=CYAN_BORDER, lw=0.5)
        ax.add_patch(rect)
        ax.text(ix + 0.55, iy + 0.18, item, ha='center', fontsize=6.5, color=TEXT)
    arrow(ax, 1.65, 1.1, 2.05, 1.1)
    arrow(ax, 4.95, 1.1, 5.35, 1.1, color=AMBER)
    arrow(ax, 5.35, 0.9, 4.95, 0.9, color=AMBER)
    label_bottom(ax, 'ABLETON LIVEAPI · 220+ TOOLS · THREAD-SAFE · REMOTE SCRIPT · PYTHON · OPEN SOURCE')
    save(fig, 'ableton-liveapi')

# ============================================================
# 23. Acoustics Research
# ============================================================
def diagram_acoustics():
    fig, ax = new_fig()
    topics = [
        ('TLM SIM', ['2D Pipe Model', 'Scattering', 'Boundaries'], AMBER),
        ('WAVEGUIDE', ['1D Instrument', 'Delay Lines', 'Reflection'], AMBER),
        ('F0 ANALYSIS', ['Multi-Method', 'SHS / YIN', 'MFCC'], AMBER),
        ('PSYCHOACOUSTICS', ['Perception', 'Room Acoustics', 'Denoising'], CYAN),
        ('NOTEBOOKS', ['Interactive', 'Calculators', 'Visualisation'], CYAN),
    ]
    for i, (title, subs, color) in enumerate(topics):
        x = 0.1 + i * 1.95
        box(ax, x, 0.4, 1.75, 1.4, title, subs, color=color, lw=1.5 if i == 2 else 1)
    label_bottom(ax, 'ACOUSTIC SIGNAL PROCESSING · TLM · WAVEGUIDE · F0 · MFCC · PYTHON / MATLAB')
    save(fig, 'acoustics-research')


# ============================================================
# RUN ALL
# ============================================================
if __name__ == '__main__':
    print('Generating diagrams...')
    diagram_gateless_gate()
    diagram_physical_tape()
    diagram_piobaire()
    diagram_mlems_synthi()
    diagram_teorainn()
    diagram_eks()
    diagram_emotion_to_cv()
    diagram_neuroverse()
    diagram_binaural_hrtf()
    diagram_usb_audio_stm32()
    diagram_windgrain()
    diagram_bela_serge()
    diagram_oto_biscuit()
    diagram_harman_spatial()
    diagram_wavenet_filter()
    diagram_erae_polytone()
    diagram_guitar()
    diagram_bioacoustics()
    diagram_ir_capture()
    diagram_verdant_drift()
    diagram_hw_presets()
    diagram_ableton()
    diagram_acoustics()
    print('Done! 23 diagrams generated.')
