#!/usr/bin/env python
# coding: utf-8

# ### 🍎🫐🥝🥗🥘🍎🫐🥝🥗🥘 CLEVER MEAL  B2B🍎🫐🥝🥗🥘🍎🫐🥝🥗🥘

# In[13]:


import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import streamlit as st
import pickle


from sklearn import datasets # sklearn comes with some toy datasets to practice
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
from matplotlib import pyplot
from sklearn.metrics import silhouette_score
from PIL import Image
from IPython.display import display
from fuzzywuzzy import fuzz, process




df= pd.read_csv(r"C:\Users\espan\OneDrive\Documents\GitHub\Clever_Meal_App\CMapp_Recommendation_Model\all_recipes_FV.csv")

X = df[["Protein(g)","Protein Calorie","Carbs(g)","Carbs Calorie", "Fat(g)", "Fat Calorie", "Total Calories"]]


# Scalling
scaler = StandardScaler()
scaler.fit(X)
X_scaled = scaler.transform(X)  # we are getting an array


# we need to get our dataframe
X_scaled_df = pd.DataFrame(X_scaled, columns = X.columns)


# KMeans 01
kmeans = KMeans(n_clusters=10, random_state=1234)
kmeans.fit(X_scaled_df)

kmeans.inertia_


# KMeans Lebels
labels = kmeans.labels_

#Clusters
clusters = kmeans.predict(X_scaled_df)

# Adding Cluster in X
X["cluster"] = clusters

# Final Data Frame
df_final = pd.merge(X, df[['Recipe_name', "Cuisine_type","Diet_type"]], left_index=True, right_index=True)














######################################################################################################################
#####################################################################################################################

#df_final= pd.read_csv(r"C:\Users\espan\OneDrive\Documents\GitHub\Clever_Meal_App\CMapp_Recommendation_Model\output.csv")

# In[14]:


# ### K Means Training Function

# In[16]:

# Load the KMeans model from the file

#with open(r"C:\Users\espan\OneDrive\Documents\GitHub\Clever_Meal_App\CMapp_Recommendation_Model\kmeans_model.pkl", "rb") as file:
    #loaded_kmeans = pickle.load(file)


####################################################################################################################################
# ## User Inputs

# ## Total Calories per  MEAL🥗✅ 

# In[17]:


### 1. Weight🏗️  & 2. Hight 🌁  & 3. Edge👵🏼👴🏻

def get_non_empty_float(prompt):
    while True:
        try:
            value = float(st.text_input(prompt))
            if value <= 0:
                st.warning("Please enter a positive non-zero value.")
            else:
                return value
        except ValueError:
            st.warning("Invalid input. Please enter a valid number.")


### 4. Gender 🚺🚹

def get_gender():
    while True:
        gender = st.text_input("Gender (male/female): ").lower()
        if gender in ['male', 'female']:
            return gender
        else:
            st.warning("Invalid gender. Please enter 'male' or 'female'.")





### 5. Nilvel of phisical Activity ⛹🏽⛹🏻‍♀️

def get_activity_level():
    # Define a list of correct spellings or keywords:
    # correct_spellings = ["sedentary", "lightly active", "moderately active", "very active"]

    activity_levels = ['sedentary', 'lightly active', 'moderately active', 'very active', 'extra active']

    # Use st.selectbox to provide valid options as suggestions
    nivel_activity = st.selectbox("Activity Level", activity_levels)

    # Optionally, you can add a warning message if the entered value is not in the list
    if nivel_activity not in activity_levels:
        st.warning("Invalid activity level. Please choose from the provided options.")
    
    return nivel_activity



### 6. Goal 🏆

def get_user_goal():
    # Define a list of correct spellings or keywords:
    user_goal = ['lose weight', 'maintain weight', 'gain weight']
    
    # Use st.selectbox to provide valid options as suggestions
    user_goals_input = st.selectbox("What is your Goal:", user_goal)

    # Optionally, you can add a warning message if the entered value is not in the list
    if user_goals_input not in user_goal:
        st.warning("Invalid user goal. Please choose from the provided options.")
    
    return user_goals_input
    


# In[20]:


def calculate_bmr(weight, height, age, gender):
    # BMR calculation using the Harris-Benedict equation
    if gender == "male":
        bmr = 88.362 + (13.397 * weight) + (4.799 * height) - (5.677 * age)
    else:
        bmr = 447.593 + (9.247 * weight) + (3.098 * height) - (4.330 * age)
    return bmr


