import streamlit as st
from supabase_connection.connection import SUPABASECONNECTION
from time import sleep
from streamlit_option_menu import option_menu

# Name the app "Job Analysis" and set the name in the tab
st.set_page_config(page_title='Job Analysis')
st.title('Job Analysis')
st.write('This app is used to analyze job data from the US Bureau of Labor Statistics.')
st.write('The data is stored in a Supabase database.')
# URL and key for your Supabase connection

# Pass the st module to the class when creating an instance
conn = st.experimental_connection("supabase", type=SUPABASECONNECTION, st_module=st)

# Add a selectbox to the sidebar to choose the page
if "selected" not in st.session_state:
    st.session_state.selected = "View Data"

if "display_format" not in st.session_state:
    st.session_state.display_format = "Table"

# Add a selectbox to the sidebar to choose the page
with st.sidebar:
    selected = option_menu("Main Menu", ["View Data", 'Insert Data', 'Update Data'], 
        icons=['search', 'input-cursor','arrow-counterclockwise'], menu_icon="bar-chart", default_index=1)
# Update the session state when the selection changes

if st.session_state.selected != selected:
    st.session_state.selected = selected

# Check which page is selected
if st.session_state.selected == "View Data":
    st.title('View Data')
    st.write('This page displays the data from the "salaries" table.')
    fields=st.multiselect('Select Fields', ['id', 'age', 'income', 'workclass', 'education', 'education_num', 'marital_status', 'occupation', 'relationship', 'race', 'sex', 'capital_gain', 'capital_loss', 'hours_per_week', 'native_country', 'fnlwgt']
, default=['id', 'age', 'income', 'workclass', 'education', 'occupation', 'race', 'sex']
)
    refresh=st.button('Refresh Data')
    if refresh:
        st.experimental_rerun()
    data = conn.select(table='salaries', function=fields)
    data = data.data
    # Display the dataframe
    display_format = st.selectbox('Select Display Format', ['Table', 'DataFrame', 'JSON'], key="display_format")

    if st.session_state.display_format != display_format:
        st.session_state.display_format = display_format

    if st.session_state.display_format == 'Table':
        # Display the data as a table
        st.table(data)

    elif st.session_state.display_format == 'DataFrame':
        # Display the data as a DataFrame
        st.dataframe(data)

    elif st.session_state.display_format == 'JSON':
        # Display the data as JSON
        st.json(data)

elif st.session_state.selected == "Insert Data":
    st.title('Insert Data')
    st.write('This page inserts data into the "salaries" table.')
    #ask for fields to insert
    age=st.number_input('Enter Age', min_value=0, max_value=110, value=0, step=1)
    income=st.selectbox('Enter Income', ['<=50K', '>50K'])
    workclass=st.text_input('Enter Workclass')
    education=st.text_input('Enter Education')
    education_num=st.number_input('Enter Education Number', min_value=0, max_value=100, value=0, step=1)
    marital_status=st.text_input('Enter Marital Status')
    occupation=st.text_input('Enter Occupation')
    relationship=st.text_input('Enter Relationship')
    race=st.text_input("Enter Race")
    sex=st.selectbox("Enter Gender", ['Male','Female'])
    capital_gain=st.number_input('Enter Capital Gain', min_value=0, max_value=1000000, value=0, step=1)
    capital_loss=st.number_input('Enter Capital Loss', min_value=0, max_value=1000000, value=0, step=1)
    hours_per_week=st.number_input('Enter Hours Per Week', min_value=0, max_value=100, value=0, step=1)
    native_country=st.text_input('Enter Native Country', value="")
    fnlwgt=st.number_input('Enter Final Weight', min_value=0, max_value=1000000, value=0, step=1)
    #update data
    insert=st.button('Insert Data')
    if insert:
        result=conn.insert(table='salaries', data={
            'age':age,
            'income':income,
            'workclass':workclass,
            'education':education,
            'education_num':education_num,
            'marital_status':marital_status,
            'occupation':occupation,
            'relationship':relationship,
            'race':race,
            'sex':sex,
            'capital_gain':capital_gain,
            'capital_loss':capital_loss,
            'hours_per_week':hours_per_week,
            'native_country':native_country,
            'fnlwgt':fnlwgt}
        )
        st.write(result.data)


