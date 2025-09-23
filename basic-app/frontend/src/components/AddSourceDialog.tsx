import {
    Tabs,
    Tab,
    Button,
    TextField,
    Dialog,
    DialogActions,
    DialogContent,
    DialogContentText,
    DialogTitle,
} from "@mui/material";
import { useState } from "react";
import FileUpload from "./FileUpload"; // Adjust the path as necessary

interface DialogProps {
    onSubmit: (query: string) => Promise<void>;
}

export default function AddSourceDialog({ onSubmit }: DialogProps) {
    const [open, setOpen] = useState(false);
    const [article, setArticle] = useState("");
    const [tabIndex, setTabIndex] = useState(0);

    const handleClickOpen = () => setOpen(true);
    const handleClose = () => setOpen(false);

    const handleSubmit = async (event: React.FormEvent) => {
        event.preventDefault();
        await onSubmit(article);
        handleClose();
    };

    return (
        <>
            <Button onClick={handleClickOpen}>Add Source</Button>
            <Dialog open={open} onClose={handleClose} fullWidth maxWidth="sm">
                <DialogTitle>Add a source</DialogTitle>

                <Tabs value={tabIndex} onChange={(_, newIndex) => setTabIndex(newIndex)} centered>
                    <Tab label="Wikipedia Article" />
                    <Tab label="File Upload" />
                </Tabs>

                <DialogContent dividers>
                    {tabIndex === 0 && (
                        <>
                            <DialogContentText>
                                Enter the article title of a Wikipedia source to load it into the RAG system.
                            </DialogContentText>
                            <form onSubmit={handleSubmit} id="article-form">
                                <TextField
                                    autoFocus
                                    required
                                    margin="dense"
                                    id="article"
                                    label="Article name"
                                    fullWidth
                                    variant="standard"
                                    onChange={(e) => setArticle(e.target.value)}
                                />
                            </form>
                        </>
                    )}

                    {tabIndex === 1 && (
                        <>
                            <DialogContentText>Upload a text file to load it into the RAG system.</DialogContentText>
                            <FileUpload />
                        </>
                    )}
                </DialogContent>

                {tabIndex === 0 && (
                    <DialogActions>
                        <Button onClick={handleClose}>Cancel</Button>
                        <Button type="submit" form="article-form">
                            Add
                        </Button>
                    </DialogActions>
                )}
            </Dialog>
        </>
    );
}