# ## 🍎🫐🥝🥗🥘🍎🫐🥝🥗🍎🫐🥝🥗🥘🍎🫐🥝🥗🍎🫐🥝🥗🥘🍎🫐🥝🥗

# In[21]:


def calculate_macronutrient_distribution(TDEE):
    
    # List to store user inputs
    user_data = []  
    
    # Macronutrient Ratios
    protein_ratio = 0.3
    fat_ratio = 0.3
    carbohydrate_ratio = 0.4

    # Caloric content per gram of each macronutrient
    protein_calories_per_gram = 4
    fat_calories_per_gram = 9
    carbohydrate_calories_per_gram = 4

    # Calculate the grams of each macronutrient
    protein_grams = (protein_ratio * TDEE) / protein_calories_per_gram
    fat_grams = (fat_ratio * TDEE) / fat_calories_per_gram
    carbohydrate_grams = (carbohydrate_ratio * TDEE) / carbohydrate_calories_per_gram

    # Calculate the calories contributed by each macronutrient
    protein_calories = protein_grams * protein_calories_per_gram
    fat_calories = fat_grams * fat_calories_per_gram
    carbohydrate_calories = carbohydrate_grams * carbohydrate_calories_per_gram
    
    #Total Calories
    total_calories = carbohydrate_calories + fat_calories + protein_calories
    
    user_data.append(
            {
        "Protein(g)": protein_grams,
        "Protein Calorie": protein_calories,
        "Carbs(g)": carbohydrate_grams,
        "Carbs Calorie": carbohydrate_calories,
        "Fat(g)": fat_grams,
        "Fat Calorie": fat_calories,
        "Total Calories": total_calories
    })
        
    user_inputs_df = pd.DataFrame(user_data)
    

    return {
        "Protein(g)": protein_grams,
        "Protein Calorie": protein_calories,
        "Carbs(g)": carbohydrate_grams,
        "Carbs Calorie": carbohydrate_calories,
        "Fat(g)": fat_grams,
        "Fat Calorie": fat_calories,
        "Total Calories": total_calories
    }


def TDEE_calculator_per_meal():
    print("Welcome to the TDEE Calculator!")
    print("Please enter the following details:")

    weight = get_non_empty_float("Weight (kg): ")
    height = get_non_empty_float("Height (cm): ")
    age = get_non_empty_float("Age (years): ")
    gender = get_gender()
    nivel_activity = get_activity_level()
    user_goals = get_user_goal()

    # Basal Metabolic Rate (BMR)
    bmr = calculate_bmr(weight, height, age, gender)

    activity_factors = {
        "sedentary": 1.2,
        "lightly active": 1.375,
        "moderately active": 1.55,
        "very active": 1.725,
        "extra active": 1.9
    }
    
    TDEE_goals = {
        "lose weight": 0.85,
        "maintain weight": 1,
        "gain weight": 1.1
    }

    ##### PER MEAL

    # Create a list to hold the data for the DataFrame
    user_inputs_parameters = []

    # Set a default value for TDEE
    TDEE = None

    if nivel_activity in activity_factors:
        TDEE = (bmr * activity_factors[nivel_activity]) / 3

        if user_goals in TDEE_goals:
            TDEE *= TDEE_goals[user_goals]
            print(f"Total Calories per meal based on your Goal is: {TDEE:.2f} calories per meal.")
        else:
            print("Invalid goal. Please choose from the provided options.")
    #else:
        #print("Invalid activity level. Please choose from the provided options.")
        

        
        
        # Calculate and display the macronutrient distribution
        macronutrient_distribution = calculate_macronutrient_distribution(TDEE)
        
        print("\nMacronutrient Distribution:")
        
        for macronutrients, value in macronutrient_distribution.items():
            
            
            # Append the nutrient and value to the data list as a tuple
            user_inputs_parameters.append((macronutrients, value))
            
            # Create a DataFrame from the data list
            df_user_inputs = pd.DataFrame(user_inputs_parameters, columns=["Macronutrients", "Value"])
            
         

    else:
        print("Invalid activity level. Please choose from the provided options.")
        
    # Transpose the DataFrame
    df_user_inputs_TP = df_user_inputs.transpose()


    # Changing the columns names

    custom_column_names = {
                  "0": "Protein(g)",
                  "1": "Protein Calorie",
                  "2": "Carbs(g)",
                  "3": "Carbs Calorie",
                  "4": "Fat(g)",
                  "5": "Fat Calorie",
                  "6": "Total Calories"}

    df_user_inputs_TP.columns = custom_column_names.values()


    # Dropping the columns "Macronutrients"

    df_user_inputs_TP = df_user_inputs_TP.drop(index="Macronutrients")

    # Resetting the index
    df_user_inputs_TP = df_user_inputs_TP.reset_index(drop=True)
        
    return df_user_inputs_TP 