elif st.session_state.selected == "Update Data":
    st.title('Update Data')
    st.write('This page updates the data in the "salaries" table.')
    #ask for id to update
    id_given=st.number_input('Enter ID to update', min_value=1, max_value=100000, step=1)
    #display information with that id
    fields=st.multiselect('Select Fields', ['id', 'age', 'income', 'workclass', 'education', 'education_num', 'marital_status', 'occupation', 'relationship', 'race', 'sex', 'capital_gain', 'capital_loss', 'hours_per_week', 'native_country', 'fnlwgt']
    , default=['id', 'age', 'income', 'workclass', 'education', 'occupation', 'race', 'sex']
    )
    data = conn.select_filter(table='salaries', function=fields, column='id', operator='eq', criteria=id_given)
    all_data=conn.select_filter(table='salaries', function='*', column='id', operator='eq', criteria=id_given)
    all_data=all_data.data
    data = data.data
    display_format = st.selectbox('Select Display Format', ['Table', 'DataFrame', 'JSON'], key="display_format")
    
    if st.session_state.display_format != display_format:
        st.session_state.display_format = display_format

    if st.session_state.display_format == 'Table':
        # Display the data as a table
        st.table(data)

    elif st.session_state.display_format == 'DataFrame':
        # Display the data as a DataFrame
        st.dataframe(data)

    elif st.session_state.display_format == 'JSON':
        # Display the data as JSON
        st.json(data)
    #ask for fields to update
    st.write('Enter the new values for the fields you want to update.')
    age=st.number_input('Enter Age', min_value=0, max_value=100, value=all_data[0]['age'], step=1)
    income=st.selectbox('Enter Income', ['<=50K', '>50K'])
    workclass=st.text_input('Enter Workclass', value=all_data[0]["workclass"])
    education=st.text_input('Enter Education', value=all_data[0]['education'])
    education_num=st.number_input('Enter Education Number', min_value=0, max_value=100, value=all_data[0]['education_num'], step=1)
    marital_status=st.text_input('Enter Marital Status', value=all_data[0]['marital_status'])
    occupation=st.text_input('Enter Occupation', value=all_data[0]['occupation'])
    relationship=st.text_input('Enter Relationship', value=all_data[0]['relationship'])
    race=st.text_input("Enter Race", value=all_data[0]['race'])
    sex=st.selectbox("Enter Gender", ['Male','Female'])
    capital_gain=st.number_input('Enter Capital Gain', min_value=0, max_value=1000000, value=int(all_data[0]['capital_gain']), step=1)
    capital_loss=st.number_input('Enter Capital Loss', min_value=0, max_value=1000000, value=int(all_data[0]['capital_loss']), step=1)
    hours_per_week=st.number_input('Enter Hours Per Week', min_value=0, max_value=100, value=int(all_data[0]['hours_per_week']), step=1)
    native_country=st.text_input('Enter Native Country', value=all_data[0]['native_country'])
    fnlwgt=st.number_input('Enter Final Weight', min_value=0, max_value=1000000, value=int(all_data[0]['fnlwgt']), step=1)
    #update data
    update=st.button('Update Data')
    if update:
        update_data={
            'age':age,
            'income':income,
            'workclass':workclass,
            'education':education,
            'education_num':education_num,
            'marital_status':marital_status,
            'occupation':occupation,
            'relationship':relationship,
            'race':race,
            'sex':sex,
            'capital_gain':capital_gain,
            'capital_loss':capital_loss,
            'hours_per_week':hours_per_week,
            'native_country':native_country,
            'fnlwgt':fnlwgt

        }
        result=conn.update(table='salaries', data=update_data,row_id=id_given)
        st.write(result.data)