import streamlit as st
import pandas as pd
import base64
from numpy import abs


filename = "full_list_v2.csv"
df = pd.read_csv(filename, dtype={'status': int})

page_volume = 50
pages_count = df.shape[0] // page_volume + 1

if 'page_num' not in st.session_state:
    st.session_state.page_num = 1

if 'prev_status' not in st.session_state:
    st.session_state.prev_status = None

st.session_state.not_display_status = []

image_liked = "src/image_liked.jpg"
image_disliked = "src/image_disliked.jpg"
image = "src/image.jpg"
icons_folder = "src/icons/"

# Header
st.set_page_config(page_title="Selector", layout="wide")
st.header("PS games selector")


def update_status(status, i):
    df.loc[i,'status'] += status
    if df.loc[i,'status'] != 0:
        df.loc[i,'status'] = df.loc[i,'status'] / abs(df.loc[i,'status'])
    df.to_csv(filename, index=False)


def display_local_image(title, URL, service=False):

    if not service:
        path = icons_folder + f"{(title).replace(' ', '').replace('(', '').replace(')', '').lower()}.jpg"
    else:
        path = title

    file = base64.b64encode(open(path, 'rb').read()).decode()

    if not service:

        st.write(f"""<div style="display: flex;
                                justify-content: center;
                                align-items: center;">
                        <a href="{URL}">
                            <img src="data:image/jpeg;base64,{file}" style="width: {192}px;
                                                                            height: {192}px;
                                                                            object-fit: contain;">
                        </a>
                    </div>""",
                unsafe_allow_html=True)
    else:
        st.write(f"""<div style="display: flex;
                                justify-content: center;
                                align-items: center;">
                            <img src="data:image/jpeg;base64,{file}" style="width: {192}px;
                                                                            height: {192}px;
                                                                            object-fit: contain;">
                    </div>""",
                unsafe_allow_html=True)


def display_cloud_image(icon_URL, URL):
    st.write(f"""<div style="display: flex;
                                      justify-content: center;
                                      align-items: center;">
                    <a href="{URL}">
                        <img src="{icon_URL}" style="width: {192}px;
                                                     height: {192}px;
                                                     object-fit: contain;">
                    </a>
                </div>""",
            unsafe_allow_html=True,
    )


st.sidebar.title("Page Selector")
for page in range(1, pages_count + 1):
    if st.sidebar.button(f"Page {page}"):
        st.session_state.page_num = page


col1, col2, col3 = st.columns([10, 10, 10])

with col1:
    show_liked = st.checkbox("liked", value=True)
    if not show_liked:
        st.session_state.not_display_status.append(1)
with col2:
    show_unknown = st.checkbox("unknown", value=True)
    if not show_unknown:
        st.session_state.not_display_status.append(0)
with col3:
    show_disliked = st.checkbox("disliked", value=False)
    if not show_disliked:
        st.session_state.not_display_status.append(-1)


with st.container():

    st.header(f"Current page {st.session_state.page_num}")
    
    for i in range((st.session_state.page_num - 1) * page_volume, 
                   min(st.session_state.page_num * page_volume,
                       df.shape[0])):
        
        display = True
        if df.status[i] in st.session_state.not_display_status:
            display = False

        try:
            if display:
                cola, colb, colc, cold, cole = st.columns([10, 6, 10, 6, 10])

                with cola:
                    
                    if df.status[i] == 1:
                        try:
                            display_local_image(df.title[i], df.psd_URL[i])
                        except Exception as e:  
                            display_cloud_image(df.icon_URL[i], df.psd_URL[i])

                        st.markdown(f"<p style='text-align: center;'>{df.platform[i]} - {df.title[i]}<br>{df.price[i]}</p>", unsafe_allow_html=True)
                    
                    else:
                        display_local_image(image_liked, df.psd_URL[i], service=True)

                with colb:

                    st.markdown("""<style>
                                    .center-container {
                                        justify-content: center;
                                        align-items: center;
                                        height: 5vh; 
                                    }
                                    </style>""",
                                    unsafe_allow_html=True)

                    st.write("<div class='center-container'>", unsafe_allow_html=True)

                    st.button(f"like_{i}", on_click=update_status, args=[1, i])

                    st.write("</div>", unsafe_allow_html=True)
                    
                with colc:

                    if df.status[i] == 0:
                        try:
                            display_local_image(df.title[i], df.psd_URL[i])
                        except Exception as e:  
                            display_cloud_image(df.icon_URL[i], df.psd_URL[i])
                        st.markdown(f"<p style='text-align: center;'>{df.platform[i]} - {df.title[i]}<br>{df.price[i]}</p>", unsafe_allow_html=True)
                    
                    else:
                        display_local_image(image, df.psd_URL[i], service=True)
                        st.markdown(f"<p style='text-align: center;color: rgba(0, 0, 0, 0);'>{df.title[i]}</p>", unsafe_allow_html=True)

                with cold:
                    st.markdown("""<style>
                                    .center-container {
                                        justify-content: center;
                                        align-items: center;
                                        height: 5vh; 
                                    }
                                    </style>""",
                                    unsafe_allow_html=True)

                    st.write("<div class='center-container'>", unsafe_allow_html=True)

                    st.button(f"dislike_{i}", on_click=update_status, args=[-1, i])

                    st.write("</div>", unsafe_allow_html=True)

                with cole:

                    if df.status[i] == -1:
                        try:
                            display_local_image(df.title[i], df.psd_URL[i])
                        except Exception as e:
                            display_cloud_image(df.icon_URL[i], df.psd_URL[i])

                        st.markdown(f"<p style='text-align: center;'>{df.platform[i]} - {df.title[i]}<br>{df.price[i]}</p>", unsafe_allow_html=True)

                    else:
                        display_local_image(image_disliked, df.psd_URL[i], service=True)
        except Exception:
            pass

    st.header(f"Current page {st.session_state.page_num}")


if st.session_state.prev_status != df.status.value_counts().to_string():
    print('-------')
    print(f'progress: {round(df.status[df.status != 0].shape[0] / df.status.shape[0]* 100, 2) }%')
    print(df.status.value_counts().sort_index().to_string())
    st.session_state.prev_status = df.status.value_counts().to_string()