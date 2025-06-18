import React, { useState } from 'react';

interface FileStatus {
  file: File;
  status: 'pending' | 'uploading' | 'success' | 'failed';
  message: string;
}

const FileUpload: React.FC = () => {
  const [files, setFiles] = useState<FileStatus[]>([]);
  const [isUploading, setIsUploading] = useState(false);
  const [globalMessage, setGlobalMessage] = useState<string>('');

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files) {
      const selectedFilesArray = Array.from(e.target.files);
      const newFiles: FileStatus[] = selectedFilesArray.map(file => {
        if (file.type === 'application/pdf') {
          return { file, status: 'pending', message: '' };
        } else {
          return { file, status: 'failed', message: 'Not a PDF file' };
        }
      });
      setFiles(prevFiles => [...prevFiles, ...newFiles.filter(f => f.status !== 'failed')]);
      const failedFiles = newFiles.filter(f => f.status === 'failed');
      if (failedFiles.length > 0) {
        setGlobalMessage(`Skipped ${failedFiles.length} non-PDF files.`);
      } else {
        setGlobalMessage('');
      }
    }
  };

  const handleRemoveFile = (indexToRemove: number) => {
    setFiles(prevFiles => prevFiles.filter((_, index) => index !== indexToRemove));
  };

  const handleUpload = async () => {
    if (files.length === 0) {
      setGlobalMessage('Please select files first.');
      return;
    }

    setIsUploading(true);
    setGlobalMessage('Uploading files...');

    const formData = new FormData();
    files.forEach(fileStatus => {
      if (fileStatus.status === 'pending') {
        formData.append('files', fileStatus.file);
      }
    });

    if (formData.getAll('files').length === 0) {
      setGlobalMessage('No pending files to upload.');
      setIsUploading(false);
      return;
    }

    setFiles(prevFiles => 
      prevFiles.map(fs => 
        fs.status === 'pending' ? { ...fs, status: 'uploading', message: 'Uploading...' } : fs
      )
    );

    try {
      const response = await fetch('http://localhost:8000/api/upload', {
        method: 'POST',
        body: formData,
      });

      const result = await response.json();

      if (response.ok) {
        setFiles(prevFiles => 
          prevFiles.map(fs => {
            const uploadedFile = result.find((res: any) => res.filename === fs.file.name);
            if (uploadedFile) {
              if (uploadedFile.status === 'failed') {
                return { ...fs, status: 'failed', message: `Error: ${uploadedFile.error}` };
              } else {
                return { ...fs, status: 'success', message: `Processed ${uploadedFile.chunks_count} chunks` };
              }
            }
            return fs;
          })
        );
        setGlobalMessage('All selected files processed.');
      } else {
        setGlobalMessage(`Error: ${result.detail || 'Failed to upload files.'}`);
        setFiles(prevFiles => 
          prevFiles.map(fs => 
            fs.status === 'uploading' ? { ...fs, status: 'failed', message: result.detail || 'Upload failed' } : fs
          )
        );
      }
    } catch (error) {
      console.error('Error:', error);
      setGlobalMessage('Network error or server unreachable.');
      setFiles(prevFiles => 
        prevFiles.map(fs => 
          fs.status === 'uploading' ? { ...fs, status: 'failed', message: 'Network error' } : fs
        )
      );
    } finally {
      setIsUploading(false);
    }
  };

  return (
    <div className="uploadContainer">
      <div className="uploadBox">
        <input
          type="file"
          accept=".pdf"
          multiple
          onChange={handleFileChange}
          disabled={isUploading}
          className="fileInput"
        />
        <button
          onClick={handleUpload}
          disabled={files.filter(f => f.status === 'pending').length === 0 || isUploading}
          className="uploadButton"
        >
          {isUploading ? 'Uploading...' : 'Upload Selected PDFs'}
        </button>
      </div>

      {globalMessage && (
        <div className="globalStatus">
          {globalMessage}
        </div>
      )}

      {files.length > 0 && (
        <div className="fileList">
          <h3>Selected Files:</h3>
          <ul>
            {files.map((fileStatus, index) => (
              <li key={index} className="fileItem">
                <span className="fileName">{fileStatus.file.name}</span>
                <span className={`fileStatus ${fileStatus.status}`}>
                  {fileStatus.status === 'uploading' ? 'Uploading...' : fileStatus.message || fileStatus.status}
                </span>
                {fileStatus.status !== 'uploading' && (
                  <button onClick={() => handleRemoveFile(index)} className="removeButton">
                    &times;
                  </button>
                )}
              </li>
            ))}
          </ul>
        </div>
      )}
    </div>
  );
};

export default FileUpload; 