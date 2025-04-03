import React from "react";
import "./ExtractedData.css";
import { useState, useEffect } from "react";

function ExtractedData({ data }) {
  const [extractedData, setExtractedData] = useState({});
  // data = {
  //   document_type: "Aadhaar",
  //   person_name: "Chaitanya Kishor Undale",
  //   country: "India",
  //   document_id: "2435 7796 7044",
  //   email: "",
  //   phone_no: "8767397768",
  //   address:
  //     " Sangli Maharashtra 415311",
  //   dob: "06/10/2004",
  //   gender: "MALE",
  //   expiry_date: "",
  // };

  useEffect(() => {
    if (!data) return; // Ensure data exists before processing

    const newData = {};
    if (data?.document_type) newData["Document Type"] = data.document_type;
    if (data?.document_id) newData["Document Id"] = data.document_id;
    if (data?.person_name) newData["Name"] = data.person_name;
    if (data?.country) newData["Country"] = data.country;
    if (data?.phone_no) newData["Phone"] = data.phone_no;
    if (data?.email) newData["Email"] = data.email;
    if (data?.address) newData["Address"] = data.address;
    if (data?.gender) newData["Gender"] = data.gender;
    if (data?.dob) newData["Date of Birth"] = data.dob;
    if (data?.expiry_date) newData["Expiry Date"] = data.expiry_date;

    console.log("New Data: ", newData); // Now logs only when `data` changes
    setExtractedData(newData);
  }, [data]);

  return (
    <div className="extracted_data">
      <table className="extracted_data_table">
        <thead>
          <tr>
            <th>Field</th>
            <th>Value</th>
          </tr>
        </thead>
        <tbody>
          {Object.entries(extractedData || {}).map(([key, value]) => (
            <tr key={key}>
              <td>{key}</td>
              <td>{value || "N/A"}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}

export default ExtractedData;
