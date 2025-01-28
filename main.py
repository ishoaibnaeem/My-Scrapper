# import os
# import time
# import pandas as pd
# import streamlit as st
# from selenium import webdriver
# from selenium.webdriver.common.by import By
# from selenium.webdriver.support.ui import Select
# from selenium.webdriver.chrome.service import Service
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC
# import re

# # Input fields
# starting_roll_no = st.number_input('Starting Roll Number', min_value=0, value=528239)
# ending_roll_no = st.number_input('Ending Roll Number', min_value=0, value=528242)
# output_filename = st.text_input('Output File Name')

# if st.button('Start Scraping') and output_filename:
#     # Sanitize output filename
#     output_filename = re.sub(r'[<>:"/\\|?*]', '_', output_filename)
    
#     # Configure WebDriver
#     service = Service()  # Replace with the actual path to chromedriver
#     driver = webdriver.Chrome(service=service)
#     driver.maximize_window()

#     # Navigate to the website
#     driver.get('https://result.biselahore.com/')
#     wait = WebDriverWait(driver, 10)

#     # Select Matric option
#     try:
#         matric_option = wait.until(EC.presence_of_element_located((By.ID, 'rdlistCourse_0')))
#         driver.execute_script("arguments[0].click();", matric_option)  # Use JavaScript click to bypass issues
#     except Exception as e:
#         st.error(f"Error clicking matric option: {e}")
#         driver.quit()
#         raise

#     data = []  # Initialize data storage

#     for roll_no in range(starting_roll_no, ending_roll_no + 1):
#         try:
#             # Input Roll Number
#             roll_number = wait.until(EC.presence_of_element_located((By.ID, 'txtFormNo')))
#             roll_number.clear()
#             time.sleep(0.5)
#             roll_number.send_keys(roll_no)
#             time.sleep(0.5)

#             # Select Exam Type
#             exam_type = wait.until(EC.presence_of_element_located((By.ID, 'ddlExamType')))
#             select_exam_type = Select(exam_type)
#             select_exam_type.select_by_visible_text('Part-I (ANNUAL)')  # Replace with desired option

#             # Select Year
#             exam_year = wait.until(EC.presence_of_element_located((By.ID, 'ddlExamYear')))
#             select_exam_year = Select(exam_year)
#             select_exam_year.select_by_visible_text('2024')  # Replace with desired year

#             # Submit Form
#             try:
#                 # Wait until the button is clickable
#                 submit_button = wait.until(EC.element_to_be_clickable((By.ID, "Button1")))
#                 # Click the button using JavaScript (to bypass potential Validate1 interference)
#                 driver.execute_script("arguments[0].click();", submit_button)
#                 print("Button clicked successfully.")
#             except Exception as e:
#                 print(f"Error while clicking the button: {e}")

#             try:
#                 # Wait for Results
#                 registration_no = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '#lblBFARM'))).text

#                 # Collect Data
#                 detail = {
#                     'roll_no': roll_no, 
#                     'registration_no': registration_no
#                 }

#                 data.append(detail)
#                 print(detail)
#             except Exception as e:
#                 st.warning(f"No data found for Roll No: {roll_no} - {e}")
#                 continue  # Skip to the next roll number

#             # Navigate back to the form page
#             driver.back()  # Go back to the previous page (form page)
#             time.sleep(2)  # Give time for the form page to reload

#         except Exception as e:
#             st.warning(f"Failed to scrape data for Roll No: {roll_no} - {e}")
#             # Refresh page and reselect Matric option if navigation fails
#             driver.refresh()
#             time.sleep(2)
#             try:
#                 matric_option = wait.until(EC.presence_of_element_located((By.ID, 'rdlistCourse_0')))
#                 driver.execute_script("arguments[0].click();", matric_option)
#             except Exception as inner_e:
#                 st.error(f"Error refreshing matric option: {inner_e}")

#     # Close the browser
#     driver.quit()

#     # Create DataFrame and Display Results
#     df = pd.DataFrame(data)
#     st.dataframe(df)

#     # Convert DataFrame to CSV
#     csv = df.to_csv(index=False)

