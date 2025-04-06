import streamlit as st 
import pandas as pd

from Optimiser.Houses import House
from Optimiser.Child import Child
from Optimiser.EggType import EggType
from Optimiser.Optimisation import Optimiser, ModelParameters
from Optimiser import Optimisation

from scripts import streamlit_functions
streamlit_functions.setup_navigation_side()

#region  Setup Functions
def convert_houses_to_dataframe(houses):
    flattened_data = []
    for house in houses:
        for child in house.children:
            child_data = {
               "name": child.name,
                "age": child.age,
                "basket_capacity": child.basket_capacity,
                "house_id": child.house_id,
                **child.preference
            }
            flattened_data.append(child_data)
    return pd.DataFrame(flattened_data)

def convert_dataframe_to_list(df):
    data_list = df.to_dict(orient='records')
    houses = []
    house_ids = set(df['house_id'])
    for house_id in house_ids:
        children = []
        for _, row in df[df['house_id'] == house_id].iterrows():
            child = Child(
                name=row['name'],
                age=row['age'],
                basket_capacity=row['basket_capacity'],
                house_id=row['house_id'],
                preference={
                    "regular": row['regular'],
                    "golden": row['golden'],
                    "healthy": row['healthy'],
                    "chocolate": row['chocolate'],
                    "white chocolate": row['white chocolate'],
                    "rum and raisin": row['rum and raisin'],
                    "dark": row['dark']
                }
            )
            children.append(child)
        house = House(id=house_id, children=children)
        houses.append(house)
    return houses

def convert_egg_types_to_dataframe(egg_types):
    # Flatten the data
    flattened_data = []
    for key, egg_type in egg_types.items():
        egg_type_data = {
            "name": egg_type.name,
            "value": egg_type.value,
            "enjoyment": egg_type.enjoyment,
            "health": egg_type.health,
            "size": egg_type.size,
            "cost": egg_type.cost
        }
        flattened_data.append(egg_type_data)

    # Convert to DataFrame
    df = pd.DataFrame(flattened_data)
    return df

def convert_dataframe_to_dict(df):
    # Convert DataFrame to dictionary
    egg_types_dict = {}
    for _, row in df.iterrows():
        egg_type = EggType(
            name=row['name'],
            value=row['value'],
            enjoyment=row['enjoyment'],
            health=row['health'],
            size=row['size'],
            cost=row['cost']
        )
        egg_types_dict[row['name']] = egg_type
    return egg_types_dict

#endregion

#region Setup Data

def get_data(): 
        
    total_supply = {"regular": 10, "golden": 20, "healthy": 50, "chocolate": 20, "white chocolate":10, "rum and raisin":10, "dark":10}

    egg_types = {
        "regular": EggType("regular", value=1, enjoyment=2, health=2, size=1, cost=1),
        "golden": EggType("golden", value=5, enjoyment=5, health=1, size=1, cost=3),
        "healthy": EggType("healthy", value=2, enjoyment=1, health=5, size=1, cost=2),
        "chocolate": EggType("chocolate", value=3, enjoyment=4, health=0, size=2, cost=2),
        "white chocolate": EggType("white chocolate", value=3, enjoyment=4, health=0, size=2, cost=2),
        "rum and raisin": EggType("rum and raisin", value=3, enjoyment=2, health=1, size=3, cost=2),
        "dark": EggType("dark", value=3, enjoyment=2, health=1, size=2, cost=2),
    }

    houses = [
    House(id=1, children=[
        Child("Alice", age=9, basket_capacity=10, house_id=1,
            preference={"regular": True, "golden": True, "healthy": True, "chocolate": False, "white chocolate":False, "rum and raisin":False, "dark":False }),
        Child("Bob", age=12, basket_capacity=8, house_id=1,
            preference={"regular": True, "golden": True, "healthy": False, "chocolate": True ,"white chocolate":False, "rum and raisin":False, "dark":False}),
    ]),
    House(id=2, children=[
        Child("Timmy", age=6, basket_capacity=10, house_id=2,
            preference={"regular": True, "golden": True, "healthy": True, "chocolate": False ,"white chocolate":False, "rum and raisin":False, "dark":False}),
        Child("Bob", age=5, basket_capacity=12, house_id=2,
            preference={"regular": True, "golden": True, "healthy": False, "chocolate": True, "white chocolate":False, "rum and raisin":False, "dark":False}),
    ]),
    House(id=3, children=[
        Child("Jasmine", age=25, basket_capacity=20, house_id=3,
            preference={"regular": False, "golden": True, "healthy": True, "chocolate": False, "white chocolate":False, "rum and raisin":True, "dark":True}),
        Child("Charlie", age=5, basket_capacity=12, house_id=3,
            preference={"regular": True, "golden": True, "healthy": False, "chocolate": True, "white chocolate":False, "rum and raisin":False, "dark":False}),
    ]),
    ]
    return total_supply, egg_types, houses
