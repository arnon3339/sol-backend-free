import numpy as np
import re
import requests
import io
import base64
from PIL import Image, ImageFilter
from fastapi import HTTPException
from modules.models.utilmodels import MonkeyAtt
import random as rnd

NFT_ATTS = {
        "body": [f"BODY-{i + 1}" for i in range(3)],
        "head": ["JUDGE GAVEL", "COFFEE POT", "TURBAN", "SLOT MACHINE", "TOILET PAPER", "TRAFFIC CONE", "ICE CREAM", "BANANA", "TOILET BOWL", "DOLL", "DUMBBELL", "HEADPHONES", "BALLOONS", "HAIRBAND", "HEADBAND", "SHOPPING BOX", "FOX MASK", "MAID HEADBAND", "FLOWERPOT", "GRADIENT HAT", "CAR WHEEL", "GOLDEN HALO", "3D GLASSES", "BOMB", "UMBRELLA", "MONITOR", "CHAINSAW", "ADVANTURE GLASSES", "MOHAWK HAIR", "THE RING", "FLAME HEAD", "FOOTBALL", "GIRL WIG", "FLOWER", "BTC BAG", "SHOWER CAP", "HEADPIECE", "VALVE", "FRYING PAN", "UFO", "SWORD", "BUTTERFLY", "BASKETBALL NET", "SNEAKERS", "TV", "SALMON", "ATOM", "POOL", "MUSHROOMS", "FLOWER CROWN", "PLUNGER", "PUMPKIN", "WINDMILL", "CHAIR", "LOTUS", "SLIME", "HEAD BUMPS", "PANTY", "HAIR BUNS", "STEAM IRON", "SYRINGES", "BANDANA", "FEDORA HAT", "HELMET", "EMPEROR HAT", "ROUND CAP", "KABUTO HAT", "FEZ", "VIKING HAT", "CHROMECAP", "CONICAL HAT", "YACHT HAT", "ETH KING CROWN", "MINER HELMET", "BEANIE", "ANDROID HAT", "WIND UP CAP", "COWBOY HAT", "TOP HAT", "QUEEN CROWN", "KING CROWN", "ANTLER HAT", "BRAINWAVE SCANNER", "CLOWN HAT", "WATCH CAP", "SQUID HAT", "IVY CAP", "KITTY CAP", "AVIATOR HELMET", "ROMAN HELMET", "SOMBRERO", "IMPOSTER CAP", "HANFU HAT", "WITCH HAT", "BUCKET HAT", "SANTA HAT", "BEANIE HAT", "SUNBONNET", "MORTARBOARD", "BASEBALL CAP", "PEPE HAT", "BRETON CAP", "HEART CAP", "NIGHTCAP", "GARRISON CAP", "PACMAN HAT", "NURSE CAP", "VISOR CAP", "BANANA CAP", "CARTOON CAP", "COMMANDER HAT", "PIRATE HAT", "SUN VISOR"],
        "eyes": [f"EYES-{'0' if i < 9 else ''}{i + 1}" for i in range(17)],
        "mouth": [f"MOUTH-{'0' if i < 9 else ''}{i + 1}" for i in range(14)],
        "clothe": ["WAVY LONG SLEEVE", "SHORT SLEEVE", "TANK TOP", "SPORT TANK TOP", "AUDIO GEAR", "VEST", "CHECKERED CAPE", "SUNGLASSES JACKET", "PLAID SHIRT", "COLLARED SHIRT", "MONK ROBE", "CASUAL OVERALLS", "TOWEL", "CRISSCROSSING STRAPS", "RAINCOAT", "OFFICE", "SUPERSTAR JACKET", "BATTLESUIT", "HIP HOP", "FUR CAPELET", "FARMMER", "EPAULET JACKET", "WEED SHIRT", "DAPPER", "FUTURISTIC SUIT", "SCALED TOP", "APORN", "SPACESUIT", "PLAIN TURTLENECK", "LAB COAT", "HISTORICAL COAT", "GYM", "GOOD GUY OVERALLS", "CUPID", "MASCOT", "AMBASSADOR", "SUSPENDER SHIRT", "BOW DRESS", "HAWAIIAN", "SCARECROW", "SUPERHERO", "FUR COLLARED JACKET", "STREETWEAR", "BIKER JACKET", "COMFY HOODIE", "TIMELESS VEST", "BEAR CLOTHE", "HOMOSAPIEN", "BOMBER JACKET", "ROUGH CUT", "SNEAKERS", "ADVENTURER VEST", "DETECTIVE", "SAILOR UNIFORM", "OFF SHOULDER", "BITCOIN T-SHIRT", "GEOMETRIC SHIRT", "EXPLOSIVE VEST", "CLOWN", "DJ", "PUFFER VEST", "MODERN JACKET", "CHAIN COLLAR", "MEDICAL COLLAR", "TRACKSUIT", "WINTER CLOTHES", "PULLOVER HOODIE", "REGAL EPAULET JACKET", "SWAT VEST", "SUMMER DRESS", "LIFE VEST", "RELAXED PROFESSIONAL", "HEROIC CAPE", "CLERICAL", "SHORT SLEEVE HOODIE", "ETH KIMONO", "SPIRITED CLOTH", "ACADEMIC GOWN", "MARTIAL ARTS GI", "ANTI HERO", "WAVE PRINT TEE", "JIGSAW KIMONO", "FIELD PACK", "KNOT CROP TOP", "BABY APRON", "WRESTLER", "AMMUNITION BELTS", "FESTIVAL", "QUILTED VEST", "TURTLE ARMOR", "BELL CHARM", "DAY TRIPPER", "ROMAN TUNIC", "STAFF UNIFORM", "SPYDER SHIRT", "CAMOUFLAGE SUIT", "BLOOMERS PANTS", "PAJAMAS", "FORMAL TUNIC", "EGYPTIAN COLLAR", "SHOPPING BAG"],
        "eyesacc": ["BANDAGE", "STONE EYE", "SCOUTER", "HIGH TECH MONOCLE", "PIRATE EYEPATCH", "HEADBAND", "HAND", "WATCH", "SMARTPHONE", "DARTS", "TELESCOPE", "CYBERNETIC EYEPIECE", "MICROSCOPE", "SCAR", "CLASSIC MONOCLE", "MAGNIFYING GLASS", "LEAF", "VR HEADSET", "3D GLASSES", "SPIRAL GLASSES", "NERD GLASSES", "RECTANGULAR SUNGLASSES", "LASER BEAM", "EYE MASK", "STYLISH SUNGLASSES", "DECORATIVE MASK", "STEAMPUNK GOGGLES", "LEMON SLICES", "SLEEP MASK", "STAR SUNGLASSES", "INFINITY SUNGLASSES", "TRAFFIC LIGHT", "MIRRORED SUNGLASSES", "FULL MOON GLASSES", "SKI GOGGLES", "TOY SUNGLASSES", "BROKEN GLASSES", "CLASSIC GLASSES", "PROTECTIVE GOGGLES", "SHOOTING SAFETY GLASSES", "TINY GLASSES", "PAPER GLASSES", "FUNKY GLASSES", "FANCY GLASSES", "ILLUMINATI GLASSES", "HEART GLASSES", "HIGH TECH VISOR", "GEOMETRIC SUNGLASSES", "PLAYFUL DISGUISE", "FASHION GLASSES", "EYE SHIELDS", "MOSAIC GLASSES", "VINTAGE SUNGLASSES", "SHUTTER GLASSES"],
        "mouthacc": ["BUBBLE GUM", "NOODLE", "USB", "PACIFIER", "CIGAR", "CAPSULE", "LOLLIPOP", "BIBS PACIFIER", "BUBBLE TEA", "SMOKING PIPE", "HAMBURGER", "MICROPHONE", "PARTY BLOWER", "TRUMPET", "COMEDIAN DRINK", "LOVE LETTER", "COFFEE", "BUBBLE", "BANANA", "VOMIT", "FOOD BOWL", "FACE MASK", "KING CHESS PIECE", "KNIFE", "ICE CREAM CONE", "BAMBOO STICK", "COCONUT", "CENTIPEDES", "ENEMA", "BACON", "FORKS", "BAUBLES", "FIRE", "BANDANA", "MUZZLE", "PENCIL", "BIRTHDAY CAKE", "LEGENDARY FRUIT", "TOOTHBRUSH", "TOOTHPASTES", "MOUSE", "BLUSH ON", "RAZOR", "BOOK", "LABTOP", "CARDS", "INHALER", "HANDKERCHIEF", "BULB SYRINGE", "WHISTLE", "LIPSTICK"] 
        }

