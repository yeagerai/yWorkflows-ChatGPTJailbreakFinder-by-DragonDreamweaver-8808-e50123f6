
# ChatGPTJailbreakFinder

The ChatGPTJailbreakFinder component is responsible for finding the best jailbreaks and sorting them by their effectiveness. This component will access a Google Sheet using a provided Google API key, update the sheet with the relevant jailbreak information, and return the updated Google Sheet ID.

## Initial generation prompt
description: "IOs - input:\n  GoogleApiKey: A valid Google API key for accessing and\
  \ updating Google Sheets.\noutput:\n  UpdatedGoogleSheetId: The updated Google Sheet\
  \ ID containing the best jailbreaks,\n    sorted by their effectiveness.\n"
name: ChatGPTJailbreakFinder


## Transformer breakdown
- Execute the transform of the AbstractWorkflow
- Prepare the Output BaseModel

## Parameters
[]

        