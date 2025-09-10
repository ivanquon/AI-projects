import React, { useState } from "react";
import { TextField, IconButton, InputAdornment } from "@mui/material";
import { ArrowForward } from "@mui/icons-material";

interface TextEntryProps {
    askRAG: (query: string) => Promise<void>;
}

export default function TextEntry({ askRAG }: TextEntryProps) {
    const [textValue, setTextValue] = useState("");

    const handleSubmit = async (event: React.FormEvent<HTMLFormElement>) => {
        event.preventDefault(); // Prevent page reload
        console.log("Form submitted with value:", textValue);
        await askRAG(textValue);
        // You can also call APIs or update state here
    };

    return (
        <form onSubmit={handleSubmit}>
            <TextField
                label="Ask something"
                fullWidth
                margin="normal"
                value={textValue}
                onChange={(e) => setTextValue(e.target.value)}
                slotProps={{
                    input: {
                        endAdornment: (
                            <InputAdornment position="end">
                                <IconButton type="submit">
                                    <ArrowForward />
                                </IconButton>
                            </InputAdornment>
                        ),
                    },
                }}
            />
        </form>
    );
}