# ## 🍎🫐🥝🥗🥘🍎🫐🥝🥗🍎🫐🥝🥗🥘🍎🫐🥝🥗

# In[22]:


def recipe_recommendation():
    
    # NOTE IN THIS USER PARAMETOR WE DONT HAVE THE CLUSTER!!!!
    df_user_inputs_parameter = TDEE_calculator_per_meal()


    # Scaling the user inputs DataFrame
    
    
    # NOT FIT THE USER INPUTS!!!! 👀👀👀👀👀👀👀👀👀👀👀👀
    
    scaler.transform(df_user_inputs_parameter)
    user_inputs_scaled = scaler.transform(df_user_inputs_parameter)

    # Apply KMeans prediction to user_inputs_scaled
    user_cluster = kmeans.predict(user_inputs_scaled)
    

    # Filter recommended recipe based on predicted cluster

    recommended_recipe_from_cluster = df_final[df_final['cluster'] == user_cluster[0]]

    # Select a random recipe from recommended recipes
    recommended_recipe = recommended_recipe_from_cluster.sample(n=1)
    
    # take the specific recipe
    dish_recommended = recommended_recipe_from_cluster["Recipe_name"].values[0]

    ##dish_recommended01 = pd.DataFrame("recipe_name.csv")

    #return recommended_recipe, dish_recommended 
    return recommended_recipe



def main():
    st.title(" ➡️ CLEVER MEAL 🍎🧠") 
    st.title("Recipe Recommendation App")
    st.subheader("Based on your Nutrition Goals!🎯🚀")

    # Assuming you have functions to get user inputs and store them in df_user_inputs_parameter DataFrame

    # Display user inputs and calculate TDEE
    st.subheader("Please introduce your information:")
    # ... (Display user inputs and TDEE calculation results)

    # Call recipe_recommendation() to get the recommended recipe
    recommended_recipe_D = recipe_recommendation()
   

    # Unpack the values from the returned tuple
    recommended_recipe= recommended_recipe_D

    # recommended_recipe, dish_recommended = recommended_recipe_D

  

   

    #############################
    st.subheader("Recommended Recipe with the Macronutrients Distribution")
    st.write(recommended_recipe)


    ##############
    #st.subheader("TDEE")
    #st.write(tdcc_01 )

    #############################
    #st.subheader("Recommended Dish Name")
    # Format the dish name in bold and red color
    #st.write(f"<p style='font-weight:bold; color:red;'>{dish_recommended}</p>", unsafe_allow_html=True)

if __name__ == "__main__":
    main()


#def main():
    #st.title(" ➡️ CLEVER MEAL 🍎🧠") 
    #st.title("Recipe Recommendation App")
    #st.subheader("Based on your Nutrition Goals!🎯🚀")

    # Assuming you have functions to get user inputs and store them in df_user_inputs_parameter DataFrame

    # Display user inputs and calculate TDEE
    #st.subheader("Please introduce your information:")
    # ... (Display user inputs and TDEE calculation results)

    # Call recipe_recommendation() to get the recommended recipe
    #recommended_recipe_D = recipe_recommendation()

    # Unpack the values from the returned tuple
    #recommended_recipe, dish_recommended = recommended_recipe_D

    #################################################################################
    #st.subheader("Recommended Dish with the Macronutrients Distribution")
    #st.write(recommended_recipe)

    ################################################################################
    #st.subheader("Recommended Dish Name")
    # Format the dish name in bold and red color
    #st.write(f"<p style='font-weight:bold; color:red;'>{dish_recommended}</p>", unsafe_allow_html=True)

    ################################################################################

    #if st.button("Get Recipe Recommendation"):
        #recommended_recipe_D = recipe_recommendation()
        #st.markdown("\nRecipe Recommendation:")
        #st.markdown(recommended_recipe_D)

#if __name__ == "__main__":
    #main()



##############################################################################################################

