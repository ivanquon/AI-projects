import { useState, useRef, useEffect } from "react";
import { List, ListItem, ListItemText, Box } from "@mui/material";
import TextEntry from "./TextEntry";

export default function Header() {
    const scrollRef = useRef<HTMLDivElement>(null);
    const [history, setHistory] = useState<string[]>([]);

    useEffect(() => {
        if (scrollRef.current) {
            scrollRef.current.scrollIntoView({ behavior: "smooth" });
        }
    }, [history]);

    const askRAG = async (query: string) => {
        setHistory((prev) => [...prev, query]);
        const res = await fetch("http://localhost:8000/rag", {
            method: "POST",
            headers: {
                Accept: "application/json",
                "Content-Type": "application/json",
            },
            body: JSON.stringify({
                query: query,
            }),
        });
        const data = await res.json();
        console.log(data);
        setHistory((prev) => [...prev, data]);
    };

    return (
        <Box>
            <List
                sx={{
                    height: "60vh",
                    border: "1px solid grey",
                    overflowY: "auto",
                }}
            >
                {history.map((item, index) => {
                    return (
                        <ListItem
                            key={index}
                            sx={{
                                whiteSpace: "normal",
                                wordBreak: "break-word", // to break long words if needed
                            }}
                        >
                            <ListItemText>{item}</ListItemText>
                        </ListItem>
                    );
                })}
                <div ref={scrollRef} />
            </List>
            <TextEntry askRAG={askRAG} />
        </Box>
    );
}
