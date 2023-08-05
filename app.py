import pandas as pd
import streamlit as st
from st_aggrid import AgGrid, DataReturnMode, GridOptionsBuilder, GridUpdateMode, JsCode
import time

from pdex_json import create_df, stat_calc, cpms_calc
st.set_page_config(layout="wide")
@st.cache_data()
def DfBuild():
    return create_df("./data/pdex_go.json")


def cell_mon(x):
    return JsCode("""function (params) {
    const selectedCountry = params.data.%s;
    return {
      component: 'agRichSelectCellEditor',
      params: {
        values: selectedCountry,
      },
      popup: true,
    };
}
    """ % (x))

dex_df = DfBuild()
data = pd.read_csv("./data/poke_genie_export 3.csv", index_col = 0)
data['atk_total'] = data.apply(lambda r: dex_df.loc[
    dex_df.dexNr.astype('int64')==int(r['Pokemon Number']),'at'].iat[0], axis=1)
data['lvl_m'] = data['Level Min'].apply(lambda x: cpms_calc[x])
# data['atk_calc'] = data.apply(lambda r: stat_calc(r['Atk IV']+dex_df.loc[
#     dex_df.dexNr.astype('int64')==int(r['Pokemon Number']), 'at'].iat[0],r['Level Min']), axis=1)
# data['def_calc'] = data.apply(lambda r: stat_calc(r['Def IV']+dex_df.loc[
#     dex_df.dexNr.astype('int64')==int(r['Pokemon Number']), 'de'].iat[0],r['Level Min']), axis=1)
# data['hp_calc'] = data.apply(lambda r: stat_calc(r['HP']+dex_df.loc[
#     dex_df.dexNr.astype('int64')==int(r['Pokemon Number']), 'hp'].iat[0],r['Level Min']), axis=1)
data[['c_at','c_de','c_hp']] = data.apply(lambda r: dex_df.loc[dex_df.dexNr.astype('int64')==int(r['Pokemon Number']), ['at','de','hp']].iloc[[0]].squeeze(axis=0), axis=1)
data.rename(columns = {'Atk IV':'atk_iv','Def IV':'def_iv'},inplace=True)
data = data.eval('cp_calc = ((atk_iv + c_at) * (def_iv + c_de)**0.5 * (HP + c_hp)**0.5 * lvl_m**2)/10')
data = data.loc[:, ['Name','Pokemon Number','CP','atk_iv','c_at','def_iv','c_de','HP','c_hp','Level Min','lvl_m','cp_calc']]
dex_df['fast_move1'] = dex_df['fast_move'].str.get(0)
dex_df['charge_move1'] = dex_df['charge_move'].str.get(0)
grid_options = GridOptionsBuilder.from_dataframe(data)
# grid_options.configure_column(field = 'names', headerName = 'Name')
# grid_options.configure_column('fast_move1', headerName = 'Fast Move', cellEditor='agRichSelectCellEditor',
#                               cellEditorSelector=cell_mon('fast_move'),
#                               cellEditorPopup=True,
#                               cellEditorParams= {
#                                   'cellHeight': 20,
#                                   'searchDebounceDelay': 50
#                               }, editable=True)
# grid_options.configure_column('charge_move1', headerName = 'Charged Move', cellEditor='agRichSelectCellEditor',
#                               cellEditorSelector=cell_mon('charge_move'),
#                               cellEditorPopup=True,
#                               cellEditorParams= {
#                                   'cellHeight': 20,
#                                   'searchDebounceDelay': 50
#                               }, editable=True)
# col_def = [{'field':n,'hide':True} for n in ['fast_move','charge_move','formId']]
# grid_options.configure_columns(['fast_move','charge_move'], hide=True)
# grid_options.configure_columns(['type_1','type_2'], width=100)
# grid_options.configure_column('charge_move',hide=True)

go = grid_options.build()
AgGrid(data, gridOptions = go, allow_unsafe_jscode = True)