#def main():
    #st.title(" ➡️ CLEVER MEAL 🍎🧠") 
    #st.title("Dish Recommendation App")
    #st.subheader("Based on your Nutrition Goals!🎯🚀")

    # Assuming you have functions to get user inputs and store them in df_user_inputs_parameter DataFrame

    # Display user inputs and calculate TDEE
    #st.subheader("Please introduce your information:")
    # ... (Display user inputs and TDEE calculation results)

    # Call recipe_recommendation() to get the recommended recipe
    #recommended_recipe_D = recipe_recommendation()

    # Unpack the values from the returned tuple
    #recommended_recipe, dish_recommended = recommended_recipe_D

    #############################
    #st.subheader("Recommended Dish with the Macronutrients Distribution")
    #st.write(recommended_recipe)

    #############################
    #st.subheader("Recommended Dish Name")
    # Format the dish name in bold and red color
    #st.write(f"<p style='font-weight:bold; color:red;'>{dish_recommended}</p>", unsafe_allow_html=True)

#if __name__ == "__main__":
 #   main()
























###########################################################################################################################



# Define the recipe_recommendation() function as you provided earlier

# Define the TDEE_calculator_per_meal() function as you provided earlier

# Define other functions and data processing steps as needed







## 👀👀👀👀👀👀👀👀👀👀👀👀 to Check


#def main():
    #st.title(" ➡️ CLEVER MEAL 🍎🧠") 
    #st.title("Dish Recommendation App")
    #st.subheader("Based on your Nutrition Goals!🎯🚀")

    # Assuming you have functions to get user inputs and store them in df_user_inputs_parameter DataFrame

    # Display user inputs and calculate TDEE
    #st.subheader("Please introduce your information:")
    # ... (Display user inputs and TDEE calculation results)

    # Call TDEE_calculator_per_meal() to get user inputs and TDEE calculation
    #df_user_inputs_parameter = TDEE_calculator_per_meal()

    # Apply KMeans prediction to user inputs and get recipe recommendation
    #recommended_recipe_D = recipe_recommendation(df_user_inputs_parameter)

    # Unpack the values from the returned tuple
    #recommended_recipe, dish_recommended = recommended_recipe_D

    #############################
    #st.subheader("Recommended Dish with the Macronutrients Distribution")
    #st.write(recommended_recipe)

    #############################
    #st.subheader("Recommended Dish Name")
    # Format the dish name in bold and red color
    #st.write(f"<p style='font-weight:bold; color:red;'>{dish_recommended}</p>", unsafe_allow_html=True)

#if __name__ == "__main__":
    #main()

































#def dish_name():
    
    #dish_name = recipe_recommendation().iloc[0]['Recipe_name']
    
    
    #return  dish_name

###############################################################################
#🍎🍎🍎🍎🍎🍎🍎🍎🍎🍎🍎🍎🍎🍎🍎🍎🍎🍎🍎🍎🍎🍎🍎🍎🍎🍎🍎🍎🍎🍎🍎🍎🍎🍎🍎🍎🍎🍎🍎🍎🍎🍎🍎
#def main():

    #st.title(" ➡️ CLEVER MEAL 🍎🧠") 

    #st.title("Dish Recommendation App")

    #st.subheader("Based on your Nutrition Goals!🎯🚀")

    # Assuming you have functions to get user inputs and store them in df_user_inputs_parameter DataFrame

    #Display user inputs and calculate TDEE
    #st.subheader("Please introduce your information:")
    # ... (Display user inputs and TDEE calculation results)

    # Call recipe_recommendation() to get the recommended recipe

    #recommended_recipe_D= recipe_recommendation()

    


    #############################
    #st.subheader("Recommended Dish with the Macronutrients Distribution")
    #st.write(recommended_recipe_D)

  
    

#if __name__ == "__main__":
    #main()

#🍎🍎🍎🍎🍎🍎🍎🍎🍎🍎🍎🍎🍎🍎🍎🍎🍎🍎🍎🍎🍎🍎🍎🍎🍎🍎🍎🍎🍎🍎🍎🍎🍎🍎🍎🍎🍎🍎🍎🍎🍎🍎🍎🍎🍎🍎🍎🍎

# In[34]:




#st.write(dish_recommended01)
    #############################

    # Display the recommended Dish
    #st.subheader("Recommended Dish based on your Nutrition Goals")
    #st.write(dish_name)
    

    

     # Display the recommended Dish
    #st.subheader("Recommended Dish")
    #st.write(recipe_name)


    #Why this is NOT WORKING?

  
    

    # Display the recommended Dish
    #st.subheader("Recommended Dish based on your Nutrition Goals")
    #st.write(dish_recommended)

    #############################
    #st.subheader("Recommended Dish with the Macronutrients Distribution")
    #st.write(recommended_recipe)
    #############################
   


#recommended_recipe_D, dish_name = recipe_recommendation()
  #############################
    # Display the dish name
    #st.subheader("Recommended Dish Name")
    #st.write(dish_name)



#####################################################################################################



