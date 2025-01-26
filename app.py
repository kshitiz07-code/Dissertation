from flask import Flask, render_template, request
import os
import pyttsx3
from gtts import gTTS
from googletrans import Translator

app = Flask(__name__)

# Initialize translator
translator = Translator()

# Full Responses Dictionary
RESPONSES = {
    "greetings": {
        "en": "Hello! How can I assist you today?",
        "ne": "नमस्ते! म तपाईंलाई आज कसरी सहयोग गर्न सक्छु?"
    },
    "hi": {
        "en": "Hi there! How can I help you today?",
        "ne": "नमस्ते! म तपाईंलाई कसरी मद्दत गर्न सक्छु?"
    },
    "hello": {
        "en": "Hello! Feel free to ask any question.",
        "ne": "नमस्ते! कुनै पनि प्रश्न सोध्न स्वतन्त्र हुनुहोस्।"
    },
    "loan": {
        "en": "You can apply for various types of loans, such as home loans, personal loans, or education loans. Contact customer support for guidance.",
        "ne": "तपाईं विभिन्न प्रकारका लोनहरूको लागि आवेदन दिन सक्नुहुन्छ, जस्तै घर लोन, व्यक्तिगत लोन, वा शिक्षा लोन। मार्गदर्शनका लागि ग्राहक सहायता सम्पर्क गर्नुहोस्।"
    },
    "balance": {
        "en": "You can check your account balance through our mobile app or visit the nearest ATM.",
        "ne": "तपाईं हाम्रो मोबाइल एप प्रयोग गरेर वा नजिकको एटीएममा गएर आफ्नो खाता ब्यालेन्स जाँच गर्न सक्नुहुन्छ।"
    },
    "interest": {
        "en": "Our savings account offers a competitive interest rate of 4% per annum. Visit our website for details.",
        "ne": "हाम्रो बचत खाताले वार्षिक ४% प्रतिस्पर्धात्मक ब्याज दर प्रदान गर्दछ। विवरणहरूको लागि हाम्रो वेबसाइट भ्रमण गर्नुहोस्।"
    },
    "atm": {
        "en": "Locate the nearest ATM using the ‘ATM Locator’ feature on our mobile app.",
        "ne": "तपाईंको नजिकको एटीएम पत्ता लगाउन हाम्रो मोबाइल एपको 'ATM लोकेटर' सुविधा प्रयोग गर्नुहोस्।"
    },
    "fraud": {
        "en": "If you suspect fraud, report it immediately via our hotline.",
        "ne": "यदि तपाईंलाई ठगीको आशंका छ भने, हाम्रो हटलाइनमा तुरुन्त रिपोर्ट गर्नुहोस्।"
    },
    "credit card": {
        "en": "Apply for a credit card through our website or visit your nearest branch for assistance.",
        "ne": "क्रेडिट कार्डको लागि हाम्रो वेबसाइटमार्फत आवेदन दिनुहोस् वा सहायताको लागि आफ्नो नजिकको शाखामा जानुहोस्।"
    },
    "mobile banking": {
        "en": "Register for mobile banking through our website or nearest branch.",
        "ne": "हाम्रो वेबसाइट वा नजिकको शाखामा गएर मोबाइल बैंकिङको लागि दर्ता गर्नुहोस्।"
    },
    "account opening": {
        "en": "Open an account by submitting required documents such as ID proof and address proof.",
        "ne": "आईडी प्रमाण र ठेगाना प्रमाण जस्ता आवश्यक कागजातहरू बुझाएर खाता खोल्नुहोस्।"
    },
    "currency": {
        "en": "Find live exchange rates for major currencies on our website.",
        "ne": "हाम्रो वेबसाइटमा प्रमुख मुद्राहरूको प्रत्यक्ष विनिमय दर पाउनुहोस्।"
    }
}

# Function to generate English voice using pyttsx3
def generate_english_voice(text):
    engine = pyttsx3.init()
    engine.save_to_file(text, 'static/en_output.mp3')
    engine.runAndWait()

# Function to generate Nepali voice using gTTS
def generate_nepali_voice(text):
    tts = gTTS(text=text, lang='ne')
    tts.save('static/ne_output.mp3')

@app.route("/", methods=["GET", "POST"])
def home():
    user_input = ''
    response = {"en": "", "ne": ""}

    if request.method == "POST":
        user_input = request.form.get("query", "")

        # Convert user input to lowercase for processing
        user_input_lower = user_input.lower()

        # Determine if the user input is in Nepali or English
        if any('\u0900' <= c <= '\u097F' for c in user_input):
            translated_input = translator.translate(user_input, src='ne', dest='en').text.lower()
        else:
            translated_input = user_input_lower

        # Default response
        response = {
            "en": "Sorry, I didn't understand that.",
            "ne": "माफ गर्नुहोस्, मैले बुझिन।"
        }

        # Check for matching keywords
        for key, value in RESPONSES.items():
            if key in translated_input:
                response = value
                break

        # Generate voice outputs
        generate_english_voice(response["en"])
        generate_nepali_voice(response["ne"])

    return render_template("index.html", user_input=user_input, response=response)

if __name__ == "__main__":
    if not os.path.exists('static'):
        os.makedirs('static')
    app.run(debug=True)
