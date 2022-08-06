# Survey Response Handler

![Site Images](assets/images/landing_image_p3.PNG)

## Intended Purpose of This Application:

This application is intended to handle the responses given to a survey, which was sent out to people to fill in via a Google Form. The survey has 21 different questions. The questions posed to the respondent result in numerical/qualitative data that the program can analyse and return organised data back to the user. The responses to these questions are all recorded on a Google Sheets worksheet which is linked to the form. The survey questions are intended to gather information relating to how much time people spend on social media and how they feel after using the various different social media platforms. 

Link to the Google Form used to carry out the survey: [Google Form Link](https://docs.google.com/forms/d/1gyEQpgbYgeGzc19Oi-IdQpPc_qcEAuxyAMB8eVllUzY/edit?usp=sharing) 

Link to the Google Sheet storing the response data: [Google Sheets Link](https://docs.google.com/spreadsheets/d/16IcQIKeoByhsuDIfVVUuOrqRdb6ImJ_Ck_sUPGSkVFM/edit?usp=sharing)

Link to the live application hosted on heroku: [Live site](https://survey-response-handler.herokuapp.com/)

## Important Note

One important item to note is that there is a counter that is updated on lines 57-58 of run.py, this is commented out to allow the tester of this application to repeatedly run the program. The counter should update with the new row total so it can tell if the form has new survey responses or the data there has already been viwed. If the comments are removed the counter will function as intended.








