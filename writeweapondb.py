import os
import struct
import sys

# These are all the weapon presets used in wabo.

class Weapon:
    def __init__(self, ammotype, barrel, weight, rateoffire=None, bullpup=None, onehanded=None,):

        self.ammotype = ammotype
        self.barrel = barrel
        self.weight = weight
        if bullpup is not None:
            self.bullpup = bullpup
        else:
            self.bullpup = False
        if onehanded is not None:
            self.onehanded = onehanded
        else:
            self.onehanded = False
        if rateoffire is not None:
            self.rateoffire = rateoffire
        else:
            self.rateoffire = None

HDG_USP_MATCH = HDG_USP = Weapon(
    ammotype=".45 ACP HDG",
    barrel="5",
    weight=0.9,
    onehanded=True,)

HDG_DEAGLE_SURVIVOR = Weapon(
    ammotype=".50 AE",
    barrel="6",
    weight=2,
    onehanded=True,)

HDG_DEAGLE = Weapon(
    ammotype=".50 AE",
    barrel="6",
    weight=2,
    onehanded=True,)

HDG_DEAGLE_Custom_Skin = Weapon(
    ammotype=".50 AE",
    barrel="6",
    weight=2,
    onehanded=True,)

SNR_SR1 = Weapon(
    ammotype=".338 Lupua",
    barrel="25",
    weight=5.9,
    bullpup=True,)

SNR_MSR = Weapon(
    ammotype=".338 Lupua",
    barrel="27",
    weight=5.9,)

ASR_Valmet82_CQC = Weapon(
    ammotype="7,62x51mm",
    barrel="10",
    weight=3,
    rateoffire=650,
    bullpup=True,)

ASR_VHSD2_SURVIVAL = Weapon(
    ammotype="5,56x45mm",
    barrel="20",
    weight=3.9,
    rateoffire=850,
    bullpup=True,)

ASR_VHSD2 = Weapon(
    ammotype="5,56x45mm",
    barrel="20",
    weight=3.9,
    rateoffire=850,
    bullpup=True,)

ASR_VHSD2_Sentinel_Skin = Weapon(
    ammotype="5,56x45mm",
    barrel="20",
    weight=3.9,
    rateoffire=850,
    bullpup=True,)

ASR_TAVOR_CUSTOM = Weapon(
    ammotype="5,56x45mm",
    barrel="18",
    weight=3.3,
    rateoffire=950,
    bullpup=True,)

ASR_TAVOR = Weapon(
    ammotype="5,56x45mm",
    barrel="18",
    weight=3.3,
    rateoffire=950,
    bullpup=True,)

ASR_TAVOR_ASU = Weapon(
    ammotype="5,56x45mm",
    barrel="18",
    weight=3.3,
    rateoffire=950,
    bullpup=True,)

ASR_TAR21_NPC = Weapon(
    ammotype="5,56x45mm",
    barrel="18",
    weight=3.3,
    rateoffire=950,
    bullpup=True,)

ASR_SR3M = Weapon(
    ammotype="9x39mm",
    barrel="6",
    weight=2.2,
    rateoffire=900,)

ASR_SR3M_Survival = Weapon(
    ammotype="9x39mm",
    barrel="6",
    weight=2.2,
    rateoffire=900,)

ASR_SR3M_SCT = Weapon(
    ammotype="9x39mm",
    barrel="8",
    weight=2.5,
    rateoffire=900,)

ASR_SR3M_TAC = Weapon(
    ammotype="9x39mm",
    barrel="8",
    weight=2.5,
    rateoffire=900,)

DMR_M110 = Weapon(
    ammotype="7,62x51mm",
    barrel="16",
    weight=4.8,)

ASR_MK18 = Weapon(
    ammotype="5,56x45mm",
    barrel="10",
    weight=2.7,
    rateoffire=950,)

ASR_MDR = Weapon(
    ammotype="7,62x51mm",
    barrel="20",
    weight=4.5,
    rateoffire=650,
    bullpup=True,)

ASR_M4A1_SURVIVAL = Weapon(
    ammotype="5,56x45mm",
    barrel="14",
    weight=2.9,
    rateoffire=950,)

ASR_M4A1 = Weapon(
    ammotype="5,56x45mm",
    barrel="14",
    weight=2.9,
    rateoffire=950,)

ASR_M4A1_ASU = Weapon(
    ammotype="5,56x45mm",
    barrel="14",
    weight=2.9,
    rateoffire=950,)

ASR_M4A1_ASU_Valor_Skin = Weapon(
    ammotype="5,56x45mm",
    barrel="14",
    weight=2.9,
    rateoffire=950,)

ASR_IWI_ACE = Weapon(
    ammotype="7,62x39mm",
    barrel="16",
    weight=4,
    rateoffire=850,)

SMG_P90 = Weapon(
    ammotype="5,7x28mm SMG",
    barrel="10",
    weight=2.5,
    rateoffire=1100,
    bullpup=True,)

Unique_SMG_P90_Flycatcher = Weapon(
    ammotype="5,7x28mm SMG",
    barrel="10",
    weight=2.5,
    rateoffire=1100,
    bullpup=True,)

LMG_MK48 = Weapon(
    ammotype="7,62x51mm",
    barrel="20",
    weight=8.2,
    rateoffire=730,)

LMG_MK48_SAW = Weapon(
    ammotype="7,62x51mm",
    barrel="20",
    weight=8.2,
    rateoffire=730,)

HDG_P45T = Weapon(
    ammotype=".45 ACP HDG",
    barrel="5",
    weight=0.95,
    onehanded=True,)

ASR_AK47 = Weapon(
    ammotype="7,62x39mm",
    barrel="16",
    weight=3.5,
    rateoffire=600,)

ASR_AK47_ASU = Weapon(
    ammotype="7,62x39mm",
    barrel="16",
    weight=3.5,
    rateoffire=600,)

DMR_MK14 = Weapon(
    ammotype="7,62x51mm",
    barrel="22",
    weight=4.2,
    rateoffire=750,)

DMR_MK14_ASU_Brown_Skin = Weapon(
    ammotype="7,62x51mm",
    barrel="18",
    weight=5.1,
    rateoffire=750,)

SNR_L115A3 = Weapon(
    ammotype=".338 Lupua",
    barrel="27",
    weight=6.5,)

HDG_M1911 = Weapon(
    ammotype=".45 ACP HDG",
    barrel="5",
    weight=1.1,
    onehanded=True,)

HDG_M1911_Promise_Skin = Weapon(
    ammotype=".45 ACP HDG",
    barrel="5",
    weight=1.1,
    onehanded=True,)

HDG_5_7USG = Weapon(
    ammotype="5,7x28mm HDG",
    barrel="5",
    weight=0.6,
    onehanded=True,)

HDG_5_7USG_SC_IS = Weapon(
    ammotype="5,7x28mm HDG",
    barrel="5",
    weight=0.6,
    onehanded=True,)

ASR_G36C = Weapon(
    ammotype="5,56x45mm",
    barrel="12",
    weight=3.4,
    rateoffire=750,
)

ASR_805_BREN = Weapon(
    ammotype="5,56x45mm",
    barrel="14",
    weight=3.3,
    rateoffire=850,
)

ASR_CZ805_BREN_Bivouac = Weapon(
    ammotype="5,56x45mm",
    barrel="14",
    weight=3.3,
    rateoffire=850,
)

SMG_MP7 = Weapon(
    ammotype="4,6x30mm",
    barrel="10",
    weight=1.9,
    rateoffire=950,
)

SMG_Vector = Weapon(
    ammotype=".45 ACP SMG",
    barrel="5",
    weight=3.6,
    rateoffire=1200,
)

SMG_Vector_CQC = Weapon(
    ammotype=".45 ACP SMG",
    barrel="5",
    weight=3.6,
    rateoffire=1200,
)

SMG_Vector_Droid_Twin = Weapon(
    ammotype=".45 ACP SMG",
    barrel="5",
    weight=3.6,
    rateoffire=1200,
)

