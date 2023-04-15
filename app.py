import streamlit as st

st.set_page_config(
    page_title="Advisor App",
    page_icon="chart_with_upwards_trend",
    layout="wide",
    initial_sidebar_state="expanded",    
    menu_items={
        "About": "# · Advisor App · Created By: GDP · ",
    },
)


st.markdown(
    """
    <style>
    MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    footer:after {
        content:" · Invest · 4M · "; 
        visibility: visible;
        display: block;
        position: 'fixed';
        #background-color: red;
        padding: 10px;
        top: 5px;
    }
    </style>
    """,
    unsafe_allow_html=True,
)
st.markdown("<div id='linkto_top'></div>", unsafe_allow_html=True)

from datetime import datetime
import warnings
warnings.filterwarnings("ignore")

from src.tools import widgets as w0



class Home(object):

    def __init__(self, today_stamp):
        self.today_stamp = str(today_stamp)[:10]        
        st.header(" 𝄖𝄖𝄖𝄗𝄗𝄗𝄘𝄘𝄘𝄙𝄙𝄙𝄚𝄚𝄚 · Home · 𝄚𝄚𝄚𝄙𝄙𝄙𝄘𝄘𝄘𝄗𝄗𝄗𝄖𝄖𝄖 ")


    def run_home(self):
        tab1, tab2, tab3, tab4 = st.tabs(
            [
                "𝄖𝄗𝄘𝄙𝄚 Summary In Brief 𝄚𝄙𝄘𝄗𝄖", 
                "𝄖𝄗𝄘𝄙𝄚 Navigation 𝄚𝄙𝄘𝄗𝄖", 
                "𝄖𝄗𝄘𝄙𝄚 Section Index 𝄚𝄙𝄘𝄗𝄖", 
                "𝄖𝄗𝄘𝄙𝄚 Disclosure 𝄚𝄙𝄘𝄗𝄖",                 
                ])
        with tab1:
            w0.home_summary_in_brief()
        with tab2:
            w0.home_navigation()
        with tab3:
            w0.home_section_index()
        with tab4:
            w0.home_focal_concepts()           
                                    



if __name__ == '__main__':    
    # st.title("𝄗"*28)
    st.title("✪ 𝄚𝄚𝄚𝄚𝄚𝄚𝄚 【 · Invest · 4m · 】 𝄚𝄚𝄚𝄚𝄚𝄚𝄚 ✪")
    st.title("𝄗"*28)

    entry = True
    if entry:
        Home(str(datetime.now())[:10]).run_home()

# st.markdown("<a href='#linkto_top'>Link to top</a>", unsafe_allow_html=True)
