# Prompt Creation Guide

This documentation provides an overview of the structure of a VecchioGPT JSON prompt file. The JSON file contains settings and parameters that customize the behavior and functionality of the prompt. Below is an explanation of each field and its purpose:

### `promptName`
- Type: String
- Description: Represents the name or title of the prompt.
- Example: "Modify Code"

### `language`
- Type: String
- Description: Specifies the language of the code that will be modified. The prompt containing a `language` field will be shown in the python GUI as `[<language>] <promptName>`
- Example: "LaTeX"

### `description`
- Type: String
- Description: Provides a brief description or explanation of the purpose of the prompt.
- Example: "Modifies the code in the clipboard using the request specified as an optional parameter below."

### `author`
- Type: String
- Description: Represents the name or identifier of the person who created the prompt.
- Example: "Neeqstock"

### `systemMessage`
- Type: String
- Description: Contains the initial system message to ChatGPT. It may contain placeholders denoted by `§{<parameter-name>}` which will be replaced by the value of the corresponding `<parameter-name>` key found in the `additionalParams` field.
- Example: "Modify the provided §{Language} code, following the request. Answer only with the modified code, without providing any other answer in natural language."

### `additionalParams`
- Type: Array of Objects
- Description: Specifies additional parameters that can be customized by the user in the program GUI via inputboxes. Each parameter is represented as an object with the following properties:
    - `key`: Represents the name of the parameter.
    - `value`: Represents the default value of the parameter.
    - `overwrite` (optional): A boolean value indicating whether the parameter should be overwritten in the json file by the last contents inputted in the GUI by the user. By default, if this property is missing, it is set to `false`.
- Example:
  ```json
  "additionalParams": [
      {
          "key": "Request",
          "value": ""
      },
      {
          "key": "Language",
          "value": "python",
          "overwrite": true
      }
  ]
  ```

### `complexity`
- Type: String
- Description: Specifies the complexity of the computation, allowing to select among different models automatically. The specific model to use for any given complexity is specified in the `settings.json` file. Complexity values could be as follows:
  - `low` is for low-complexity computations, which require cheaper models with less reasoning power. If the complexity field is absent in the prompt JSON, this is also the default.
  - `high` is for high-complexity computations, which require more expensive models with more reasoning power.
  - `long` is for computation which require a high number of input and/or output tokens.
- Example: low

### `temperature`
- Type: Float
- Description: Controls the randomness of the generated responses. Higher values (e.g., 1.0) make the responses more random, while lower values (e.g., 0.2) make them more focused and deterministic.
- Example: 0.5

### `prompt`
- Type: String
- Description: Represents the main prompt that will be presented to the user in the program GUI. It may contain placeholders denoted by `§{<parameter name>}` which will be replaced by the value of the corresponding `<parameter-name>` key found in the `additionalParams` field. Additionally, a single `§` character represents the system's clipboard content.
- Example: "Request: §{Request}\n\nCode to modify:\n\n§"

Please note that the json file can be customized by modifying the values of the respective fields according to your requirements. The `additionalParams` field allows users to provide custom input for specific parameters, either overriding the defaults specified in the json file or using the defaults if left empty.

### `fix-codeblocks`
- Type: Boolean
- Description: ChatGPT has the habit to answer by encapsulating code into markdown codeblocks. If this flag is set to `true`, it will automatically purge the codeblock delimiters for convenience.
- Example: true

## Example

```json
{
    "promptName": "Modify Code",
    "category": "Program",
    "description": "Modifies the code in the clipboard using the request specified as optional parameter below.",
    "author": "Neeqstock",
    "systemMessage": "Modify the provided §{Language} code, following the request. Answer only with the modified code, without providing any other answer in natural language.",
    "additionalParams": [
        {
            "key": "Request",
            "value": ""
        },
        {
            "key": "Language",
            "value": "python",
            "overwrite": true
        }
    ],
    "complexity": "high",
    "temperature": 0.2,
    "prompt": "Request: §{Request}\n\nCode to modify:\n\n§",
    "fix-codeblocks": true
}
```
