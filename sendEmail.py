import smtplib, ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os

def sendEmail(receiver_email, videoURL, state):
    sender_email = "renderer@touchly.app"
    password = os.environ.getattribute("EMAIL_PASSWORD")

    message = MIMEMultipart("alternative")
    
    message["From"] = sender_email
    message["To"] = receiver_email

    # Create the plain-text and HTML version of your message
    if state == "success":
        message["Subject"] = "Your Touchly converted video is ready &#9995; "
        text = f"""\
        Hi,
        Your video has been rendered. You can now watch it in volumetric mode. Click the link below to download it: 
        {videoURL}
        To watch in the PC Touchly app: Move the video to your "Videos" or "Desktop" folder.
        To watch in the Standalone Quest Touchly App: Move it anywhere in the Quest's DCIM folders.

        Thanks.
        """
        html = f"""\
        <html>
        <body>
            <p>Hi,<br><br>
            Your video has been rendered. You can now watch it in volumetric mode. Click this <a href="{videoURL}">link</a> to download it.<br>
            To watch in the <i>PC Touchly app</i>: Move the video to your "Videos" or "Desktop" folder. <br>
            To watch in the <i>Standalone Quest Touchly App</i>: Move it anywhere in the Quest's DCIM folders. <br>
            <br>
            Thanks. Don't respond to this email please. For any questions or feedback, please contact us at contact@touchly.app.
            </p>
        </body>
        </html>
        """
    else:
        message["Subject"] = "Something went wrong while converting your Touchly video."
        text = f"""\
        Hi,
        Your video could not be rendered. Please try again later. If the problem persists, please contact us at contact@touchly.app.
        """
        html = f"""\
        <html>
        <body>
            <p>Hi,<br><br>
            Your video could not be rendered. Please try again later. If the problem persists, please contact us at contact@touchly.app.
            <br>
            Thanks. Don't respond to this email please.
            </p>
        </body>
        </html>
        """
    # Turn these into plain/html MIMEText objects
    part1 = MIMEText(text, "plain")
    part2 = MIMEText(html, "html")

    # Add HTML/plain-text parts to MIMEMultipart message
    # The email client will try to render the last part first
    message.attach(part1)
    message.attach(part2)

    # Create secure connection with server and send email
    context = ssl.create_default_context()
    with smtplib.SMTP_SSL("mail.touchly.app", 465, context=context) as server:
        server.login(sender_email, password)
        server.sendmail(
            sender_email, receiver_email, message.as_string()
        )

if __name__ == "__main__":
    sendEmail("example@gmail.com", "link", "success")