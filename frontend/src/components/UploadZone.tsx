import React from "react";
import { api } from "../services/api";

export const UploadZone: React.FC = () => {
  const [files, setFiles] = React.useState<FileList | null>(null);
  const [status, setStatus] = React.useState<string>("");

  const onUpload = async () => {
    if (!files || files.length === 0) return;
    setStatus("Uploading...");
    try {
      await api.upload(files);
      setStatus("Uploaded and processing complete.");
    } catch (e: any) {
      setStatus("Upload failed: " + e.message);
    }
  };

  return (
    <div className="border rounded p-3">
      <input type="file" multiple accept="application/pdf" onChange={(e) => setFiles(e.target.files)} />
      <button className="ml-2 px-3 py-1 bg-blue-600 text-white rounded" onClick={onUpload}>Upload</button>
      <div className="text-sm mt-2">{status}</div>
    </div>
  );
};