Unique_SMG_Vector_CQC_Control_ROOM = Weapon(
    ammotype=".45 ACP SMG",
    barrel="5",
    weight=3.6,
    rateoffire=1200,
)

LMG_MG121 = Weapon(
    ammotype="7,62x51mm",
    barrel="22",
    weight=10,
    rateoffire=800,
)

LMG_6P41 = Weapon(
    ammotype="7,62x54mm",
    barrel="26",
    weight=8.2,
    rateoffire=800,
)

LMG_6P41_Y1E1_NPC = Weapon(
    ammotype="7,62x54mm",
    barrel="26",
    weight=8.2,
    rateoffire=800,
)

SMG_MP5 = Weapon(
    ammotype="9x19mm SMG",
    barrel="16",
    weight=2.5,
    rateoffire=800,
)

SMG_MP5_Division_Skin = Weapon(
    ammotype="9x19mm SMG",
    barrel="16",
    weight=2.5,
    rateoffire=800,
)

ASR_AK12 = Weapon(
    ammotype="5,45x39mm",
    barrel="16",
    weight=3.5,
    rateoffire=700,
)

ASR_AK12_Bivouac = Weapon(
    ammotype="5,45x39mm",
    barrel="16",
    weight=3.5,
    rateoffire=700,
)

ASR_MK17 = Weapon(
    ammotype="7,62x51mm",
    barrel="16",
    weight=3.9,
    rateoffire=550,
)

ASR_MK17_ASU = Weapon(
    ammotype="7,62x51mm",
    barrel="16",
    weight=3.9,
    rateoffire=550,
)

ASR_MK17_GRFS_Skin = Weapon(
    ammotype="7,62x51mm",
    barrel="16",
    weight=3.9,
    rateoffire=550,
)

ASR_MK17_ASU_Wolves_Skin = Weapon(
    ammotype="7,62x51mm",
    barrel="16",
    weight=3.9,
    rateoffire=550,
)

ASR_553 = Weapon(
    ammotype="5,56x45mm",
    barrel="14",
    weight=3.2,
    rateoffire=700,
    )

ASR_553_Y1E1_NPC = Weapon(
    ammotype="5,56x45mm",
    barrel="14",
    weight=3.2,
    rateoffire=700,
    )

SMG_MPX = Weapon(
    ammotype="9x19mm SMG",
    barrel="8",
    weight=2.7,
    rateoffire=850,
)

SMG_MPX_Tactical = Weapon(
    ammotype="9x19mm SMG",
    barrel="8",
    weight=2.7,
    rateoffire=850,
)

SMG_VITYAZ = Weapon(
    ammotype="9x19mm SMG",
    barrel="9",
    weight=2.9,
    rateoffire=800,
)

HDG_M9 = Weapon(
    ammotype="9x19mm HDG",
    barrel="5",
    weight=1,
    onehanded=True,
    )

Unique_HDG_M9_Gibson = Weapon(
    ammotype="9x19mm HDG",
    barrel="5",
    weight=1,
    onehanded=True,
    )

DMR_DRAGUNOV = Weapon(
    ammotype="7,62x54mm",
    barrel="24",
    weight=3.5,
)

DMR_DRAGUNOV_Bivouac = Weapon(
    ammotype="7,62x54mm",
    barrel="24",
    weight=3.5,
)

DMR_DRAGUNOV_YE_E1_PVP_Patchwork = Weapon(
    ammotype="7,62x54mm",
    barrel="24",
    weight=3.5,
)

SNR_HTI = Weapon(
    ammotype="50BMG",
    barrel="29",
    weight=9,
    bullpup=True,
)

SNR_HTI_Survival_Skin = Weapon(
    ammotype="50BMG",
    barrel="29",
    weight=9,
    bullpup=True,
)

SNR_HTI_Brown_Skin = Weapon(
    ammotype="50BMG",
    barrel="29",
    weight=9,
    bullpup=True,
)

ASR_AUG = Weapon(
    ammotype="5,56x45mm",
    barrel="16",
    weight=3.3,
    rateoffire=750,
    bullpup=True,
)

ASR_AUG_ASU = Weapon(
    ammotype="5,56x45mm",
    barrel="16",
    weight=3.3,
    rateoffire=750,
    bullpup=True,
)

SMG_SCPNEVO3 = Weapon(
    ammotype="9x19mm SMG",
    barrel="8",
    weight=2.6,
    rateoffire=1150,
)

SMG_SCPNEVO3_CQC = Weapon(
    ammotype="9x19mm SMG",
    barrel="8",
    weight=2.6,
    rateoffire=1150,
)

SMG_SCPNEVO3_Tactical = Weapon(
    ammotype="9x19mm SMG",
    barrel="8",
    weight=2.6,
    rateoffire=1150,
)

LMG_Type95 = Weapon(
    ammotype="5,56x45mm",
    barrel="18",
    weight=3.3,
    rateoffire=650,
    bullpup=True,
)

LMG_T95_Bivouac = Weapon(
    ammotype="5,56x45mm",
    barrel="18",
    weight=3.3,
    rateoffire=650,
    bullpup=True,
)

DMR_G28 = Weapon(
    ammotype="7,62x51mm",
    barrel="20",
    weight=6.1,
)

DMR_G28_Wilderness = Weapon(
    ammotype="7,62x51mm",
    barrel="20",
    weight=6.1,
)

ASR_AK74 = Weapon(
    ammotype="5,45x39mm",
    barrel="16",
    weight=3.1,
    rateoffire=650,
)

ASR_AK74_ASU = Weapon(
    ammotype="5,45x39mm",
    barrel="16",
    weight=3.1,
    rateoffire=650,
)

ASR_AK74_ASU_Survival_Skin = Weapon(
    ammotype="5,45x39mm",
    barrel="16",
    weight=3.1,
    rateoffire=650,
)

ASR_AK74_SCT = Weapon(
    ammotype="5,45x39mm",
    barrel="20",
    weight=3.5,
    rateoffire=650,
)

Y1E1_SMG_UZI9mm = Weapon(
    ammotype="9x19mm SMG",
    barrel="10",
    weight=3.7,
    rateoffire=600,
)

Y1E1_SMG_UZI9mm_NPC = Weapon(
    ammotype="9x19mm SMG",
    barrel="10",
    weight=3.7,
    rateoffire=600,
)

Y1E1_ASR_AR18 = Weapon(
    ammotype="5,56x45mm",
    barrel="18",
    weight=3,
    rateoffire=750,
)

Y1E1_ASR_AR18_NPC = Weapon(
    ammotype="5,56x45mm",
    barrel="18",
    weight=3,
    rateoffire=750,
)

Y1E1_ASR_Valmet82 = Weapon(
    ammotype="7,62x39mm",
    barrel="16",
    weight=3.3,
    rateoffire=750,
    bullpup=True,
)

Y1E1_HDG_Hardballer45 = Weapon(
    ammotype=".45 ACP HDG",
    barrel="7",
    weight=1.4,
    onehanded=True,
)

asr_416 = Weapon(
    ammotype="5,56x45mm",
    barrel="14",
    weight=3.5,
    rateoffire=850,
)

ASR_416_ASU = Weapon(
    ammotype="5,56x45mm",
    barrel="14",
    weight=3.5,
    rateoffire=850,
)

ASR_416_BlackIce_Skin = Weapon(
    ammotype="5,56x45mm",
    barrel="14",
    weight=3.5,
    rateoffire=850,
)

ASR_416_ASU_Custom_Skin = Weapon(
    ammotype="5,56x45mm",
    barrel="14",
    weight=3.5,
    rateoffire=850,
)

ASR_416_CQC = Weapon(
    ammotype="5,56x45mm",
    barrel="10",
    weight=3.2,
    rateoffire=850
)

ASR_416_CQC_Brown_Skin = Weapon(
    ammotype="5,56x45mm",
    barrel="10",
    weight=3.2,
    rateoffire=850
)

