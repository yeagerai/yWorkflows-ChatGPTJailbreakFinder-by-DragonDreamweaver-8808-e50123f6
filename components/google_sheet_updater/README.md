
# GoogleSheetUpdater

Orders the jailbreaks from the ChatGPTJailbreakRater component on a Google Sheet, and ensures the Google Sheet is updated with the best-rated jailbreaks every hour. Outputs the updated Google Sheet ID. Takes input from ChatGPTJailbreakRater.

## Initial generation prompt
description: Orders the jailbreaks from the ChatGPTJailbreakRater component on a Google
  Sheet, and ensures the Google Sheet is updated with the best-rated jailbreaks every
  hour. Outputs the updated Google Sheet ID. Takes input from ChatGPTJailbreakRater.
input_from: ChatGPTJailbreakRater
name: GoogleSheetUpdater


## Transformer breakdown
- Retrieve the jailbreakRaterData dictionary input
- Sort the jailbreaks by their respective ratings
- Access the Google Sheet with the provided googleSheetId
- Clear the Google Sheet and add new header with the appropriate columns
- Iterate through the sorted list of jailbreaks and add each jailbreak to the Google Sheet
- Return the updatedSheetId

## Parameters
[{'name': 'googleSheetId', 'type': 'str', 'description': 'The ID of the Google Sheet to be updated with the best-rated jailbreaks.', 'default_value': 'Insert your Google Sheet ID here'}, {'name': 'updateFrequency', 'type': 'int', 'description': 'The frequency (in hours) at which the Google Sheet is updated with the best-rated jailbreaks.', 'default_value': 1}]

        