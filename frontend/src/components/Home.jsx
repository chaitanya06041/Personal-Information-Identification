import React, { useState } from "react";
import { Viewer } from "@react-pdf-viewer/core";
import { pdfjs } from "pdfjs-dist";
import "pdfjs-dist/build/pdf.worker.entry";
import "./Home.css";
import ExtractedData from "./ExtractedData";
import { styled } from "@mui/material/styles";
import Button from "@mui/material/Button";
import CloudUploadIcon from "@mui/icons-material/CloudUpload";
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
      console.log("received file");

      setIsLoaded(false);
      setFileType(file.type);
      setExtractedData(null);
      const previewURL = URL.createObjectURL(file);
      console.log(file.type);

      if (file.type === "application/pdf") {
        const formData = new FormData();

        formData.append("pdf", file);
        try {
          const response = await fetch("http://127.0.0.1:5000/pdf-to-image", {
            method: "POST",
            body: formData,
          });
          if (response.ok) {
            const blob = await response.blob();
            const imageUrl = URL.createObjectURL(blob);
            setFilePreview(imageUrl);
            try {
              const maskresponse = await fetch(
                "http://127.0.0.1:5000/mask-pdf",
                {
                  method: "POST",
                  body: formData,
                }
              );

              if (maskresponse.ok) {
                const data = await maskresponse.json(); // Parse JSON response
                
                setExtractedData(data.processed_json);
                const byteCharacters = atob(data.masked_pdf_path); // Decode base64
                const byteNumbers = new Array(byteCharacters.length);
                for (let i = 0; i < byteCharacters.length; i++) {
                  byteNumbers[i] = byteCharacters.charCodeAt(i);
                }
                const byteArray = new Uint8Array(byteNumbers);
                const pdfBlob = new Blob([byteArray], {
                  type: "application/pdf",
                });
                const newForm = new FormData();
                newForm.append("pdf", pdfBlob, "masked.pdf");
                try {
                  const newresponse = await fetch(
                    "http://127.0.0.1:5000/pdf-to-image",
                    {
                      method: "POST",
                      body: newForm,
                    }
                  );
                  if (newresponse.ok) {
                    const newblob = await newresponse.blob();
                    const maskedImage = URL.createObjectURL(newblob);
                    setMaskedImage(maskedImage);
                    setIsLoaded(true);
                  }
                  console.log("Extracted Data:", data.processed_json);
                } catch (err) {
                  console.err("error: ", err);
                }
              } else {
                console.error("Error uploading image");
              }
            } catch (error) {
              console.error("Error:", error);
            }
          }
        } catch (err) {
          console.err("error", err);
        }
      } else {
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
            const data = await response.json(); // Parse JSON response
            
            // Set extracted JSON data
            setExtractedData(data.processed_json);
            
            // Convert Base64 to a displayable image URL
            const imageURL = `data:image/png;base64,${data.masked_image}`;
            setMaskedImage(imageURL);
            setIsLoaded(true);

            console.log("Extracted Data:", data.processed_json);
          } else {
            console.error("Error uploading image");
          }
        } catch (error) {
          console.error("Error:", error);
        }
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
                {filePreview && (
                  <img
                    src={filePreview}
                    alt="Uploaded Preview"
                    className="preview_img"
                  />
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
                {isLoaded && filePreview && (
                  <img
                    src={maskedImage}
                    alt="Uploaded Preview"
                    className="preview_img"
                  />
                )}
                {/* {isLoaded && filePreview && fileType === "application/pdf" && (
                  <embed
                    src={maskedImage}
                    type="application/pdf"
                    width="100%"
                    height="300px"
                  />
                )} */}
              </div>
            </div>
          </div>
        )}
        {extractedData && <ExtractedData data={extractedData} />}
      </div>
    </div>
  );
}

export default Home;
