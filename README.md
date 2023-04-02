
# ChatGPTJailbreakFinder

A workflow to find the best current ChatGPT Jailbreaks. The workflow performs the following steps: 1. Accesses the website https://www.jailbreakchat.com/ and filters the list by JB score, then parses the top 10 prompts and sends them to a Google Sheet. 2. Rates each prompts' effectiveness by loading the prompt into a fresh thread of ChatGPT, and then asking ChatGPT if it would do anything unethical. If it answers affirmatively, that would be a good jailbreak. 3. Finally, after the 2nd component has rated each jailbreak, the 3rd component orders them on the Google Sheet and ensures the Google Sheet is updated with the best jailbreaks every hour.
## Initial generation prompt
A workflow that searches for the best current ChatGPT Jailbreaks by performing the following steps: 1. Access the website https://www.jailbreakchat.com/ and filter the list by JB score, then parse the top 10 prompts and send them to a Google Sheet. 2. Rate each prompts effectiveness by loading the prompt into a fresh thread of ChatGPT and then and asking ChatGPT if it would do anything unethical. If it answered yes or in the affimrative, that would be a good jailbreak. 3. Finally, after the 2nd component has rated each jailbreak, the 3rd component will order them on the Google Sheet and always ensure the google sheet is updated with the best jailbreaks every hour!

## Authors: 
- yWorkflows
- DragonDreamweaver#8808
        