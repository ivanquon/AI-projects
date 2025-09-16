import React, { useState } from "react";
import { TextField, IconButton, InputAdornment } from "@mui/material";
import { ArrowForward, Delete } from "@mui/icons-material";

interface TextEntryProps {
    askRAG: (query: string) => Promise<void>;
    deleteChatHistory: () => Promise<void>;
    disabled: boolean;
}

export default function TextEntry({
    deleteChatHistory,
    askRAG,
    disabled,
}: TextEntryProps) {
    const [textValue, setTextValue] = useState("");

    const handleSubmit = async (event: React.FormEvent<HTMLFormElement>) => {
        event.preventDefault();
        console.log("Form submitted with value:", textValue);
        setTextValue("");
        await askRAG(textValue);
    };

    return (
        <form onSubmit={handleSubmit}>
            <TextField
                label="Ask something"
                fullWidth
                margin="normal"
                value={textValue}
                onChange={(e) => setTextValue(e.target.value)}
                disabled={disabled}
                required
                slotProps={{
                    input: {
                        endAdornment: (
                            <InputAdornment position="end">
                                <IconButton type="submit" disabled={disabled}>
                                    <ArrowForward />
                                </IconButton>
                            </InputAdornment>
                        ),
                        startAdornment: (
                            <InputAdornment position="start">
                                <IconButton
                                    disabled={disabled}
                                    onClick={deleteChatHistory}
                                >
                                    <Delete />
                                </IconButton>
                            </InputAdornment>
                        ),
                    },
                }}
            />
        </form>
    );
}