def get_att_list(the_hex, att_name):
    global NFT_ATTS
    ref_att = NFT_ATTS[att_name]
    is_zero = True
    the_ints = []
    for a_hex in the_hex:
        a_int = int(a_hex, 16)
        if a_int > 0:
            is_zero = False
        the_ints.append(a_int)
    if is_zero:
        return NFT_ATTS[att_name]
    bins_string = ""
    for a_int in the_ints:
        a_bins_string = bin(a_int).split('b')[-1]
        bins_string = bins_string + "0"*(4 - len(a_bins_string)) + a_bins_string
    bin_array = np.array(list("0"*(len(ref_att) - len(bins_string)) + bins_string))
    bin_array = bin_array[-len(ref_att):]
    print(bin_array)
    att_indicies = np.where(bin_array == "1")[0]
    return [ref_att[i] for i in att_indicies]

def get_found_set(search_words, att_name):
    search_list = get_search_list(search_words)
    the_set = set()
    for att_i, att in enumerate(NFT_ATTS[att_name]):
        for search in search_list:
            if search in att:
                the_set.add(att)
    return the_set

def get_search_list(org_words):
    word = []
    word_list = []
    pthesis = ""
    pthesis_start_ref = ['[', '(', '{', '<']
    pthesis_end_ref= [']', ')', '}', '>']
    pstart_index = -1
    print(org_words)
    for c_i, c in enumerate(org_words):
        if c in pthesis_start_ref and pstart_index == -1:
            pstart_index = pthesis_start_ref.index(c)
            word = [c_i]
        elif pstart_index != -1 and c == pthesis_end_ref[pstart_index]:
            pstart_index = -1
            word.append(c_i)
            word_list.append(word)
    group_rem_list = []
    if word_list and word_list[0][0] != 0:
        group_rem_list += [org_words[0:word_list[0][0]]]
    if len(word_list) > 1:
        for w_i in range(len(word_list) - 1):
            group_rem_list += [org_words[word_list[w_i][1] + 1: word_list[w_i + 1][0]]]
    if word_list and word_list[-1][-1] + 1 != len(word_list):
        group_rem_list += [org_words[word_list[-1][-1] + 1:len(org_words)]]
    rem_words = [re.sub(r'\s+', ' ', w) for w in group_rem_list]
    new_words = [re.sub(r'\s+', ' ', org_words[begin + 1: end]) for [begin, end] in word_list]
    all_space_search_list = new_words + rem_words if word_list else [org_words]
    all_search_list = []
    for w in all_space_search_list:
        re_split_w = re.split(r'\s+', w)
        if re_split_w[0] == '' and re_split_w[-1] == '':
            all_search_list.append(' '.join(re_split_w[1:-1]))
        elif re_split_w[0] == '':
            all_search_list.append(' '.join(re_split_w[1:]))
        elif re_split_w[-1] == '':
            all_search_list.append(' '.join(re_split_w[:-1]))
        else:
            all_search_list.append(' '.join(re_split_w))

    all_ref_words = []
    for ref_words in NFT_ATTS.values():
        all_ref_words += ref_words
    new_all_search_list = []
    for w in all_search_list:
        if w in all_ref_words:
            new_all_search_list.append(w)
        else:
            new_all_search_list += re.split(r'\s+', w)
    return [w for w in new_all_search_list if w != '']

def img2b64blur(img):
    base64_image = base64.b64encode(open('./images/lq/monkey.jpg','rb').read())
    image_data = base64.b64decode(base64_image)

    image = Image.open(io.BytesIO(image_data))

    blurred_image = image.filter(ImageFilter.BLUR)

    output = io.BytesIO()
    blurred_image.save(output, format='JPEG')    
    output.seek(0)

    blurred_base64 = base64.b64encode(output.read()).decode('utf-8')
    return blurred_base64
    #raise HTTPException(status_code=500, detail="Server error!")
