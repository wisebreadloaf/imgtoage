import streamlit as st
import replicate
import json
import base64
import requests
import subprocess
import cloudinary
import cloudinary.uploader
import cloudinary.api
import gradio as gr
import cv2
import os


cloud_name = (os.getenv("CLOUD_NAME"),)
cloudinary.config(
    cloud_name=os.getenv("CLOUD_NAME"),
    api_key=os.getenv("CLOUD_API"),
    api_secret=os.getenv("CLOUD_API_SECRET"),
)


st.title("Image to GIF Converter")

input_column, output_column = st.columns(2)

picture = input_column.camera_input("Take a picture")
if picture:
    count = 1
    bytes_data = picture.getvalue()
    try:
        with open(f"./data/captured_image{count}.png", "wb") as f:
            f.write(bytes_data)
    except Exception as e:
        print(f"Error writing file: {e}")
    st.markdown(
        """
        <style>
            .stAlert {
                width: 105%; /* Adjust the width as needed */
                margin: auto; /* Center the alert */
            }
        </style>
        """,
        unsafe_allow_html=True,
    )
    st.success("Image saved successfully.")
st.markdown(
    """
    <style>
        .stFileUploaderFileData {
            margin-top: 20px;
        }
        .st-emotion-cache-1lp7pgu {
            margin-top: 15px;
        }
        .st-emotion-cache-1mdkfbq{
            margin-top: 16px;
        }
    </style>
    """,
    unsafe_allow_html=True,
)
uploaded_file = input_column.file_uploader("Upload an image", type=["jpg", "png"])


def create_gif(image):
    # response = cloudinary.uploader.upload(image)
    # print(response)
    # input_img = response["secure_url"]
    #
    # url = "http://localhost:5000/predictions"
    # headers = {"Content-Type": "application/json"}
    # data = {
    #     "input": {
    #         "image": input_img,
    #         "target_age": "default",
    #     }
    # }
    #
    # response = requests.post(url, headers=headers, json=data)
    # if response.status_code == 200:
    #     with open("output.json", "w") as f:
    #         json.dump(response.json(), f)
    #     print("Response saved to output.json")
    # else:
    #     print(f"Request failed with status code: {response.status_code}")
    #
    # public_ids = [response["public_id"]]
    # image_delete_result = cloudinary.api.delete_resources(
    #     public_ids, resource_type="image", type="upload"
    # )
    # print(image_delete_result)
    response = cloudinary.uploader.upload(image)
    print(response)
    input_img = response["secure_url"]

    output = replicate.run(
        "yuval-alaluf/sam:9222a21c181b707209ef12b5e0d7e94c994b58f01c7b2fec075d2e892362f13c",
        input={
            "image": f"{input_img}",
            "target_age": "default",
        },
    )
    # with open("./data/output.json", "r") as file:
    #     data = json.load(file)
    #
    # output_value = data.get("output")
    # base64_gif = output_value.split(",")[1]
    # gif_data = base64.b64decode(base64_gif)
    # with open("./data/output.gif", "wb") as f:
    #     f.write(gif_data)
    #
    return f'<h8 style = "font-size: 14px;">Output</h8><img style="border: 0.5px solid rgb(225, 225, 225, 0.2); border-radius:15px; height: 378px; width: 378px;" src="{output}" alt="Generated GIF">'


if picture or uploaded_file:
    if picture:
        image_to_process = picture
    else:
        image_to_process = uploaded_file
    output_image = create_gif(image_to_process)
    output_column.markdown(output_image, unsafe_allow_html=True)
    # with open("./data/output.gif", "rb") as f:
    #     st.markdown(
    #         """
    #     <style>
    #         .stDownloadButton button {
    #             width : 380px;
    #             padding: 10px 20px; /* Adjust padding to change size */
    #             font-size: 16px; /* Adjust font size to change text size */
    #         }
    #     </style>
    #     """,
    #         unsafe_allow_html=True,
    #     )
    #
    #     output_column.download_button(
    #         label="Download GIF", data=f, file_name="output.gif", mime="image/gif"
    #     )

path = "/home/bored/Downloads/"

data_folder = "data"
if not os.path.exists(data_folder):
    os.makedirs(data_folder)

iface = gr.Interface(
    fn=create_gif,
    inputs=gr.components.Image(),
    outputs=gr.components.Image(),
    title="Age transformation using Style-GAN",
    description="Upload an image and see yourself age.",
)

iface.launch()
