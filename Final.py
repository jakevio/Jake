import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st


df = pd.read_csv("Fast Food Restaurants.csv",
                 encoding='unicode_escape',
                 header=0,
                 names=['id', 'dateAdded', 'dateUpdated', 'address', 'categories', 'city', 'country', 'keys',
                        'latitude', 'longitude', 'name', 'postalCode', 'province', 'sourceURLs', 'websites'],
                 usecols=['id', 'address', 'categories', 'city', 'country', 'latitude',
                          'longitude', 'name', 'postalCode', 'province'])
statelist = ['AK', 'AL', 'AR', 'AZ', 'CA', 'CO', 'CT', 'DE', 'FL', 'GA', 'GU', 'HI', 'IA',
             'ID', 'IL', 'IN', 'KS', 'KY', 'LA', 'MA', 'MD', 'ME', 'MI', 'MN', 'MO', 'MP', 'MS', 'MT',
             'NC', 'ND', 'NE', 'NH', 'NJ', 'NM', 'NV', 'NY', 'OH', 'OK', 'OR', 'PA', 'PR', 'RI', 'SC',
             'SD', 'TN', 'TX', 'UM', 'UT', 'VA', 'VI', 'VT', 'WA', 'WI', 'WV', 'WY']

def createnamelist():
    namelist = []
    for i in df['name']:
        if i in namelist:
            continue
        else:
            namelist.append(i)
    return namelist

def createcitylist(state,company):
    staterestaurantsdf = df.loc[(df['province'] == state) & (df['name'] == company)]
    return staterestaurantsdf

def piechart():
    namelist = createnamelist()
    choosename = st.selectbox('Select a company to see the states it is in.', namelist)
    df2 = df.filter(items=['name','province'])
    df2 = df2.set_index('name')
    filter_data = (df2.index == choosename)
    df3 = df2[filter_data]
    df3 = df3.sort_values(by=['province'])
    df4 = df3.value_counts('province')
    df4 = df4.to_frame()
    df4.columns = ['restaurants']
    st.write(df4)
    restaurantlist = df4['restaurants'].values.tolist()
    smallstatelist = df4.index.tolist()
    fig, axes = plt.subplots()
    axes.set_title('State Breakdown for Restaurant')
    axes.pie(restaurantlist, labels = smallstatelist)
    st.pyplot(fig)

def piechart2():
    namelist = createnamelist()
    company = st.selectbox('Select a company.', namelist)
    state = st.selectbox('Select a state.', statelist)
    df2 = createcitylist(state,company)
    st.write(df2)

def home():
    st.image("https://sambadenglish.com/wp-content/uploads/2020/10/mcdonalds-free-meals.jpg")
    st.header("My Final Project: An Analyzation of US Fast Food")
    st.balloons()
    st.markdown("""Hello everyone! Today I will be presenting my final project for CS230.
    In this project I will be attempting to display some of the skills I learned throughout
    the length of this course to depict data on fast food locations in the United States.
    This includes the depictions of a map, bar chart, pie chart, and interactive tables.""" )

def barGraph(df):
    st.write()
    state = st.multiselect('Select States:', statelist)
    df2 = df['province'].value_counts('province')
    df2 = df2*10000 #This is done in order to adjust to make it the actual totals#
    df2 = df2.to_frame()
    df2.columns = ['Locations']
    fig = plt.figure()
    locationtable = df2.loc[state].astype(int)
    st.write(locationtable)
    plt.bar(df2.loc[state].index, locationtable['Locations'],color= 'turquoise')
    plt.xlabel('States')
    plt.ylabel('Number of Locations')
    st.pyplot(fig)

def map(df):
    st.write()
    state = st.selectbox('Select a state: ', statelist)
    filter_data = (df['province'] == state)
    st.map(df[filter_data])
    st.caption('Each dot represents a Fast Food restaurant location')

def top(df):
    st.write()
    number = st.slider(label = 'Choose how many top restaurants you would like to see ', min_value=1, max_value=100,value=5)
    top_five_restaurants_count_series = df['name'].value_counts().nlargest(number)
    top_five_restaurants_count = top_five_restaurants_count_series.to_frame()
    st.write("Count",top_five_restaurants_count)
    top_five_restaurants_count.columns = ['Locations']
    topchoice = st.multiselect('Select Restaurant[s]', top_five_restaurants_count.index)
    filter_data = top_five_restaurants_count.filter(items=topchoice, axis=0)
    st.bar_chart(filter_data)

st.title('CS230 Final Project')
st.text('By: Jake Violette')
st.sidebar.title("Navigation")
selection = st.sidebar.radio("Go to", ["Home", "Map", "Top Restaurant Comparison", "State Comparison",
                                       "Company Pie Chart","Company Address in State"])
if selection == "Home":
    home()
if selection == "State Comparison":
    barGraph(df)
if selection == "Map":
    map(df)
if selection == "Top Restaurant Comparison":
    top(df)
if selection == "Company Pie Chart":
    piechart()
if selection == "Company Address in State":
    piechart2()
