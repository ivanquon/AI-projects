import { useState, useRef, useEffect } from "react"
import { List, ListItem, ListItemText, Box } from "@mui/material"
import TextEntry from "./TextEntry"

interface Message {
    content: string
    type: "human" | "ai"
}

const BACKEND_URL = import.meta.env.BACKEND_URL

export default function ChatBox() {
    const scrollRef = useRef<HTMLDivElement>(null)
    const [history, setHistory] = useState<Message[]>([])
    const [waiting, setWaiting] = useState<boolean>(false)

    //Clear history on page load/reload so that previous sessions do not persist
    //If persistent history was wanted I would store it in localstorage for this project since it is small.
    useEffect(() => {
        deleteChatHistory()
    }, [])

    useEffect(() => {
        if (scrollRef.current) {
            scrollRef.current.scrollIntoView({ behavior: "smooth" })
        }
    }, [history])

    const askRAG = async (query: string) => {
        setWaiting(true)
        setHistory((prev) => [...prev, { content: query, type: "human" }])
        await fetch(`${BACKEND_URL}/rag`, {
            method: "POST",
            headers: {
                "Accept": "application/json",
                "Content-Type": "application/json",
            },
            body: JSON.stringify({
                query: query,
            }),
        })

        const res = await fetch(`${BACKEND_URL}/rag`, {
            method: "GET",
        })
        const data = await res.json()
        console.log(data)
        setHistory(data)
        setWaiting(false)
    }

    const deleteChatHistory = async () => {
        await fetch(`${BACKEND_URL}/rag`, {
            method: "DELETE",
        })
        const res = await fetch(`${BACKEND_URL}/rag`, {
            method: "GET",
        })
        const data = await res.json()
        console.log(data)
        setHistory(data)
    }

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
                                justifyContent: message.type === "human" ? "flex-end" : "flex-start",
                            }}
                        >
                            <Box
                                sx={{
                                    backgroundColor: message.type === "human" ? "lightblue" : "lightgreen",
                                    color: "black",
                                    p: 2,
                                    borderRadius: 2,
                                    maxWidth: "70%",
                                    whiteSpace: "pre-wrap",
                                    wordBreak: "break-word",
                                    textAlign: "left",
                                }}
                            >
                                <ListItemText>{message.content}</ListItemText>
                            </Box>
                        </ListItem>
                    )
                })}
                <div ref={scrollRef} />
            </List>
            <TextEntry deleteChatHistory={deleteChatHistory} disabled={waiting} askRAG={askRAG} />
        </Box>
    )
}
