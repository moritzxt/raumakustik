import streamlit as st
import base64

# Page to display and download user guide
st.set_page_config(page_title= 'User guide', layout='wide')
st.subheader('PDF user guide')

# Open user guide in streamlit
with open("pages/user_guide.pdf", "rb") as f:
    pdf_bytes = f.read()

    # Convert the PDF bytes to base64
    pdf_base64 = base64.b64encode(pdf_bytes).decode('utf-8')

    # Embed the PDF in Streamlit using an HTML tag
    st.markdown(f'<embed src="data:application/pdf;base64,{pdf_base64}" width="700" height="700" type="application/pdf">', unsafe_allow_html=True)