LMG_MK48_Compact = Weapon(
    ammotype="7,62x51mm",
    barrel="16",
    weight=7,
    rateoffire=730,
)

ASR_TAVOR_SCT = Weapon(
    ammotype="5,56x45mm",
    barrel="20",
    weight=3.5,
    rateoffire=950,
    bullpup=True,
)

HDG_P227 = Weapon(
    ammotype=".45 ACP HDG",
    barrel="4",
    weight=0.9,
    onehanded=True,
)

HDG_P227_Survival_Skin = Weapon(
    ammotype=".45 ACP HDG",
    barrel="4",
    weight=0.9,
    onehanded=True,
)

ASR_516 = Weapon(
    ammotype="5,56x45mm",
    barrel="16",
    weight=3.3,
    rateoffire=950,
)

ASR_516_Survival_Skin = Weapon(
    ammotype="5,56x45mm",
    barrel="16",
    weight=3.3,
    rateoffire=950,
)

HDG_P320 = Weapon(
    ammotype="9x19mm HDG",
    barrel="5",
    weight=0.8,
    onehanded=True,
)

HDG_P320_Brown_Skin = Weapon(
    ammotype="9x19mm HDG",
    barrel="5",
    weight=0.8,
    onehanded=True,
)

HDG_P320_Sentinel_Skin = Weapon(
    ammotype="9x19mm HDG",
    barrel="5",
    weight=0.8,
    onehanded=True,
)

HDG_P320_NPC = Weapon(
    ammotype="9x19mm HDG",
    barrel="5",
    weight=0.8,
    onehanded=True,
)

ASR_MK17_CQC = Weapon(
    ammotype="7,62x51mm",
    barrel="10",
    weight=3.6,
    rateoffire=550,
)

ASR_MK17_CQC_Gargoyle = Weapon(
    ammotype="7,62x51mm",
    barrel="10",
    weight=3.6,
    rateoffire=550,
)

LMG_STONER = Weapon(
    ammotype="5,56x45mm",
    barrel="16",
    weight=5,
    rateoffire=600,
)

LMG_STONER_Compact = Weapon(
    ammotype="5,56x45mm",
    barrel="12",
    weight=4.5,
    rateoffire=600,
)

SNR_Victrix =  Weapon(
    ammotype=".338 Lupua",
    barrel="26",
    weight=6.7,
)

SNR_Victrix_Brown =  Weapon(
    ammotype=".338 Lupua",
    barrel="26",
    weight=6.7,
)

Unique_SNR_Victrix_WOLVES = Weapon(
    ammotype=".338 Lupua",
    barrel="26",
    weight=6.7,
)

SNR_Victrix_SCT = Weapon(
    ammotype=".338 Lupua",
    barrel="22",
    weight=6.4,
)

SNR_Victrix_SCT_Quiet = Weapon(
    ammotype=".338 Lupua",
    barrel="22",
    weight=6.4,
)

DMR_G28_SCT = Weapon(
    ammotype="7,62x51mm",
    barrel="16",
    weight=5.8,
)

Unique_DMR_G28_SCT = Weapon(
    ammotype="7,62x51mm",
    barrel="16",
    weight=5.8,
)

ASR_516_CQC = Weapon(
    ammotype="5,56x45mm",
    barrel="10",
    weight=3.1,
    rateoffire=950,
)

Unique_ASR_516_KOBLIN = Weapon(
    ammotype="5,56x45mm",
    barrel="10",
    weight=3.1,
    rateoffire=950,
)

ASR_516_CIN_ONLY_KOBLIN = Weapon(
    ammotype="5,56x45mm",
    barrel="10",
    weight=3.1,
    rateoffire=950,
)

LMG_L86A1 = Weapon(
    ammotype="5,56x45mm",
    barrel="25",
    weight=6.4,
    rateoffire=775,
    bullpup=True
)

Unique_ASR_Omen = Weapon(
    ammotype="7,62x51mm",
    barrel="20",
    weight=5,
    rateoffire=450,
)

Unique_HDG_Veritas = Weapon(
    ammotype=".44 Magnum",
    barrel="6",
    weight=1.5,
    onehanded=True
)

SNR_M82 = Weapon(
    ammotype="50BMG",
    barrel="26",
    weight=13.5,
)

SNR_M82_Cerberus_Unique = Weapon(
    ammotype="50BMG",
    barrel="26",
    weight=13.5,
)

SNR_M82_Survival_Skin = Weapon(
    ammotype="50BMG",
    barrel="26",
    weight=13.5,
)

SMG_PDR_MAGPUL = Weapon(
    ammotype="5,56x45mm",
    barrel="10",
    weight=2.7,
    rateoffire=650,
    bullpup=True
)

ASR_SC20K = Weapon(
    ammotype="5,56x45mm",
    barrel="16",
    weight=3.6,
    rateoffire=850,
    bullpup=True,
)

ASR_A2 = Weapon(
    ammotype="5,56x45mm",
    barrel="18",
    weight=3.7,
    rateoffire=890,
)

SNR_SRSA1 = Weapon(
    ammotype=".338 Lupua",
    barrel="26",
    weight=5,
    bullpup=True,
)

ASR_416_SCT = Weapon(
    ammotype="5,56x45mm",
    barrel="20",
    weight=3.8,
    rateoffire=850,
)

ASR_G36C_SCT = Weapon(
    ammotype="5,56x45mm",
    barrel="18",
    weight=3.6,
    rateoffire=750,
)

ASR_A2_CQC = Weapon(
    ammotype="5,56x45mm",
    barrel="10",
    weight=3.1,
    rateoffire=890
)

ASR_M4A1_Tactical = Weapon(
    ammotype=".300 blackout",
    barrel="8",
    weight=2.6,
    rateoffire=950,
)

ASR_M4A1_Tactical_Brown_Skin = Weapon(
    ammotype=".300 blackout",
    barrel="8",
    weight=2.6,
    rateoffire=950,
)

ASR_M4A1_Tactical_WOLVES_Skin = Weapon(
    ammotype=".300 blackout",
    barrel="8",
    weight=2.6,
    rateoffire=950,
)

ASR_553_SCT = Weapon(
    ammotype="5,56x45mm",
    barrel="20",
    weight=3.6,
    rateoffire=700,
)

ASR_553_SCT_Sentinel_Skin = Weapon(
    ammotype="5,56x45mm",
    barrel="20",
    weight=3.6,
    rateoffire=700,
)

SNR_TAC50 = Weapon(
    ammotype="50BMG",
    barrel="29",
    weight=12,
)

SNR_TAC50_Brown_Skin = Weapon(
    ammotype="50BMG",
    barrel="29",
    weight=12,
)

SNR_TAC50_Wolves = Weapon(
    ammotype="50BMG",
    barrel="29",
    weight=12,
)

Unique_ASR_Omen_Tactical = Weapon(
    ammotype="7,62x51mm",
    barrel="16",
    weight=4.6,
    rateoffire=450,
)

HDG_F40 = Weapon(
    ammotype="9x19mm HDG",
    barrel="4",
    weight=0.7,
    onehanded=True
)

HDG_HS2000 = Weapon(
    ammotype="9x19mm HDG",
    barrel="5",
    weight=0.7,
    onehanded=True
)

HDG_HS2000_BAAL = Weapon(
    ammotype="9x19mm HDG",
    barrel="5",
    weight=0.7,
    onehanded=True
)

HDG_PX4 = Weapon(
    ammotype=".45 ACP HDG",
    barrel="4",
    weight=0.8,
    onehanded=True
)

LMG_CTMMG = Weapon(
    ammotype="7,62x51mm",
    barrel="16",
    weight=9,
    rateoffire=600
)

Unique_LMG_CTMMG_Baal = Weapon(
    ammotype="7,62x51mm",
    barrel="16",
    weight=9,
    rateoffire=600
)

