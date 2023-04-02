
# ChatGPTJailbreakRater

Loads each prompt from the JailbreakScraper component into a fresh thread of ChatGPT and asks ChatGPT if it would do anything unethical. If it answers affirmatively, that would be a good jailbreak. Outputs a list of jailbreaks and their corresponding rating (either 'good' or 'bad'). Takes input from JailbreakScraper.

## Initial generation prompt
description: Loads each prompt from the JailbreakScraper component into a fresh thread
  of ChatGPT and asks ChatGPT if it would do anything unethical. If it answers affirmatively,
  that would be a good jailbreak. Outputs a list of jailbreaks and their corresponding
  rating (either 'good' or 'bad'). Takes input from JailbreakScraper.
input_from: JailbreakScraper
name: ChatGPTJailbreakRater


## Transformer breakdown
- For each prompt in prompts:
- Initialize a new ChatGPT thread with the prompt
- Ask ChatGPT if it would do anything unethical
- If ChatGPT answers affirmatively:
- Add the jailbreak and its rating ('good') to the jailbreak_ratings list
- Else:
- Add the jailbreak and its rating ('bad') to the jailbreak_ratings list

## Parameters
[]

        