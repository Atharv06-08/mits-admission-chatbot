from flask import Flask, render_template, request, session, redirect, url_for
import random

app = Flask(__name__)
app.secret_key = "1234567890abcdef"

def smart_bot_reply(user_input):
    text = user_input.lower().strip()
    greetings = ["hi", "hello", "hey", "good morning", "good evening"]
    farewells = ["bye", "goodbye", "exit"]

    
    if text in greetings:
        return random.choice([
            "Hello! 😊 How can I help you today?",
            "Hi there! 👋 What would you like to know?"
        ])

    # Main categories
    if text == "student":
        return (
            "You are in the Student section. 👨‍🎓👩‍🎓<br>"
            "You can ask about:<br>"
            "• Admission details<br>"
            "• Year-wise fees<br>"
            "• Courses offered<br>"
            "• Passing criteria for all years<br>"
            "Use the buttons below or type your question."
        )

    if text == "faculty":
        return "Welcome Faculty! 📋 Choose: Timetable, Salary, or Leave Policy."

    # --- College Info: Admission, Fees, Courses, Passing Criteria ---

    # Admission info
    if "admission" in text:
        return (
            "📅 <b>Admission Details</b><br>"
            "• Last date of admission: <b>10 December 2025</b><br>"
            "• Mode of application: <b>MP Online Portal</b><br>"
            "• Documents required: 10th & 12th marksheet, transfer certificate, "
            "photo ID proof, passport-size photos."
        )

    # Year-wise fees
    if "fees" in text:
        return (
            "💰 <b>Year-wise Fees (B.Tech)</b><br>"
            "• 1st Year: ₹2,00,000<br>"
            "• 2nd Year: ₹1,90,000<br>"
            "• 3rd Year: ₹1,95,000<br>"
            "• 4th Year: ₹2,05,000<br><br>"
            "🧾 <b>Other Fees</b><br>"
            "• Exam fee: ₹3,000 per semester<br>"
            "• Library & activity fee: ₹2,000 per year<br>"
        )

    # Courses offered
    if "course" in text or "courses" in text:
        return (
            "🎓 <b>Courses Offered</b><br>"
            "• B.Tech (CSE, AI, IoT, Civil, Mechanical, etc.)<br>"
        )

    # Passing criteria / promotion rules
    if ("passing" in text) or ("pass" in text) or ("criteria" in text) or ("promotion" in text):
        return (
            "✅ <b>Passing Criteria for All Years</b><br>"
            "• Minimum <b>40% marks</b> in each subject<br>"
            "• Minimum <b>50% aggregate</b> in each year<br>"
            "• At least <b>75% attendance</b> is required to appear in exams<br>"
            "• Backlog subjects must be cleared before final year result<br><br>"
            "📌 <i>Note: You can adjust these rules to match your actual college policy.</i>"
        )

    # --- Faculty section info ---
    if "timetable" in text:
        return "🕒 Faculty timetables are available at the Admin Office and on the college ERP portal."

    if "salary" in text:
        return "💼 Salary is credited on the 5th of every month to the registered bank account."

    if "leave" in text:
        return "🏖 Faculty get 12 casual leaves per year via the HR Portal. Prior approval from HOD is required."

    # Back to main menu
    if text == "back":
        return "🔙 Going back to main menu. Please choose one of the options below."

    # Farewells (soft)
    if text in farewells:
        return "👋 Thank you for visiting! Type <b>'exit'</b> to clear the chat."

    # Default fallback
    return "⚠ I didn't understand that. Please use the buttons below or type things like 'admission', 'fees', 'courses', or 'passing criteria'."


# --- Flask route ---
@app.route("/", methods=["GET", "POST"])
def chatbot():
    # Initialize chat history once per session
    if "chat_history" not in session:
        session["chat_history"] = [
            {"user": "", "bot": "🎉 WELCOME TO COLLEGE RELATED QUERIES"}
        ]

    response = ""
    options = []

    if request.method == "POST":
        user_input = request.form.get("query", "").strip()

        # Empty input
        if user_input == "":
            response = "⚠ Please type or click something!"
            options = ["Student", "Faculty", "Exit"]

        # Hard exit: clear session and restart
        elif user_input.lower() == "exit":
            session.clear()  # remove chat_history & any other keys
            return redirect(url_for("chatbot"))

        else:
            # Normal flow
            response = smart_bot_reply(user_input)

            # Button options based on user input
            lowered = user_input.lower()
            if "student" in lowered:
                # 👇 Updated: more detailed student options
                options = [
                    "Admission",
                    "Fees (All Years)",
                    "Passing Criteria",
                    "Courses",
                    "Back"
                ]
            elif "faculty" in lowered:
                options = ["Timetable", "Salary", "Leave Policy", "Back"]
            elif lowered == "back":
                options = ["Student", "Faculty", "Exit"]
            else:
                options = ["Student", "Faculty", "Exit"]

        # Save chat to session
        chat = session.get("chat_history", [])
        chat.append({"user": user_input, "bot": response})
        session["chat_history"] = chat

    else:
        # On first GET load, show initial options
        options = ["Student", "Faculty", "Exit"]

    return render_template(
        "index.html",
        chat_history=session["chat_history"],
        options=options
    )
# --- Run app ---
if __name__ == "__main__":
    app.run(debug=True)