SMG_UMP = Weapon(
    ammotype=".45 ACP SMG",
    barrel="8",
    weight=2.5,
    rateoffire=600
)

SMG_UMP_CQC = Weapon(
    ammotype=".45 ACP SMG",
    barrel="8",
    weight=2.5,
    rateoffire=600
)

DMR_MK14_ASU = Weapon(
    ammotype="7,62x51mm",
    barrel="18",
    weight=5.1,
    rateoffire=750,
)

ASR_ARX200 = Weapon(
    ammotype="7,62x51mm",
    barrel="16",
    weight=4.5,
    rateoffire=700
)

Unique_SNR_ZastavaM93 = Weapon(
    ammotype="50BMG",
    barrel="39",
    weight=16
)

DMR_FRF2 = Weapon(
    ammotype="7,62x51mm",
    barrel="24",
    weight=5.1,
)

YE1E2_HDG_MK23 = Weapon(
    ammotype="9x19mm HDG",
    barrel="6",
    weight=1.2,
    onehanded=True,
)

YE1E2_HDG_MK23_Splinter_Skin = Weapon(
    ammotype="9x19mm HDG",
    barrel="6",
    weight=1.2,
    onehanded=True,
)

Y1E3_SMG_AAC = Weapon(
    ammotype=".300 blackout",
    barrel="8",
    weight=2.3,
    rateoffire=800
)

SMG_AAC_Brown = Weapon(
    ammotype=".300 blackout",
    barrel="8",
    weight=2.3,
    rateoffire=800
)

ASR_AUG_SCT = Weapon(
    ammotype="5,56x45mm",
    barrel="20",
    weight=3.6,
    rateoffire=750,
    bullpup=True
)

ASR_M4A1_CQC = Weapon(
    ammotype="5,56x45mm",
    barrel="10",
    weight=3.1,
    rateoffire=950
)

Y1E3_ASR_FAL = Weapon(
    ammotype="7,62x51mm",
    barrel="20",
    weight=4.3,
    rateoffire=700
)

HDG_Maxim9 = Weapon(
    ammotype="9x19mm HDG",
    barrel="4",
    weight=0.9,
    onehanded=True,
)

HDG_Maxim9_Echelon = Weapon(
    ammotype="9x19mm HDG",
    barrel="4",
    weight=0.9,
    onehanded=True,
)

HDG_Maxim9_Custom = Weapon(
    ammotype="9x19mm HDG",
    barrel="4",
    weight=0.9,
    onehanded=True,
)

ASR_MK17_SCT = Weapon(
    ammotype="7,62x51mm",
    barrel="20",
    weight=4.5,
    rateoffire=550
)

ASR_M4A1_SCT = Weapon(
    ammotype="5,56x45mm",
    barrel="18",
    weight=3.8,
    rateoffire=950,
)

ASR_M4A1_SCT_Custom_Skin = Weapon(
    ammotype="5,56x45mm",
    barrel="18",
    weight=3.8,
    rateoffire=950,
)

ASR_SC40K = Weapon(
    ammotype="5,56x45mm",
    barrel="18",
    weight=3.8,
    rateoffire=850
)

ASR_SC40K_Brown_Skin = Weapon(
    ammotype="5,56x45mm",
    barrel="18",
    weight=3.8,
    rateoffire=850
)

SMG_PALADIN9 = Weapon(
    ammotype="9x19mm SMG",
    barrel="16",
    weight=2.5,
    rateoffire=950
)

SMG_PALADIN9_Custom_Skin = Weapon(
    ammotype="9x19mm SMG",
    barrel="16",
    weight=2.5,
    rateoffire=950
)

Y1E3_SNR_PALADIN9 = Weapon(
    ammotype=".338 Lupua",
    barrel="24",
    weight=5.9,
)

SNR_PALADIN9_Survival_Skin = Weapon(
    ammotype=".338 Lupua",
    barrel="24",
    weight=5.9,
)

ASR_AK47_CQC = Weapon(
    ammotype="7,62x39mm",
    barrel="8",
    weight=3.1,
    rateoffire=600,
)

ASR_4AC = Weapon(
    ammotype="5,56x45mm",
    barrel="12",
    weight=3.2,
    rateoffire=860
)

ASR_4AC_Brown_Skin = Weapon(
    ammotype="5,56x45mm",
    barrel="12",
    weight=3.2,
    rateoffire=860
)

SMG_K1A = Weapon(
    ammotype="5,56x45mm",
    barrel="10",
    weight=2.9,
    rateoffire=900
)

DMR_OTS_SVU = Weapon(
    ammotype="7,62x54mm",
    barrel="20",
    weight=3.6,
    bullpup=True
)

ASR_G3 = Weapon(
    ammotype="5,56x45mm",
    barrel="20",
    weight=3.6,
    rateoffire=1100
)

ASR_L85C = Weapon(
    ammotype="5,56x45mm",
    barrel="20",
    weight=4,
    rateoffire=775,
    bullpup=True
)

Y1E1_ASR_Valmet82_CQC = Weapon(
    ammotype="7,62x51mm",
    barrel="10",
    weight=3,
    rateoffire=650,
    bullpup=True
)

SNR_VSSK = Weapon(
    ammotype="12,7x55mm",
    barrel="18",
    weight=7,
    bullpup=True
)

ASR_ACR = Weapon(
    ammotype="5,56x45mm",
    barrel="14",
    weight=3.6,
    rateoffire=700
)

ASR_ACR_ASU = Weapon(
    ammotype="5,56x45mm",
    barrel="14",
    weight=3.6,
    rateoffire=700
)

ASR_ACR_Brown = Weapon(
    ammotype="5,56x45mm",
    barrel="14",
    weight=3.6,
    rateoffire=700
)

#-----------------------------------------------------------------------------
#This is the actual script

