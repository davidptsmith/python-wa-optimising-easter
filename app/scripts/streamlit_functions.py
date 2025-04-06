# Import base streamlit dependency
import streamlit as st


def setup_navigation_side():
    st.set_page_config(
        page_title="Optimiser Easter"
    )

    with st.sidebar:
            ## Hack around to make the icon bunny bigger
            md = '''
<style>
  div[data-testid="stSidebarHeader"] > img, div[data-testid="collapsedControl"] > img {
      height: 15rem;
      width: auto;
  }
  
  div[data-testid="stSidebarHeader"], div[data-testid="stSidebarHeader"] > *,
  div[data-testid="collapsedControl"], div[data-testid="collapsedControl"] > * {
      display: flex;
      align-items: center;
  }
</style>
'''
            st.markdown(md, unsafe_allow_html=True)
            ## Gets the bunny image to display as a logo
            logo_url = "https://static.vecteezy.com/system/resources/previews/043/101/816/non_2x/easter-rabbit-cartoon-clip-art-free-png.png"
            st.logo(logo_url, size="large")


    ## sidebar data 
    sidebar_title = "Optimser Easter"
    st.sidebar.markdown(f"<div><h1 style='display:inline-block'>{sidebar_title}</h1></div>", unsafe_allow_html=True)
    
    sidebar_subheading = "Creating the Best Egg Hunt"
    st.sidebar.markdown(sidebar_subheading)

    sidebar_body = '''
  Optimising Easter with mixed integer linear programming. 

  This application has been designed to assist the Easter Bunny with designing the perfect Easter egg hunt.

    ---
    <p style="font-size:14px; text-align: center;">
       Optimising Easter
    </p>

    </br>
    </br>


    '''
    st.sidebar.markdown(sidebar_body,unsafe_allow_html=True)

def setup_footer():
    sidebar_body = '''

    </br>

    ---
    
    <p style=font-size:14px; text-align:center;">
    Optimser Easter - Easter Bunny - Best Egg Hunt
    </p>

    '''

    st.markdown(sidebar_body,unsafe_allow_html=True)