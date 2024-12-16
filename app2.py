import streamlit as st
from jamaibase import JamAI, protocol

# Initialize JamAI
jamai = JamAI(
    api_key="jamai_sk_6d64f260d2fc7ed0e66972067a401e9d7d1bbbfab5d56d04",
    project_id="proj_fb54d54ac6988d5d96d06495"
)

def fetch_recipe(input_data):
    """Fetch personalized health advice using JamAI and action tables."""
    try:
        # Validate input data
        if not input_data:
            return {"error": "Input data is missing."}

        # Call the JamAI action table
        completion = jamai.add_table_rows(
            "action",
            protocol.RowAddRequest(
                table_id="RecipeGenerator",
                data=[input_data],  # Send input data as a list of dictionaries
                stream=False
            )
        )

        # Ensure rows are returned
        if completion.rows:
            # Extract the first row's output column
            output_row = completion.rows[0].columns

            # Safely access fields
            recipeName = (
                output_row["RecipeName"].message.content
                if "RecipeName" in output_row and hasattr(output_row["RecipeName"], "message")
                else None
            )
            recipeIngredients = (
                output_row["Recipe_ingredients"].message.content
                if "Recipe_ingredients" in output_row and hasattr(output_row["Recipe_ingredients"], "message")
                else None
            )
            recipeDuration = (
                output_row["Recipe_duration"].message.content
                if "Recipe_duration" in output_row and hasattr(output_row["Recipe_duration"], "message")
                else None
            )

            recipeSteps = (
                output_row["Steps"].message.content
                if "Steps" in output_row and hasattr(output_row["Steps"], "message")
                else None
            )
            # Return the results
            return {
                "Recipe Name": recipeName,
                "Ingredients": recipeIngredients,
                "Duration": recipeDuration,
                "Recipe": recipeSteps
            }
        else:
            return {"error": "No data returned from the API."}

    except Exception as e:
        # Handle errors gracefully
        return {"error": f"An error occurred: {str(e)}"}



# Streamlit UI: Main Application
st.title("Culinary Playground")
st.markdown("Discover the joy of cooking with the JamAI Base-powered Recipe Generator, your ultimate kitchen companion! Whether you're working with a random mix of ingredients or planning a gourmet meal, we've got you covered.")


# User Inputs
with st.form(" "):
    available = st.text_area("Available ingredients")
    tags = st.text_area("Tags")
    serving_size = st.number_input(
        "Serving size",
        min_value=1,
        max_value=100,
        step=1,
        value=1,
    )

    # Submit button
    submitted = st.form_submit_button("Get Recipe")

# Display outputs only after submission
if submitted:
    if all([available, serving_size, tags]):
        st.info("Generating mouth-watering recipe ...")

        # Prepare input data
        input_data = {
            "Available_ingredients": available,
            "Serving_size": serving_size,
            "Tags": tags
        }

        # Fetch advice
        result = fetch_recipe(input_data)

        # Display results
        if "error" in result:
            st.error(result["error"])
        else:
            st.markdown("### Results")
            for key, value in result.items():
                if value:  # Display only fields with non-empty content
                    # Use custom markdown and HTML for cleaner display
                    st.markdown(
                        f"<h3 style='color: #4CAF50;'>{key}:</h3>",  # Styled header
                        unsafe_allow_html=True,
                    )

                    # Special formatting for Motivation (poetry)
                    if key:
                        st.markdown(f"<p style='font-size: 16px;'>{value}</p>", unsafe_allow_html=True)
    else:
        st.error("Please fill in all fields before submitting!")



# Footer
st.markdown("---")
st.caption("Powered by JamAI. Ensure API credentials are properly configured.")