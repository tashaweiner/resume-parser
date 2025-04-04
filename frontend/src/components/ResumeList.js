import React from "react";

function ResumeList({ resumes, onSelect }) {
  return (
    <ul>
      {resumes.map((resume, index) => (
        <li
          key={index}
          style={{ cursor: "pointer", paddingBottom: "0.5rem" }}
          onClick={() => onSelect(resume)}
        >
          {resume.content.name || resume.filename}
        </li>
      ))}
    </ul>
  );
}

export default ResumeList;