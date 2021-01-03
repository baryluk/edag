#!/usr/bin/env python3


# https://eesemi.com/ic-package-types.htm
# https://eesemi.com/d2pak.htm
#

SOIC8 = "SOIC-8"
UFQFPN32 = "UFQFPN32"  # 32-pin, 5x5 mm, 0.5mm pitch ultra thin fine pitch quad flat package outline
HSOP8 = "HSOP-8"  # SOIC-8 with thermal pad.

# Metric code, Imperial code
m_0201 = "SMD 0201 metric"
m_0402, i_01005 = "SMD 0402 metric", "SMD 01005 imperial"
m_0603, i_0201 = "SMD 0603 metric", "SMD 0201 imperial"
m_1005, i_0402 = "SMD 1005 metric", "SMD 0402 imperial"
m_2012, i_0805 = "SMD 2012 metric", "SMD 0805 imperial"
m_2520, i_1008 = "SMD 2520 metric", "SMD 1008 imperial"
m_3216, i_1206 = "SMD 3216 metric", "SMD 1206 imperial"
m_3225, i_1210 = "SMD 3225 metric", "SMD 1210 imperial"
m_4516, i_1806 = "SMD 4516 metric", "SMD 1806 imperial"
m_4532, i_1812 = "SMD 4532 metric", "SMD 1812 imperial"
m_5025, i_2010 = "SMD 5025 metric", "SMD 2010 imperial"
m_6332, i_2512 = "SMD 6332 metric", "SMD 2512 imperial"

SOT32_6 = "SOT32-6"
SOT_23 = "SOT-23"
SOT_89 = "SOT-89"
USP_6B = "USP-6B"  # TorexSemiconductor Ltd.
TO_220 = "TO-220"
TO_220_short_shoulder = "TO-220 (short shoulder)"

# TI package designators.

TI_KC = TO_220
TI_KCS = TO_220_short_shoulder
# TI_KCT = TO_220  # ??
TI_KTT = TO_263
TI_DCY = SOT_223

# Texas Instruments PowerFLEX from 1996.
# https://www.ti.com/lit/ml/slit115a/slit115a.pdf
# https://application-notes.digchip.com/001/1-1111.pdf

POWER_FLEX_2 = "PowerFLEX 2-Lead"  # Texas Instruments, R-PSFM-G2
TI_KTP = POWER_FLEX_2  # Some KTP might be 3 pin?
POWER_FLEX_3 = "PowerFLEX 3-Lead"  # Texas Instruments, R-PSFM-G3
TI_KTE = POWER_FLEX_3
POWER_FLEX_5 = "PowerFLEX 5-Lead"  # Texas Instruments, R-PSFM-G5
TI_KTG = POWER_FLEX_5
POWER_FLEX_7 = "PowerFLEX 7-Lead"  # Texas Instruments, R-PSFM-G7
TI_KTN = POWER_FLEX_7
POWER_FLEX_9 = "PowerFLEX 9-Lead"  # Texas Instruments, R-PSFM-G9
TI_KTA = POWER_FLEX_9
POWER_FLEX_14 = "PowerFLEX 14-Lead"  # Texas Instruments, dual sided, R-PDSO-G14
TI_DBX = POWER_FLEX_14
POWER_FLEX_15 = "PowerFLEX 15-Lead"  # Texas Instruments, staggered, R-PDSO-G14
# Texas Instruments, staggered, heat sink area segmented. R-PSFM-G10
POWER_FLEX_15_segmented = "PowerFLEX 15-Lead segmented"
TI_KTC = POWER_FLEX_15
TI_KTR = POWER_FLEX_15  # confirm if any of these use segmented heat sink area

TO_220FP = "TO-220FP"

# TO-252, a SMD variant of TO-251. Slightly smaller than TO-263 (DPAK).
DPAK_3 = "DPAK_3"  # aka TO-252. 3 pins with 90 mils (2.3mm) spacing.
# DPAK-3 used on Advanced Power Electronics AP9870GH, Power MOSFET.
DPAK_5 = "DPAK_5"  # aka TO-252. 5 pins with 45 mils (1.1mm) spacing.
# DPAK-5 used on Globaltech GS1581D, dual input LDO regulator.

TO_252_3 = DPAK_3
TO_252_5 = DPAK_5

# TO-263, very similar to TO-220,
# but intented for SMD, with shorter leads, and shorter metal tab (and no mounting hole).
# Sometimes called for this reason SMD-220.
# A bit bigger than TO-252 (DPAK).
D2PAK = "D2PAK"  # aka TO-263
DDPAK = D2PAK  # aka TO-263
TO_263AA = D2PAK

