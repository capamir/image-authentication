import React, { useCallback, useState } from "react";
import { useDropzone } from "react-dropzone";
import { ArrowUpTrayIcon, XMarkIcon } from "@heroicons/react/24/solid";
import axios from "axios";

function Uploader({ styles }) {
  const [file, setFile] = useState("");
  const [rejected, setRejected] = useState([]);
  const [isUploading, setIsUploading] = useState(false);
  const [message, setMessage] = useState("");
  const [compressedImage, setCompressedImage] = useState("");

  const onDrop = useCallback((acceptedFiles, rejectedFiles) => {
    if (acceptedFiles?.length) {
      setFile(
        Object.assign(acceptedFiles[0], {
          preview: URL.createObjectURL(acceptedFiles[0]),
        })
      );
    }

    if (rejectedFiles?.length) {
      setRejected((previousFiles) => [...previousFiles, ...rejectedFiles]);
    }
  }, []);

  const { getRootProps, getInputProps, isDragActive } = useDropzone({
    accept: {
      "image/*": [],
    },
    maxSize: 1024 * 1000,
    onDrop,
  });

  const removeFile = () => {
    setFile("");
  };

  const removeAll = () => {
    setFile("");
    setRejected([]);
  };

  const removeRejected = (name) => {
    setRejected((files) => files.filter(({ file }) => file.name !== name));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    uploading(file, setIsUploading, setMessage);
  };

  const uploading = async (file, setIsUploading, setMessage) => {
    const formData = new FormData();
    formData.append("image", file);
    setIsUploading(true);
    try {
      const config = {
        headers: {
          "Content-Type": "multipart/form-data",
        },
        responseType: 'arraybuffer'
      };
      const { data } = await axios.post(
        "http://127.0.0.1:8000/api/products/upload/",
        formData,
        config
      );

      // Convert binary data to base64 string
      const base64String = btoa(
        new Uint8Array(data).reduce(
          (data, byte) => data + String.fromCharCode(byte),
          ''
        )
      );

      // Set compressed image data
      const compressedImageData = `data:image/jpeg;base64,${base64String}`;
      setCompressedImage(compressedImageData);
      setMessage(""); // Clear any previous error messages
      setIsUploading(false);
    } catch (error) {
      setIsUploading(false);
      setMessage(`Error: ${error.message}`);
      console.log(error.message);
    }
  };

  return (
    <form onSubmit={handleSubmit}>
      <div
        {...getRootProps({
          className: styles,
        })}
      >
        <input {...getInputProps()} />
        <div className="flex flex-col items-center justify-center gap-4">
          <ArrowUpTrayIcon className="w-5 h-5 fill-current" />
          {isDragActive ? (
            <p>Drop the files here ...</p>
          ) : (
            <p>Drag & drop files here, or click to select files</p>
          )}
        </div>
      </div>

      {/* Preview */}
      <section className="mt-10">
        <div className="flex gap-4">
          <h2 className="title text-3xl font-semibold">Preview</h2>
          <h2 className="title text-3xl font-semibold">
            {isUploading ? "uploading" : message ? message : ""}
          </h2>

          <button
            type="button"
            onClick={removeAll}
            className="mt-1 text-[12px] uppercase tracking-wider font-bold text-neutral-500 border border-secondary-400 rounded-md px-3 hover:bg-secondary-400 hover:text-white transition-colors"
          >
            Remove all files
          </button>

          <button
            type="submit"
            className="ml-auto mt-1 text-[12px] uppercase tracking-wider font-bold text-neutral-500 border border-purple-400 rounded-md px-3 hover:bg-purple-400 hover:text-white transition-colors"
          >
            Upload to server
          </button>
        </div>

        {/* Accepted files */}
        <h3 className="title text-lg font-semibold text-neutral-600 mt-10 border-b pb-3">
          Accepted Files
        </h3>
        <ul className="mt-6 grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 xl:grid-cols-6 gap-10">
          {file && (
            <li className="relative h-32 rounded-md shadow-lg">
              <img
                src={file.preview}
                alt={file.name}
                className="h-full w-full object-contain rounded-md"
              />
              <button
                type="button"
                className="w-7 h-7 border border-secondary-400 bg-secondary-400 rounded-full flex justify-center items-center absolute -top-3 -right-3 hover:bg-white transition-colors"
                onClick={removeFile}
              >
                <XMarkIcon className="w-5 h-5  hover:fill-secondary-400 transition-colors" />
              </button>
              <p className="mt-2 text-neutral-500 text-[12px] font-medium">
                {file.name}
              </p>
            </li>
          )}
        </ul>

        {/* Display compressed image */}
        {compressedImage && (
          <div className="mt-6">
            <h3 className="title text-lg font-semibold text-neutral-600 border-b pb-3">
              Compressed Image
            </h3>
            <img src={compressedImage} alt="Compressed" className="mt-4 max-w-full h-auto" />
          </div>
        )}

        {/* Rejected Files */}
        <h3 className="title text-lg font-semibold text-neutral-600 mt-24 border-b pb-3">
          Rejected Files
        </h3>
        <ul className="mt-6 flex flex-col">
          {rejected.map(({ file, errors }) => (
            <li key={file.name} className="flex items-start justify-between">
              <div>
                <p className="mt-2 text-neutral-500 text-sm font-medium">
                  {file.name}
                </p>
                <ul className="text-[12px] text-red-400">
                  {errors.map((error) => (
                    <li key={error.code}>{error.message}</li>
                  ))}
                </ul>
              </div>
              <button
                type="button"
                className="mt-1 py-1 text-[12px] uppercase tracking-wider font-bold text-neutral-500 border border-secondary-400 rounded-md px-3 hover:bg-secondary-400 hover:text-white transition-colors"
                onClick={() => removeRejected(file.name)}
              >
                remove
              </button>
            </li>
          ))}
        </ul>
      </section>
    </form>
  );
}

export default Uploader;