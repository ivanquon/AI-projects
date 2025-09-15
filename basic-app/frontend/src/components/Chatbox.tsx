import { useState, useRef, useEffect } from "react";
import { List, ListItem, ListItemText, Box } from "@mui/material";
import TextEntry from "./TextEntry";

interface Message {
    content: string;
    type: "human" | "ai";
}

export default function Header() {
    const scrollRef = useRef<HTMLDivElement>(null);
    const [history, setHistory] = useState<Message[]>([]);
    const [waiting, setWaiting] = useState<boolean>(false);

    useEffect(() => {
        if (scrollRef.current) {
            scrollRef.current.scrollIntoView({ behavior: "smooth" });
        }
    }, [history]);

    const askRAG = async (query: string) => {
        setWaiting(true);
        setHistory((prev) => [...prev, { content: query, type: "human" }]);
        await fetch("http://localhost:8000/rag", {
            method: "POST",
            headers: {
                Accept: "application/json",
                "Content-Type": "application/json",
            },
            body: JSON.stringify({
                query: query,
            }),
        });

        const res = await fetch("http://localhost:8000/rag", {
            method: "GET",
        });
        const data = await res.json();
        console.log(data);
        setHistory(data);
        setWaiting(false);
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
                {history.map((message, index) => {
                    return (
                        <ListItem
                            key={index}
                            sx={{
                                justifyContent:
                                    message.type === "human"
                                        ? "flex-end"
                                        : "flex-start",
                            }}
                        >
                            <Box
                                sx={{
                                    backgroundColor:
                                        message.type === "human"
                                            ? "#a2a7eeff"
                                            : "#E5E5EA",
                                    color: "black",
                                    px: 2,
                                    py: 1,
                                    borderRadius: 2,
                                    maxWidth: "70%",
                                    whiteSpace: "pre-wrap",
                                    wordBreak: "break-word",
                                    textAlign: "left",
                                    boxShadow: 1,
                                }}
                            >
                                <ListItemText>{message.content}</ListItemText>
                            </Box>
                        </ListItem>
                    );
                })}
                <div ref={scrollRef} />
            </List>
            <TextEntry disabled={waiting} askRAG={askRAG} />
        </Box>
    );
}