# D2PAKs can have 3 to 9 terminals, sometimes 2 terminals (central pin of 3 terminal one can be missing).
D2PAK_3 = "D2PAK-3"  # terminal pitch 100mils, central terminal missing.
D2PAK_4 = "D2PAK-4"  # terminal pitch 100mils
D2PAK_5 = "D2PAK-5"  # terminal pitch 67mils
D2PAK_6 = "D2PAK-6"
D2PAK_7 = "D2PAK-7"  # terminal pitch 50mils
D2PAK_9 = "D2PAK-9"


# DIP - 0.6" wide. Standard lead pitch of 0.1 inch.
DIP4 = "DIP-4"
DIP6 = "DIP-6"  # Not very common.
DIP8 = "DIP-8"
DIP14 = "DIP-14"
DIP16 = "DIP-16"
DIP18 = "DIP-18"
DIP20 = "DIP-20"  # Not very common.
DIP24 = "DIP-24"
DIP28 = "DIP-28"
DIP32 = "DIP-32"
DIP36 = "DIP-36"  # Uncommon.
DIP40 = "DIP-40"
DIP48 = "DIP-48"  # Uncommon.
DIP52 = "DIP-52"  # Uncommon.
DIP64 = "DIP-64"  # Uncommon, i.e. Motorola 68000 or Zilog Z180.

# The row spacing is usually 0.6 inch (15.24mm) - JEDEC MS-011, or 0.3 inch (7.62mm) - JEDEC MS-001.
# Less common row spacings, are: 0.4 inch (10.16mm) - JEDEC MS-010, 0.9 inch (22.86mm),
# as well 0.75 inch with 0.07 lead pitch.
# Some old Sovet Union / Eastern block countries used pitch of 2.5mm (instead of 2.54mm).

# SDIP - Narrow, 0.3" wide
DIP4N = "DIP-4N"
DIP6N = "DIP-6N"
DIP8N = "DIP-8N"
DIP14N = "DIP-14N"
DIP16N = "DIP-16N"
DIP18N = "DIP-18N"
DIP20N = "DIP-20N"
DIP24N = "DIP-24N"  # Not very common as 0.3".
DIP28N = "DIP-28N"

# NORBIT_2 = "NORBIT 2" # Philips/Mullard NORBIT 2, aka Valvo NORBIT-S, et all.
# Usually a 17 pin DIP-style, with 5.08mm (0.2inch) spacing, 9 pins on one side, 8 pins staggered on the other side.

# Skinny Dual In-line package (SDIP or SPDIP).
SDIP4 = DIP4N

# Variants of packages: CERDIP / CDIP (cermic), PDIP (plastic)

# SPDIP - Denser version of PDIP, with 0.07" (1.778 mm) lead pitch.
SPDIP8 = "SPDIP-8"

# SIP - Single in-line (pin) package. Aka SIPP.
SIP7 = "SIP-7"
SIP9 = "SIP-9"
SIP24 = "SIP-24"

# QIP - Quad in-line package.
QIP_42 = "QIP-42"

QIP_with_tabs = "QIP-.. with tabs"  # HA1306  # TODO(baryluk): Find stuff.

# SOIC - Small Outline IC. aka SO.  1.27mm pitch.
# JEDAC MS-012 (3.9mm body width)
# JEDAC MS-013 (7.50mm body width)
# JEITA (previously EIAJ) SDP. EIAJ Type II is 5.3mm body width.
SOIC8N = "SOIC-8-N"
SOIC16N
SOIC14N

# Most manufacturers will usually use high pin ones using JEITA/EIAJ, and JEDEC for small pin count ones.
# Often the 5.3mm wide ones will be refered as SOP, and the 3.9mm and 7.5mm ones as SOIC.

SOIC8W = "SOIC-8"

SOP8 = "SOP-8"

# mini-SOIC, aka micro-SOIC. 0.5mm pitch, 3.0mm body width.
miniSOIC_8 = "miniSOIC-8"
miniSOIC_10 = "miniSOIC-10"

# SOJ - Small-outline J-leaded package. A version of SOIC with J-type leads instead of gull-wing leads.
SOJ12 = "SOJ-12"

# SSOP - Shrink small-outline package
# Lead spacing of 0.0256in (0.65mm) or 0.025in (0.635mm), or rearly 0.5mm.

# TSOP - Thin small outline package
# Sometimes used by flash memories, etc.
TSOP48 = "TSOP-48"   # i.e. Hynix HY29LV800

# TSSOP - Thin-shrink small outline package
TSSOP16 = "TSSOP-16"