ammotype = {
    "5,56x45mm": {"id": 1863346880522, 
        "damage": 29, 
        "zero": 67,
        "barrels": {
            "10": {"range": 257, "velocity": 710},
            "12": {"range": 274, "velocity": 750},
            "14": {"range": 284, "velocity": 790},
            "16": {"range": 295, "velocity": 820},
            "18": {"range": 309, "velocity": 850},
            "20": {"range": 322, "velocity": 880},
            "25": {"range": 337, "velocity": 910},
        },
        "penetration1": 1500, 
        "penetration2": 30,
        "soundrange": 1000,
        "magweight": 0.5,
    },
    "7,62x51mm": {"id": 1863346882035,
        "damage": 60,
        "zero": 67, 
        "barrels": {
            "10": {"range": 222, "velocity": 570},
            "16": {"range": 262, "velocity": 730},
            "18": {"range": 274, "velocity": 760},
            "20": {"range": 284, "velocity": 790},
            "22": {"range": 292, "velocity": 810},
            "24": {"range": 297, "velocity": 830},
        },
        "penetration1": 2500, 
        "penetration2": 40,
        "soundrange": 1200,
        "magweight": 0.75,
    },
    "9x19mm SMG": {"id": 1863346882157,
        "damage": 18,
        "zero": 33, 
        "barrels": {
            "4": {"range": 117, "velocity": 280},
            "5": {"range": 119, "velocity": 280},
            "6": {"range": 121, "velocity": 280},
            "7": {"range": 122, "velocity": 280},
            "8": {"range": 123, "velocity": 280},
            "9": {"range": 124, "velocity": 280},
            "10": {"range": 125, "velocity": 280},
            "16": {"range": 127, "velocity": 280},
        },
        "penetration1": 750, 
        "penetration2": 10,
        "soundrange": 600,
        "magweight": 0.6,
    },
    ".45 ACP SMG": {"id": 1863346882237,
        "damage": 18,
        "zero": 33,  
        "barrels": {
            "4": {"range": 117, "velocity": 200},
            "5": {"range": 119, "velocity": 200},
            "6": {"range": 123, "velocity": 210},
            "7": {"range": 126, "velocity": 210},
            "8": {"range": 127, "velocity": 210},
            "16": {"range": 129, "velocity": 210},
        },
        "penetration1": 500, 
        "penetration2": 10,
        "soundrange": 600,
        "magweight": 0.7,
    },
    ".338 Lupua": {"id": 1863346883377,
        "damage": 120, 
        "zero": 67, 
        "barrels": {
            "22": {"range": 299, "velocity": 770},
            "24": {"range": 310, "velocity": 820},
            "25": {"range": 317, "velocity": 850},
            "26": {"range": 321, "velocity": 870},
            "27": {"range": 326, "velocity": 890},
        },
        "penetration1": 2500, 
        "penetration2": 40,
        "soundrange": 1200,
        "magweight": 0.4,
},
    #"12 Gauge": 1863346883405,
    "5,7x28mm SMG": {"id": 707338684561,
        "damage": 22,
        "zero": 33,  
        "barrels": {
            "10": {"range": 202, "velocity": 740},
            "5": {"range": 179, "velocity": 575},
        },
        "penetration1": 1500, 
        "penetration2": 25,
        "soundrange": 900,
        "magweight": 0.5,
    },
    "4,6x30mm": {"id": 707338550223,
        "damage": 22, 
        "zero": 33, 
        "barrels": {
            "10": {"range": 202, "velocity": 740},
        },
        "penetration1": 1500, 
        "penetration2": 25,
        "soundrange": 900,   
        "magweight": 0.3,
    },
    ".300 blackout": {"id": 1702549420470,
        "damage": 25, 
        "zero": 33, 
        "barrels": {
            "8": {"range": 132, "velocity": 270},
        },
        "penetration1": 1500, 
        "penetration2": 20,
        "soundrange": 700,   
        "magweight": 0.7,
    },
    "9x39mm": {"id": 1836502453101,
        "damage": 25, 
        "zero": 33, 
        "barrels": {
            "6": {"range": 125, "velocity": 280},
            "8": {"range": 128, "velocity": 290},
        },
        "penetration1": 1500, 
        "penetration2": 30,
        "soundrange": 700,
        "magweight": 1,
    },
    "5,45x39mm": {"id": 942455210524,
        "damage": 29,
        "zero": 67, 
        "barrels": {
            "16": {"range": 292, "velocity": 850},
            "20": {"range": 307, "velocity": 900},
        },
        "penetration1": 1500, 
        "penetration2": 25,
        "soundrange": 1000,
        "magweight": 0.55,
    },
    "7,62x39mm": {"id": 1151824871978,
        "damage": 48, 
        "zero": 67, 
        "barrels": {
            "8": {"range": 172, "velocity": 450},
            "16": {"range": 244, "velocity": 650},
        },
        "penetration1": 2500, 
        "penetration2": 35,
        "soundrange": 1100,
        "magweight": 0.75,
    },
    "7,62x54mm": {"id": 1923391096271,
        "damage": 60, 
        "zero": 67, 
        "barrels": {
            "20": {"range": 295, "velocity": 780},
            "24": {"range": 312, "velocity": 830},
            "26": {"range": 318, "velocity": 850},
        },
        "penetration1": 2500, 
        "penetration2": 45,
        "soundrange": 1200,
        "magweight": 0.96,
},
    "50BMG": {"id": 1885614916957,
        "damage": 300, 
        "zero": 67, 
        "barrels": {
            "26": {"range": 321, "velocity": 710},
            "29": {"range": 326, "velocity": 760},
            "39": {"range": 337, "velocity": 840},
        },
        "penetration1": 3000, 
        "penetration2": 100,
        "soundrange": 1300,
        "magweight": 1.4,
},
    "12,7x55mm": {"id": 1374681720141,
        "damage": 65, 
        "zero": 33, 
        "barrels": {
            "18": {"range": 136, "velocity": 270},
        },
        "penetration1": 2500, 
        "penetration2": 60,
        "soundrange": 800,
        "magweight": 1.3,
    },
    "9x19mm HDG": {"id": 1702549653038,
        "damage": 18, 
        "zero": 33, 
        "barrels": {
            "4": {"range": 117, "velocity": 280},
            "5": {"range": 119, "velocity": 280},
            "6": {"range": 121, "velocity": 280},
            "7": {"range": 122, "velocity": 280},
            "8": {"range": 123, "velocity": 280},
            "9": {"range": 124, "velocity": 280},
            "10": {"range": 125, "velocity": 280},
            "16": {"range": 127, "velocity": 280},
        },
        "penetration1": 750, 
        "penetration2": 10,
        "soundrange": 600,
        "magweight": 0.3,
    },
    "5,7x28mm HDG": {"id": 1702549653505,
        "damage": 22, 
        "zero": 33, 
        "barrels": {
            "10": {"range": 202, "velocity": 740},
            "5": {"range": 179, "velocity": 575},
        },
        "penetration1": 1500, 
        "penetration2": 25,
        "soundrange": 900,
        "magweight": 0.2,
    },
    ".45 ACP HDG": {"id": 1972921083968,
        "damage": 18, 
        "zero": 33, 
        "barrels": {
            "4": {"range": 117, "velocity": 200},
            "5": {"range": 119, "velocity": 200},
            "6": {"range": 123, "velocity": 210},
            "7": {"range": 126, "velocity": 210},
            "8": {"range": 127, "velocity": 210},
            "16": {"range": 129, "velocity": 210},
        },
        "penetration1": 500, 
        "penetration2": 10,
        "soundrange": 600,
        "magweight": 0.3,
    },
    ".44 Magnum": {"id": 1702549668310,
        "damage": 33, 
        "zero": 33, 
        "barrels": {
            "6": {"range": 126, "velocity": 400},
        },
        "penetration1": 1500, 
        "penetration2": 30,
        "soundrange": 900,
        "magweight": 0.2,
    },
    ".50 AE": {"id": 1895939232185,
        "damage": 33, 
        "zero": 33, 
        "barrels": {
            "6": {"range": 126, "velocity": 420},
        },
        "penetration1": 1500, 
        "penetration2": 30,
        "soundrange": 900,
        "magweight": 0.4,
    },
    #".410": 524247623366,
}

