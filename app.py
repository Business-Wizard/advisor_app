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
    f""" 
    <style>
    #.reportview-container .main .block-container{{
        padding-top: {1.3}rem;
        padding-right: {2.5}rem;
        padding-left: {3.4}rem;
        padding-bottom: {3.4}rem;
    }} 
    </style> 
    """,
    unsafe_allow_html=True,
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

from src.tools import lists as l0
from src.tools import widgets as w0



class Credentials(object):

    def __init__(self, today_stamp):
        self.today_stamp = today_stamp
        self.authUser = False

    def check_password(self):
        try:
            access_dict = st.secrets["passwords"]
            nameUser = list(access_dict.keys())[0]
            passWord = list(access_dict.values())[0]
            if nameUser == "admin" and passWord == "lord_gordon":
                self.authUser = True
                return self.authUser
        except:
            pass

        def password_entered():
            st.session_state.username = list(st.secrets["passwords"].keys())[0]
            st.session_state.password = list(st.secrets["passwords"].values())[0]
            condition_A = st.session_state["username"] in st.secrets["passwords"]
            condition_B = (st.session_state["password"]== st.secrets["passwords"][st.session_state["username"]])
            if condition_A == True and condition_B == True:
                st.session_state["password_correct"] = True
                del st.session_state["password"]
                del st.session_state["username"]
            else:
                st.session_state["password_correct"] = False

        if "password_correct" not in st.session_state:
            st.title(f" ~ 4M ~  \n\- Today Date: [{self.today_stamp}]\n")
            st.write(f"{'__'*25} \n {'__'*25}")
            with st.form("login_credentials"):
                nameUser = st.text_input("Username", key="username")
                wordPass = st.text_input("Password", key="password")
                st.form_submit_button("Login", help="click to submit login credentials", on_click=password_entered, )
                self.authUser = False
                return self.authUser
        elif not st.session_state["password_correct"]:
            st.title(f" ~ 4M ~  \n\ - Today Date: [{self.today_stamp}]\n")
            st.write(f"{'__'*25} \n {'__'*25}")
            with st.form("login_credentials"):
                nameUser = st.text_input("Username", key="username")
                wordPass = st.text_input("Password", key="password")
                st.form_submit_button("Login", help="click to submit login credentials", on_click=password_entered, )
                st.error("😕 User not known or password incorrect")
                self.authUser = False
                return self.authUser
        else:
            self.authUser = True
            return self.authUser


class Home(object):

    def __init__(self, today_stamp):
        self.today_stamp = str(today_stamp)[:10]        
        st.header("𝄖𝄗𝄘𝄙𝄚 · Home · ")


    def run_home(self):
        tab1, tab2 = st.tabs(["𝄖𝄗𝄘𝄙𝄚 Disclosure 𝄚𝄙𝄘𝄗𝄖", "𝄖𝄗𝄘𝄙𝄚 MISC 𝄚𝄙𝄘𝄗𝄖"])
        with tab1:
            w0.home_disclosure()


def page_login(today_stamp):
    authUser = Credentials(today_stamp).check_password()
    return authUser


if __name__ == '__main__':    
    st.title("𝄗"*24)
    st.title(f"✪ 𝄚𝄚𝄚𝄚𝄚 【 · Invest · 4m · 】 𝄚𝄚𝄚𝄚𝄚 ✪")
    st.title("𝄗"*24)
    
    today_stamp = str(datetime.now())[:10]

    if page_login(today_stamp) == True:
        Home(today_stamp).run_home()

st.markdown("<a href='#linkto_top'>Link to top</a>", unsafe_allow_html=True)
