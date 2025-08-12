# from  boltiotai import openai
# import os
# import sys

# print("Assistant: Hello! How can I assist you today?\n")
# Question=input("You: ")
# while True:
#     openai.api_key = os.environ['OPENAI_API_KEY']
#     if openai.api_key == "":
#       sys.stderr.write("""
#       You haven't set up your API key yet.

#       If you don't have an API key yet, visit:

#       https://platform.openai.com/signup

#       1. Make an account or sign in
#       2. Click "View API Keys" from the top right menu.
#       3. Click "Create new secret key"

#       Then, open the Secrets Tool and add OPENAI_API_KEY as a secret.
#       """)
#       exit(1)

#     response = openai.chat.completions.create(
#         model="gpt-3.5-turbo",
#         messages=[{
#             "role": "system",
#             "content": "You are a helpful assistant."
#         }, 
#                   #{
#         #     "role": "user",
#         #     "content": "Who won the world series in 2020?"
#         # }, {
#         #     "role":
#         #     "assistant",
#         #     "content":
#         #     "The Los Angeles Dodgers won the World Series in 2020."
#         # }, 
#                   {
#             "role": "user",
#             "content": Question
#         }])
#     output=response["choices"][0]["message"]["content"]
#     print("Assistant:",output,"\n")

#     Question=input("You: ")


#Custom recipe generator


from boltiotai import openai
import os
from flask import Flask, render_template_string, request
openai.api_key = os.environ['OPENAI_API_KEY']
def generate_tutorial(components):

 response = openai.chat.completions.create(
  model="gpt-3.5-turbo",
  messages=[{
   "role": "system",
   "content": "You are a helpful assistant"
  }, {
   "role":
   "user",
   "content":
   f"Suggest a recipe using the items listed as available. Make sure you have a nice name for this recipe listed at the start. Also, include a funny version of the name of the recipe on the following line. Then share the recipe in a step-by-step manner. In the end, write a fun fact about the recipe or any of the items used in the recipe. Here are the items available: {components}, Haldi, Chilly Powder, Tomato Ketchup, Water, Garam Masala, Oil"
  }])
 return response['choices'][0]['message']['content']

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def hello():
 output = ""
 if request.method == 'POST':
  components = request.form['components']
  output = generate_tutorial(components)
