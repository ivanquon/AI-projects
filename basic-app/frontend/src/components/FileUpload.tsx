import { useCallback, useState } from "react"
import { useDropzone } from "react-dropzone"
import { Box, Typography, Paper, CircularProgress, Snackbar, Alert } from "@mui/material"
import type { AlertColor } from "@mui/material"
import CloudUploadIcon from "@mui/icons-material/CloudUpload"

const BACKEND_URL = import.meta.env.BACKEND_URL

interface SnackbarState {
    open: boolean
    message: string
    severity: AlertColor
}

export default function FileUpload() {
    const [uploading, setUploading] = useState(false)
    const [snackbar, setSnackbar] = useState<SnackbarState>({
        open: false,
        message: "",
        severity: "success",
    })

    const onDrop = useCallback(async (acceptedFiles: File[]) => {
        if (acceptedFiles.length === 0) return

        const file = acceptedFiles[0]
        const formData = new FormData()
        formData.append("file", file)

        setUploading(true)

        try {
            const response = await fetch(`${BACKEND_URL}/sources/file`, {
                method: "POST",
                body: formData,
            })

            if (!response.ok) throw new Error("Upload failed")

            setSnackbar({
                open: true,
                message: "File uploaded successfully!",
                severity: "success",
            })
        } catch (error: any) {
            setSnackbar({
                open: true,
                message: error.message || "Something went wrong",
                severity: "error",
            })
        } finally {
            setUploading(false)
        }
    }, [])

    const { getRootProps, getInputProps, isDragActive } = useDropzone({
        onDrop,
        accept: {
            "application/pdf": [".pdf"],
            "text/plain": [".txt"],
            "application/msword": [".doc"],
            "application/vnd.openxmlformats-officedocument.wordprocessingml.document": [".docx"],
        },
        multiple: false,
    })

    return (
        <Box sx={{ mt: 4, width: "100%", maxWidth: 500, mx: "auto" }}>
            <Paper
                {...getRootProps()}
                elevation={3}
                sx={{
                    p: 4,
                    textAlign: "center",
                    border: "2px dashed #ccc",
                    backgroundColor: isDragActive ? "#f0f0f0" : "#fafafa",
                    cursor: "pointer",
                }}
            >
                <input {...getInputProps()} />
                <CloudUploadIcon sx={{ fontSize: 48, color: "#999" }} />
                <Typography variant="h6" sx={{ mt: 2 }}>
                    {isDragActive ? "Drop the file here..." : "Drag & drop a file here, or click to select"}
                </Typography>
            </Paper>

            {uploading && (
                <Box sx={{ mt: 2, textAlign: "center" }}>
                    <CircularProgress />
                    <Typography variant="body2" sx={{ mt: 1 }}>
                        Uploading...
                    </Typography>
                </Box>
            )}

            <Snackbar
                open={snackbar.open}
                autoHideDuration={4000}
                onClose={() => setSnackbar((prev) => ({ ...prev, open: false }))}
                anchorOrigin={{ vertical: "bottom", horizontal: "center" }}
            >
                <Alert
                    onClose={() => setSnackbar((prev) => ({ ...prev, open: false }))}
                    severity={snackbar.severity}
                    sx={{ width: "100%" }}
                >
                    {snackbar.message}
                </Alert>
            </Snackbar>
        </Box>
    )
}
