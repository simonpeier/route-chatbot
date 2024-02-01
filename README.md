# Route Chatbot

A chatbot based on Google Dialogflow. It has two main abilities. It can calculate routes with the desired means of
transportation. On the other hand it can also find and recommend places (such as restaurants, zoos, etc.) for a specific
location.

## Requirements

Install the following packages to be able to run the chatbot:

```
pip install requests
pip install google-cloud-dialogflow
```

Furthermore, you need to create your own API keys for the API's used.

1. Create a key-file for the dialogflow api according to <insert-link>. Then in the `dialogflow.py` file, replace the
   content of the `GOOGLE_APPLICATION_CREDENTIALS` variable with the path to your own key-file.
2. Create a config.ini file with the following content:
   ```
   [API_KEYS]
   API_GOOGLE_DIRECTIONS = <YOUR_API_KEY>
   ```
   Replace `<YOUR_API_KEY>` with your own google directions api key.