# This is a HTML template for a Custom Recipe Generator web page. It includes a form for users to input a list of ingredients/items they have, and two JavaScript functions for generating a recipe based on the input and copying the output to the clipboard. The template uses the Bootstrap CSS framework for styling.
 return render_template_string('''

<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Custom Recipe Generator</title>
    <link href="https://cdn.jsdelivr.net/npm/tailwindcss@2.2.19/dist/tailwind.min.css" rel="stylesheet">
    <link href="https://fonts.googleapis.com/css2?family=Lora:wght@400;700&display=swap" rel="stylesheet">
    <style>
        body {
            background: linear-gradient(135deg, #f5f6f5 0%, #e8ecef 100%), url('https://www.transparenttextures.com/patterns/tablecloth.png');
            background-blend-mode: overlay;
            transition: background 0.3s ease, color 0.3s ease;
            color: #1e2a44;
        }
        body.dark {
            background: linear-gradient(135deg, #1e2a44 0%, #2f3b5c 100%), url('https://www.transparenttextures.com/patterns/tablecloth.png');
            background-blend-mode: overlay;
            color: #e6e9ec;
        }
        .container {
            transition: transform 0.3s ease, box-shadow 0.3s ease, background 0.3s ease;
            background: #ffffff;
            border: 1px solid #d4d8db;
        }
        .dark .container {
            background: #141c30;
            border: 1px solid #3b4a6b;
            box-shadow: 0 10px 20px rgba(0, 0, 0, 0.5);
        }
        .container:hover {
            transform: translateY(-2px);
            box-shadow: 0 10px 20px rgba(0, 0, 0, 0.15);
        }
        .btn-primary {
            background: linear-gradient(to right, #1e3a8a, #d4a017);
            position: relative;
            overflow: hidden;
        }
        .dark .btn-primary {
            background: linear-gradient(to right, #15295e, #b3870f);
        }
        .btn-primary::after {
            content: '';
            position: absolute;
            top: 50%;
            left: 50%;
            width: 0;
            height: 0;
            background: rgba(255, 255, 255, 0.2);
            border-radius: 50%;
            transform: translate(-50%, -50%);
            transition: width 0.5s ease, height 0.5s ease;
        }
        .btn-primary:hover::after {
            width: 250px;
            height: 250px;
        }
        .btn-primary:hover {
            background: linear-gradient(to right, #d4a017, #1e3a8a);
        }
        .dark .btn-primary:hover {
            background: linear-gradient(to right, #b3870f, #15295e);
        }
        .output-card {
            animation: fadeIn 0.5s ease-out;
            background: #f9fafb;
        }
        .dark .output-card {
            background: #1e2a44;
            border-color: #3b4a6b;
        }
        @keyframes fadeIn {
            from { opacity: 0; transform: scale(0.98); }
            to { opacity: 1; transform: scale(1); }
        }
        .loading-spinner {
            animation: pulse 1.5s infinite;
        }
        @keyframes pulse {
            0%, 100% { opacity: 1; }
            50% { opacity: 0.6; }
        }
        .dark .input-field {
            background: #2a3757;
            border-color: #3b4a6b;
            color: #e6e9ec;
        }
        .dark .input-field::placeholder {
            color: #8a94a6;
        }
        .dark .text-gray-800 {
            color: #e6e9ec;
        }
        .dark .text-navy-700 {
            color: #a3bffa;
        }
        .dark .bg-white {
            background: #1e2a44;
        }
        .dark .border-navy-200 {
            border-color: #3b4a6b;
        }
        .toggle-btn {
            transition: background 0.3s ease, transform 0.3s ease;
        }
        .toggle-btn:hover {
            transform: scale(1.05);
        }
    </style>
    <script>
      async function generateTutorial() {
        const components = document.querySelector("#components").value;
        const output = document.querySelector("#output");
        const loadingSpinner = document.querySelector("#loading-spinner");
        const outputCard = document.querySelector("#output-card");
        output.textContent = "";
        outputCard.classList.remove("output-card");
        loadingSpinner.classList.remove("hidden");
        const response = await fetch("/generate", {
          method: "POST",
          body: new FormData(document.querySelector("#tutorial-form")),
        });
        const newOutput = await response.text();
        loadingSpinner.classList.add("hidden");
        output.textContent = newOutput;
        outputCard.classList.add("output-card");
      }
      function copyToClipboard() {
        const output = document.querySelector("#output");
        const textarea = document.createElement("textarea");
        textarea.value = output.textContent;
        document.body.appendChild(textarea);
        textarea.select();
        document.execCommand("copy");
        document.body.removeChild(textarea);
        alert("Recipe copied to clipboard!");
      }
      function toggleTheme() {
        document.body.classList.toggle("dark");
        const toggleBtn = document.querySelector("#toggle-theme");
        toggleBtn.textContent = document.body.classList.contains("dark") ? "☀️ Light Mode" : "🌙 Dark Mode";
      }
    </script>
</head>
<body class="min-h-screen flex items-center justify-center p-4 sm:p-6 font-lora bg-cover">
    <div class="container max-w-3xl mx-auto rounded-xl shadow-lg p-6 sm:p-8 md:p-10">
        <div class="flex justify-between items-center mb-6">
            <h1 class="text-4xl sm:text-5xl font-bold text-navy-700 dark:text-navy-400 tracking-tight">
                Recipe Generator
            </h1>
            <button
                id="toggle-theme"
                class="toggle-btn bg-gray-200 dark:bg-gray-700 text-gray-800 dark:text-gray-200 px-4 py-2 rounded-lg text-base"
                onclick="toggleTheme()"
            >
                🌙 Dark Mode
            </button>
        </div>
        <form id="tutorial-form" onsubmit="event.preventDefault(); generateTutorial();" class="mb-8">
            <div class="mb-6">
                <label for="components" class="block text-lg font-semibold text-gray-800 mb-3">
                    Available Ingredients
                </label>
                <input
                    type="text"
                    class="input-field w-full p-4 border border-navy-200 rounded-lg focus:outline-none focus:ring-2 focus:ring-navy-500 transition bg-navy-50 placeholder-gray-500 text-base"
                    id="components"
                    name="components"
                    placeholder="Enter ingredients, e.g., Bread, Chicken, Tomato"
                    required
                />
            </div>
            <button
                type="submit"
                class="w-full btn-primary text-white font-semibold py-3 rounded-lg text-base transition duration-300 transform hover:scale-102"
            >
                Generate Recipe
            </button>
        </form>
        <div id="output-card" class="rounded-lg shadow-md p-6 sm:p-8 relative">
            <div class="flex justify-between items-center mb-4">
                <h2 class="text-xl font-semibold text-navy-700">Your Recipe</h2>
                <button
                    class="bg-navy-600 dark:bg-navy-700 text-white px-4 py-2 rounded-lg hover:bg-navy-700 dark:hover:bg-navy-800 transition duration-300 transform hover:scale-105 text-base"
                    onclick="copyToClipboard()"
                >
                    Copy Recipe
                </button>
            </div>
            <div id="loading-spinner" class="hidden absolute inset-0 flex items-center justify-center bg-opacity-75 rounded-lg">
                <div class="loading-spinner text-navy-600 dark:text-navy-400 text-base font-semibold">Preparing your recipe...</div>
            </div>
            <pre id="output" class="text-gray-800 dark:text-gray-200 whitespace-pre-wrap bg-white p-5 rounded-lg border border-navy-200 min-h-[200px] text-base">{{ output }}</pre>
        </div>
    </div>
</body>
</html>
''',
                output=output)


@app.route('/generate', methods=['POST'])
def generate():
 components = request.form['components']
 return generate_tutorial(components)
if __name__ == '__main__':
 app.run(host='0.0.0.0', port=8080)