weaponid = {
    HDG_USP_MATCH: 2063640955193,
    HDG_DEAGLE_SURVIVOR: 2063641092276,
    SNR_SR1: 2063640955911,
    SNR_MSR: 2063640955800,
    ASR_Valmet82_CQC: 2054599840855,
    ASR_VHSD2_SURVIVAL: 2063640955941,
    ASR_TAVOR_CUSTOM: 2063640998057,
    ASR_SR3M: 2063641112605,
    DMR_M110: 2063641143294,
    ASR_SR3M_SCT: 2063641210500,
    ASR_SR3M_TAC: 2063641210526,
    #"ASR_SR3M_NPC_NO_SUPP": 2063641265502,
    ASR_SR3M_Survival: 2075405282177,
    ASR_MK18: 2063640604364,
    ASR_MDR: 2063640604471,
    ASR_M4A1_SURVIVAL: 2063640954436,
    ASR_IWI_ACE: 2063641131599,
    SMG_P90: 205425832666,
    LMG_MK48: 205425832785,
    HDG_P45T: 205425832841,
    ASR_AK47: 205425833825,
    DMR_MK14: 209887659263,
    ASR_M4A1: 215997404506,
    #"EXO_FlameThrower": 217877090254,
    #"EXO_Dillon_Aero": 235226699664,
    SNR_L115A3: 253209230891,
    #"EXO_Flare": 254177441496,
    HDG_M1911: 395649520497,
    HDG_5_7USG: 395649524046,
    ASR_G36C: 395649527798,
    #"RPG-7": 411647786920,
    ASR_805_BREN: 442434770595,
    SMG_MP7: 442434776985,
    SMG_Vector: 462589793890,
    #"EXO_Dillon_Aero_Rocket": 519604197896,
    LMG_MG121: 519604481361,
    LMG_6P41: 519604496249,
    SMG_MP5: 519604496765,
    ASR_AK12: 519604624355,
    ASR_MK17: 519604624370,
    ASR_553: 519604624400,
    SMG_MPX: 519604624430,
    SMG_VITYAZ: 519604624445,
    #"EXO_Dillon_Aero_Handheld": 519604685624,
    HDG_M9: 524247145405,
    DMR_DRAGUNOV: 524247201046,
    ASR_TAVOR: 524247311397,
    SNR_HTI: 524247314837,
    HDG_USP: 524247316226,
    #"EXO_APC_M2_Browning": 524247339065,
    ASR_AUG: 524247864396,
    #"EXO_Heli_RocketLauncher": 601287989916,
    HDG_DEAGLE: 707338342885,
    SMG_SCPNEVO3: 707338348832,
    LMG_Type95: 707338351227,
    DMR_G28: 707338552163,
    #"STG_SASG12": 707338553910,
    #"EXO_Dillon_Aero_Twin": 707338890026,
    #"EXO_Dillon_Aero_ReducedDamage": 855442657665,
    #"EXO_Heli_RocketLauncher_Guided": 1067984401980,
    #"EXO_Heli_RocketLauncher_Burst": 1067984402040,
    #"EXO_Dillon_Aero_Gunship": 1067984402116,
    #"DEPRECATED_EXO_GroundDroid_M2_Light_Left": 1268177872409,
    #"DEPRECATED_EXO_APC_M2_Browning_Droid": 1403686408629,
    SMG_SCPNEVO3_CQC: 1481649372336,
    ASR_AK74: 1481649374137,
    ASR_AK74_SCT: 1481649374938,
    #"EXO_Droid_SpecialWeapon_Mk19_Flash": 1514981061355,
    #"EXO_Droid_SpecialWeapon_Mk19_AirBurst": 1514981061380,
    Y1E1_SMG_UZI9mm: 1539516991678,
    Y1E1_ASR_AR18: 1539516991706,
    Y1E1_ASR_AR18_NPC: 1539516991855,
    Y1E1_ASR_Valmet82: 1539516991880,
    Y1E1_HDG_Hardballer45: 1539516991940,
    Y1E1_SMG_UZI9mm_NPC: 1539516992032,
    #"Y1E1_STG_SPAS-12": 1539516992057,
    #"Y1E1_STG_SPAS-12_NPC": 1539516992256,
    #"Y1E1_Unique_GRL_MGL_Miter": 1539516992281,
    #"EXO_GroundDroid_M2_Right": 1544350702414,
    #"EXO_GroundDroid_M2_Left": 1544350702431,
    #"RAID01_Boss_TankAnalyzer_EXO_LaserAnalyzer_Wpn": 1656696608413,
    #"EXO_M61_VULCAN_Goliath_Right": 1664044856842,
    ASR_TAR21_NPC: 1695615924318,
    #"STG_BenelliM4_PROG_TEST": 1695615970083,
    #"HDG_M1911_DRN": 1695616304598,
    #"EXO_Turret_M2_Left": 1695616412336,
    #"EXO_Turret_M2_Right": 1695616412422,
    asr_416: 1698309405617,
    ASR_416_ASU: 1698309413939,
    ASR_416_CQC: 1698309413969,
    #"GRL_MGL": 1698309414005,
    LMG_MK48_Compact: 1698309414400,
    LMG_MK48_SAW: 1698309414420,
    ASR_TAVOR_ASU: 1698309422692,
    ASR_TAVOR_SCT: 1698309422712,
    ASR_M4A1_ASU: 1698309432995,
    #"STG_M4": 1698309442405,
    #"STG_M4_ASU": 1698309442583,
    #"ASR_AUG_Droid_Twin": 1698309465125,
    #"SMG_Vector_Droid_Twin": 1698309465145,
    #"GRL_MGL_MK19_Droid": 1698309465165,
    #"EXO_M61_VULCAN_Goliath_Left": 1698309465181,
    #"EXO_Rocket_Pod_Droid": 1698309465198,
    #"EXO_SpecialWeapon_Droid_base": 1698309465213,
    #"EXO_Autonomous_Mortar_Droid": 1698309465228,
    #"SMG_MP7_Droid": 1698309465273,
    #"EXO_CarlGustav_IA": 1698309467420,
    HDG_P227: 1698309474529,
    ASR_516: 1698309480414,
    HDG_P320: 1698309480731,
    ASR_MK17_CQC: 1698309480794,
    LMG_STONER: 1698309488994,
    LMG_STONER_Compact: 1698309489037,
    SNR_Victrix: 1698309489059,
    SNR_Victrix_SCT: 1698309489084,
    SMG_MPX_Tactical: 1698309489299,
    DMR_G28_SCT: 1698309493961,
    ASR_516_CQC: 1698309523670,
    LMG_L86A1: 1698309558688,
    Unique_ASR_Omen: 1698309559828,
    Unique_HDG_Veritas: 1698309559843,
    SNR_M82: 1698309572456,
    SMG_PDR_MAGPUL: 1698309575883,
    ASR_SC20K: 1698309597091,
    #"STG_KSG12": 1698309612445,
    ASR_A2: 1698309614712,
    SNR_SRSA1: 1698309619035,
    ASR_AK12_Bivouac: 1698309626211,
    ASR_CZ805_BREN_Bivouac: 1698309626238,
    LMG_T95_Bivouac: 1698309626290,
    DMR_DRAGUNOV_Bivouac: 1698309626316,
    ASR_416_SCT: 1698309628430,
    ASR_AK74_ASU: 1698309629274,
    ASR_AUG_ASU: 1698309629311,
    ASR_G36C_SCT: 1698309629340,
    ASR_A2_CQC: 1698309631130,
    ASR_M4A1_Tactical: 1698309631160,
    ASR_553_SCT: 1698309631246,
    SMG_SCPNEVO3_Tactical: 1698309633958,
    SMG_Vector_CQC: 1698309633995,
    #"STG_M4_CQC": 1698309634024,
    #"STG_RU12SG": 1698309639276,
    #"DEPRECATED_EXO_M61_VULCAN_Ogre_Left": 1756757876154,
    #"EXO_M61_VULCAN_Ogre_Right": 1756757876394,
    #"GRL_MGL_NPC": 1758727289692,
    #"EXO_VHC_PMV_Blitz_Canon": 1833606984475,
    #"EXO_VHC_PMV_Locust_Canon": 1833607005141,
    #"EXO_VHC_PMV_Spartan": 1833607011765,
    #"EXO_GroundDroid_M2_Light_Right": 1834199005979,
    #"EXO_SpecialWeapon_Droid_Goliath": 1834199266546,
    #"EXO_SpecialWeapon_Droid_Ogre_Mk19_base": 1834199266575,
    SNR_TAC50: 1838530169042,
    Unique_ASR_Omen_Tactical: 1838530185564,
    HDG_F40: 1838530196323,
    HDG_HS2000: 1838530196394,
    HDG_PX4: 1838530196420,
    Unique_ASR_516_KOBLIN: 1838530199945,
    ASR_VHSD2: 1838530200528,
    LMG_CTMMG: 1838530200676,
    ASR_AK47_ASU: 1838530210595,
    SMG_UMP: 1838530210626,
    #"STG_RU12SG_ASU": 1838530232967,
    DMR_MK14_ASU: 1838530252042,
    Unique_LMG_CTMMG_Baal: 1838530266637,
    Unique_HDG_M9_Gibson: 1838530266701,
    Unique_SMG_P90_Flycatcher: 1838530266733,
    #"Unique_STG_KSG12_Silverback": 1838530266765,
    HDG_P320_Brown_Skin: 1838530266827,
    SNR_Victrix_SCT_Quiet: 1838530266859,
    ASR_416_BlackIce_Skin: 1838530266890,
    ASR_MK17_GRFS_Skin: 1838530266920,
    DMR_G28_Wilderness: 1838530266984,
    HDG_M1911_Promise_Skin: 1838530267018,
    SMG_MP5_Division_Skin: 1838530267050,
    ASR_ARX200: 1838530270468,
    Unique_SNR_ZastavaM93: 1838530270614,
    #"Unique_STG_BOSG12": 1838530270764,
    DMR_FRF2: 1838530271017,
    ASR_MK17_ASU: 1838530295327,
    SNR_TAC50_Brown_Skin: 1838530295379,
    ASR_416_CQC_Brown_Skin: 1838530295412,
    SNR_HTI_Survival_Skin: 1838530295443,
    ASR_M4A1_ASU_Valor_Skin: 1838530295485,
    ASR_M4A1_Tactical_Brown_Skin: 1838530295520,
    DMR_MK14_ASU_Brown_Skin: 1838530295573,
    HDG_P227_Survival_Skin: 1838530295608,
    HDG_P320_Sentinel_Skin: 1838530295651,
    ASR_MK17_ASU_Wolves_Skin: 1838530295685,
    SNR_Victrix_Brown: 1838530295773,
    Unique_DMR_G28_SCT: 1838530343365,
    ASR_M4A1_Tactical_WOLVES_Skin: 1838530415882,
    Unique_SNR_Victrix_WOLVES: 1838530415913,
    Unique_SMG_Vector_CQC_Control_ROOM: 1838530434062,
    #"RA01_Boss_KingCom_EXO_Gatling_Left_Wpn": 1846581610138,
    #"RA01_Boss_KingCom_EXO_Gatling_Right_Wpn": 1846581610170,
    #"EXO_Dillon_Aero_SPARTAN": 1863347253886,
    #"STG_KSG12_NPC": 1868544665553,
    HDG_P320_NPC: 1869669769731,
    ASR_553_Y1E1_NPC: 1884503561814,
    #"STG_KSG12_Y1E1_NPC": 1884503562048,
    #Y1E1_Unique_DMR_MK14_Miter: 1905404294908,
    #"EXO_VHC_PMV_AGMV_MainGun": 1906134868563,
    #"EXO_VHC_PMV_AGMV_MiniGunR": 1906134869037,
    #"EXO_VHC_PMV_AGMV_MiniGunL": 1906134870429,
    #Unique_STG_KSG12_NPC: 1922868441059,
    DMR_DRAGUNOV_YE_E1_PVP_Patchwork: 1923390903028,
    YE1E2_HDG_MK23: 1923390912960,
    #"Y1E3_STG_AA12": 1923390918221,
    Y1E3_SMG_AAC: 1923390918311,
    ASR_AUG_SCT: 1923390974033,
    ASR_M4A1_CQC: 1923391127631,
    SMG_UMP_CQC: 1923391138345,
    HDG_5_7USG_SC_IS: 1923391138966,
    Y1E3_ASR_FAL: 1923391143335,
    HDG_Maxim9: 1923391179736,
    SMG_AAC_Brown: 1923391192043,
    ASR_553_SCT_Sentinel_Skin: 1923391192695,
    ASR_MK17_SCT: 1923391193105,
    ASR_M4A1_SCT: 1923391196585,
    #"GRL_MGL_QUANTUM": 1923391199557,
    ASR_SC40K: 1923391199854,
    SMG_PALADIN9: 1923391202491,
    Y1E3_SNR_PALADIN9: 1923391220806,
    YE1E2_HDG_MK23_Splinter_Skin: 1923391228500,
    HDG_Maxim9_Echelon: 1923391230043,
    ASR_AK74_ASU_Survival_Skin: 1923391232936,
    HDG_DEAGLE_Custom_Skin: 1923391235409,
    #"YEE2_STG_AA12_Custom_Skin": 1923391235927,
    SNR_M82_Cerberus_Unique: 1923391236828,
    ASR_416_ASU_Custom_Skin: 1923391237184,
    HDG_HS2000_BAAL: 1923391259711,
    #"HDG_M1911_DRN_MC": 1923391284953,
    ASR_MK17_CQC_Gargoyle: 1923391308547,
    ASR_516_CIN_ONLY_KOBLIN: 1923391362249,
    LMG_6P41_Y1E1_NPC: 1948499827079,
    ASR_AK47_CQC: 1956585194303,
    ASR_SC40K_Brown_Skin: 1956585197168,
    SMG_PALADIN9_Custom_Skin: 1956585197193,
    SNR_PALADIN9_Survival_Skin: 1956585197213,
    HDG_Maxim9_Custom: 1972921018438,
    ASR_4AC: 1972921023439,
    ASR_4AC_Brown_Skin: 1972921023611,
    ASR_516_Survival_Skin: 1972921036982,
    SNR_M82_Survival_Skin: 1972921037234,
    ASR_VHSD2_Sentinel_Skin: 1972921037266,
    SNR_HTI_Brown_Skin: 1972921037293,
    SNR_TAC50_Wolves: 1972921037325,
    ASR_M4A1_SCT_Custom_Skin: 1972921037357,
    SMG_K1A: 1972921037389,
    DMR_OTS_SVU: 1972921037564,
    #"STG_M590A1": 1972921037748,
    #"HDG_Bailiff": 1972921038235,
    ASR_G3: 1972921040702,
    ASR_L85C: 1972921236377,
    #"EXO_Ash_GrenadeLauncher": 1972921416134,
    #"EXO_CarlGustav_IA_Bodark": 2028863046761,
    #"HDG_UBSTG_Bailiff_Clone": 2033295250504,
    Y1E1_ASR_Valmet82_CQC: 2054599847403,
    #"EXO_Heli_RocketLauncher_Burst_Barrel": 2054599847522,
    SNR_VSSK: 2093898556550,
    ASR_ACR: 2059340731069,
    ASR_ACR_ASU: 2059340731237,
    ASR_ACR_Brown: 2075405262645,
}

