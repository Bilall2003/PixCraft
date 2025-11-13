import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st
from sklearn.cluster import KMeans
import cv2
from rembg import remove
import io
from PIL import Image

class Main:
    def main(Self):
        
        img_upl=st.file_uploader(label="Upload Image",
                key="image_uploader1",
                type=["jpg", "png"]) 
       
        if img_upl is not None:
            # Read and display the uploaded image
            image = Image.open(img_upl)
            if st.button("Show image"):
                st.image(image, caption="🖼 Uploaded Image")
        else:
            st.info("👆 Upload an image to begin.")
            
        if img_upl is not None:
            options = ["Select", "Remove Background", "Blur Image", "Color Quantization"]
            choice = st.selectbox("Choose Service", options, key="select_box1")

            if choice == "Remove Background":
                try:
                    if len(image.shape) == 2:
                        st.warning("⚠️ Grayscale image detected.")
                    if image.shape[2] == 4:
                        st.warning("⚠ RGBA image detected — using only RGB channels.")
                    if image.shape[2] != 3:
                        st.error(f"❌ Unsupported image format with {image.shape[2]} channels.")
                    if image.shape[2]==3:
                        try:
                            st.success("✅ RGB image detected.")
                            
                            with st.spinner("Generating image......"):
                                rb_img=remove(image)
                                st.image(rb_img,use_container_width=True,caption="Without background")
                                
                            buf=io.BytesIO()
                            plt.imsave(buf,rb_img)
                            buf.seek(0)
                            
                            st.download_button(
                                label="📥Download image",
                                data=buf,
                                file_name="rb_image.png",
                                mime="image/png"
                            )
                        except Exception as e:
                            st.error(f"something went wrong{e}")
                            
                
                except Exception as e:
                    st.error(f"⚠️ Something went wrong: {e}")
                
            elif choice == "Blur Image":
                try:
            
                    if len(image.shape)==2:
                        st.warning("⚠️ Grayscale image detected.")
                    if image.shape[2]==4:
                        st.warning("⚠ RGBA image detected — using only RGB channels.")
                    if image.shape[2]!=3:
                        st.error(f"❌ Unsupported image format with {image.shape[2]} channels.")
                    if image.shape[2]==3:
                        try:
                            st.success("✅ RGB image detected.")
                            
                            ksize = st.slider("Select blur strength", 3, 400, 15, step=2)  # blur strength,step=2 will provide increment by 2 odd number gaussian requirement
                            with st.spinner("Applying blur..."):
                                blur = cv2.GaussianBlur(image, (ksize, ksize), 0)  # ksize,ksize=same amount of blur on both x and y axis u can change it too

                            st.image(blur, caption="Blurred Image", use_container_width=True)
                            
                            buf=io.BytesIO()
                            plt.imsave(buf,blur)
                            buf.seek(0)
                            
                            st.download_button(
                                label="📥Download Image",
                                data=buf,
                                file_name="blur_img.png",
                                mime="image/png"
                            )
                            
                            
                        except Exception as e:
                            st.error(f"something went wrong {e}")
                
                except Exception as e:
                    st.error(f"Something went wrong {e}")
       
            elif choice == "Color Quantization":
                
                try:
                
                    if len(image.shape) == 2:
                        st.warning("⚠️ Grayscale image detected.")
                    if image.shape[2] == 4:
                        st.warning("⚠ RGBA image detected — using only RGB channels.")
                    if image.shape[2] != 3:
                        st.error(f"❌ Unsupported image format with {image.shape[2]} channels.")
                    if image.shape[2]==3:
                        st.success("✅ RGB image detected.")
                    
                        h,w,c=image.shape
                        image_2d=image.reshape((h*w,c))
                        
                        st.info("Number of Colors in image increase Generation time")
                        cluster=st.slider("Select amount of Color",min_value=3,max_value=100)
                        
                        with st.status("Hold on, image is generating....") as status:
                            
                            st.write("Infusing Colors......")
                            model=KMeans(n_clusters=cluster)
                            labels=model.fit_predict(image_2d)
                            
                            rgb_codes=model.cluster_centers_.round(0).astype(np.uint8)
                            
                            quantized_img=np.reshape(rgb_codes[labels],(h,w,c))
                            
                            fig,ax=plt.subplots(figsize=(15,6),nrows=1,ncols=2,dpi=250)
                            
                            ax[0].imshow(image)
                            ax[0].set_title("Original image")
                            ax[0].axis("off")
                            ax[1].imshow(quantized_img)
                            ax[1].set_title("Quantized image")
                            ax[1].axis("off")
                            
                        status.update(label="✅Image Generated",state="complete")
                        st.pyplot(fig)
                            
                        buf = io.BytesIO()
                        plt.imsave(buf, quantized_img)
                        buf.seek(0)

                        # Download button
                        st.download_button(
                            label="📥Download Quantized Image",
                            data=buf,
                            file_name="quantized_image.png",
                            mime="image/png"
                        )
                
                except Exception as e:
                    st.error(f"⚠ Something Went Wrong {e}")
                    
       
class App(Main):
    
    def app(self):
        
        st.sidebar.markdown("""
            <h3 style="
                padding-top: 50px;
                font-size: 40px;
                color: pink;
                text-align: center;
                font-weight: 800;
            ">
            Pixcraft ✨
            </h3>
            """, unsafe_allow_html=True)
        
        st.sidebar.markdown("""
                <h3 style="
                font-size: 20px;
                font-weight: 500;
                text-align:center;
                ">
                Pixcraft Offers Various Services:
                You Can 👇🏻\n
                
            1️⃣ Remove Backgrounds:Instantly remove image backgrounds with precision — perfect for product photos, portraits, or creative designs.

            2️⃣ Blur Images:
            Apply customizable blur effects to highlight subjects or create an aesthetic depth-of-field look.

            3️⃣ Color Quantization:
            Simplify your images by reducing the number of colors while maintaining visual quality — ideal for compression, artistic effects, or preprocessing in computer vision tasks.
                </h3>
                """,unsafe_allow_html=True)
        


        st.sidebar.markdown("""
            <style>
            .blink-warning {
                animation: blinker 1s linear infinite;
                
                font-weight: bold;
                color:red;
                font-size:18px;
            }

            @keyframes blinker {
                50% {
                    opacity: 0.2;
                }
            }
            
            </style>
            """, unsafe_allow_html=True)

        # Apply the blinking class manually to the warning container
        st.sidebar.markdown(
            '<div class="blink-warning">⚠️ Only RGB images supported here...</div>',
            unsafe_allow_html=True
        )




    
obj=App()
obj.app()
obj.main()
        
    
