from dotenv import load_dotenv
import sqlite3
import google.generativeai as genai
import os
import streamlit as st
load_dotenv()
os.getenv("GOOGLE_API_KEY")
#genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
genai.configure(api_key=os.environ['GOOGLE_API_KEY'])

def get_gemini_res(que,prompt):
    model = genai.GenerativeModel('gemini-pro')
    response = model.generate_content([prompt[0],que])
    return response.text

def read_sql(sql,db):
    conn = sqlite3.connect(db)
    cur = conn.cursor()
    cur.execute(sql)
    rows=cur.fetchall()
    conn.commit() 
    conn.close()
    for row in rows:
        print(row)
    return rows

prompt=[
    """
    You are an expert in converting English questions to SQL query!
    The SQL database has the name STUDENT and has the following columns - NAME, CLASS, 
    SECTION,Marks \n\nFor example,\nExample 1 - How many entries of records are present?, 
    the SQL command will be something like this SELECT COUNT(*) FROM STUDENT ;
    \nExample 2 - Tell me all the students studying in Data Science class?, 
    the SQL command will be something like this SELECT * FROM STUDENT 
    where CLASS="Data Science"; 
    also the sql code should not have ``` in beginning or end and sql word in output

    """


]

st.set_page_config(page_title="I can Retrieve Any SQL query")
st.header("Gemini App To Retrieve SQL Data")

que=st.text_input("Input: ",key="input")

submit=st.button("Ask the question")

# if submit is clicked
if submit:
    response=get_gemini_res(que,prompt)
    print(response)
    response=read_sql(response,"student.db")
    st.subheader("The REsponse is")
    for row in response:
        print(row)
        st.header(row)