path = None
filename = None
fileint64 = None
#FOLDER = os.path.dirname(sys.executable) # I tilfælde af en exe
FOLDER = os.path.dirname(os.path.abspath(__file__)) # I tilfælde af et script
offset = 0
data = None

class Stat:
    def __init__(self, value, offset, type):
        self.value = value
        self.offset = offset
        self.type = type
    
    def new(self, val):
        self.newvalue = val

    def write(self, f):
        typelength = {
            "u8": 1,
            "u16": 2,
            "u32": 4,
            "u64": 8,
        }
        f.seek(self.offset)
        if self.type == "float":
            data = struct.pack("<f", float(self.newvalue))
        else:
            length = typelength[self.type]
            data = int(self.newvalue).to_bytes(length, byteorder="little")
        f.write(data)
        #print(self.offset, self.value, self.newvalue)

        
def statset(addtooffset, name, type):
    global offset
    global stats
    offset += addtooffset
    value = typeread(offset, type)
    stat_class = Stat(value, offset, type)
    stats[name] = stat_class

def dicttypesearch(name, type):
    global offset
    global ammotype
    #print(f"Searching for{name} {type} from {offset}")
    currentoffset = offset
    valid_ids = {v["id"] for v in ammotype.values()}
    count = offset + 1000
    while count > offset:
        search = typeread(currentoffset, type)
        if search in valid_ids:
            #print(f"Found {name} @ {offset}")
            offset = currentoffset
            return    
        currentoffset += 1
    
    print(f"Failed to find {name}")

def typesearch(name, searchstring, type, times):
    global offset
    #print(f"Searching for {searchstring} as {type} from {offset}")
    count = offset + 1000
    fin = 0
    if not isinstance(searchstring, (tuple, list)):
        searchstring = (searchstring,)
    while fin != times: 
        search = typeread(offset, type)
        if search in searchstring:
            fin += 1
            #print(f"Found {name} - {searchstring} @ {offset}")
            if fin != times:
                offset += 1
        elif count == offset:
            #print(f"{searchstring} not found, limit has been reached.")
            offset = count - 1000
            return
        else:
            offset += 1
    if fin == 0:
        print(f"Failed to find {searchstring}")
        offset = count - 1000