# TSSOP with exposed pad.
TSSOP16_EP = "TSSOP-16 ExposedPAD"

# PSOP - Plastic Small Outline Package
PSOP44 = "PSOP-44"  # i.e. Hynix HY29LV800

# FBGA - Fine-Pitch Ball Grid Array
FBGA48 = "FBGA-48"  # i.e. Hynix HY29LV800, 8mm x 9mm

SQP
SW
QFN  # Quad Flat No-Lead ?
QFP  # quad flat-pack?
SOP
SOT23
SOT223
SOT89
SO
VSO
SSOP
HTSSOP
TSSOP
HSOP
PMFP
SQFP
LQFP
HLQFP
HTQFP
TQFP
PGA
PLCC
PQFP
SOP
PQFP100L
SOT26
SOT363
SSOP_16L
SOT89
TO_252
SOT223
SOT523
SSOP
T7_TO220
FDIP
PDIP
PENTAWATT
TO2205
TO220ISO
QDIP
TO232
TO263
TO268
SIP
SO
TO3
TO52
TO99
SOT223
SOT23
SQL
TSOP
ZIP
FlatPack
FTO220
GSOP28
ITO3p
ITO220
JLCC
LBGA_180L
LCC
BQFP132
CERQUAD
CLCC
CPGA
DIP_tab
EBGA_680L
PSDIP
QFP
SBGA_192L
SC_70_5L  # SC-70 5L
SOJ_32L
SOJ
SOP_EIAJ_Type_II_14L
SO_8
SO_14
TO_220AB
LL_34  # melf diode
LL_41  # melf diode
SOT_89
SOD_123  # usually diodes
SOD_123FL  # usually diodes
SMAF
SMBF
SMA
SMB
SMC
TO_277
TO_252
TO_263
DO_214AC
DO_214AB
DO_214AA
SOD_323
SOD_523
SOD_723
SOT_223
SOT_363
SOT_23_6
SOP4

# TH parts, for diodes
R_1
DO_41
DO_15
DO_27
R_6
DO_35
DO_41
TO_220AB
TO_220AC
ITO_220AB
ITO_220AC
TO_247
TO_126
TO_92
TO_251
DIP_4  # 4 lead, usually for bridge rectifiers
SEP  # 4 lead, usually for bridge rectifiers

# Diode outlines.

DO_204_AA = DO_7 = "DO-7"  # common for 1N34A germanium diodes.
DO_204_AB = DO_14 = "DO-14"
DO_204_AC = DO_15 = "DO-15"
DO_204_AD = DO_16 = "DO-16"
DO_204_AE = DO_26 = "DO-26"
DO_204_AF = DO_29 = "DO-29"
DO_204_AG = DO_34 = "DO-34"
DO_204_AH = DO_35 = "DO-35"  # common for small signal, low power diodes, such as 1N4148
SOD27 = DO_35
DO_204_AJ = "DO-204-AJ"
DO_204_AK = "DO-204-AK"
DO_204_AL = DO_41 = "DO-41"  # Common for rectification diodes, for larger currents, like 1N4001 - 1N4007 series.
SOD66 = DO_41
DO_204_AM = "DO-204-AM"
DO_204_AN = "DO-204-AN"
DO_204_AP = "DO-204-AP"
DO_204_AR = "DO-204-AR"

# MELF - Metal electrode leadless face
# DO-213 , and EN 140401-803 standards.
# Used for diodes, zeners and precision resistors.
# https://www.vishay.com/docs/28714/melfpre.pdf

# L: 5.8 mm, Ø: 2.2 mm, 1.0 W, 500 V.
# Basically EIA / DIN 0207 (mils).
# Metric size code: RC6123M. Often rated for only 0.4W and 350V.
DO_213AB = SOD_106 = MELF = MMB = "MELF"

# L: 3.6 mm, Ø: 1.4 mm, 0.25 W, 200 V
# Basically EIA / DIN 0204 (mils).
# Metric size code: RC3715M
DO_213AA = SOD_80 = MiniMELF = MMA = "MiniMELF"

# L: 2.2 mm, Ø: 1.1 mm, 0.2 W, 100 V
# Basically EIA / DIN 0102
# Metric size code: RC2211M
MicroMELF = MMU = "MicroMELF"

# Often MELF, do have color code markings according to IEC 60062 with 5 bands,
# and possibly a 6th interrupted band between 4th and 5th full bands to
# indicate temp coef.

# The recommended solder pads do differ between wave soldering and reflow soldering.

# Similar to MELF but with squared electroes for easier handling.
QuadroMELF = "QuadroMELF"
"SQ_MELF"
"B_BELF"
