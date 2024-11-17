from flask import Flask, render_template, request, redirect, flash

app = Flask(__name__)
app.secret_key = "your_secret_key"

# Predefined static list of topics
predefined_topics = ["Technology", "Health", "Sports"]

# In-memory storage for user-submitted topics
topics = predefined_topics.copy()


@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        # Get the selected or entered topic
        topic = request.form.get("topic")
        if topic:
            if topic not in topics:  # Avoid duplicate topics
                topics.append(topic)
                flash(f"Topic '{topic}' added successfully!", "success")
            else:
                flash(f"Topic '{topic}' already exists!", "warning")
        else:
            flash("Topic cannot be empty!", "danger")
        return redirect("/")  # Redirect to the home page to display the updated list

    # Render the homepage with the current list of topics
    return render_template(
        "index.html", topics=topics, predefined_topics=predefined_topics
    )


if __name__ == "__main__":
    app.run(debug=True)
