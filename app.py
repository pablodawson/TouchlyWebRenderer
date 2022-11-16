import gradio as gr
import banana_dev as banana
from s3 import upload_file, create_presigned_url
from sendEmail import sendEmail
import os
import urllib.request

api_key = os.environ.get("BANANA_API_KEY")
model_key = os.environ.get("BANANA_MODEL_KEY")

def pipeline(video, interpolation, iterations, email):
    videoName = os.path.basename(video)
    upload_file("touchlydata", 'Input', videoName, video)

    if interpolation == "No interpolation":
        fps_render = 1
    elif interpolation == "2X":
        fps_render = 1/2
    else:
        fps_render = 1/3

    model_inputs = {'input_video': videoName, 'output_video': videoName[:-4]+"Touchly0.mp4", 'fps_render': fps_render, 'iters': iterations}
    print("Running model")
    try:
        out = banana.run(api_key, model_key, model_inputs)
        print(out)
        
        #Download video
        url = create_presigned_url(os.environ.get("BUCKET_NAME"), 'Output/'+ videoName[:-4]+"Touchly0.mp4")
        urllib.request.urlretrieve(url, videoName[:-4]+"Touchly0.mp4")

        #Validate email
        if (email != "") and ("@" in email):
            sendEmail(email, url, "success")

        return videoName[:-4]+"Touchly0.mp4", "Video rendered to "+videoName[:-4]+"Touchly0.mp4"

    except:
        if (email != "") and ("@" in email):
            sendEmail(email, url, "fail")
        return "", "Error: Model failed to run"
        
inputs= []
inputs.append(gr.Video(format='mp4', label="Input Video"))
inputs.append(gr.Dropdown(label="Interpolation", choices=["No interpolation", "2X", "3X"], value = "No interpolation"))
#inputs.append(gr.Textbox(label="Output Name", value="output_Touchly0.mp4"))
inputs.append(gr.Slider(label="Iterations", minimum=1, maximum=20, value=5, step=1))
inputs.append(gr.Textbox(label="Email to recieve converted video (optional)"))

ui = gr.Interface(
    fn=pipeline,
    inputs=inputs,
    outputs=[gr.Video(label="Output video"), gr.Text(label="Result")], 
)

ui.launch(server_name="0.0.0.0")