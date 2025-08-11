import React, { useState } from "react";
import { api } from "../utils/api";

export default function UploadForm() {
  const [video, setVideo] = useState(null);
  const [instructions, setInstructions] = useState("");
  const [downloadUrl, setDownloadUrl] = useState(null);
  const [loading, setLoading] = useState(false);

  const handleUpload = async (e) => {
    e.preventDefault();
    if (!video) {
      alert("Please select a video file.");
      return;
    }

    setLoading(true);
    const formData = new FormData();
    formData.append("video", video);
    formData.append("instructions", instructions || "{}");

    try {
      const response = await api.post("/edit", formData, {
        headers: { "Content-Type": "multipart/form-data" },
        responseType: "blob", // needed to handle binary video response
      });

      const url = window.URL.createObjectURL(new Blob([response.data]));
      setDownloadUrl(url);
    } catch (error) {
      console.error("Error uploading video:", error);
      alert("Upload failed");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="p-4 max-w-lg mx-auto bg-white shadow rounded">
      <h1 className="text-xl font-bold mb-4">AI Video Editor Upload</h1>
      <form onSubmit={handleUpload}>
        <input
          type="file"
          accept="video/*"
          onChange={(e) => setVideo(e.target.files[0])}
          className="mb-4"
        />
        <textarea
          placeholder='Enter instructions as JSON, e.g. {"cut":[0,5]}'
          value={instructions}
          onChange={(e) => setInstructions(e.target.value)}
          className="border w-full p-2 mb-4"
        />
        <button
          type="submit"
          disabled={loading}
          className="bg-blue-500 text-white px-4 py-2 rounded"
        >
          {loading ? "Processing..." : "Upload & Edit"}
        </button>
      </form>
      {downloadUrl && (
        <div className="mt-4">
          <a
            href={downloadUrl}
            download="edited_video.mp4"
            className="bg-green-500 text-white px-4 py-2 rounded"
          >
            Download Edited Video
          </a>
        </div>
      )}
    </div>
  );
}

