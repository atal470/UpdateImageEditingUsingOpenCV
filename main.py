
from flask import Flask, flash, request, redirect, url_for,request,render_template,make_response
from werkzeug.utils import secure_filename
import os
import cv2
import time
UPLOAD_FOLDER = 'static'
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}

app = Flask(__name__)
app.secret_key = 'super secret key'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
def processimage(filename,operation):

	print(f"The operation is {operation}{filename}")

	img=cv2.imread(f"static/{filename}")
	# response = img.tobytes()
	#
	# # Set content type and caching headers
	# response.headers['Content-Type'] = 'image/jpeg'
	# response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate'
	# response.headers['Pragma'] = 'no-cache'
	# response.headers['Expires'] = '0'
	match operation:
		case "cgray":
			imgprocessed=cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
			newfilename=f"static/{filename}"
			cv2.imwrite(f"static/{filename}", imgprocessed)
			return newfilename
		case "cpng":
			newfilename = f"static/{filename.split('.')[0]}.png"
			cv2.imwrite(f"static/{filename.split('.')[0]}.png", img)
			return newfilename
		case "cjpg":
			newfilename = f"static/{filename.split('.')[0]}.jpg"
			cv2.imwrite(newfilename, img)
			return newfilename

		case "cwebp":
			newfilename = f"static/{filename.split('.')[0]}.webp"
			cv2.imwrite(f"static/{filename.split('.')[0]}.webp", img)
			return newfilename

	pass

@app.route('/')

def hello_world():

	return render_template("index.html")
@app.route('/about')

def about_html():
	return render_template("about.html")

@app.route('/edit',methods=['GET','POST'])
def edit_html():

	if request.method=='POST':

		operation=request.form.get("operation")
		if 'file' not in request.files:
			flash('No file part')
			return redirect(request.url)
		file = request.files['file']

		if file.filename == '':
			flash('No selected file')
			return redirect(request.url)
		if file and allowed_file(file.filename):
			filename = secure_filename(file.filename)
			file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
			new=processimage(filename,operation)
			#
			timestamp = int(time.time())
			redirect_url = url_for('hello_world', _external=True) + f'?timestamp={timestamp}'

			flash(f"The file is <a href='/{new}'>here</a>")
			return redirect(redirect_url)
	return "post"


if __name__ == '__main__':

	app.run(host='0.0.0.0', port=8555)

