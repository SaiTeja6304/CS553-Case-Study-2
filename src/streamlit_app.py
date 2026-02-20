import streamlit as st
import response as rp
from db import create_connection, create_table, insert_log, close_connection

st.set_page_config(page_title="VLM Chat", page_icon=":robot_face:", layout="wide")
st.title("VLM Chat")

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "uploaded_image" not in st.session_state:
    st.session_state.uploaded_image = None
if "db_connection" not in st.session_state:
    conn, cursor = create_connection()
    create_table(conn, cursor)
    st.session_state.db_conn = conn
    st.session_state.db_cursor = cursor

st.chat_message("assistant").markdown("I am a helpful chatbot to answer your questions about the uploaded image")
    
for role, msg in st.session_state.chat_history:
    st.chat_message(role).markdown(msg)

with st.sidebar:
    with st.expander("Model Selection"):
        use_local_model = st.checkbox("Use local model", value=False)
        st.info("Selecting local model will run the model locally (responses may take longer to generate).", icon="ℹ️")
        


image = st.file_uploader("Upload an image", type=["png", "jpg", "jpeg"])
st.session_state.uploaded_image = image
if image is not None:
    st.image(image)
query = st.chat_input("Ask a question about the image")

if query:
    if st.session_state.uploaded_image is None:
        st.error("Please upload an image")
    else:
        st.chat_message("user").markdown(query)

        with st.spinner("Processing..."):
            # Convert chat history to a concatenated string 
            chat_history_str = "\n".join([f"{role}: {msg}" for role, msg in st.session_state.chat_history])
            
            if use_local_model:
                response = rp.generate_response(image, query, True, chat_history_str)
            else:
                response = rp.generate_response(image, query, False, chat_history_str)
        
        st.chat_message("assistant").markdown(response)

        # Add to history after successful response
        st.session_state.chat_history.append(("user", query))
        st.session_state.chat_history.append(("assistant", response))
        
        try:
            insert_log(st.session_state.db_conn, 
            st.session_state.db_cursor, 
            "hf-local" if use_local_model else "hf-inference", 
            query, response, chat_history_str)
        except Exception as e:
            st.error(f"Failed to insert log: {str(e)}")

