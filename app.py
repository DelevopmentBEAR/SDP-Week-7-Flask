from flask import Flask, render_template, request, send_from_directory, url_for
import os 
import uuid 
import db 

app = Flask(__name__)

# Puts user uploaded images into directory 'user_feedback_images'
app.config['UPLOAD_FOLDER'] = 'user_feedback_images'

@app.route("/")
def homepage():
    return render_template("feeback_form.html")

@app.route("/submit_feedback", methods=["POST"])
def submit_feedback():
    feedback =request.form.to_dict()
    print(feedback)
    
    # Read data from form
    # name = request.form["name"]
    # email = request.form["email"]
    # description = request.form["description"]
    
    # Read image file from the form
    image_file = request.files["image"]
    # Save the image to disk with a unique file name
    # If image has no name;
    if image_file.filename:
        # Unqiue name is given to image file with uuid
        save_filename = f'{uuid.uuid4()}_{image_file.filename}'
        # Join with name for save
        save_location = os.path.join(app.config['UPLOAD_FOLDER'], save_filename)
        # Saves image file with new name to directory
        image_file.save(save_location)
        # Connects back to 'feedback' for database
        feedback['image_path'] = save_filename

    # Save feedback to database
    db.save_feedback(feedback)
    
    #TODO - error handling
    #TODO - security

    return render_template("thank_you.html")

@app.route("/admin")
def admin_page():
    feedbacks = db.get_all_feedbacks()
    if feedbacks is None:
        feedbacks = []
    
    feedback_count = len(feedbacks)
    user_image_location = app.config['UPLOAD_FOLDER']
    return render_template("admin.html", feedback_count=feedback_count, feedbacks=feedbacks, user_image_location=user_image_location)

@app.route("/user_feedback_images/<filename>")
def user_feedback_image(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5001)