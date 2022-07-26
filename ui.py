import streamlit as st
import numpy as np
from joblib import load
from sklearn.preprocessing import StandardScaler

# import default feature values
defaults = load('defaults.joblib') 
values = defaults

# import model
model = load('elastic-net-model.joblib')

st.title('Housing Price Predictor')
st.header('Instructions')
st.caption('Modify the features below to best describe the house you intend to sell. Press "Submit" when finished for our model to recommend a selling price.')

st.header('Features')

col1, col2 = st.columns(2)

with col1:
    st.subheader('Zoning Classification')
    ms_zoning_dict = {'Residential Low Density':'RL', 'Residential High Density':'RH', 'Floating Village Residential':'FV', 'Residential Medium Density':'RM', 'Commercial':'C (all)'} # from data_description.txt
    ms_zone = st.selectbox('The general zoning classification', ms_zoning_dict.keys())
    for option in ms_zoning_dict:
        if option == ms_zone:
            values['MSZoning_{zone}'.format(zone=ms_zoning_dict[option])][0] = 1
        else: 
            values['MSZoning_{zone}'.format(zone=ms_zoning_dict[option])][0] = 0
        # st.write('MSZoning_{zone}'.format(zone=ms_zoning_dict[option]))
        # st.write(values['MSZoning_{zone}'.format(zone=ms_zoning_dict[option])][0])
    
    # calculate overall grade using overall quality and overall condition as done in the model notebook
    st.subheader('Overall Quality')
    overall_quality = st.number_input('Overall material and finish quality of the house (1-10).', 1, 10)
    st.subheader('Overall Condition')
    overall_condition = np.log1p(st.number_input('Overall condition of the house (1-10).', 1, 10)) # identified as skewed feature in model notebook
    values['OverallGrade'][0] = overall_quality*overall_condition
    # st.write(values['OverallGrade'][0])

    st.subheader('General Living Area')
    general_living_area = st.number_input('Area of general living space (in square feet).', 0.0)
    values['GrLivArea-Sq'][0] = np.sqrt(general_living_area)
    # st.write(values['GrLivArea-Sq'][0])

    st.subheader('Main Exterior Material')
    exterior_dict = {'Asbestos Shingles':'AsbShng', 'Asphalt Shingles':'AsphShn', 'Brick Common':'BrkComm', 'Brick Face':'BrkFace', 'Cinder Block':'CBlock', 'Cement Board':'CemntBd', 'Hard Board':'HdBoard', 'Imitation Stucco':'ImStucc', 'Metal Siding':'MetalSd', 'Plywood':'Plywood', 'Stone':'Stone', 'Stucco':'Stucco', 'Vinyl Siding':'VinylSd', 'Wood Siding':'Wd Sdng', 'Wood Shingles':'WdShing'} # from data_description.txt
    exterior = st.selectbox('The main construction material used for the exterior of the house.', exterior_dict.keys())
    # exterior
    for option in exterior_dict:
        if option == exterior:
            values['Exterior1st_{exterior}'.format(exterior=exterior_dict[option])][0] = 1
        else: 
            values['Exterior1st_{exterior}'.format(exterior=exterior_dict[option])][0] = 0
        # st.write('Exterior1st_{exterior}'.format(exterior=exterior_dict[option]))
        # st.write(values['Exterior1st_{exterior}'.format(exterior=exterior_dict[option])][0])

    
with col2:
    st.subheader('Neighborhood')
    neighborhood_options_dict = {'Bloomington Heights':'Blmngtn', 'Bluestem':'Blueste', 'Briardale':'BrDale', 'Brookside':'BrkSide', 'Clear Creek':'ClearCr', 'College Creek':'CollgCr', 'Crawford':'Crawfor', 'Edwards':'Edwards', 'Gilbert':'Gilbert', 'Iowa DOT and Rail Road':'IDOTRR', 'Meadow Village':'MeadowV', 'Mitchell':'Mitchel', 'Northridge':'NoRidge', 'Northpark Villa':'NPkVill', 'Northridge Heights':'NridgHt', 'Northwest Ames':'NWAmes', 'Old Town':'OldTown', 'South & West of Iowa State University':'SWISU', 'Sawyer':'Sawyer', 'Sawyer West':'SawyerW', 'Somerset':'Somerst', 'Stone Brook':'StoneBr', 'Timberland':'Timber', 'Veenker':'Veenker'} # from data_description.txt
    neighborhood = st.selectbox('The neighborhood the house is located in.', neighborhood_options_dict)
    # neighborhood
    for option in neighborhood_options_dict:
        if option == neighborhood:
            values['Neighborhood_{neighborhood}'.format(neighborhood=neighborhood_options_dict[option])][0] = 1
        else: 
            values['Neighborhood_{neighborhood}'.format(neighborhood=neighborhood_options_dict[option])][0] = 0
        # st.write('Neighborhood_{neighborhood}'.format(neighborhood=neighborhood_options_dict[option]))
        # st.write(values['Neighborhood_{neighborhood}'.format(neighborhood=neighborhood_options_dict[option])][0])

    st.subheader('House Year Built')
    house_year_built = np.log1p(st.number_input('Original construction year of the house.', 1850)) # identified as skewed feature in model notebook
    values['YearBuilt'][0] = house_year_built 
    # st.write(values['YearBuilt'][0])

    st.subheader('Condition')
    condition_options_dict = {'Adjacent to arterial street':'Artery', 'Adjacent to feeder street':'Feedr', 'Normal':'Norm', 'Within 200\' of North-South Railroad':'RRNn', 'Adjacent to North-South Railroad':'RRAn', 'Near positive off-site feature--park, greenbelt, etc.':'PosN', 'Adjacent to postive off-site feature':'PosA', 'Within 200\' of East-West Railroad':'RRNe', 'Adjacent to East-West Railroad':'RRAe'} # from data_description.txt
    condition = st.selectbox('The condition of closest proximity to the house.', condition_options_dict)
    # condition
    for option in condition_options_dict:
        if option == condition:
            values['Condition1_{condition}'.format(condition=condition_options_dict[option])][0] = 1
        else: 
            values['Condition1_{condition}'.format(condition=condition_options_dict[option])][0] = 0
        # st.write('Condition1_{condition}'.format(condition=condition_options_dict[option]))
        # st.write(values['Condition1_{condition}'.format(condition=condition_options_dict[option])][0])
    
    st.subheader('Total Area')
    total_area = st.number_input('Total area, including basement, of house (in square feet).', 0.0)
    values['AllSF-Sq'][0] = np.sqrt(total_area) 
    # st.write(values['AllSF-Sq'][0])

price_estimate = 0.00
if st.button('Submit'):
    # scale values
    stdSc = StandardScaler()
    transformed_values = stdSc.fit_transform(values.T)
    price_estimate = model.predict(transformed_values.T)
    st.subheader('Price Estimate')
    st.write('Estimated selling price: ${price}'.format(price=np.expm1(price_estimate)[0].round(2))) # inverse log transform