#     # Create a download button
#     st.download_button(
#         label="Download CSV",
#         data=csv,
#         file_name=f'{output_filename}.csv',
#         mime='text/csv',
#     )
import os
import time
import pandas as pd
import streamlit as st
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import re

# Input fields
starting_roll_no = st.number_input('Starting Roll Number', min_value=0, value=528239)
ending_roll_no = st.number_input('Ending Roll Number', min_value=0, value=528242)
output_filename = st.text_input('Output File Name')

if st.button('Start Scraping') and output_filename:
    # Sanitize output filename
    output_filename = re.sub(r'[<>:"/\\|?*]', '_', output_filename)
    
    # Configure WebDriver
    service = Service()  # Replace with the actual path to chromedriver
    driver = webdriver.Chrome(service=service)
    driver.maximize_window()

    # Navigate to the website
    driver.get('https://result.biselahore.com/')
    wait = WebDriverWait(driver, 10)

    # Select Matric option
    try:
        matric_option = wait.until(EC.presence_of_element_located((By.ID, 'rdlistCourse_0')))
        driver.execute_script("arguments[0].click();", matric_option)  # Use JavaScript click to bypass issues
    except Exception as e:
        st.error(f"Error clicking matric option: {e}")
        driver.quit()
        raise

    data = []  # Initialize data storage

    def scrape_roll_number(roll_no):
        try:
            # Input Roll Number
            roll_number = wait.until(EC.presence_of_element_located((By.ID, 'txtFormNo')))
            roll_number.clear()
            time.sleep(0.5)
            roll_number.send_keys(roll_no)
            time.sleep(0.5)

            # Select Exam Type
            exam_type = wait.until(EC.presence_of_element_located((By.ID, 'ddlExamType')))
            select_exam_type = Select(exam_type)
            select_exam_type.select_by_visible_text('Part-I (ANNUAL)')  # Replace with desired option

            # Select Year
            exam_year = wait.until(EC.presence_of_element_located((By.ID, 'ddlExamYear')))
            select_exam_year = Select(exam_year)
            select_exam_year.select_by_visible_text('2024')  # Replace with desired year

            # Submit Form
            submit_button = wait.until(EC.element_to_be_clickable((By.ID, "Button1")))
            driver.execute_script("arguments[0].click();", submit_button)

            # Wait for Results
            registration_no = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '#lblBFARM'))).text

            # Collect Data
            detail = {
                'roll_no': roll_no, 
                'registration_no': registration_no
            }

            data.append(detail)
            print(detail)

            # Navigate back to the form page
            driver.back()
            time.sleep(2)  # Give time for the form page to reload

            return True
        except TimeoutException:
            st.warning(f"No data found for Roll No: {roll_no}")
            driver.get('https://result.biselahore.com/')  # Refresh the page
            time.sleep(2)
            try:
                matric_option = wait.until(EC.presence_of_element_located((By.ID, 'rdlistCourse_0')))
                driver.execute_script("arguments[0].click();", matric_option)
            except Exception as inner_e:
                st.error(f"Error refreshing matric option: {inner_e}")
            return False
        except Exception as e:
            st.warning(f"Failed to scrape data for Roll No: {roll_no} - {e}")
            driver.get('https://result.biselahore.com/')  # Refresh the page
            time.sleep(2)
            try:
                matric_option = wait.until(EC.presence_of_element_located((By.ID, 'rdlistCourse_0')))
                driver.execute_script("arguments[0].click();", matric_option)
            except Exception as inner_e:
                st.error(f"Error refreshing matric option: {inner_e}")
            return False

    for roll_no in range(starting_roll_no, ending_roll_no + 1):
        scrape_roll_number(roll_no)

    # Close the browser
    driver.quit()

    # Create DataFrame and Display Results
    df = pd.DataFrame(data)
    st.dataframe(df)

    # Convert DataFrame to CSV
    csv = df.to_csv(index=False)

    # Create a download button
    st.download_button(
        label="Download CSV",
        data=csv,
        file_name=f'{output_filename}.csv',
        mime='text/csv',
    )
