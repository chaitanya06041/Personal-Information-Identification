import React, { useState } from "react";
import "./Home.css";
import { styled } from "@mui/material/styles";
import Button from "@mui/material/Button";
import CloudUploadIcon from "@mui/icons-material/CloudUpload";
import { Viewer } from "@react-pdf-viewer/core";
import "@react-pdf-viewer/core/lib/styles/index.css";
import { OrbitProgress } from "react-loading-indicators";

const VisuallyHiddenInput = styled("input")({
  clip: "rect(0 0 0 0)",
  clipPath: "inset(50%)",
  height: 1,
  overflow: "hidden",
  position: "absolute",
  bottom: 0,
  left: 0,
  whiteSpace: "nowrap",
  width: 1,
});

function Home() {
  const [filePreview, setFilePreview] = useState(null);
  const [fileType, setFileType] = useState("");
  const [isLoaded, setIsLoaded] = useState(false);
  const [maskedImage, setMaskedImage] = useState(null);
  const [extractedData, setExtractedData] = useState(null);

  const handleFileChange = async (event) => {
    const file = event.target.files[0];

    if (file) {
      setIsLoaded(false);
      setFileType(file.type);
      const previewURL = URL.createObjectURL(file);
      setFilePreview(previewURL);

      const formData = new FormData();
      formData.append("image", file);

      try {
        const response = await fetch("http://127.0.0.1:5000/mask-image", {
          method: "POST",
          body: formData,
        });

        if (response.ok) {
          // Get the image blob and create an image URL
          const blob = await response.blob();
          const imageURL = URL.createObjectURL(blob);
          setIsLoaded(true);
          setMaskedImage(imageURL);
          console.log(imageURL);
        } else {
          console.error("Error uploading image");
        }
      } catch (error) {
        console.error("Error:", error);
      }
    }
  };

  return (
    <div className="home">
      <div className="home_container">
        <div className="input_row">
          Upload a file to mask
          <Button
            component="label"
            role={undefined}
            variant="contained"
            tabIndex={-1}
            startIcon={<CloudUploadIcon />}
          >
            Upload file
            <VisuallyHiddenInput
              type="file"
              accept=".jpg, .jpeg, .png, .pdf"
              onChange={handleFileChange}
            />
          </Button>
        </div>

        {filePreview && (
          <div className="file_previews">
            <div className="original_image">
              <p>Original File</p>
              <div className="image_container">
                {filePreview && fileType.startsWith("image/") && (
                  <img
                    src={filePreview}
                    alt="Uploaded Preview"
                    className="preview_img"
                  />
                )}
                {filePreview && fileType === "application/pdf" && (
                  <iframe
                    src={filePreview}
                    width="100%"
                    height="500px"
                  ></iframe>
                )}
              </div>
            </div>
            <div className="masked_image">
              <p>Masked Image</p>
              <div className="image_container">
                {!isLoaded && (
                  <OrbitProgress
                    variant="spokes"
                    color="#000000"
                    size="medium"
                    text="Loading"
                    textColor="Black"
                  />
                )}
                {isLoaded && filePreview && fileType.startsWith("image/") && (
                  <img
                    src={maskedImage}
                    alt="Uploaded Preview"
                    className="preview_img"
                  />
                )}
                {isLoaded && filePreview && fileType === "application/pdf" && (
                  <embed
                    src={filePreview}
                    type="application/pdf"
                    width="100%"
                    height="300px"
                  />
                )}
              </div>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}

export default Home;
