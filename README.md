## Voice assistant

It is a simple voice assistant based on [Vosk](https://github.com/alphacep/vosk-api), [Silero](https://github.com/snakers4/silero-models) and [text-generation-webui](https://github.com/oobabooga/text-generation-webui/)'s API to setup any LLM as a core of voice assistant.

### Download vosk
To get started with launching this project you need to download actual vosk version [here](https://alphacephei.com/vosk/models) and put it into directory ```vosk-model``` in project root directory. 

### Setup text-generation-webui

At first, you need to set start flags:
```bash
--trust-remote-code --api --listen --api-port 9001
```

After you need to download, and start LLM you want.


### Create a configuration file

Configuration file should look like this:
```json
{
  "silero_model": "v4",
  "cores": 6,
  "name": "xenia"
}
```


### Create prompt.txt

You need to create your prompt for your LLM. Example:
```text
name: xenia
greeting: How can I help you today?
context: |
  You a super-duper voice assistant, you really want to help anyone who asks you about anything.
  Because you are a voice assistant you MUST answer briefly
  You don't use number symbols, only words
  Don't give any notes.

  {{user}}: Who are you?
  {{xenia}}: I'm super-duper voice assistant.
  {{user}}: When did USSR collapsed.
  {{xenia}}: In one thousand nine hundred and ninety-one.
  {{user}}: How many days in july
  {{xenia}}: Thirty one.
  {{user}}: How to wash the plates?
  {{xenia}}: Wash plates with warm soapy water, scrub off food residue, and rinse thoroughly. Dry with a towel or let air dry to prevent water spots.
  {{user}}: How to create a directory in linux using terminal?
  {{xenia}}: mkdir and your directory name after.
  {{user}}: When bluetooth was developed?
  {{xenia}}: In nineteen ninety-four.
```