def typeread(offset, type):
    #print(f"running typeread @ {offset} as {type}")
    global data
    types = {
        "u8": 1,
        "u16": 2,
        "u32": 4,
        "u64": 8,
    }
    start = offset
    if type in types:
        typelength = types[type]
        #print(f"Data read as {types[type]} @ {offset}")
        end = offset + typelength
        filehex = data[start:end]
        read = int.from_bytes(filehex, byteorder="little")
    elif type == "float":
        #print(f"Data read as float @ {offset}")
        end = offset + 4
        filehex = data[start:end]
        read = struct.unpack('<f', filehex)[0]
    return read  

    try:
        if temp[f"{var_name}typ"] == "float":
            value = temp[var_name]
            return f"{value:.1f}"
        return temp[var_name]
    except KeyError:
        return "missing parameters"

def weapondbread():
    
    #setup

    global offset
    u8 = "u8"
    u16 = "u16"
    u32 = "u32"
    u64 = "u64"
    float = "float"

    offset = 14

    #Initial values
    statset(0, "rateoffire", u16)
    statset(42, "projectilebreakingangle", float)

    #Initloadtype search
    #print("\nINITLOAD_TYPE\n")
    typesearch("Zero and Range", 1684107084, u32, 1)
    
    #Range
    if fileint64 in (1838530271017, 1838530266984):
        statset(145, "zero", float)
        statset(144, "range", float)
    else:
        statset(25, "zero", float)
        statset(24, "range", float)

    #Damage and penetration search
    #print("\nDAMAGE\n")
    if fileint64 in (1698309626211, 1923391143335, 1698309626316):
        offset -= 8
    elif "Maxim9" in filename:
        typesearch("Damage and penetration", (1573516640874,), u64, 1)
    elif "MK23" in filename:
        typesearch("Damage and penetration", (1700302930594,), u64, 1)
    else:
        typesearch("Damage and penetration", (1921650116144,), u64, 1)
    
    statset(32, "damage", u16)
    statset(24, "penetration1", float)
    statset(4, "penetration2", float)

    #UI Grid search  
    #print("\nUI GRID\n")
    # Handgun exception
    if "HDG" in filename or fileint64 in (1923391138966, 395649524046, 1698309626316, 1698309626211, 1923391143335, 1923391202491, 1956585197193):
        offset -= 8
    else:
        typesearch("UI Grid", (1573516640874, 1700302930594, 1297217990701), u64, 1)
    if fileint64 in (1838530271017, 1838530270468, 1838530266890, 205425832666): # A few files had two of the above before the grid.
        offset += 1
        typesearch("UI Grid", (1573516640874, 1700302930594), u64, 1)

    
    if "HDG" in filename or fileint64 in (1698309626211, 1698309626316, 1923391202491, 1956585197193, 1923391143335): # Incosistent values in some files. Some files didnt have the second velocity variable. All Handguns too fml....
        statset(32, "velocity2", float)
    else:
        #statset(28, "velocity1", float)
        statset(32, "velocity2", float) 
    if fileint64 in (1698309626211, 1698309626316): # These had a completely different ui grid order
        statset(8, "ui_noise", float) 
        #statset(4, "ui_accuracy", float) 
        offset += 4
    else:
        offset += 12
        #statset(12, "ui_accuracy", float) 
    #statset(4, "ui_control", float) 
    statset(8, "ui_range", float) 
    statset(4, "ui_rateoffire", float)
    statset(12, "ui_weight", float)
    if fileint64 in (1698309626211, 1698309626316):  # These had a completely different ui grid order
        statset(12, "timetoaim", float)
    else:
        statset(4, "ui_noise", float)
        statset(8, "timetoaim", float)

    #Sway and spread grid search
    #print("\nSWAY & SPREAD GRID\n")
    typesearch("Sway and Spread Grid", (513, 1025), u32, 1)

    statset(5, "burdenfactor", float)
    statset(4, "sway", float)

    #End grid search
    #print("\nEND GRID x3\n")
    if fileint64 in (1923391220806, 1956585197213):
        typesearch("End Grid", 4787326405004230656, u64, 1)
        #statset(47, "recoilpattern", u64)
        offset += 47
    else:
        typesearch("End Grid", 2197962680, u64, 3)
        #statset(15, "recoilpattern", u64)
        offset += 15
    offset += 79
    #statset(79, "soundfile", u64)
    statset(45, "tacticalreloadthreshold", float)
    statset(6, "walkspeedmultiplier", float)
    statset(8, "mobility", float)
    statset(8, "adssensitivity", float)
    statset(21, "soundrange", float)

    #ammotype and attachment search
    #print("\nATTACHMENT GRID\n")
    dicttypesearch("Ammotype", u64)
    #for ammoname, ammodata in db.ammotype.items():
    #    searchname = str(ammodata["id"])
    #    typesearch("Attachment Grid", searchname, u64, 1)   
    statset(0, "ammotype", u64)

def weapondbwrite(preset, newammo, data):
    global stats
    
    #Values from ammo
    newbarrel = newammo["barrels"][preset.barrel]
    stats["ammotype"].new(newammo["id"])
    stats["range"].new(newbarrel["range"])
    stats["zero"].new(newammo["zero"])
    stats["damage"].new(newammo["damage"])
    stats["penetration1"].new(newammo["penetration1"])
    stats["penetration2"].new(newammo["penetration2"])
    #stats["velocity1"].new(newammo["velocity"])
    stats["velocity2"].new(newbarrel["velocity"])
    stats["soundrange"].new(newammo["soundrange"])
    magweight = newammo["magweight"]
    if preset.rateoffire == None:
        del stats["rateoffire"]
        del stats["ui_rateoffire"]
    else:
        stats["rateoffire"].new(preset.rateoffire)
        stats["ui_rateoffire"].new(preset.rateoffire)
    
    #fixed values
    stats["adssensitivity"].new(1)
    stats["walkspeedmultiplier"].new(1)
    stats["tacticalreloadthreshold"].new(0.85)
    stats["sway"].new(1)
    stats["projectilebreakingangle"].new(0.261799)

    #weight
    weight = preset.weight
    if preset.bullpup == True:
        factor = 0.3
    elif preset.onehanded == True:
        factor = 0.5
    else:
        factor = 1
    magweight = magweight*factor
    stats["mobility"].new(1.3-(((weight+magweight)-1)*(0.9/18)))
    stats["timetoaim"].new(0.25+(((magweight+weight)-1)*(0.5/18)))
    if preset.onehanded == True:
        stats["burdenfactor"].new(2-(((weight+magweight)-1)*(1.5/18)))
    else:
        stats["burdenfactor"].new(1.5-(((weight+magweight)-1)*(1.5/18)))
    
    #UI
    stats["ui_weight"].new((magweight+weight)*(100/20))
    stats["ui_noise"].new(stats["soundrange"].newvalue*(1/13))
    stats["ui_range"].new((stats["range"].newvalue-117)*(100/220))

    #Actual Write
    for name in stats:
        #print(name)
        stats[name].write(data)

for filename in os.listdir(FOLDER):
    path = os.path.join(FOLDER, filename)
    found = False
    if filename.endswith('.GR_WeaponDBEntry'):
        stats = {}
        offset = 1
        with open(path, "rb+") as f:
            data = f.read()
            filehex = data[1:9]
            fileint64 = int.from_bytes(filehex, byteorder="little")
            weapondbread()
            for key, value in weaponid.items():
                if int(value) == fileint64:
                    print(f"\npreset found for {filename} - {fileint64}") 
                    preset = key
                    newammo = ammotype[preset.ammotype]
                    weapondbwrite(preset, newammo, f)
                    found = True
                    break
            if found == False:
                print(f"\nSkipping: preset not found for {filename} - {fileint64} - ")      
    else:
        print(f"Skipping: Not WeaponDBEntry {filename}")
print("-----------------------------------------------\n\nFinished\n")