#endregion

st.markdown("## 🐰 Easter Bunny Optimisation Tool 🐰"
)

st.markdown("## Data Setup")
## Get data sources from function - this could be replaced to get from an API or file. 
total_supply, egg_types, houses = get_data()

st.markdown("### Egg Types")
df_egg_types = convert_egg_types_to_dataframe(egg_types)
df_egg_types_out = st.data_editor(df_egg_types )
egg_types = convert_dataframe_to_dict(df_egg_types_out)
with st.expander("See Data"):
    st.write(egg_types)

st.markdown("### Egg Supply")
df_supply_out = st.data_editor(pd.DataFrame(total_supply.items(), columns=['Egg Name', 'Supply']))
total_supply = df_supply_out.set_index('Egg Name')['Supply'].to_dict()
with st.expander("See Data"):
    st.write(total_supply)

st.markdown("### Houses & Children")
df_houses = convert_houses_to_dataframe(houses)
df_houses_out = st.data_editor(df_houses, num_rows="dynamic")

houses_list = convert_dataframe_to_list(df_houses_out)
with st.expander("See Data"):
    st.write(houses_list)


st.markdown("---")

st.markdown("## Optimiser")
st.markdown("##### Paramters")

## Using class to easily hook up model parameters to be passed to the model
model_paramters = ModelParameters()
with st.expander("Optimisation Parameters", False):
    c1 , c2 = st.columns(2)
    with c1:
        model_paramters.golden_egg_name = st.text_input("Golden Egg Name", model_paramters.golden_egg_name)
        model_paramters.health_min= st.number_input("Min Healthy", value=model_paramters.health_min, max_value=10,min_value=0)
        model_paramters.fairness_threshold= st.number_input("Min Fairness", value=model_paramters.fairness_threshold, max_value=10,min_value=0)
    with c2:
        model_paramters.egg_rate = st.number_input("Egg Rate", value=model_paramters.egg_rate, max_value=10,min_value=0)
        model_paramters.happiness_min = st.number_input("Min Happiness", value=model_paramters.happiness_min, max_value=10,min_value=0)

if 'results_1' not in st.session_state:
    st.session_state.key = 'results_1'  
    st.session_state["results_1"] = False

## Using button to trigger the run of optimser - output stored in session state 
st.markdown("##### Run Optimiser")
if st.button("Run Optimisation"):
    result = Optimisation.Optimiser.optimize_easter_enjoyment(houses_list, egg_types, total_supply, model_paramters)
    st.session_state["results_1"] = result

## Display output of Optimisation 
## Using Streamlit session state to store output as any chances call re-run from top to bottom.
if st.session_state["results_1"]:
    with st.expander("Optimisation Results", True):
        result = st.session_state["results_1"]
        if result == "No Solution Found":
            st.warning('No optimal solution found')
        else:
            total_cost = 0
            total_enjoyment = 0
            for house in houses_list:
                st.markdown(f"**House number {house.id}**")
                for child in house.children:
                        st.write(f"{child.name} got: {result[child.name]}")
                        for egg in result[child.name]:
                            total_cost += egg_types[egg].cost
                            total_enjoyment += egg_types[egg].enjoyment
            st.markdown(f"**Outcomes**")
            st.write(f"Total Cost: ${total_cost}")
            st.write(f"Total Joy: {total_enjoyment} 😊 ")

## Using Streamlit session state to store output as any chances call re-run from top to bottom.
if 'results_2' not in st.session_state:
    st.session_state.key = 'results_2'  
    st.session_state["results_2"] = False

## Hidden second model - used to reveal the budget friendly model later in the talk
## Using session state to handle hiding output
if st.session_state["results_1"]:
    with st.expander("Further Models"):
        st.markdown("##### Run Budget Optimiser")
        if st.button("Run Budget Optimisation"):
            result = Optimisation.Optimiser.optimize_easter_cost(houses_list, egg_types, total_supply, model_paramters)
            st.session_state["results_2"] = result

    if st.session_state["results_2"]:
            with st.expander("Budget Optimisation Results"):
                result = st.session_state["results_2"]
                if result == "No Solution Found":
                    st.warning('No optimal solution found')
                else:
                    total_cost = 0
                    total_enjoyment = 0
                    for house in houses_list:
                        st.markdown(f"**House number {house.id}**")
                        for child in house.children:
                                st.write(f"{child.name} got: {result[child.name]}")
                                for egg in result[child.name]:
                                    total_cost += egg_types[egg].cost
                                    total_enjoyment += egg_types[egg].enjoyment
                    st.markdown(f"**Outcomes**")
                    st.write(f"Total Cost: ${total_cost}")
                    st.write(f"Total Joy: {total_enjoyment} 🙃 ")

streamlit_functions.setup_footer()