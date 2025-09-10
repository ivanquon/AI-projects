import Button from "@mui/material/Button";
import TextField from "@mui/material/TextField";
import Dialog from "@mui/material/Dialog";
import DialogActions from "@mui/material/DialogActions";
import DialogContent from "@mui/material/DialogContent";
import DialogContentText from "@mui/material/DialogContentText";
import DialogTitle from "@mui/material/DialogTitle";
import { useState } from "react";

interface DialogProps {
    onSubmit: (query: string) => Promise<void>;
}

export default function AddSourceDialog({ onSubmit }: DialogProps) {
    const [open, setOpen] = useState(false);
    const [article, setArticle] = useState("");

    const handleClickOpen = () => {
        setOpen(true);
    };

    const handleClose = () => {
        setOpen(false);
    };

    const handleSubmit = (event: React.FormEvent) => {
        event.preventDefault();
        console.log(article);
        onSubmit(article);
        handleClose();
    };

    return (
        <>
            <Button onClick={handleClickOpen}>Add a Wikipedia Article</Button>
            <Dialog open={open} onClose={handleClose}>
                <DialogTitle>Add Article</DialogTitle>
                <DialogContent>
                    <DialogContentText>
                        Enter the article title of a wikipedia source to load it
                        into the RAG system
                    </DialogContentText>
                    <form onSubmit={handleSubmit} id="subscription-form">
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
                </DialogContent>
                <DialogActions>
                    <Button onClick={handleClose}>Cancel</Button>
                    <Button type="submit" form="subscription-form">
                        Add
                    </Button>
                </DialogActions>
            </Dialog>
        </>
    );
}
