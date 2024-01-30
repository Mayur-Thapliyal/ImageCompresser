import streamlit as st
import os,shutil,io
from PIL import Image

def get_image_extension(image: Image):
    return image.format

def is_directory(path):
    return os.path.isdir(path)
def get_image_as_bytes(image):
    buffer = io.BytesIO()
    image.save(buffer, format=get_image_extension(image))
    return buffer.getvalue()


def compress_image_from_path(image_path, output_path, quality):
    with Image.open(image_path) as img:
        img.save(output_path, optimize=True, quality=quality)
def show_and_download_image(image):
    # Display the image
    st.image(image, caption="Streamlit Image", use_column_width=True)

    # Create a download button
    download_button = st.download_button(
        label="Download Image",
        data=get_image_as_bytes(image),
        file_name="streamlit_image.png",
    )

    # Check if the download button is clicked
    if download_button:
        st.success("Download started!")
def compress_PIL_image(image:Image)->(Image):
    image = Image.open(image)
    output_buffer = io.BytesIO()
    image.save(output_buffer ,format=get_image_extension(image), optimize=True, quality=quality)

    # The optimized image data is now stored in the BytesIO object
    # You can access it using getvalue() method
    return image


def copy_root_dir(folder_path: str):
    src_dir_list = folder_path.rstrip('/').split('/')
    replace_dir_name = "copy_" + src_dir_list.pop(-1)
    src_dir_list.append(replace_dir_name)
    new_path = "/".join(src_dir_list)
    if os.path.exists(new_path):
        shutil.rmtree(new_path)
    shutil.copytree(folder_path, new_path, symlinks=False, ignore=None)
    return new_path
    
def traverse_folder(folder_path,quality):
    if is_directory(folder_path):
        for dirs, subdir, files in os.walk(folder_path):
            if files!=[]:
                for file in files:
                    file_path =os.path.join(dirs,file)
                    image_path = file_path
                    output_path = file_path
                    compress_image_from_path(image_path, output_path, quality)
        st.write(f"Compression Done OP folder = {folder_path}")
    
if __name__ == "__main__":
    st.title("Image Compressor")
    folder_path = st.text_input("Image dir I/P")
    quality= st.slider(
        'Select a range of quality',
        0, 100,95)
    if folder_path != None and os.path.isdir(folder_path):
        new_folder_path = copy_root_dir(folder_path)
        traverse_folder(new_folder_path,quality)
    st.write("***OR***")
    uploaded_file = st.file_uploader("Image to Compress",type=['png','webp','jpeg'])
    if uploaded_file:
        # image = Image.open(uploaded_file)
        uploaded_file
        image = compress_PIL_image(image=uploaded_file)
        show_and_download_image(image)
        
        
    