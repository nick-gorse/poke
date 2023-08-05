import numpy as np
import json
import pandas as pd


cpms = [0.0939999967813491, 0.135137430784308, 0.166397869586944, 0.192650914456886, 0.215732470154762, 0.236572655026622, 0.255720049142837, 0.273530381100769, 0.290249884128570, 0.306057381335773, 0.321087598800659, 0.335445032295077, 0.349212676286697, 0.362457748778790, 0.375235587358474, 0.387592411085168, 0.399567276239395, 0.411193549517250, 0.422500014305114, 0.432926413410414, 0.443107545375824, 0.453059953871985, 0.462798386812210, 0.472336077786704, 0.481684952974319, 0.490855810259008, 0.499858438968658, 0.508701756943992, 0.517393946647644, 0.525942508771329, 0.534354329109191, 0.542635762230353, 0.550792694091796, 0.558830599438087, 0.566754519939422, 0.574569148039264, 0.582278907299041, 0.589887911977272, 0.597400009632110, 0.604823657502073, 0.612157285213470, 0.619404110566050, 0.626567125320434, 0.633649181622743, 0.640652954578399, 0.647580963301656, 0.654435634613037, 0.661219263506722, 0.667934000492096, 0.674581899290818, 0.681164920330047, 0.687684905887771, 0.694143652915954, 0.700542893277978, 0.706884205341339, 0.713169102333341, 0.719399094581604, 0.725575616972598, 0.731700003147125, 0.734741011137376, 0.737769484519958, 0.740785574597326, 0.743789434432983, 0.746781208702482, 0.749761044979095, 0.752729105305821, 0.755685508251190, 0.758630366519684, 0.761563837528228, 0.764486065255226, 0.767397165298461, 0.770297273971590, 0.773186504840850, 0.776064945942412, 0.778932750225067, 0.781790064808426, 0.784636974334716, 0.787473583646825, 0.790300011634826, 0.792803950958807, 0.795300006866455, 0.797803921486970, 0.800300002098083, 0.802803892322847, 0.805299997329711, 0.807803863460723, 0.810299992561340, 0.812803834895026, 0.815299987792968, 0.817803806620319, 0.820299983024597, 0.822803778631297, 0.825299978256225, 0.827803750922782, 0.830299973487854, 0.832803753381377, 0.835300028324127, 0.837803755931569, 0.840300023555755, 0.842803729034748, 0.845300018787384, 0.847803702398935, 0.850300014019012, 0.852803676019539, 0.855300009250640, 0.857803649892077, 0.860300004482269, 0.862803624012168, 0.865299999713897]
cpms_calc = {((level/2)+1): cpms[level] for level in range(len(cpms))}


def stat_calc(_x, _y):
    return _x * cpms_calc[_y]


def sec_t(x):
    return f"{x['names']['English']}" if x else ""

def move_li(x):
    li = [{k.removesuffix("_FAST").replace("_"," ").title():x[k]} for k in x]
    if not li:
        return [{}]
    return li


def stats_dic(x):
    try:
        if not x:
            return {}
        return {'at': x['attack'], 'de': x['defense'], 'hp': x['stamina']}
    except TypeError as err:
        print(x)
        raise err


def poke_name(name, form, type):
    if name.title() == form.replace("_", " ").title():
        return name.title(), None
    form_li = [w.title() for w in form.split("_")]
    name_f = form_li.pop(0)
    name_ret = ""
    form_ret = None
    if form_ret1 := [w for w in form_li if w in ['Galarian','Alola','Midnight','Midday','Sunny','Baile','Hisuian']]:
        name_ret = " (" + " ".join(form_li) + ")" if name_f == name.title() else name_ret
        form_ret = form_ret1[0]
    return name.title()+name_ret, form_ret


def get_poke(pokx):
    # if not pokx:
    na, form_o = poke_name(pokx['names']['English'], pokx['formId'], pokx['primaryType']['names']['English'])
    _ = {'dexNr': pokx['dexNr'], 'names': na, 'form':form_o, 'type_1': pokx['primaryType']['names']['English'],
         'type_2': sec_t(pokx['secondaryType']), 'fast_move': move_li(pokx['quickMoves']),
         'charge_move': move_li(pokx['cinematicMoves']),'formId': pokx['formId']} | stats_dic(pokx['stats'])
    return _


def create_df(x):
    with open(x, "r") as f:
        data = json.loads(f.read())

    poke = []
    for pok in data:

        poke.append(get_poke(pok))
        if not pok['regionForms']:
            continue
        try:
            for reg_pok in pok['regionForms'].values():
                poke.append(get_poke(reg_pok))
        except (KeyError,TypeError) as err:
            print(pok['regionForms'])
            raise err


    return pd.DataFrame.from_records(poke)


__all__ = [create_df, stat_calc, cpms_calc]

if __name__ == '__main__':
    df = create_df("./data/pdex_go.json")
    # print(df)
